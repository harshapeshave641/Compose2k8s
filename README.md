# Compose-to-K8s

A Python tool to convert Docker Compose files into organized Kubernetes manifests and deploy them to a local Minikube cluster.

---

## Features (Included)

- **Parse Docker Compose YAML** and generate:
  - Kubernetes **Deployments** (one per service)
  - **Services** (for exposed ports)
  - **ConfigMaps and Secrets** (from environment variables)
  - **PersistentVolumes and PersistentVolumeClaims** (for named volumes)
  - **hostPath Volumes** (for local paths)
  - **HorizontalPodAutoscaler (HPA)** for each service (with default settings)
  - **Ingress** (from a simple config file)
- **Organized output:** All manifests are grouped in the `output/` directory by resource type:
  - `deployments/`, `services/`, `configmaps/`, `secrets/`, `hpas/`, `pvcs/`, `pvs/`, `ingress/`
- **Script to deploy** all generated manifests to Minikube in the correct order (ConfigMaps/Secrets → PV/PVC → Deployments → Services → HPAs → Ingress)

- **Sample Compose and Ingress config files** included
- **YAML validation and deployment testing scripts**

---

## Not Included / Limitations

- **Image building:**  
  Does not build Docker images from Dockerfiles; assumes images are already built and pushed to a registry.
- **depends_on:**  
  Not enforced; only parsed and optionally logged.
- **restart policy:**  
  Not mapped to Kubernetes restart policies.
- **healthcheck:**  
  Not mapped to Kubernetes `livenessProbe` or `readinessProbe`.
- **Resource limits/requests:**  
  Compose `deploy.resources` not mapped to Kubernetes resource settings (default values are set).
- **Advanced networking:**  
  Compose `networks`, `network_mode`, `extra_hosts`, `dns`, etc. are not mapped.
- **Logging:**  
  Compose logging options are not mapped to Kubernetes logging.
- **Placement/constraints:**  
  Compose `deploy.placement` and node constraints are not mapped.
- **Update/rollback config:**  
  Compose `deploy.update_config` and `rollback_config` are not mapped.
- **External secrets/configs:**  
  Only inline environment variables are supported; Compose `secrets` and `configs` (external files) are not mapped.
- **Multiple Compose files:**  
  Only a single Compose file is supported at a time; no support for overrides or file merging.
- **Custom labels/annotations:**  
  Only basic labels are set; custom Compose labels are not mapped to Kubernetes labels or annotations.
- **Service types:**  
  Only ClusterIP services are created by default; no support for NodePort or LoadBalancer types unless manually edited.
- **Compose extensions:**  
  Extensions like `extends` or `profiles` are not supported.
- **Image pull policies:**  
  No mapping for Compose `pull_policy` or Kubernetes `imagePullPolicy`.

---

## Requirements

- Python 3.7+
- [PyYAML](https://pypi.org/project/PyYAML/)
- [Minikube](https://minikube.sigs.k8s.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

Install Python dependencies:
```sh
pip install -r requirements.txt
```

---

## Usage

### 1. Generate Kubernetes Manifests

```sh
python src/cli.py generate samples/sample1.yml --ingress-config samples/ingress-config.yml
```

- All manifests will be written to the `output/` directory, grouped by resource type.

### 2. List Generated Files

```sh
python src/cli.py list
```

### 3. View a Specific Manifest

```sh
python src/cli.py view deployments/web-deployment.yaml
```

### 4. Deploy to Minikube

```sh
python src/deployer/minikube.py
```

- This will start Minikube (if needed) and apply all manifests in the correct order.

### 5. Test the Deployment

```sh
python src/cli.py test
```

### 6. Clean Output Directory

```sh
python src/cli.py clean
```

---

## Sample Files

- `samples/sample1.yml` — Example Docker Compose file
- `samples/ingress-config.yml` — Example Ingress configuration

---

## Notes

- Images referenced in your Compose file **must be built and pushed to a registry** (e.g., Docker Hub) before deploying to Kubernetes.
- The generated manifests provide a solid foundation for running your app on Kubernetes. For advanced features (storage, resource limits, etc.), you can extend the manifests as needed.
- See the "Not Included / Limitations" section above for unsupported Compose features.

---

## Project Structure

```
compose-to-k8s/
├── src/
│   ├── parser/
│   ├── generator/
│   ├── utils/
│   └── deployer/
├── samples/
├── output/
│   ├── deployments/
│   ├── services/
│   ├── configmaps/
│   ├── secrets/
│   ├── hpas/
│   ├── pvcs/
│   ├── pvs/
│   └── ingress/
├── requirements.txt
└── README.md
```

---

## License

MIT License
