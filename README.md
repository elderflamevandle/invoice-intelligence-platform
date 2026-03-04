# Vendor Invoice Intelligence System  
**Freight Cost Prediction & Invoice Risk Flagging**

## 📌 Table of Contents
- <a href="#project-overview">Project Overview</a>
- <a href="#business-objectives">Business Objectives</a>
- <a href="#data-sources">Data Sources</a>
- <a href="#eda">Exploratory Data Analysis</a>
- <a href="#models-used">Models Used</a>
- <a href="#metrics">Evaluation Metrics</a>
- <a href="#architecture-and-tech-stack">Architecture & Tech Stack</a>
- <a href="#project-structure">Project Structure</a>
- <a href="#how-to-run-this-project">How to Run This Project</a>
- <a href="#kubernetes-aws-deployment">Kubernetes & AWS Deployment</a>
- <a href="#author--contact">Author & Contact</a>
---

<h2><a class="anchor" id="project-overview"></a>📌 Project Overview</h2>

This project implements an **end-to-end machine learning system** designed to support finance teams by:

1. **Predicting expected freight cost** for vendor invoices.
2. **Flagging high-risk invoices** that require manual review due to abnormal cost, freight, or operational patterns.

---

<h2><a class="anchor" id="business-objectives"></a>🎯 Business Objectives</h2>

### 1. Freight Cost Prediction (Regression)

**Objective:**  
Predict the expected freight cost for a vendor invoice using quantity, invoice value, and historical behavior.

**Why it matters:**
- Freight is a non-trivial component of landed cost.
- Poor freight estimation impacts margin analysis and budgeting.
- Early prediction improves procurement planning and vendor negotiation.

![](images/freight_prediction.png)
---

### 2. Invoice Risk Flagging (Classification)

**Objective:**  
Predict whether a vendor invoice should be flagged for manual approval due to abnormal cost, freight, or delivery patterns.

**Why it matters:**
- Manual invoice review does not scale.
- Financial leakage often occurs in large or complex invoices.
- Early risk detection improves audit efficiency and operational control.

![](images/flag_invoice_prediction.png)
---

<h2><a class="anchor" id="data-sources"></a>📂 Data Sources</h2>

Data is stored in a relational SQLite database (`inventory.db`) with the following tables:

- `vendor_invoice` – Invoice-level financial and timing data  
- `purchases` – Item-level purchase details  
- `purchase_prices` – Reference purchase prices  
- `begin_inventory`, `end_inventory` – Inventory snapshots  

SQL aggregation is used to generate **invoice-level features**.

---

<h2><a class="anchor" id="eda"></a>📊 Exploratory Data Analysis (EDA)</h2>

EDA focuses on **business-driven questions**, such as:

- Do flagged invoices have higher financial exposure?
- Does freight scale linearly with quantity?
- Does freight cost depend on quantity?

Statistical tests (t-tests) are used to confirm that flagged invoices differ meaningfully from normal invoices.

---

<h2><a class="anchor" id="models-used"></a>🤖 Models Used</h2>

### Regression (Freight Prediction)
- Linear Regression (baseline)
- Decision Tree Regressor
- Random Forest Regressor (final model)

### Classification (Invoice Flagging)
- Logistic Regression (baseline)
- Decision Tree Classifier
- Random Forest Classifier (final model with GridSearchCV)

Hyperparameter tuning is performed using **GridSearchCV** with F1-score to handle class imbalance.

---

<h2><a class="anchor" id="metrics"></a>📈 Evaluation Metrics</h2>

### Freight Prediction
- MAE
- RMSE
- R² Score

### Invoice Flagging
- Accuracy
- Precision, Recall, F1-score
- Classification report
- Feature importance analysis

---

<h2><a class="anchor" id="architecture-and-tech-stack"></a>🏗 Architecture & Tech Stack</h2>

This project is built using a modern decoupled Microservices architecture to ensure high scalability and performance:

