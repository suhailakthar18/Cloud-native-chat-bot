import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

from kubernetes import client, config

# ------------------- CONFIG -------------------

BOT_TOKEN = os.getenv("BOT_TOKEN")
OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL = "llama2"

# ✅ Your Chat ID
CHAT_ID = 765360130

# ------------------- K8s SETUP -------------------

try:
    config.load_incluster_config()
except:
    config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

# ------------------- OLLAMA -------------------

def call_ollama(prompt):
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        return res.json().get("response", "Error from model")
    except Exception as e:
        return f"Ollama error: {str(e)}"

# ------------------- K8s FUNCTIONS -------------------

def get_pods(all_namespaces=False):
    if all_namespaces:
        pods = v1.list_pod_for_all_namespaces()
        return [f"{p.metadata.namespace}/{p.metadata.name} - {p.status.phase}" for p in pods.items]
    else:
        pods = v1.list_namespaced_pod(namespace="default")
        return [f"{p.metadata.name} - {p.status.phase}" for p in pods.items]

def get_deployments():
    deps = apps_v1.list_deployment_for_all_namespaces()
    return [f"{d.metadata.namespace}/{d.metadata.name}" for d in deps.items]

def get_failing_pods():
    pods = v1.list_pod_for_all_namespaces()
    failing = []

    for p in pods.items:
        if p.status.phase != "Running":
            failing.append(f"{p.metadata.namespace}/{p.metadata.name} - {p.status.phase}")

        if p.status.container_statuses:
            for c in p.status.container_statuses:
                if c.state.waiting:
                    reason = c.state.waiting.reason
                    if reason:
                        failing.append(f"{p.metadata.namespace}/{p.metadata.name} - {reason}")

    return list(set(failing)) or ["No failing pods"]

def scale_deployment(name, replicas, namespace="default"):
    try:
        body = {"spec": {"replicas": replicas}}
        apps_v1.patch_namespaced_deployment(name, namespace, body)
        return f"Scaled deployment '{name}' to {replicas} replicas"
    except Exception as e:
        return f"Error scaling deployment: {str(e)}"

def restart_pod(name, namespace="default"):
    try:
        v1.delete_namespaced_pod(name=name, namespace=namespace)
        return f"Pod {name} restarted successfully"
    except Exception as e:
        return f"Error restarting pod: {str(e)}"

# ------------------- ALERT SYSTEM -------------------

ALERTED_PODS = set()

async def monitor_cluster(app):
    while True:
        try:
            failing = get_failing_pods()

            if failing and failing != ["No failing pods"]:
                for pod in failing:
                    if pod not in ALERTED_PODS:
                        ALERTED_PODS.add(pod)

                        await app.bot.send_message(
                            chat_id=CHAT_ID,
                            text=f"⚠️ ALERT: Pod issue detected\n{pod}"
                        )

            await asyncio.sleep(20)

        except Exception as e:
            print(f"Monitor error: {e}")
            await asyncio.sleep(10)

# ------------------- COMMAND HANDLER -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running. Send commands!")

# ------------------- MESSAGE HANDLER -------------------

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    # 🔹 Pod count
    if "how many pods" in user_text:
        pods = get_pods()
        reply = f"Total pods: {len(pods)}"

    # 🔹 All pods (IMPORTANT: first)
    elif "all pods" in user_text:
        reply = "\n".join(get_pods(all_namespaces=True)[:20])

    # 🔹 Default namespace pods
    elif "pods" in user_text and "failing" not in user_text:
        reply = "\n".join(get_pods()[:20])

    # 🔹 Failing pods
    elif "failing pods" in user_text:
        reply = "\n".join(get_failing_pods())

    # 🔹 Deployments
    elif "deployment" in user_text:
        reply = "\n".join(get_deployments())

    # 🔹 Scale deployment
    elif "scale" in user_text:
        try:
            parts = user_text.split()
            name = parts[1]
            replicas = int(parts[2])
            reply = scale_deployment(name, replicas)
        except:
            reply = "Usage: scale <deployment_name> <replicas>"

    # 🔥 Restart pod
    elif "restart pod" in user_text:
        try:
            parts = user_text.split()
            pod_name = parts[-1]
            reply = restart_pod(pod_name)
        except:
            reply = "Usage: restart pod <pod_name>"

    # 🤖 LLM fallback
    else:
        reply = call_ollama(user_text)

    await update.message.reply_text(reply)

# ------------------- MAIN -------------------

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

# Start background monitoring
async def post_init(application):
    application.create_task(monitor_cluster(application))

app.post_init = post_init

print("🚀 Bot running with monitoring + auto-heal")
app.run_polling()
