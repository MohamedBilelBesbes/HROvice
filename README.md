# Attestation Generation Platform – CI/CD on AWS

A microservice-based web platform for automated attestation (certificate) generation, fully containerized and deployed through a CI/CD pipeline on **AWS** using **Jenkins**, **Docker**, **Ansible**, and **Kubernetes**.

---

## Overview

The system automates attestation generation via a backend service written in Python and a lightweight web frontend. The deployment pipeline ensures continuous integration, delivery, and infrastructure automation across a Kubernetes cluster.

---

## Stack & Tooling

**Development**
- Python for PDF generation (fpdf)
- RESTful backend with modular microservice structure  
- Docker & Dockerfile for image creation  
- Docker Compose for local orchestration  

**CI/CD & DevOps**
- Jenkins declarative pipeline for automated build, test, and deploy stages  
- GitHub integration with Jenkins SCM polling  
- Docker Hub for container registry  
- Kompose to convert Docker Compose specs into Kubernetes manifests  
- Ansible for configuration management and cluster provisioning  
- Kubernetes for workload orchestration and service discovery  

**Cloud Infrastructure**
- AWS EC2 nodes as Kubernetes worker/master nodes  
- AWS S3 for artifact storage  
- IAM for access control  
- VPC for cluster isolation and networking  

---

## Architecture

- **Microservices**: Independent, containerized components for application logic and database  
- **Infrastructure as Code**: Automated provisioning via Ansible playbooks  
- **Deployment**: Rolling deployments managed by Kubernetes Deployment and Service YAMLs  
- **Orchestration**: Kompose-generated manifests ensure reproducibility of deployments across clusters  
