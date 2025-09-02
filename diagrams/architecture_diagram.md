# SageMaker Calculator - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AWS Cloud Environment                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────┐ │
│  │   SageMaker     │    │      Amazon      │    │     SageMaker Model     │ │
│  │     Studio      │    │        S3        │    │       Registry          │ │
│  │                 │    │                  │    │                         │ │
│  │ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────────────┐ │ │
│  │ │ JupyterLab  │ │───▶│ │model.tar.gz  │ │───▶│ │   SKLearn Model     │ │ │
│  │ │ Notebooks   │ │    │ │              │ │    │ │                     │ │ │
│  │ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────────────┘ │ │
│  └─────────────────┘    └──────────────────┘    └─────────────────────────┘ │
│           │                       │                          │               │
│           │                       │                          │               │
│           ▼                       ▼                          ▼               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    SageMaker Endpoint                                   │ │
│  │                                                                         │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────┐ │ │
│  │  │   ML Instance   │    │   Model Server  │    │   Inference Code    │ │ │
│  │  │  (ml.t2.medium) │    │                 │    │                     │ │ │
│  │  │                 │    │ ┌─────────────┐ │    │ ┌─────────────────┐ │ │ │
│  │  │ ┌─────────────┐ │    │ │ Flask/Gunic │ │    │ │  inference.py   │ │ │ │
│  │  │ │   Docker    │ │    │ │   Server    │ │    │ │                 │ │ │ │
│  │  │ │ Container   │ │    │ └─────────────┘ │    │ └─────────────────┘ │ │ │
│  │  │ └─────────────┘ │    │                 │    │ ┌─────────────────┐ │ │ │
│  │  └─────────────────┘    └─────────────────┘    │ │calculator_model │ │ │ │
│  │                                                 │ │     .py         │ │ │ │
│  │                                                 │ └─────────────────┘ │ │ │
│  │                                                 └─────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
└────────────────────────────────────┼─────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Client Applications                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────┐ │
│  │   Python SDK    │    │   REST API       │    │    Web Application      │ │
│  │   (boto3)       │    │   (HTTP/HTTPS)   │    │                         │ │
│  │                 │    │                  │    │                         │ │
│  │ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────────────┐ │ │
│  │ │ invoke_     │ │    │ │ POST /invoke │ │    │ │   Frontend UI       │ │ │
│  │ │ endpoint()  │ │    │ │              │ │    │ │                     │ │ │
│  │ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────────────┘ │ │
│  └─────────────────┘    └──────────────────┘    └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Development Environment
- **SageMaker Studio**: Cloud-based ML IDE
- **JupyterLab**: Interactive development environment
- **Notebooks**: Development and deployment workflows

### 2. Model Storage
- **Amazon S3**: Stores packaged model artifacts (model.tar.gz)
- **Model Registry**: Manages model versions and metadata

### 3. Inference Infrastructure
- **SageMaker Endpoint**: Managed inference service
- **ML Instance**: Compute resource (ml.t2.medium)
- **Model Server**: Handles HTTP requests and responses
- **Docker Container**: Isolated runtime environment

### 4. Application Code
- **inference.py**: SageMaker inference handler
- **calculator_model.py**: Core business logic
- **Dependencies**: Python packages and libraries

### 5. Client Access
- **Python SDK**: Programmatic access via boto3
- **REST API**: HTTP/HTTPS endpoint for web integration
- **Web Applications**: Frontend interfaces

## Data Flow

1. **Development**: Code written in JupyterLab notebooks
2. **Packaging**: Model files packaged into tar.gz
3. **Upload**: Artifacts uploaded to S3 bucket
4. **Deployment**: SageMaker creates endpoint with model
5. **Inference**: Clients send requests to endpoint
6. **Response**: Processed results returned to clients