import boto3
import json

def invoke_endpoint_http(endpoint_name, payload):
    """Make HTTP request to SageMaker endpoint"""
    
    # Create SageMaker Runtime client
    runtime = boto3.client('sagemaker-runtime')
    
    # Invoke endpoint
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(payload)
    )
    
    # Parse response
    result = json.loads(response['Body'].read().decode())
    return result

def test_calculator_endpoint():
    """Test the calculator endpoint with HTTP requests"""
    
    endpoint_name = 'pytorch-inference-2025-09-02-16-11-53-984'
    
    # Test cases
    test_cases = [
        {"operation": "add", "a": 10, "b": 5},
        {"operation": "subtract", "a": 20, "b": 8},
        {"operation": "multiply", "a": 4, "b": 7},
        {"operation": "divide", "a": 15, "b": 3},
        {"operation": "sqrt", "a": 25},
        {"operation": "sin", "a": 30}
    ]
    
    print("Testing Calculator Endpoint via HTTP:")
    print("=" * 50)
    
    for test_data in test_cases:
        try:
            result = invoke_endpoint_http(endpoint_name, test_data)
            print(f"Input: {test_data}")
            print(f"Output: {result}")
            print("-" * 30)
        except Exception as e:
            print(f"Error with {test_data}: {e}")
            print("-" * 30)

if __name__ == "__main__":
    test_calculator_endpoint()