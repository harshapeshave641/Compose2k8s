import yaml
def parse_docker_compose(file_path):
    with open(file_path, 'r') as f:
        compose_data = yaml.safe_load(f)

    print(compose_data)
    services = compose_data.get('services', {})
    print(f"Found {len(services)} service(s): {list(services.keys())}")

    for service_name, service_config in services.items():
        print(f"\n=== {service_name} ===")
        print(f"Image: {service_config.get('image')}")
        print(f"Ports: {service_config.get('ports')}")
        print(f"Environment: {service_config.get('environment')}")
        print(f"Depends on: {service_config.get('depends_on')}")
    return compose_data

if __name__ == "__main__":
    parse_docker_compose("../../samples/sample1.yml")
