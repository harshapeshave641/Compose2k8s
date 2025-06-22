from utils.env import is_secret_key
import os

def generate_deployment(service_name, config, named_volumes=None):
    named_volumes = named_volumes or set()

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

    if config.get('command'):
        container['command'] = config['command'] if isinstance(config['command'], list) else [config['command']]

    ports = config.get('ports')
    if ports:
        container['ports'] = []
        for port in ports:
            if ':' in port:
                _, container_port = port.split(':')
            else:
                container_port = port
            container['ports'].append({'containerPort': int(container_port)})

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
        vol_name = f"{service_name}-volume-{idx}"

        if ':' not in v:
            # Named volume without mountPath → skip or default?
            if v in named_volumes:
                continue  # Might need to mount elsewhere
            continue

        host_path, container_path = v.split(':', 1)

        volume_mounts.append({
            'name': vol_name,
            'mountPath': container_path
        })

        if host_path.strip() == "":
            # emptyDir
            volumes.append({
                'name': vol_name,
                'emptyDir': {}
            })
        elif host_path.startswith('.') or host_path.startswith('/'):
            # hostPath
            abs_path = os.path.abspath(host_path)
            volumes.append({
                'name': vol_name,
                'hostPath': {
                    'path': abs_path,
                    'type': 'DirectoryOrCreate'
                }
            })
        elif host_path in named_volumes:
            # PVC
            volumes.append({
                'name': vol_name,
                'persistentVolumeClaim': {
                    'claimName': host_path
                }
            })
        else:
            # Fallback to PVC if unknown
            volumes.append({
                'name': vol_name,
                'persistentVolumeClaim': {
                    'claimName': host_path
                }
            })
        
        container['resources'] = {
            "requests": {
                "cpu": "100m",
                "memory": "128Mi"
            },
            "limits": {
                "cpu": "500m",
                "memory": "512Mi"
            }
        }       

    
    if volume_mounts:
        container['volumeMounts'] = volume_mounts
        deployment['spec']['template']['spec']['volumes'] = volumes

    return deployment
