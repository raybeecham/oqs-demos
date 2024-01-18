# Quantum-Safe Curl Docker Image README

This Docker image is configured to utilize quantum-safe cryptography (QSC) operations. It contains the `oqs-curl` setup, and you can use it to create the Docker image and run a container with an OQS-enabled TLS test server.

## Quick Start

### Building the Docker Image and Running the Container

To get started, you need to have Docker installed. Follow these steps to build the Docker image and run the container:

1. **Open a terminal**.

2. **Navigate to the directory with the Dockerfile** for `oqs-curl`.

3. **Build the Docker image** with the following command:
   ```bash
   docker build -t oqs-curl .
   ```
4. **Start a Docker Container** with the following command:
    ```bash
    docker run -it oqs-curl
    ```
5. **Query the Server**
Inside the Docker container resulting from the previous command, you can query the server by issuing the following `curl` command:

    ```bash
    curl --curves kyber768 https://localhost:4433
    ```

### Prerequisites
- Ensure you have Docker installed on your system.

### Run an OQS-Enabled TLS Test Server
To start an OQS-enabled TLS test server, run the following command:

```bash
docker run -it openquantumsafe/curl
```

### Query the Server
Inside the Docker container resulting from the previous command, you can query the server by issuing the following `curl` command:

```bash
curl --curves kyber768 https://localhost:4433
```

Replace `kyber768` with any Key Exchange Algorithm (KEM) supported by `oqs-provider`.

### Retrieve Data from Other QSC-Enabled TLS Servers
You can use this Docker image to retrieve data from any OQS-enabled TLS 1.3 server by running:

```bash
docker run -it openquantumsafe/curl curl <OQS-server URL>
```

Additionally, you can specify a particular OQS algorithm using the `--curves` option.

## Performance Testing

### TLS Handshake Performance

#### Default Test
To perform TLS handshake performance testing with default settings (dilithium2 SIG_ALG and kyber768 KEM_ALG), run:

```bash
docker run -it openquantumsafe/curl perftest.sh
```

#### Customized Test
Customize the test duration, KEM, and SIG algorithms by setting environment variables. For example, to test dilithium3 and kyber768 for 5 seconds, run:

```bash
docker run -e TEST_TIME=5 -e KEM_ALG=kyber768 -e SIG_ALG=dilithium3 -it openquantumsafe/curl perftest.sh
```

### Algorithm Performance

#### Run All Algorithms
To test the performance of all supported cryptographic algorithms (classic and quantum-safe), run:

```bash
docker run -it openquantumsafe/curl openssl speed
```

#### Run Specific Algorithm
Test the performance of a specific algorithm by providing parameters as you would with `openssl speed`. For example, to test kyber512, run:

```bash
docker run -it openquantumsafe/curl openssl speed -seconds 2 kyber512
```


## Classic Algorithm Names

If you want to measure performance with classic (non-quantum-safe) cryptographic algorithms, you can use the following names:

- For signature algorithms (SIG_ALG): ed25519 and ed448.
- For key exchange mechanisms (KEM_ALG): X25519, P-384, P-256, and P-521.
