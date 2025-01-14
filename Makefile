ENV_FILE := .env

ifneq (,$(wildcard $(ENV_FILE)))
  include $(ENV_FILE)
  export $(shell grep -v '^#\|^$$' $(ENV_FILE) | sed 's/ *=.*//' | xargs)
#   export $(shell sed 's/=.*//' $(ENV_FILE))
endif

# Variables
REGISTRY_NAME?=

# SERVICE_DIR ?=
IMAGE_NAME ?=
IMAGE_TAG ?= $(shell git rev-parse --short HEAD)

# DOCKER_IMAGE_NAME:=${REGISTRY_NAME}/$(IMAGE_NAME)

K8S_NAMESPACE=churn-api-dev
K8S_CONFIG_PATH=k8s/overlays/dev


# Docker build and push targets
.PHONE: build
build: DOCKER_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
build:	
	@echo "Building Docker image.."
	@echo "IMAGE:: $(DOCKER_IMAGE_NAME):$(IMAGE_TAG)"
	@cd $(SERVICE_DIR) && \
	docker build -t $(DOCKER_IMAGE_NAME):$(IMAGE_TAG) .
	docker tag $(DOCKER_IMAGE_NAME):$(IMAGE_TAG) $(DOCKER_IMAGE_NAME):latest

# Run the application container
.PHONY: run
run: DOCKER_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
run:
	@echo "Running Docker image.."
	@echo "IMAGE::" $(DOCKER_IMAGE_NAME):$(IMAGE_TAG)
	docker run --rm -it -p 8080:8080 $(DOCKER_IMAGE_NAME):latest

.PHONY: push
push: DOCKER_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
push:
	@echo "Pushing Docker image to registry..."
	docker push $(DOCKER_IMAGE_NAME):$(IMAGE_TAG)

.PHONY: deploy
update_manifest: DOCKER_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
update_manifest:
# echo "building and deploying $(SERVICE)..."
# echo image name :
# docker build -t image_name docker_build_args -f docker_file .
# docker tag image_name registry_name/fullanme
# docker push registry_name/fullanme
	@echo "updating manifests..."
	@echo $(MANIFESTS_DIR)/overlays/$(DEPLOYMENT_ENV)
	@cd $(MANIFESTS_DIR)/overlays/$(DEPLOYMENT_ENV)
	@kustomize edit set image "$(IMAGE_NAME)=$(DOCKER_IMAGE_NAME):$(IMAGE_TAG)"

	

# # Kubernetes deployment targets
# deploy:
# 	@echo "Applying Kubernetes manifests..."
# 	kubectl apply -k $(K8S_CONFIG_PATH)

# undeploy:
# 	@echo "Undeploying Kubernetes manifests..."
# 	kubectl delete -k $(K8S_CONFIG_PATH)

# # Testing target (requires pytest and API server running)
# test:
# 	@echo "Running tests..."
# 	pytest tests/

# Clean up Docker images
clean: DOCKER_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
clean:
	@echo "Removing Docker images..."
	docker rmi $(DOCKER_IMAGE_NAME):$(IMAGE_TAG)

# Build and deploy pipeline
build-and-deploy: build push deploy

# Build, test, and deploy pipeline
build-test-deploy: build push test deploy


## 


api_build: IMAGE_NAME=api
api_build: SERVICE_DIR=services/churn_prediction/
api_build: build

api_run: IMAGE_NAME=api
api_run: run

api_push: IMAGE_NAME=api
api_push: push

frontend_build: IMAGE_NAME=frontend
frontend_build: SERVICE_DIR=services/frontend/
frontend_build: build

frontend_run: IMAGE_NAME=frontend
frontend_run: run

frontend_push: IMAGE_NAME=api
frontend_push: push


api_update_manifest: MANIFESTS_DIR=manifest
api_update_manifest: update_manifest

dev_api_update_manifest: DEPLOYMENT_ENV=dev
dev_api_update_manifest: api_update_manifest

prod_api_update_manifest: DEPLOYMENT_ENV=dev
prod_api_update_manifest: api_update_manifest

# Help command to display available targets
help:
	@echo "Available Makefile targets:"
	@echo "  build            - Build the Docker image"
	@echo "  push             - Push the Docker image to the registry"
	@echo "  deploy           - Deploy Kubernetes manifests"
	@echo "  undeploy         - Undeploy Kubernetes manifests"
	@echo "  test             - Run the test suite"
	@echo "  clean            - Remove Docker images"
	@echo "  build-and-deploy - Build, push, and deploy the application"
	@echo "  build-test-deploy- Build, test, push, and deploy the application"