# Installing Airflow

## Add Helm Repository

```bash
helm repo add bitnami-azure https://marketplace.azurecr.io/helm/v1/repo
```

## Install airflow with Helm

```bash
# Helm release name
HELM_RELEASE_NAME=airflow-dev-sunrise
# Target namespace
NAMESPACE=airflow
# Helm chart
HELM_CHART=apache-airflow/airflow
# Install
helm install $HELM_RELEASE_NAME $HELM_CHART --namespace $NAMESPACE --debug --set airflow.cloneDagFilesFromGit.enabled=true \
                --set airflow.cloneDagFilesFromGit.repository=https://github.com/qurixtechnology/airflow-dags \
                --set airflow.cloneDagFilesFromGit.branch=main \
                --set airflow.baseUrl=http://127.0.0.1:8080
```

```bash
# Update Helm
helm upgrade $AIRFLOW_RELEASE bitnami-azure/airflow --namespace $NAMESPACE --set airflow.cloneDagFilesFromGit.enabled=true \
                --set airflow.cloneDagFilesFromGit.repository=https://github.com/qurixtechnology/airflow-dags \
                --set airflow.cloneDagFilesFromGit.branch=main \
                --set airflow.baseUrl=http://127.0.0.1:8080 
```

## Check Service

```bash
kubectl describe svc $AIRFLOW_RELEASE -n $NAMESPACE
```

```bash
helm show values bitnami/airflow > values.yaml
```

## Update Helm values

```bash
helm show values apache-airflow/airflow > values.yaml

helm upgrade --install airflow apache-airflow/airflow -n airflow  \
  -f values.yaml \
  --debug
```

## Add Ingress

```bash
NAMESPACE=ingress-basic

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --create-namespace \
  --namespace $NAMESPACE \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz

# Add the ingress-nginx repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

```


## Get credentials

```bash
export AIRFLOW_PASSWORD=$(kubectl get secret --namespace "default" airflow-dev-sunrise -o jsonpath="{.data.airflow-password}" | base64 --decode)
```