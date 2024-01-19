# Author: Ray Beecham
# Date: 1/18/2024

import subprocess


# function to run a Docker container from the specified image with optional environment variables
def run_docker_container(
    image_name: str = "openquantumsafe/curl",
    additional_args: str = "",
    env_vars: dict = None,
):
    env_args = (
        " ".join([f"-e {k}={v}" for k, v in env_vars.items()]) if env_vars else ""
    )
    try:
        command = f"docker run {env_args} {additional_args} {image_name}"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Docker container: {e}")


# function to query the server using the specified curves
def query_server(curves: str, url: str = "https://localhost:4433"):
    try:
        command = f"docker run -it openquantumsafe/curl curl --curves {curves} {url}"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error querying the server: {e}")


# function to run a TLS handshake performance test with specified parameters
def run_tls_handshake_performance_test(
    test_time: int = 200, kem_alg: str = "kyber768", sig_alg: str = "dilithium2"
):
    run_docker_container(
        additional_args="-it",
        env_vars={"TEST_TIME": str(test_time), "KEM_ALG": kem_alg, "SIG_ALG": sig_alg},
        image_name="openquantumsafe/curl perftest.sh",
    )


# function to run an algorithm performance test with specified parameters
def run_algorithm_performance_test(seconds: int = 2, alg: str = ""):
    command = (
        f"docker run -it openquantumsafe/curl openssl speed -seconds {seconds} {alg}"
    )
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running algorithm performance test: {e}")


if __name__ == "__main__":
    # Run the Docker container
    run_docker_container()

    # Query the server
    query_server("kyber768")

    # Run TLS handshake performance test
    run_tls_handshake_performance_test(5, "kyber768", "dilithium3")

    # Run specific algorithm performance test
    run_algorithm_performance_test(2, "kyber512")