- **Frontend (UI):** [Streamlit](https://streamlit.io/) provides the visual dashboard for financial analysts to intuitively input invoices and view AI predictions.
- **Backend (API):** [FastAPI](https://fastapi.tiangolo.com/) powers lightning-fast, asynchronous REST API endpoints (`/predict_freight`, `/predict_invoice_flag`) that host the heavy Machine Learning models in an isolated environment.
- **Dependency Management:** [Poetry](https://python-poetry.org/) handles exact reproducible environment locks to prevent SciKit-Learn version collisions.
- **Containerization:** [Docker & Docker Compose](https://www.docker.com/) package the Frontend and Backend into isolated, portable containers.
- **Cloud Orchestration:** [Kubernetes (K8s) & AWS](https://kubernetes.io/) handles enterprise-grade scaling, using LoadBalancers and ReplicaSets for massive real-world deployment on Amazon Web Services (AWS EKS).

---

<h2><a class="anchor" id="project-structure"></a>📁 Project Structure</h2>

```bash
inventory-invoice-analytics/
│
├── data/
│   └── inventory.db
│
├── freight_cost_prediction/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
│
├── invoice_flagging/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
│
├── inference/
│   ├── predict_freight.py
│   └── predict_invoice_flag.py
│
├── models/
│   ├── predict_freight_model.pkl
│   ├── scaler.pkl
│   └── predict_flag_invoice.pkl
│
├── config.py                  # Global configurations & paths
├── logger.py                  # Centralized logging pipeline
├── app.py                     # Streamlit Frontend application
├── fastapi_app.py             # FastAPI Backend server
├── pyproject.toml             # Poetry dependency configuration
├── poetry.lock                # Poetry exact dependency tree
├── Dockerfile.api             # Build instructions for API container
├── Dockerfile.streamlit       # Build instructions for UI container
├── docker-compose.yml         # Container orchestration manifest
├── kubernetes.yaml            # AWS K8s Deployment and LoadBalancer manifest
├── README.md
└── .gitignore
```

---

<h2><a class="anchor" id="how-to-run-this-project"></a>🚀 How to Run This Project</h2>

### Method 1: The Modern Way (Docker Desktop)
We strongly recommend using **Docker Compose** so you never have to manually install machine learning dependencies.

1. Clone the repository:
```bash
git clone https://github.com/yourusername/inventory-invoice-analytics.git
cd inventory-invoice-analytics
```
2. Build and launch the UI and API Containers simultaneously:
```bash
docker-compose up --build
```
3. Open your browser to `http://localhost:8501`. Have fun!

---

### Method 2: The Manual Way (Poetry)
If you wish to test or retrain the models directly on your bare metal:

1. Install Poetry, then install project dependencies:
```bash
poetry install
```
2. (Optional) Retrain models:
```bash
poetry run python freight_cost_prediction/train.py
poetry run python invoice_flagging/train.py
```
3. Launch the Backend API (Terminal 1)
```bash
poetry run python fastapi_app.py
``` 
4. Launch the Frontend UI (Terminal 2)
```bash
poetry run streamlit run app.py
```

---

<h2><a class="anchor" id="kubernetes-aws-deployment"></a>☁️ Kubernetes & AWS Deployment</h2>

This project includes a production-ready `kubernetes.yaml` manifest designed to be deployed onto a managed cloud Kubernetes cluster such as **Amazon Elastic Kubernetes Service (AWS EKS)**.

**Architecture Benefits on AWS:**
- **Auto-Scaling:** The FastAPI Deployment is configured with Replicas, meaning AWS will automatically spin up multiple API pods across diverse EC2 worker nodes when invoice prediction traffic spikes.
- **Internal Security:** The ML backend (`invoice-api-service`) utilizes a `ClusterIP`, completely hiding the sensitive modeling algorithms from the public internet. It exists strictly within the secure AWS VPC.
- **Global Availability:** The Streamlit frontend (`invoice-ui-service`) utilizes a `LoadBalancer` which triggers AWS to provision an Elastic Load Balancer (ELB), assigning a highly-available public IP address accessible to authorized users globally.

To deploy on your AWS EKS cluster:
```bash
kubectl apply -f kubernetes.yaml
```

---
<h2><a class="anchor" id="author--contact"></a>Author & Contact</h2>

**Ayushi Mishra**  
Data Scientist  
📧 Email: techclasses0810@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/ayushi-mishra-30813b174/)  
🔗 [Portfolio](https://www.youtube.com/@techclasses0810/)



