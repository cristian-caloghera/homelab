# Use Go 1.23 bookworm as development stage
FROM golang:1.24-bookworm AS development

# Move to a working directory called build
WORKDIR /build

COPY src/ /build

# Install dependencies
RUN go get -u && go mod tidy

# Build the application
# Turn off CGO to ensure static binaries
RUN CGO_ENABLED=0 go build

# Production stage
# =======================================================
# Create a production stage to run the application binary
FROM scratch

# Move to working directory /prod
WORKDIR /prod

# Copy binary from builder stage
COPY --from=development /build/heatoil-reader /prod

# Start the application
ENTRYPOINT ["/prod/heatoil-reader"]
