import subprocess
import os
import sys

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(result.returncode)

def apply_manifests_in_order(base_output):
    # Define the order of resource types and their subfolders
    order = [
        ("configmaps", "configmap"),
        ("secrets", "secret"),
        ("pvcs", "persistentvolumeclaim"),
        ("pvs", "persistentvolume"),
        ("deployments", "deployment"),
        ("services", "service"),
        ("hpas", "horizontalpodautoscaler"),
        ("ingress", "ingress"),
    ]
    for folder, kind in order:
        dir_path = os.path.join(base_output, folder)
        if not os.path.exists(dir_path):
            continue
        files = [f for f in os.listdir(dir_path) if f.endswith(".yaml")]
        for file in files:
            run_command(f"kubectl apply -f \"{os.path.join(dir_path, file)}\"")

def main():
    base_output = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output"))

    # Start minikube if not running
    print("Checking if Minikube is running...")
    status = subprocess.run("minikube status", shell=True, capture_output=True, text=True)
    if "Running" not in status.stdout:
        print("Starting Minikube...")
        run_command("minikube start")
    else:
        print("Minikube is already running.")

    # Apply manifests in the correct order, grouped by resource type
    print(f"Applying Kubernetes manifests from {base_output} in the correct order...")
    apply_manifests_in_order(base_output)

    print("\nAll manifests applied!")
    print("To check your pods and services, run:")
    print("  kubectl get pods")
    print("  kubectl get svc")
    print("\nTo access your app via Ingress, run:")
    print("  minikube tunnel")
    print("and visit the host defined in your ingress config (e.g., http://myapp.local).")

if __name__ == "__main__":
    main()