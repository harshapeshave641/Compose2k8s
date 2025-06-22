def generate_service(service_name, config):
    ports = config.get('ports')
    if not ports:
        return None 

    service_ports = []
    for port in ports:
        if isinstance(port, int):
            target = port
            exposed = port
        elif isinstance(port, str):
            if ':' in port:
                exposed, target = port.split(':')
            else:
                exposed = target = port
        else:
            continue

        service_ports.append({
            'port': int(exposed),
            'targetPort': int(target),
            'protocol': 'TCP'
        })

    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': f"{service_name}-svc"
        },
        'spec': {
            'selector': {
                'app': service_name
            },
            'ports': service_ports,
            'type': 'ClusterIP'
        }
    }

    return service
