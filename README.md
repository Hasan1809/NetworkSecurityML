# 🛡️ Network Security ML: Phishing Website Detection

A comprehensive machine learning solution that identifies phishing websites by analyzing URL characteristics and webpage features. This project combines traditional ML techniques with modern MLOps practices to deliver a production-ready phishing detection system.

## 📋 Table of Contents

- [Project Description](#-project-description)
- [Features & Highlights](#-features--highlights)
- [Installation & Setup](#-installation--setup)
- [Usage Instructions](#-usage-instructions)
- [Dataset & Parameters](#-dataset--parameters)
- [Technologies & Tools](#-technologies--tools)
- [AWS Deployment](#-aws-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact & Support](#-contact--support)

## 🎯 Project Description

In an era where cyber threats are increasingly sophisticated, this project tackles the critical problem of phishing website detection. By leveraging machine learning algorithms, we analyze 30+ URL and webpage features to accurately classify websites as legitimate or phishing attempts.

The system processes various website characteristics - from URL structure and domain properties to security certificates and page content indicators - to make real-time predictions that help protect users from malicious websites.

## ✨ Features & Highlights

- **🎯 High Accuracy Detection**: Advanced ensemble methods for superior phishing detection performance
- **🚀 Real-time Predictions**: FastAPI-powered REST API for instant website classification
- **📊 Comprehensive Feature Analysis**: 30+ engineered features covering URL, domain, and content characteristics
- **🔄 Automated ML Pipeline**: End-to-end training pipeline with data validation and transformation
- **📈 Experiment Tracking**: MLflow integration for model versioning and performance monitoring
- **🐳 Containerized Deployment**: Docker-based deployment for consistent environments
- **☁️ Cloud-Ready Architecture**: Full AWS integration with automated CI/CD workflows
- **📋 Interactive Results**: Web-based interface displaying prediction results in formatted tables

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)
- AWS CLI configured (for cloud deployment)
- MongoDB instance (for data storage)

### Local Development Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/NetworkSecurityML.git
   cd NetworkSecurityML
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:

   ```env
   MONGO_DB_URL=your_mongodb_connection_string
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=your_aws_region
   ECR_REPOSITORY_NAME=your_ecr_repository
   ```

5. **Data Setup**
   ```bash
   # Upload your dataset to MongoDB
   python push_data.py
   ```

## 📖 Usage Instructions

### Training the Model

Run the complete ML pipeline:

```bash
python main.py
```

Or train via the API:

```bash
python app.py
# Navigate to http://localhost:8080/train
```

### Making Predictions

1. **Via Web Interface**

   ```bash
   python app.py
   # Open http://localhost:8080/docs
   # Use the /predict endpoint to upload a CSV file
   ```

2. **Via Direct API Call**

   ```bash
   curl -X POST "http://localhost:8080/predict" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@your_data.csv"
   ```

3. **Programmatic Usage**

   ```python
   from src.utils.ml_utils.model.estimator import NetworkModel
   from src.utils.main_utils.utils import load_object

   # Load trained model
   preprocessor = load_object("final_model/preprocessor.pkl")
   model = load_object("final_model/model.pkl")
   network_model = NetworkModel(preprocessor=preprocessor, model=model)

   # Make predictions
   predictions = network_model.predict(your_dataframe)
   ```

### Docker Deployment

```bash
# Build image
docker build -t network-security-ml .

# Run container
docker run -d -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_REGION=your_region \
  network-security-ml
```

## 📊 Dataset & Parameters

Our model analyzes **31 carefully engineered features** that capture various aspects of website legitimacy:

### URL Structure Features

- **having_IP_Address**: Whether the URL contains an IP address instead of domain name
- **URL_Length**: Categorized length of the URL (short/medium/long)
- **Shortining_Service**: Presence of URL shortening services (bit.ly, tinyurl, etc.)
- **having_At_Symbol**: Use of @ symbol in URL (often indicates redirection)
- **double_slash_redirecting**: Presence of "//" in URL path (suspicious redirection)
- **Prefix_Suffix**: Use of "-" in domain name (common in phishing)

### Domain & SSL Features

- **having_Sub_Domain**: Number of subdomains (multiple subdomains can be suspicious)
- **SSLfinal_State**: SSL certificate status and validity
- **Domain_registeration_length**: How long the domain has been registered
- **age_of_domain**: Age of the domain since registration
- **DNSRecord**: DNS record existence and validity

### Page Content Features

- **Favicon**: Whether favicon is loaded from external domain
- **port**: Use of non-standard ports
- **HTTPS_token**: Misleading use of "https" in domain name
- **Request_URL**: Percentage of objects loaded from different domains
- **URL_of_Anchor**: Percentage of anchors pointing to different domains
- **Links_in_tags**: Percentage of links in meta, script, and link tags from different domains

### Form & Interaction Features

- **SFH**: Server Form Handler - where forms submit data
- **Submitting_to_email**: Forms that submit to email addresses
- **Abnormal_URL**: URL doesn't match the registered domain's whois data
- **Redirect**: Number of redirects in the page

### JavaScript & Pop-up Features

- **on_mouseover**: Status bar changes on mouseover
- **RightClick**: Right-click functionality disabled
- **popUpWidnow**: Presence of pop-up windows
- **Iframe**: Use of invisible or suspicious iframes

### Traffic & Ranking Features

- **web_traffic**: Website popularity ranking
- **Page_Rank**: Google PageRank value
- **Google_Index**: Whether the website is indexed by Google
- **Links_pointing_to_page**: Number of external websites linking to this page
- **Statistical_report**: Presence in phishing blacklists or security reports

### Target Variable

- **Result**: Binary classification (0 = Legitimate, 1 = Phishing)

All features are preprocessed and normalized using KNN imputation to handle missing values while preserving the underlying data distribution patterns.

## 🔧 Technologies & Tools

### Core ML Stack

- **Python 3.10**: Primary development language
- **Scikit-learn**: Machine learning algorithms and preprocessing
- **Pandas & NumPy**: Data manipulation and analysis
- **FastAPI**: High-performance web framework for API development

### MLOps & Experiment Tracking

- **MLflow**: Experiment tracking, model registry, and lifecycle management
- **DagsHub**: Collaborative MLOps platform for version control and experiment sharing
- **Automated Pipelines**: Structured data ingestion → validation → transformation → training workflow

### Data & Storage

- **MongoDB**: Document-based database for flexible data storage
- **PyMongo**: Python MongoDB driver with SSL/TLS support
- **YAML**: Configuration management and schema validation

### Deployment & DevOps

- **Docker**: Containerization for consistent deployment environments
- **GitHub Actions**: Automated CI/CD workflows with testing and deployment
- **AWS Integration**: Seamless cloud deployment and scaling

### Web & API

- **Uvicorn**: ASGI server for high-performance API serving
- **Jinja2**: Template engine for web interface
- **CORS Middleware**: Cross-origin resource sharing for web integration

## ☁️ AWS Deployment

This project leverages a complete AWS ecosystem for scalable, production-ready deployment:

### Architecture Overview

```
GitHub → GitHub Actions → ECR → EC2 → S3
   ↓           ↓           ↓      ↓     ↓
 Source    CI/CD      Images   App   Models
```

### AWS Services Integration

**🐳 Amazon ECR (Elastic Container Registry)**

- Automated Docker image building and storage
- Version-controlled container images
- Seamless integration with deployment pipeline

**🖥️ Amazon EC2 (Elastic Compute Cloud)**

- Self-hosted GitHub runners for deployment
- Production application hosting
- Auto-scaling capabilities for varying loads

**📦 Amazon S3 (Simple Storage Service)**

- Model artifact storage and versioning
- Training pipeline artifacts backup
- Static asset hosting

**🔐 IAM (Identity and Access Management)**

- Fine-grained access control
- Secure service-to-service communication
- Environment-specific permissions

### Deployment Workflow

1. **Continuous Integration**: GitHub Actions automatically run tests and linting
2. **Image Building**: Docker images are built and pushed to ECR on successful tests
3. **Deployment**: Self-hosted runners pull latest images and deploy to EC2
4. **Model Sync**: Trained models and artifacts are automatically synced to S3

### Environment Management

The deployment supports multiple environments with isolated resources:

- **Development**: Feature testing and integration
- **Staging**: Pre-production validation
- **Production**: Live phishing detection service

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

This project uses several open-source libraries. Please refer to their respective licenses:

- Scikit-learn: BSD License
- FastAPI: MIT License
- MLflow: Apache 2.0 License
