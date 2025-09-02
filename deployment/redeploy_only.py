import boto3
import sagemaker
from sagemaker.pytorch import PyTorchModel
from sagemaker import get_execution_role
import time

def delete_existing_endpoint(endpoint_name):
    """Delete existing endpoint if it exists"""
    try:
        sagemaker_client = boto3.client('sagemaker')
        sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
        print(f"Deleting existing endpoint: {endpoint_name}")
        
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

def redeploy_with_existing_model():
    """Redeploy using existing model artifacts"""
    
    sagemaker_session = sagemaker.Session()
    role = get_execution_role()
    
    # Delete existing endpoint
    delete_existing_endpoint('math-calculator-endpoint')
    
    # Use existing model artifacts (replace with your S3 path)
    bucket = sagemaker_session.default_bucket()
    model_artifacts = f"s3://{bucket}/calculator-model/model.tar.gz"
    
    print(f"Using existing model: {model_artifacts}")
    
    # Create PyTorch model
    pytorch_model = PyTorchModel(
        model_data=model_artifacts,
        role=role,
        entry_point='inference.py',
        framework_version='1.12',
        py_version='py38'
    )
    
    # Deploy endpoint
    predictor = pytorch_model.deploy(
        initial_instance_count=1,
        instance_type='ml.t2.medium',
        endpoint_name='math-calculator-endpoint'
    )
    
    # Configure JSON serialization
    from sagemaker.serializers import JSONSerializer
    from sagemaker.deserializers import JSONDeserializer
    
    predictor.serializer = JSONSerializer()
    predictor.deserializer = JSONDeserializer()
    
    # Test
    test_data = {"operation": "add", "a": 10, "b": 5}
    result = predictor.predict(test_data)
    print(f"Test result: {result}")
    
    return predictor

if __name__ == "__main__":
    redeploy_with_existing_model()