import yaml

def generate_ingress_from_config(config_path):
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)

    ingress_cfg = data.get('ingress', {})
    host = ingress_cfg.get('host', 'local.project.test')
    rules = ingress_cfg.get('rules', [])
    tls_cfg = ingress_cfg.get('tls', {})

    paths = []
    for entry in rules:
        service = entry['service']
        path = entry['path']
        port = entry['port']
        paths.append({
            'path': path,
            'pathType': 'Prefix',
            'backend': {
                'service': {
                    'name': f"{service}-svc",
                    'port': {'number': port}
                }
            }
        })

    ingress = {
        'apiVersion': 'networking.k8s.io/v1',
        'kind': 'Ingress',
        'metadata': {
            'name': 'project-ingress',
            'annotations': {
                'nginx.ingress.kubernetes.io/rewrite-target': '/'
            }
        },
        'spec': {
            'rules': [
                {
                    'host': host,
                    'http': {
                        'paths': paths
                    }
                }
            ]
        }
    }

    # Add TLS if enabled
    if tls_cfg.get('enabled'):
        ingress['spec']['tls'] = [{
            'hosts': [host],
            'secretName': tls_cfg.get('secretName', 'tls-secret')
        }]

    return ingress