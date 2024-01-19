from flask import Blueprint, render_template, request
import subprocess

# Create a Flask Blueprint
alg_perf = Blueprint('alg_perf', __name__, template_folder='templates')

@alg_perf.route('/run-alg-perf-test', methods=['GET', 'POST'])
def run_alg_perf_test():
    if request.method == 'POST':
        alg_name = request.form.get('alg_name', 'kyber512')
        test_seconds = request.form.get('test_seconds', '2')

        command = [
            "docker", "run", "openquantumsafe/curl", "openssl", "speed",
            "-seconds", test_seconds, alg_name
        ]
        result = subprocess.run(command, check=True, capture_output=True)
        alg_perf_result = result.stdout.decode() if result.returncode == 0 else result.stderr.decode()

        return render_template('alg_perf_results.html', alg_perf_result=alg_perf_result)
    else:
        # Render a form for inputting test parameters
        return render_template('alg_perf_test.html')
