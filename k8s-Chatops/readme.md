## Kubernetes Monitoring Bot

This project enables you to monitor Kubernetes objects and receive alerts when changes occur.

### Features

1. Check Pods
2. Check Deployments
3. Scale Deployments
4. Detect Pod/Deployment Failures
5. Monitor Cluster State
6. Receive Alerts

---

## Prerequisites

Make sure the following are installed:

* Docker (with proper permissions)
* kubectl
* kind (Kubernetes in Docker)

---

## Setup Instructions

### Step 1 — Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

```bash
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

### Verify kubectl

```bash
kubectl version --client
```

---

### Step 2 — Install kind

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
```

```bash
chmod +x kind
sudo mv kind /usr/local/bin/
```

### Verify kind

```bash
kind --version
```

---

### Step 3 — Create and Verify Cluster

```bash
kind create cluster
```

```bash
kubectl get nodes
```

---

### Step 4 — Test Kubernetes Setup

```bash
kubectl create deployment nginx --image=nginx
kubectl get pods
```

---

### Step 5 — Configure Bot Secret

Navigate to the Kubernetes manifests:

```bash
cd k8s_files
```

Encode your Telegram bot token:

```bash
echo -n "your_token" | base64
```

Replace the encoded value in the `secrets.yaml` file.

---

### Step 6 — Deploy to Kubernetes

```bash
kubectl apply -f .
```

---

## Notes

* Ensure your cluster is running before deploying
* Verify all resources using:

```bash
kubectl get all
```
