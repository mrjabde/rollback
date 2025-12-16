# Demo: Kubernetes & Helm Rollback

## Prérequis
Remplacer `DOCKER_USER` par votre nom d'utilisateur DockerHub dans tous les fichiers (`k8s/deployment.yaml`, `helm/values.yaml`).

## Étape 1 : Build & Push des images

Nous allons construire deux versions distinctes de la même app.

```bash
# 1. Build Version 1 (Texte Bleu)
docker build --build-arg VER=1 -t abdessamaddevops/flask-app:v1 .

# 2. Build Version 2 (Texte Rouge)
docker build --build-arg VER=2 -t abdessamaddevops/flask-app:v2 .

# 3. Push vers le registre
docker push abdessamaddevops/flask-app:v1
docker push abdessamaddevops/flask-app:v2

kubectl create namespace flask-app
kubectl apply -f k8s/deployment.yaml
kubectl port-forward svc/flask-app 8080:80 -n flask-app
# Vérifier dans le navigateur : http://localhost:30001 -> Affiche "Version 1"
kubectl set image deployment/flask-app flask=abdessamaddevops/flask-app:v2 -n flask-app
kubectl port-forward svc/flask-app 8080:80 -n flask-app
# Vérifier dans le navigateur -> Affiche "Version 2"
# Vérifier l'historique
kubectl rollout history deployment/flask-app -n flask-app

# Annuler le déploiement
kubectl rollout undo deployment/flask-app -n flask-app
kubectl port-forward svc/flask-app 8080:80 -n flask-app

# Vérifier le statut
kubectl rollout status deployment/flask-app -n flask-app
# Vérifier dans le navigateur -> Retour à "Version 1"

kubectl delete -f k8s/deployment.yaml

# Installation initiale avec le tag v1
helm install flask-app ./helm -n flask-app --set image.tag=v1
kubectl port-forward svc/flask-app 8080:80 -n flask-app
# Vérifier navigateur -> "Version 1"

# Upgrade vers le tag v2
helm upgrade flask-app ./helm -n flask-app --set image.tag=v2
kubectl port-forward svc/flask-app 8080:80 -n flask-app
# Vérifier navigateur -> "Version 2"

# Voir l'historique des releases
helm history flask-app -n flask-app

# Rollback à la révision 1 (qui utilisait l'image v1)
helm rollback flask-app 1 -n flask-app
kubectl port-forward svc/flask-app 8080:80 -n flask-app

# Vérifier navigateur -> Retour à "Version 1"