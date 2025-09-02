# SageMaker Calculator Deployment Guide

## Prerequisites
1. AWS Account with SageMaker access
2. SageMaker Studio setup
3. IAM role with SageMaker permissions

## Step-by-Step Deployment

### Phase 1: SageMaker Studio Setup

1. **Access SageMaker Studio**
   - Go to AWS Console → SageMaker → Studio
   - Launch Studio or create new domain
   - Open JupyterLab

2. **Upload Project Files**
   - Upload entire `SageMakerCalculator` folder to Studio
   - Or clone from repository

### Phase 2: Model Development

1. **Open Development Notebook**
   ```
   notebooks/calculator_development.ipynb
   ```

2. **Run All Cells**
   - Test calculator model locally
   - Validate inference pipeline
   - Verify SageMaker session

### Phase 3: Model Deployment

1. **Open Deployment Notebook**
   ```
   notebooks/sagemaker_deployment.ipynb
   ```

2. **Execute Deployment Steps**
   - Package model code
   - Upload to S3
   - Create SageMaker model
   - Deploy to endpoint

3. **Note Endpoint Name**
   - Default: `math-calculator-endpoint`
   - Use for API calls

### Phase 4: API Testing

1. **Test via Notebook**
   - Use predictor object in deployment notebook
   - Test various operations

2. **Test via Script**
   ```bash
   python tests/test_api.py
   ```

### Phase 5: REST API Access

#### Option 1: AWS SDK (Python)
```python
import boto3
import json

runtime = boto3.client('sagemaker-runtime')
response = runtime.invoke_endpoint(
    EndpointName='math-calculator-endpoint',
    ContentType='application/json',
    Body=json.dumps({"operation": "add", "a": 10, "b": 5})
)
```

#### Option 2: HTTP Request
```bash
curl -X POST https://runtime.sagemaker.REGION.amazonaws.com/endpoints/math-calculator-endpoint/invocations \
-H "Content-Type: application/json" \
-H "Authorization: AWS4-HMAC-SHA256 ..." \
-d '{"operation": "add", "a": 10, "b": 5}'
```

#### Option 3: API Gateway Integration
- Create API Gateway
- Connect to SageMaker endpoint
- Enable public REST API access

## Monitoring and Management

### CloudWatch Metrics
- Endpoint invocations
- Model latency
- Error rates

### Cost Optimization
- Use `ml.t2.medium` for development
- Scale to `ml.m5.large` for production
- Enable auto-scaling if needed

### Cleanup
```python
# Delete endpoint
predictor.delete_endpoint()

# Delete model
sklearn_model.delete_model()
```

## Troubleshooting

### Common Issues
1. **Role Permissions**: Ensure SageMaker execution role has S3 access
2. **Endpoint Limits**: Check account limits for endpoints
3. **Instance Types**: Verify instance type availability in region

### Error Handling
- Check CloudWatch logs for detailed errors
- Validate input JSON format
- Ensure model.tar.gz contains all files

## Production Considerations

### Security
- Use VPC endpoints
- Enable encryption at rest
- Implement proper IAM policies

### Performance
- Monitor latency metrics
- Consider multi-model endpoints
- Implement caching if needed

### Scalability
- Enable auto-scaling
- Use Application Load Balancer
- Consider batch transform for bulk operations