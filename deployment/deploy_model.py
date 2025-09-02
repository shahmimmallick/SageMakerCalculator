import boto3
import sagemaker
from sagemaker.pytorch import PyTorchModel
from sagemaker import get_execution_role
import tarfile
import os

def create_model_tar():
    """Create model.tar.gz with inference code"""
    # Create code directory structure
    os.makedirs('code', exist_ok=True)
    
    # Copy source files to code directory
    import shutil
    shutil.copy('../src/calculator_model.py', 'code/')
    shutil.copy('../src/inference.py', 'code/')
    
    # Create tar file
    with tarfile.open('model.tar.gz', 'w:gz') as tar:
        tar.add('code', arcname='code')
    
    # Cleanup
    shutil.rmtree('code')
    print("Created model.tar.gz")

def delete_existing_endpoint(endpoint_name):
    """Delete existing endpoint if it exists"""
    import time
    try:
        sagemaker_client = boto3.client('sagemaker')
        sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
        print(f"Deleting existing endpoint: {endpoint_name}")
        
        # Wait for deletion to complete
        while True:
            try:
                sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
                print("Waiting for endpoint deletion...")
                time.sleep(10)
            except:
                print("Endpoint deleted successfully")
                break
    except:
        print(f"No existing endpoint found: {endpoint_name}")

def deploy_calculator_model():
    """Deploy the calculator model to SageMaker"""
    
    sagemaker_session = sagemaker.Session()
    
    # Delete existing endpoint
    delete_existing_endpoint('math-calculator-endpoint')
    
    try:
        role = get_execution_role()
    except:
        # For local development, you'll need to set this
        role = input("Enter your SageMaker execution role ARN: ")
    
    create_model_tar()
    
    # Upload to S3
    bucket = sagemaker_session.default_bucket()
    model_artifacts = sagemaker_session.upload_data(
        path='model.tar.gz',
        bucket=bucket,
        key_prefix='calculator-model'
    )
    
    print(f"Model uploaded to: {model_artifacts}")
    
    # Create PyTorch model (works for custom Python code)
    pytorch_model = PyTorchModel(
        model_data=model_artifacts,
        role=role,
        entry_point='inference.py',
        source_dir=None,
        framework_version='1.12',
        py_version='py38'
    )
    
    # Deploy endpoint
    predictor = pytorch_model.deploy(
        initial_instance_count=1,
        instance_type='ml.t2.medium',
        endpoint_name='math-calculator-endpoint'
    )
    
    print(f"Model deployed to endpoint: {predictor.endpoint_name}")
    return predictor

def get_endpoint_logs(endpoint_name):
    """Get CloudWatch logs for the endpoint"""
    import boto3
    from datetime import datetime, timedelta
    
    logs_client = boto3.client('logs')
    log_group = f'/aws/sagemaker/Endpoints/{endpoint_name}'
    
    try:
        # Get logs from last 10 minutes
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=10)
        
        response = logs_client.filter_log_events(
            logGroupName=log_group,
            startTime=int(start_time.timestamp() * 1000),
            endTime=int(end_time.timestamp() * 1000)
        )
        
        print(f"\n=== Endpoint Logs for {endpoint_name} ===")
        for event in response['events']:
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            print(f"[{timestamp}] {event['message']}")
            
    except Exception as e:
        print(f"Could not fetch logs: {e}")

def test_endpoint(predictor):
    """Test the deployed endpoint"""
    from sagemaker.serializers import JSONSerializer
    from sagemaker.deserializers import JSONDeserializer
    
    predictor.serializer = JSONSerializer()
    predictor.deserializer = JSONDeserializer()
    
    test_data = {
        "operation": "add",
        "a": 10,
        "b": 5
    }
    
    try:
        result = predictor.predict(test_data)
        print(f"Test result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        # Show logs on error
        get_endpoint_logs(predictor.endpoint_name)
    
    return result

def view_logs(endpoint_name='math-calculator-endpoint'):
    """View endpoint logs manually"""
    get_endpoint_logs(endpoint_name)

if __name__ == "__main__":
    predictor = deploy_calculator_model()
    test_endpoint(predictor)
    
    # View logs
    print("\n=== Viewing Endpoint Logs ===")
    view_logs(predictor.endpoint_name)