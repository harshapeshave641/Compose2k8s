import yaml
import os

def generate_hpa(service_name, min_replicas=1, max_replicas=5, cpu_utilization=80):
    return {
        "apiVersion": "autoscaling/v2",
        "kind": "HorizontalPodAutoscaler",
        "metadata": {
            "name": f"{service_name}-hpa"
        },
        "spec": {
            "scaleTargetRef": {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "name": service_name
            },
            "minReplicas": min_replicas,
            "maxReplicas": max_replicas,
            "metrics": [
                {
                    "type": "Resource",
                    "resource": {
                        "name": "cpu",
                        "target": {
                            "type": "Utilization",
                            "averageUtilization": cpu_utilization
                        }
                    }
                }
            ]
        }
    }

def generate_hpas_for_services(services, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for service_name in services:
        hpa = generate_hpa(service_name)
        with open(os.path.join(output_dir, f"{service_name}-hpa.yaml"), "w") as f:
            yaml.dump(hpa, f)
        print(f"HPA manifest for service '{service_name}' generated.")

