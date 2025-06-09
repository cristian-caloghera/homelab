package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
	"unicode"

	influxdb2 "github.com/influxdata/influxdb-client-go/v2"
	"github.com/influxdata/influxdb-client-go/v2/api"
)

func removeNonNumericChars(s string) string {
	var sb strings.Builder
	for _, r := range s {
		if unicode.IsDigit(r) {
			sb.WriteRune(r)
		}
	}
	return sb.String()
}

// getHTMLContent fetches the HTML content from a given URL.
func getHTMLContent(url string) (string, error) {
	// Send an HTTP GET request to the URL.
	resp, err := http.Get(url)
	if err != nil {
		return "", fmt.Errorf("error making HTTP request: %w", err)
	}
	defer resp.Body.Close() // Ensure the response body is closed after we're done with it

	// Check if the response status code is OK (200).
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("server returned non-OK status: %s", resp.Status)
	}

	// Read the entire response body.
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("error reading response body: %w", err)
	}

	// Convert the byte slice to a string and return it.
	return string(body), nil
}

type Tank struct {
	available  uint64
	capacity   uint64
	fillVolume uint64
	percentage float64
}

func getTankFrom(url string) (Tank, error) {
	log.Printf("Retrieving response from %v", url)
	html, err := getHTMLContent(url)
	if err != nil {
		return Tank{}, err
	}

	lines := strings.Split(html, "\n")

	aString := removeNonNumericChars(lines[66])
	pString := removeNonNumericChars(lines[67])
	cString := removeNonNumericChars(lines[68])
	fString := removeNonNumericChars(lines[69])

	a, err := strconv.ParseUint(aString, 10, 64)
	if err != nil {
		return Tank{}, err
	}
	c, err := strconv.ParseUint(cString, 10, 64)
	if err != nil {
		return Tank{}, err
	}
	f, err := strconv.ParseUint(fString, 10, 64)
	if err != nil {
		return Tank{}, err
	}
	p, err := strconv.ParseFloat(pString, 64)
	if err != nil {
		return Tank{}, err
	}

	t := Tank{
		available:  a,
		capacity:   c,
		fillVolume: f,
		percentage: p / 100.0,
	}

	log.Printf("Computed tank: %v", t)

	return t, nil
}

func doWork(url string, dbWrite api.WriteAPI) {
	tank, err := getTankFrom(url)
	if err == nil {
		// Create a point
		tags := map[string]string{
			"location": "oil tank",
		}
		fields := map[string]interface{}{
			"available":  tank.available,
			"fillVolume": tank.fillVolume,
			"percentage": tank.percentage,
		}
		point := influxdb2.NewPoint(
			"heatoil",
			tags,
			fields,
			time.Now(),
		)

		// Write the point (non-blocking)
		dbWrite.WritePoint(point)
		log.Println("Queued data point for writing to bucket.")
	} else {
		log.Printf("%+v", err)
	}
}

func getEnvVar(envVar string) string {
	value := os.Getenv(envVar)
	if value == "" {
		log.Fatal("Environment variable " + envVar + " has no value! Cannot continue!")
	}
	return value
}

func main() {
	log.Println("Program is running.")

	urlString := getEnvVar("READ_URL")

	if !strings.HasPrefix(urlString, "http://") {
		urlString = "http://" + urlString
	}

	// set default tick interval
	defaultInterval := 5
	intervalString := os.Getenv("READ_INTERVAL")
	interval, err := strconv.Atoi(intervalString)
	if err != nil {
		interval = defaultInterval
	}

	intervalDuration := time.Duration(interval) * time.Second
	log.Printf("Reading from %v every %v.", urlString, intervalDuration)

	// get InfluxDB2 connection details from environment
	dbURL := getEnvVar("INFLUXDB2_URL")
	dbToken := getEnvVar("INFLUXDB2_TOKEN")

	log.Printf("Establishing connection to InfluxDB2: %v", dbURL)
	dbClient := influxdb2.NewClient(dbURL, dbToken)
	// validate client connection health
	_, err = dbClient.Health(context.Background())
	if err != nil {
		log.Fatal("Connection is not successful. Aborting!")
	}
	log.Println("Connection is successful.")

	// Defer the closing of the client to ensure it happens when main() exits
	defer func() {
		log.Println("Closing InfluxDB client...")
		dbClient.Close()
	}()

	var dbWriter api.WriteAPI = dbClient.WriteAPI("BuruOrg", "ww29")

	// keep on spinning forever (aka CTRL-C)
	for {
		doWork(urlString, dbWriter)
		time.Sleep(intervalDuration)
	}
}
