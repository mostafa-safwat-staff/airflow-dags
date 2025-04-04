# Airflow K8s Ops

A comprehensive project for managing Apache Airflow deployments on Kubernetes (AKS) using Helm.

## Project Structure

```
.
├── README.md
├── dags/                  # Your Airflow DAGs
├── config/                # Configuration files
├── scripts/               # Helper scripts
├── plugins/               # Custom Airflow plugins
├── docker/                # Custom Dockerfile(s)
└── Makefile               # Command management
```

## Prerequisites

- kubectl configured with access to your AKS cluster
- Helm v3 installed
- Docker (if building custom images)
- Make

## Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/airflow-k8s-ops.git
cd airflow-k8s-ops
```

### 2. Update configuration

Edit the files in the `config/` directory to match your environment:
- `airflow-values.yaml`: Main configuration
- `values-dev.yaml`: Development environment specifics
- `values-staging.yaml`: Staging environment specifics
- `values-prod.yaml`: Production environment specifics

### 3. Deploy Airflow

Using Make:
```bash
# Deploy to development environment
make deploy ENV=dev

# Deploy to staging environment
make deploy ENV=staging

# Deploy to production environment
make deploy ENV=prod
```

Using the deploy script:
```bash
./scripts/deploy.sh --env dev --action deploy
```

### 4. Access Airflow UI

```bash
make airflow-ui
```
Then open http://localhost:8080 in your browser

## Common Tasks

### Building custom Airflow image

If you need additional Python packages:

1. Update the `docker/Dockerfile`
2. Build and push the image:
```bash
make build-image
make push-image
```
3. Update your values file to use the custom image

### Adding new DAGs

1. Add your DAG files to the `dags/` directory
2. Add any required Python dependencies to `dags/requirements.txt`
3. Deploy the changes:
```bash
make upgrade
```
