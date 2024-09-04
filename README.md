## Project Overview

This project shows how to set up a Python Flask app that connects to a MongoDB database on a Kubernetes cluster using Minikube. The setup includes features like automatically adjusting resources, saving data permanently, securing access, and managing resources efficiently.

## Prerequisites

Ensure the following tools are installed on your system:
- Python 3.10 or later
- Docker
- Minikube
- kubectl

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Yasin-Siddiquee/Flask-MongoDB_Kubernetes-deployment.git
cd flask-mongodb-k8s
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run MongoDB Using Docker

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 5. Run the Flask Application

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```


## Dockerization

### 1. Build and Push the Docker Image  
Build the Docker image for the Flask application and push it to Docker Hub.

```bash
docker build -t your-dockerhub-username/flask-mongodb-app:latest .
docker push your-dockerhub-username/flask-mongodb-app:latest
```
Replace your-dockerhub-username with your Docker Hub username.


## Kubernetes Deployment

### 1. Start Minikube

```bash
minikube start
```

### 2. Apply Kubernetes YAML Files
Deploy the Flask application and MongoDB to the Kubernetes cluster.

```bash
kubectl apply -f flask-deployment.yaml
kubectl apply -f mongo-statefulset.yaml
kubectl apply -f hpa.yaml
```

## Accessing the Application  
Access the Flask application through the URL provided by Minikube.  
```bash
minikube service flask-service --url
```
Test the endpoints using curl:

- GET request:
```bash
curl <MINIKUBE_URL>
```
- POST request:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"sampleKey":"sampleValue"}' <MINIKUBE_URL>/data
```
- GET data:
```bash
curl <MINIKUBE_URL>/data
```

## DNS Resolution in Kubernetes
Kubernetes uses internal DNS to manage inter-pod communication. Services are automatically assigned DNS names which other pods can use to communicate without needing IP addresses.
- The Flask app connects to MongoDB via the DNS name `mongo-service`, which resolves to the internal cluster IP of the MongoDB service.

## Resource Requests and Limits
The Flask and MongoDB pods are configured with the following requests and limits:

- Flask:
     Request: 0.2 CPU, 250Mi memory
     Limit: 0.5 CPU, 500Mi memory
- MongoDB:
     Request: 0.2 CPU, 250Mi memory
     Limit: 0.5 CPU, 500Mi memory

## Design Choices
- Deployment: Flask is deployed with 2 replicas for redundancy and load balancing.
- StatefulSet for MongoDB: Provides persistent storage with authentication.
- Persistent Volume and Claims: Ensures data persistence even if the MongoDB pod restarts.
- Horizontal Pod Autoscaler: Scales Flask pods based on CPU utilization.
- Resource Requests and Limits: Ensures efficient resource utilization, preventing resource starvation.

## Testing and Autoscaling
To test autoscaling, simulate high CPU load:
```bash
kubectl exec -it <flask-pod-name> -- stress --cpu 2 --timeout 30s
```

Monitor the Horizontal Pod Autoscaler:
```bash
kubectl get hpa -w
```
