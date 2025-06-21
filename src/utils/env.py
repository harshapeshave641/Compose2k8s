import os
import re

def is_secret_key(key):
    key = key.lower()
    return any(word in key for word in ["password", "secret", "token", "key"])

def resolve_env_value(value):
    # Handles $VAR or ${VAR}
    match = re.match(r"\$?\{?(\w+)\}?", value)
    if match:
        var_name = match.group(1)
        return os.environ.get(var_name, "")
    return value

def generate_configmap_and_secret(service_name, env_list):
    configmap_data = {}
    secret_data = {}

    for item in env_list:
        if isinstance(item, str) and '=' in item:
            k, v = item.split('=', 1)
        elif isinstance(item, dict):
            k, v = list(item.items())[0]
        else:
            continue

        resolved_v = resolve_env_value(v)
        if is_secret_key(k):
            secret_data[k] = resolved_v
        else:
            configmap_data[k] = resolved_v

    manifests = []

    if configmap_data:
        configmap = {
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {
                'name': f"{service_name}-config"
            },
            'data': configmap_data
        }
        manifests.append((f"{service_name}-configmap.yaml", configmap))

    if secret_data:
        secret = {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {
                'name': f"{service_name}-secret"
            },
            'type': 'Opaque',
            'stringData': secret_data
        }
        manifests.append((f"{service_name}-secret.yaml", secret))

    return manifests
