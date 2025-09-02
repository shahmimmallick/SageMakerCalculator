import requests
import json
import os

def call_sagemaker_endpoint():
    """Call endpoint from SageMaker Studio environment"""
    
    # Use SageMaker Studio's built-in credentials
    endpoint_name = 'pytorch-inference-2025-09-02-16-11-53-984'
    
    # This works only inside SageMaker Studio
    import boto3
    runtime = boto3.client('sagemaker-runtime')
    
    payload = {"operation": "add", "a": 10, "b": 5}
    
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(payload)
    )
    
    result = json.loads(response['Body'].read().decode())
    return result

if __name__ == "__main__":
    try:
        result = call_sagemaker_endpoint()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        print("Run this from SageMaker Studio or configure AWS credentials first")