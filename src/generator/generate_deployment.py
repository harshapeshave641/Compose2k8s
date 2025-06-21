from utils.env import is_secret_key
import os

def generate_deployment(service_name, config):
    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': service_name,
            'labels': {'app': service_name}
        },
        'spec': {
            'replicas': 1,
            'selector': {'matchLabels': {'app': service_name}},
            'template': {
                'metadata': {'labels': {'app': service_name}},
                'spec': {
                    'containers': [
                        {
                            'name': service_name,
                            'image': config.get('image'),
                        }
                    ]
                }
            }
        }
    }

    container = deployment['spec']['template']['spec']['containers'][0]

    # Command
    if config.get('command'):
        container['command'] = config['command'] if isinstance(config['command'], list) else [config['command']]

    # Ports
    ports = config.get('ports')
    if ports:
        container['ports'] = []
        for port in ports:
            if ':' in port:
                _, container_port = port.split(':')
            else:
                container_port = port
            container['ports'].append({'containerPort': int(container_port)})

    # Environment: envFrom ConfigMap/Secret
    env = config.get('environment')
    if env:
        container['envFrom'] = []
        if any(not is_secret_key(e.split('=')[0] if isinstance(e, str) else list(e.keys())[0]) for e in env):
            container['envFrom'].append({'configMapRef': {'name': f"{service_name}-config"}})
        if any(is_secret_key(e.split('=')[0] if isinstance(e, str) else list(e.keys())[0]) for e in env):
            container['envFrom'].append({'secretRef': {'name': f"{service_name}-secret"}})

    # Volumes
    volume_mounts = []
    volumes = []
    volume_defs = config.get('volumes', [])
    for idx, v in enumerate(volume_defs):
        if ':' not in v:
            continue  # Skip named volumes for now

        host_path, container_path = v.split(':', 1)
        host_path = os.path.abspath(host_path)

        vol_name = f"{service_name}-volume-{idx}"

        volume_mounts.append({
            'name': vol_name,
            'mountPath': container_path
        })

        volumes.append({
            'name': vol_name,
            'hostPath': {
                'path': host_path,
                'type': 'DirectoryOrCreate'
            }
        })

    if volume_mounts:
        container['volumeMounts'] = volume_mounts
        deployment['spec']['template']['spec']['volumes'] = volumes

    return deployment
