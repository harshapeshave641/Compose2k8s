import argparse
import os
import yaml
from parser.yamlParser import parse_docker_compose
from generator.generate_deployment import generate_deployment
from generator.generate_service import generate_service
from generator.generate_ingress import generate_ingress_from_config
from utils.env import generate_configmap_and_secret
def main():
    parser = argparse.ArgumentParser(description='Convert Docker Compose to Kubernetes manifests')
    parser.add_argument('compose_file', help='Path to docker-compose.yml')
    parser.add_argument('--ingress-config', help='Path to ingress-config.yml', required=False)

    args = parser.parse_args()

    compose_data = parse_docker_compose(args.compose_file)
    services = compose_data.get('services', {})

    os.makedirs('output', exist_ok=True)

    for service_name, service_config in services.items():
        # Generate Deployment
        deployment = generate_deployment(service_name, service_config)
        with open(f'output/{service_name}-deployment.yaml', 'w') as f:
            yaml.dump(deployment, f)
        
        # Generate Service (if ports exist)
        if service_config.get('ports'):
            service = generate_service(service_name, service_config)
            with open(f'output/{service_name}-service.yaml', 'w') as f:
                yaml.dump(service, f)

        manifests = generate_configmap_and_secret(service_name, service_config.get('environment', []))
        for filename, manifest in manifests:
            with open(f'output/{filename}', 'w') as f:
                yaml.dump(manifest, f)

    if args.ingress_config:
        ingress = generate_ingress_from_config(args.ingress_config)
        with open('output/ingress.yaml', 'w') as f:
            yaml.dump(ingress, f)
        print("Ingress manifest generated.")

    print(f"Generated manifests are saved in the 'output' directory.")

if __name__ == "__main__":
    main()