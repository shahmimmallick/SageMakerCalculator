import boto3
import json

def test_calculator_endpoint():
    """Test the deployed calculator endpoint"""
    
    runtime = boto3.client('sagemaker-runtime')
    endpoint_name = 'math-calculator-endpoint'
    
    test_cases = [
        {'operation': 'add', 'a': 10, 'b': 5},
        {'operation': 'multiply', 'a': 7, 'b': 8},
        {'operation': 'divide', 'a': 20, 'b': 4},
        {'operation': 'sqrt', 'a': 16},
        {'operation': 'sin', 'a': 30},
        {'operation': 'power', 'a': 2, 'b': 3}
    ]
    
    print("Testing Calculator API:")
    print("-" * 50)
    
    for test_case in test_cases:
        try:
            response = runtime.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='application/json',
                Body=json.dumps(test_case)
            )
            
            result = json.loads(response['Body'].read().decode())
            
            print(f"Input: {test_case}")
            print(f"Output: {result}")
            print("-" * 30)
            
        except Exception as e:
            print(f"Error testing {test_case}: {str(e)}")

if __name__ == "__main__":
    test_calculator_endpoint()