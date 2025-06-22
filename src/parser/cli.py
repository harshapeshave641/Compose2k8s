import argparse
import os
import yaml
from parser.yamlParser import parse_docker_compose
from generator.generate_deployment import generate_deployment
from generator.generate_service import generate_service
from generator.generate_ingress import generate_ingress_from_config
from utils.env import generate_configmap_and_secret
from generator.generate_hpa import generate_hpa

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Convert Docker Compose to Kubernetes manifests')
    parser.add_argument('compose_file', help='Path to docker-compose.yml')
    parser.add_argument('--ingress-config', help='Path to ingress-config.yml', required=False)

    args = parser.parse_args()

    compose_data = parse_docker_compose(args.compose_file)
    services = compose_data.get('services', {})

    base_output = 'output'
    dirs = {
        'deployments': os.path.join(base_output, 'deployments'),
        'services': os.path.join(base_output, 'services'),
        'configmaps': os.path.join(base_output, 'configmaps'),
        'secrets': os.path.join(base_output, 'secrets'),
        'hpas': os.path.join(base_output, 'hpas'),
        'pvcs': os.path.join(base_output, 'pvcs'),
        'pvs': os.path.join(base_output, 'pvs'),
        'ingress': os.path.join(base_output, 'ingress')
    }
    for d in dirs.values():
        ensure_dir(d)

    from generator.generate_pvc_pv import generate_pv_and_pvc_templates_from_compose

    # Generate PV and PVCs and move them to correct folders
    generate_pv_and_pvc_templates_from_compose(compose_data, base_output)
    # Move generated PV/PVC files to their folders
    for f in os.listdir(base_output):
        if f.endswith('-pv.yaml'):
            os.replace(os.path.join(base_output, f), os.path.join(dirs['pvs'], f))
        elif f.endswith('-pvc.yaml'):
            os.replace(os.path.join(base_output, f), os.path.join(dirs['pvcs'], f))

    for service_name, service_config in services.items():
        # Deployment
        deployment = generate_deployment(service_name, service_config)
        with open(os.path.join(dirs['deployments'], f'{service_name}-deployment.yaml'), 'w') as f:
            yaml.dump(deployment, f)
        
        # Service
        if service_config.get('ports'):
            service = generate_service(service_name, service_config)
            with open(os.path.join(dirs['services'], f'{service_name}-service.yaml'), 'w') as f:
                yaml.dump(service, f)

        # ConfigMap/Secret
        manifests = generate_configmap_and_secret(service_name, service_config.get('environment', []))
        for filename, manifest in manifests:
            if 'secret' in filename:
                outdir = dirs['secrets']
            else:
                outdir = dirs['configmaps']
            with open(os.path.join(outdir, filename), 'w') as f:
                yaml.dump(manifest, f)

        # HPA
        hpa = generate_hpa(service_name)
        with open(os.path.join(dirs['hpas'], f'{service_name}-hpa.yaml'), 'w') as f:
            yaml.dump(hpa, f)

    if args.ingress_config:
        ingress = generate_ingress_from_config(args.ingress_config)
        with open(os.path.join(dirs['ingress'], 'ingress.yaml'), 'w') as f:
            yaml.dump(ingress, f)
        print("Ingress manifest generated.")

    print(f"Generated manifests are saved in the '{base_output}' directory, grouped by resource type.")

if __name__ == "__main__":
    main()