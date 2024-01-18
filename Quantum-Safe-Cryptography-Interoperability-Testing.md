# Testing Quantum-Safe Cryptography Interoperability with Docker

In this tutorial, we'll explore how to test interoperability with quantum-safe cryptography (QSC) using Docker and the Open Quantum Safe project (OQS). We'll use a Docker container that provides a simple way to test QSC algorithms with an NGINX server enhanced for QSC.

## Prerequisites

Before you begin, ensure you have the following prerequisites:

- Docker installed on your system.

## Step 1: Download the Test CA Certificate

1. If not already done, download the test CA certificate (`CA.crt`) from the [Open Quantum Safe test server](https://test.openquantumsafe.org/CA.crt) to a directory on your local system.

## Step 2: Run the Docker Container

2. Open your terminal and navigate to the directory where you have the `CA.crt` file.

3. Run the following Docker command to run a container with `curl` for testing QSC algorithms:

   ```bash
   sudo docker run -v `pwd`:/ca -it openquantumsafe/curl:latest curl --cacert /ca/CA.crt https://test.openquantumsafe.org:6003 --curves bikel5
    ```
4. Replace /ca/CA.crt with the correct path to your CA.crt file if necessary.

The command will connect to the QSC test server, and if successful, you will receive a response indicating the successful connection with the specified algorithm (ecdsap256-bikel5 in this example).

