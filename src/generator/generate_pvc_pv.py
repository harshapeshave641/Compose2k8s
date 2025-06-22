import yaml
import os

def generate_pv(volume_name, host_path="/mnt/data", size="1Gi", access_modes=None):
    access_modes = access_modes or ["ReadWriteOnce"]
    return {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {"name": f"{volume_name}-pv"},
        "spec": {
            "capacity": {"storage": size},
            "accessModes": access_modes,
            "hostPath": {"path": os.path.join(host_path, volume_name)},
            "persistentVolumeReclaimPolicy": "Retain"
        }
    }

def generate_pvc(volume_name, size="1Gi", access_modes=None):
    access_modes = access_modes or ["ReadWriteOnce"]
    return {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {"name": f"{volume_name}-pvc"},
        "spec": {
            "accessModes": access_modes,
            "resources": {"requests": {"storage": size}},
            "volumeName": f"{volume_name}-pv"
        }
    }

def generate_pv_and_pvc_templates_from_compose(compose_data, output_dir, host_path="/mnt/data"):
    named_volumes = compose_data.get("volumes", {})
    if not named_volumes:
        print("No named volumes found in compose file.")
        return

    os.makedirs(output_dir, exist_ok=True)

    for volume_name in named_volumes:
        pv = generate_pv(volume_name, host_path=host_path)
        pvc = generate_pvc(volume_name)
        with open(os.path.join(output_dir, f"{volume_name}-pv.yaml"), "w") as f:
            yaml.dump(pv, f)
        with open(os.path.join(output_dir, f"{volume_name}-pvc.yaml"), "w") as f:
            yaml.dump(pvc, f)
        print(f"PV and PVC templates for volume '{volume_name}' generated.")

