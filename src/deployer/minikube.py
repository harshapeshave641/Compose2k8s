import subprocess
import os
import sys

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(result.returncode)

def apply_manifests_in_order(output_dir):
    # Define the order of resource types
    order = [
        "configmap",
        "secret",
        "persistentvolumeclaim",
        "deployment",
        "service",
        "ingress"
    ]
    files = os.listdir(output_dir)
    # Apply files by resource type order
    for kind in order:
        for file in files:
            if kind in file.lower() and file.endswith(".yaml"):
                run_command(f"kubectl apply -f \"{os.path.join(output_dir, file)}\"")

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output"))

    # Start minikube if not running
    print("Checking if Minikube is running...")
    status = subprocess.run("minikube status", shell=True, capture_output=True, text=True)
    if "Running" not in status.stdout:
        print("Starting Minikube...")
        run_command("minikube start")
    else:
        print("Minikube is already running.")

    # Apply manifests in the correct order
    print(f"Applying Kubernetes manifests from {output_dir} in the correct order...")
    apply_manifests_in_order(output_dir)

    print("\nAll manifests applied!")
    print("To check your pods and services, run:")
    print("  kubectl get pods")
    print("  kubectl get svc")
    print("\nTo access your app via Ingress, run:")
    print("  minikube tunnel")
    print("and visit the host defined in your ingress config (e.g., http://myapp.local).")

if __name__ == "__main__":
    main()