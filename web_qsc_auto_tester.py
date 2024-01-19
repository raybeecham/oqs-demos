# Author: Ray Beecham
# Date: 1/18/2024
# Description: This script is designed to test and verify quantum-safe cryptographic algorithms
#              using Docker containers to execute curl and OpenSSL commands on a test server.

from flask import Flask, render_template, request
import subprocess
import os
import requests

# Create the application instance
app = Flask(__name__)

CA_CERT_URL = "https://test.openquantumsafe.org/CA.crt"
CA_CERT_PATH = "CA.crt"
DOCKER_IMAGE = "openquantumsafe/curl:latest"
OQS_SERVER_URL = "https://test.openquantumsafe.org"

# Algorithm combinations to test
ALGORITHM_COMBINATIONS = [
    {"sig_alg": "ecdsap256", "kem_alg": "bikel1", "port": 6001},
    {"sig_alg": "rsa3072", "kem_alg": "kyber768", "port": 6058},
    {"sig_alg": "sphincssha2128fsimple", "kem_alg": "bikel5", "port": 6003},
    {"sig_alg": "dilithium2", "kem_alg": "frodo640aes", "port": 6088},
    # Add more combinations if needed
]

# Download the CA certificate
def download_ca_certificate():
    try:
        response = requests.get(CA_CERT_URL)
        with open(CA_CERT_PATH, 'wb') as file:
            file.write(response.content)
    except requests.RequestException as e:
        return f"Failed to download CA certificate: {e}"
    return "Downloaded CA certificate."

# Run the Docker container with curl
def run_docker_curl(port, kem_alg):
    try:
        command = [
            "docker", "run", "-v", f"{os.getcwd()}:/ca", DOCKER_IMAGE,
            "curl", "--cacert", "/ca/CA.crt",
            f"{OQS_SERVER_URL}:{port}", "--curves", kem_alg
        ]
        result = subprocess.run(command, check=True, capture_output=True)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

# Run the Docker container with OpenSSL
def run_docker_openssl(port):
    try:
        command = [
            "docker", "run", "-v", f"{os.getcwd()}:/ca", DOCKER_IMAGE,
            "openssl", "s_client", "--connect", f"test.openquantumsafe.org:{port}",
            "-CAfile", "/ca/CA.crt"
        ]
        result = subprocess.run(command, check=True, capture_output=True)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

# function to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# function to run the test
@app.route('/run-test', methods=['POST'])
def run_test():
    ca_message = download_ca_certificate()
    openssl_result = run_docker_openssl(6000)  # Call this once outside the loop
    output = []
    for combination in ALGORITHM_COMBINATIONS:
        curl_result = run_docker_curl(combination["port"], combination["kem_alg"])
        output.append((combination, curl_result))
    
    return render_template('results.html', output=output, ca_message=ca_message, openssl_result=openssl_result)


if __name__ == '__main__':
    app.run(debug=True)
