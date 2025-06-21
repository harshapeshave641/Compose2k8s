# Compose-to-K8s

A Python tool to convert Docker Compose files into Kubernetes manifests and deploy them to a local Minikube cluster.

---

## Features

- Parse Docker Compose YAML and generate:
  - Kubernetes Deployments
  - Services
  - ConfigMaps and Secrets (from environment variables)
  - Ingress (from a simple config file)
- Output all manifests to an `output/` directory
- Script to deploy all generated manifests to Minikube in the correct order

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
python -m src.parser.cli samples/sample1.yml --ingress-config samples/ingress-config.yml
```

- All manifests will be written to the `output/` directory.

### 2. Deploy to Minikube

```sh
python src/deployer/deploy_to_minikube.py
```

- This will start Minikube (if needed) and apply all manifests in the correct order.

---

## Sample Files

- `samples/sample1.yml` — Example Docker Compose file
- `samples/ingress-config.yml` — Example Ingress configuration

---

## Notes

- Images referenced in your Compose file **must be built and pushed to a registry** (e.g., Docker Hub) before deploying to Kubernetes.
- The generated manifests provide a solid foundation for running your app on Kubernetes. For advanced features (storage, resource limits, etc.), you can extend the manifests as needed.

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
├── requirements.txt
└── README.md
```

---

## License

MIT License