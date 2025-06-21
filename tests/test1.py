import subprocess
import sys
import time
import yaml
import os

def run_command(cmd, capture_output=False):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(result.stdout)
        print(result.stderr)
        sys.exit(result.returncode)
    return result.stdout if capture_output else None

def check_pods_ready(namespace="default", timeout=180):
    print("Checking if all pods are running and ready...")
    for _ in range(timeout // 5):
        output = run_command(f"kubectl get pods -n {namespace}", capture_output=True)
        lines = output.strip().split('\n')[1:]
        if not lines:
            print("No pods found yet.")
            time.sleep(5)
            continue
        all_ready = True
        for line in lines:
            cols = line.split()
            name, ready, status = cols[0], cols[1], cols[2]
            print(f"Pod: {name}, Status: {status}, Ready: {ready}")
            if status != "Running" or not ready.startswith(ready.split('/')[1]):
                all_ready = False
        if all_ready:
            print("All pods are running and ready!")
            return True
        time.sleep(5)
    print("Timeout: Not all pods are running and ready.")
    return False

def check_services(namespace="default"):
    print("\nChecking services...")
    output = run_command(f"kubectl get svc -n {namespace}", capture_output=True)
    print(output)
    return output

def check_ingress(namespace="default"):
    print("\nChecking ingress...")
    output = run_command(f"kubectl get ingress -n {namespace}", capture_output=True)
    print(output)
    return output

def check_configmaps(namespace="default"):
    print("\nChecking ConfigMaps...")
    output = run_command(f"kubectl get configmap -n {namespace}", capture_output=True)
    print(output)
    return output

def check_secrets(namespace="default"):
    print("\nChecking Secrets...")
    output = run_command(f"kubectl get secret -n {namespace}", capture_output=True)
    print(output)
    return output

def check_deployments(namespace="default"):
    print("\nChecking Deployments...")
    output = run_command(f"kubectl get deployment -n {namespace}", capture_output=True)
    print(output)
    return output

def check_pvc(namespace="default"):
    print("\nChecking PersistentVolumeClaims...")
    output = run_command(f"kubectl get pvc -n {namespace}", capture_output=True)
    print(output)
    return output

def validate_yaml_files(output_dir):
    print("\nValidating YAML syntax of generated manifests...")
    for file in os.listdir(output_dir):
        if file.endswith(".yaml"):
            path = os.path.join(output_dir, file)
            try:
                with open(path, 'r') as f:
                    yaml.safe_load(f)
                print(f"{file}: VALID")
            except Exception as e:
                print(f"{file}: INVALID YAML - {e}")

def main():
    print("Running detailed Minikube deployment tests...")

    # Check Minikube status
    status = run_command("minikube status", capture_output=True)
    if "Running" not in status:
        print("Minikube is not running. Please start Minikube and deploy your manifests first.")
        sys.exit(1)

    # Validate YAML files
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output"))
    validate_yaml_files(output_dir)

    # Check Deployments
    check_deployments()

    # Check Pods
    pods_ok = check_pods_ready()
    if not pods_ok:
        print("Pods are not ready. Test failed.")
        sys.exit(1)

    # Check Services
    check_services()

    # Check Ingress
    check_ingress()

    # Check ConfigMaps
    check_configmaps()

    # Check Secrets
    check_secrets()

    # Check PVCs
    check_pvc()

    print("\nAll detailed checks completed. If all resources are present and pods are running, your deployment is healthy!")

if __name__ == "__main__":
    main()