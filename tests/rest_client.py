import requests
import json
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

class SageMakerCalculatorClient:
    def __init__(self, endpoint_name, region=None):
        self.endpoint_name = endpoint_name
        
        # Auto-detect region if not provided
        if region is None:
            session = boto3.Session()
            region = session.region_name or 'us-east-1'
        
        self.region = region
        self.endpoint_url = f'https://runtime.sagemaker.{region}.amazonaws.com/endpoints/{endpoint_name}/invocations'
        
        # Get fresh credentials
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if not credentials:
            raise Exception("AWS credentials not found. Run 'aws configure' or set environment variables.")
        
        self.credentials = credentials.get_frozen_credentials()
    
    def calculate(self, operation, a, b=None):
        """Make REST API calculation request"""
        
        payload = {"operation": operation, "a": a}
        if b is not None:
            payload["b"] = b
        
        # Create AWS request
        request = AWSRequest(
            method='POST',
            url=self.endpoint_url,
            data=json.dumps(payload),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        
        # Sign with SigV4
        SigV4Auth(self.credentials, 'sagemaker', self.region).add_auth(request)
        
        # Make HTTP request
        response = requests.post(
            request.url,
            data=request.body,
            headers=dict(request.headers)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

# Usage example
if __name__ == "__main__":
    # Auto-detect region or specify manually
    client = SageMakerCalculatorClient('pytorch-inference-2025-09-02-16-11-53-984')
    print(f"Using region: {client.region}")
    print(f"Endpoint URL: {client.endpoint_url}")
    print()
    
    # Test calculations
    print("Calculator API Test:")
    print("=" * 30)
    
    tests = [
        ("add", 10, 5),
        ("multiply", 6, 7),
        ("sqrt", 16, None),
        ("sin", 90, None)
    ]
    
    for operation, a, b in tests:
        try:
            result = client.calculate(operation, a, b)
            print(f"{operation}({a}, {b}) = {result}")
        except Exception as e:
            print(f"Error: {e}")