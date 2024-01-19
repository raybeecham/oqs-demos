from flask import Blueprint, render_template, request
import subprocess

# Create a Flask Blueprint
tls_perf = Blueprint("tls_perf", __name__, template_folder="templates")


@tls_perf.route("/run-tls-perf-test", methods=["GET", "POST"])
def run_tls_perf_test():
    if request.method == "POST":
        test_time = request.form.get("test_time", "200")
        kem_alg = request.form.get("kem_alg", "kyber768")
        sig_alg = request.form.get("sig_alg", "dilithium2")

        command = [
            "docker",
            "run",
            "-e",
            f"TEST_TIME={test_time}",
            "-e",
            f"KEM_ALG={kem_alg}",
            "-e",
            f"SIG_ALG={sig_alg}",
            "openquantumsafe/curl",
            "perftest.sh",
        ]
        result = subprocess.run(command, check=True, capture_output=True)
        tls_perf_result = (
            result.stdout.decode() if result.returncode == 0 else result.stderr.decode()
        )

        return render_template("tls_perf_results.html", tls_perf_result=tls_perf_result)
    else:
        # Render a form for inputting test parameters
        return render_template("tls_perf_test.html")
