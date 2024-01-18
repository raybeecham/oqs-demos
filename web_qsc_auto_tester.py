from flask import Flask, render_template, request
import subprocess
import os
import requests

app = Flask(__name__)

CA_CERT_URL = "https://test.openquantumsafe.org/CA.crt"
CA_CERT_PATH = "CA.crt"
DOCKER_IMAGE = "openquantumsafe/curl:latest"
OQS_SERVER_URL = "https://test.openquantumsafe.org"

ALGORITHM_COMBINATIONS = [
    {"sig_alg": "ecdsap256", "kem_alg": "bikel1", "port": 6001},
    {"sig_alg": "ecdsap256", "kem_alg": "bikel3", "port": 6002},
    # Add more combinations as needed
]

def download_ca_certificate():
    try:
        response = requests.get(CA_CERT_URL)
        with open(CA_CERT_PATH, 'wb') as file:
            file.write(response.content)
    except requests.RequestException as e:
        return f"Failed to download CA certificate: {e}"
    return "Downloaded CA certificate."

def run_docker_curl(port, kem_alg):
    try:
        command = [
            "docker", "run", "-v", f"{os.getcwd()}:/ca", "-it", DOCKER_IMAGE,
            "curl", "--cacert", "/ca/CA.crt",
            f"{OQS_SERVER_URL}:{port}", "--curves", kem_alg
        ]
        result = subprocess.run(command, check=True, capture_output=True)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

def run_docker_openssl(port):
    try:
        command = [
            "docker", "run", "-v", f"{os.getcwd()}:/ca", "-it", DOCKER_IMAGE,
            "openssl", "s_client", "--connect", f"test.openquantumsafe.org:{port}",
            "-CAfile", "/ca/CA.crt"
        ]
        result = subprocess.run(command, check=True, capture_output=True)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-test', methods=['POST'])
def run_test():
    ca_message = download_ca_certificate()
    output = []
    for combination in ALGORITHM_COMBINATIONS:
        curl_result = run_docker_curl(combination["port"], combination["kem_alg"])
        openssl_result = run_docker_openssl(6000)
        output.append((combination, curl_result, openssl_result))
    return render_template('results.html', output=output, ca_message=ca_message)

if __name__ == '__main__':
    app.run(debug=True)
