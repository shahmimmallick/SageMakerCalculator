# SageMaker Calculator Project

A comprehensive math calculator model deployed on Amazon SageMaker for real-time inference with FastAPI integration.

## 🏗️ Project Architecture

```
SageMakerCalculator/
├── src/
│   ├── calculator_model.py         # Core calculator logic with math operations
│   ├── inference.py               # SageMaker inference handler (model_fn, predict_fn)
│   └── requirements.txt           # Model dependencies
├── deployment/
│   ├── sagemaker_deployment.ipynb # Interactive deployment notebook
│   ├── deploy_model.py           # Automated deployment script
│   └── redeploy_only.py          # Quick redeployment script
├── tests/
│   ├── http_client.py            # Direct SageMaker endpoint testing
│   ├── rest_client.py            # REST API client with authentication
│   └── studio_client.py          # SageMaker Studio environment client
├── notebooks/
│   └── calculator_development.ipynb # Model development and testing
├── requirements.txt              # Project dependencies
├── README.md                    # This file
└── DEPLOYMENT_GUIDE.md          # Detailed deployment instructions
```

## 🚀 Quick Start

### 1. Deploy to SageMaker

**Option A: Interactive (Recommended for first-time users)**
```bash
# In SageMaker Studio
open deployment/sagemaker_deployment.ipynb
# Run all cells step by step
```

**Option B: Automated**
```bash
cd deployment
python deploy_model.py
```

### 2. Test the Endpoint

```python
import boto3
import json

runtime = boto3.client('sagemaker-runtime')
response = runtime.invoke_endpoint(
    EndpointName='your-endpoint-name',
    ContentType='application/json',
    Body=json.dumps({"operation": "add", "a": 10, "b": 5})
)
result = json.loads(response['Body'].read().decode())
print(result)  # {'operation': 'add', 'input_a': 10, 'input_b': 5, 'result': 15, 'status': 'success'}
```

## 📊 Supported Operations

| Operation | Parameters | Example | Description |
|-----------|------------|---------|-------------|
| `add` | a, b | `{"operation": "add", "a": 10, "b": 5}` | Addition |
| `subtract` | a, b | `{"operation": "subtract", "a": 10, "b": 3}` | Subtraction |
| `multiply` | a, b | `{"operation": "multiply", "a": 4, "b": 7}` | Multiplication |
| `divide` | a, b | `{"operation": "divide", "a": 15, "b": 3}` | Division |
| `power` | a, b | `{"operation": "power", "a": 2, "b": 3}` | Exponentiation |
| `sqrt` | a | `{"operation": "sqrt", "a": 16}` | Square root |
| `sin` | a | `{"operation": "sin", "a": 90}` | Sine (degrees) |
| `cos` | a | `{"operation": "cos", "a": 60}` | Cosine (degrees) |
| `tan` | a | `{"operation": "tan", "a": 45}` | Tangent (degrees) |
| `log` | a | `{"operation": "log", "a": 10}` | Natural logarithm |

## 🔧 API Response Format

**Success Response:**
```json
{
    "operation": "add",
    "input_a": 10,
    "input_b": 5,
    "result": 15,
    "status": "success"
}
```

**Error Response:**
```json
{
    "error": "Division by zero",
    "status": "error"
}
```

## 🌐 Access Methods

### 1. Direct SageMaker Runtime API
```python
# See tests/http_client.py for complete example
runtime = boto3.client('sagemaker-runtime')
response = runtime.invoke_endpoint(...)
```

### 2. REST API with Authentication
```python
# See tests/rest_client.py for complete example
client = SageMakerCalculatorClient('endpoint-name')
result = client.calculate('add', 10, 5)
```

### 3. FastAPI Proxy Server
See separate project: `CalculatorAPI/` for REST API server that can be called from Postman.

## 🔍 Monitoring and Debugging

### View Endpoint Logs
```python
from deployment.deploy_model import view_logs
view_logs('your-endpoint-name')
```

### Check Endpoint Status
```bash
aws sagemaker describe-endpoint --endpoint-name your-endpoint-name
```

## 🛠️ Development

### Local Testing
```python
from src.calculator_model import MathCalculator

calc = MathCalculator()
result = calc.calculate('add', 10, 5)
print(result)  # 15
```

### Model Updates
1. Modify `src/calculator_model.py`
2. Test locally in `notebooks/calculator_development.ipynb`
3. Redeploy using `deployment/redeploy_only.py`

## 📋 Prerequisites

- AWS Account with SageMaker access
- AWS CLI configured or SageMaker Studio environment
- Python 3.8+
- Required IAM permissions:
  - `sagemaker:CreateModel`
  - `sagemaker:CreateEndpoint`
  - `sagemaker:InvokeEndpoint`
  - `s3:GetObject`, `s3:PutObject`

## 🚨 Cost Management

**Important:** SageMaker endpoints incur charges while running.

### Delete Endpoint When Done
```python
# In notebook or script
predictor.delete_endpoint()

# Or via AWS CLI
aws sagemaker delete-endpoint --endpoint-name your-endpoint-name
```

### Estimated Costs
- `ml.t2.medium`: ~$0.065/hour
- `ml.m5.large`: ~$0.115/hour

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new operations
4. Update documentation
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.