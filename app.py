from flask import Flask, request, jsonify
import subprocess
import os
import uuid
import platform
import importlib.util
import json

app = Flask(__name__)
UPLOAD_FOLDER = "/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/execute", methods=["POST"])
def execute():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        uploaded_file = request.files["file"]
        unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        uploaded_file.save(file_path)

        # Determine OS
        current_os = platform.system()

        if current_os == "Linux":
            # Use nsjail on Linux
            cmd = [
                "nsjail",
                "-Mo",
                "--rlimit_cpu", "5",
                "--rlimit_as", "200",
                "--disable_proc",
                "--chroot", "/app",
                "--user", "1000",
                "--group", "1000",
                "--",
                "python3", file_path
            ]
        else:
            # macOS / others: run script directly
            cmd = ["python3", file_path]

        # Run the script
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )

        stdout_data = process.stdout.strip()
        stderr_data = process.stderr.strip()

        # Dynamically import and call main()
        spec = importlib.util.spec_from_file_location("user_script", file_path)
        user_script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_script)

        # Check if main exists
        if not hasattr(user_script, "main"):
            return jsonify({"error": "Uploaded script does not define a main() function"}), 400

        # Call main() and check JSON-serializable
        result_data = user_script.main()
        try:
            json.dumps(result_data)  # Test if JSON-serializable
        except (TypeError, ValueError):
            return jsonify({"error": "Return value of main() is not JSON-serializable"}), 400

        return jsonify({
            "result": result_data,
            "stdout": stdout_data,
            "stderr": stderr_data
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 408
    except Exception as e:
        return jsonify({"error": str(e)}), 500
