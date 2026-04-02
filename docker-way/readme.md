## System Monitoring Bot

This project allows you to check basic system properties such as:

1. Free Memory
2. Disk Space
3. Uptime
4. List files in a directory
5. CPU Usage

---

## Setup Instructions

Clone the repository, navigate to the `docker` folder, build the image, and run it.

---

### **Approach 1**

* Make sure your LLM is running on the host machine
* Run the container using:

```bash
docker run -d -e BOT_TOKEN=<Replace-Your-Token> <your-image-name>
```

---

### **Approach 2**

* Run the Docker container for Ollama:

```bash
docker run -d --name ollama ollama/ollama
```

* Exec into the container:

```bash
docker exec -it ollama bash
```

* Pull the model:

```bash
ollama pull llama2
```

---

### **Approach 3**

* Simply run:

```bash
docker-compose up
```
