# Author: Ray Beecham
# Date: 1/18/2024

import subprocess
import os
import requests

CA_CERT_URL = "https://test.openquantumsafe.org/CA.crt"
CA_CERT_PATH = "CA.crt"
DOCKER_IMAGE = "openquantumsafe/curl:latest"
OQS_SERVER_URL = "https://test.openquantumsafe.org"

ALGORITHM_COMBINATIONS = [
    {"sig_alg": "ecdsap256", "kem_alg": "bikel1", "port": 6001},
    {"sig_alg": "ecdsap256", "kem_alg": "bikel3", "port": 6002},
]


# function to download the CA certificate
def download_ca_certificate():
    try:
        response = requests.get(CA_CERT_URL)
        with open(CA_CERT_PATH, "wb") as file:
            file.write(response.content)
        print(f"Downloaded CA certificate to {CA_CERT_PATH}")
    except requests.RequestException as e:
        print(f"Failed to download CA certificate: {e}")


# function to run curl in a Docker container
def run_docker_curl(port, kem_alg):
    try:
        command = [
            "docker",
            "run",
            "-v",
            f"{os.getcwd()}:/ca",
            "-it",
            DOCKER_IMAGE,
            "curl",
            "--cacert",
            "/ca/CA.crt",
            f"{OQS_SERVER_URL}:{port}",
            "--curves",
            kem_alg,
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Docker curl command: {e}")


# function to run oppenssl in a Docker container
def run_docker_openssl(port):
    try:
        command = [
            "docker",
            "run",
            "-v",
            f"{os.getcwd()}:/ca",
            "-it",
            DOCKER_IMAGE,
            "openssl",
            "s_client",
            "--connect",
            f"test.openquantumsafe.org:{port}",
            "-CAfile",
            "/ca/CA.crt",
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Docker openssl command: {e}")


# function to test a combination of algorithms
def test_combination(combination):
    print(
        f"\nTesting combination: {combination['sig_alg']} with {combination['kem_alg']} on port {combination['port']}"
    )
    run_docker_curl(combination["port"], combination["kem_alg"])
    run_docker_openssl(6000)


def main():
    download_ca_certificate()
    for combination in ALGORITHM_COMBINATIONS:
        test_combination(combination)


if __name__ == "__main__":
    main()
