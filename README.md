# 🚀 Kubernetes ChatOps Monitoring Bot

A ChatOps-based system that integrates **Telegram Bot + LLM (Ollama) + Kubernetes** to monitor, manage, and automate cluster operations.

---

## 📌 Features

* ✅ Check Pods & Deployments
* ✅ Scale Deployments
* ✅ Detect Failures (CrashLoopBackOff, etc.)
* ✅ Monitor Cluster State
* ✅ Real-time Alerts on Telegram
* ✅ LLM-powered interaction (via Ollama)

---

## 🏗️ Architecture

```
User (Telegram)
      │
      ▼
Telegram Bot (Python)
      │
      ▼
LLM (Ollama - optional)
      │
      ▼
Kubernetes API Server
      │
      ├── Get Resources (Pods, Deployments)
      ├── Perform Actions (Scale, Restart)
      └── Watch Events (Failures, Alerts)
                │
                ▼
        Telegram Notifications
```

---

## ⚙️ Setup Guide

Detailed setup instructions are split into separate guides:

* 🖥️ **VM / Local Setup**
  → See: `docs/vm-setup.md`

* 🐳 **Docker Setup (All approaches)**
  → See: `docs/docker-setup.md`

* ☸️ **Kubernetes Deployment**
  → See: `docs/k8s-setup.md`

---

## 📡 Example Commands (Telegram)

* `pod` → List all pods
* `/deployments` → List deployments
* `/scale nginx 3` → Scale deployment
* `/status` → Cluster status
* `/alerts` → Recent failures

---

## 🔥 DevOps Concepts Demonstrated

* ChatOps (Telegram Bot automation)
* Kubernetes API interaction
* Docker containerization
* Infrastructure as Code (K8s manifests)
* Monitoring & Alerting
* LLM integration (Ollama)

---

## 📈 Future Improvements

* 🔹 Add Prometheus + Grafana monitoring
* 🔹 Implement RBAC for security
* 🔹 Replace subprocess with Kubernetes Python Client
* 🔹 Add CI/CD pipeline (Jenkins / GitHub Actions)
* 🔹 Webhook-based Telegram bot

---

## 👨‍💻 Author

**Suhail Akthar**
Aspiring DevOps & Cloud Engineer
