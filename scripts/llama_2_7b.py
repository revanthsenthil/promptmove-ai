"""import requests
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

# Define the required SCOPES
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# Replace 'NAME_OF_FILE' with your service account JSON file name that you downloaded
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Load credentials from the service account file with the specified SCOPES
cred = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Create an authentication request
auth_req = google.auth.transport.requests.Request()

# Refresh the credentials
cred.refresh(auth_req)

# Obtain the bearer token
bearer_token = cred.token


project_id = "senior-design-404616"

endpoint_id = "3325585068394545152"

# Define the base URL for your specific region (us-central1 in this example)
base_url = f"https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/us-central1/endpoints/{endpoint_id}:predict"


# Define the request body for your specific prompt and parameters
prompt = "Write a poem about Valencia."

request_body = {
    "instances": [
        {
            "prompt": "Write a poem about Valencia.",
            "max_length": 200,
            "top_k": 10
        }
    ]
}

# Create the full URL using the project and endpoint IDs
full_url = base_url.format(project_id=project_id, endpoint_id=endpoint_id)

headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}
print(full_url)
# Send a POST request to the model endpoint
resp = requests.post(full_url, json=request_body, headers=headers)


# Print the response from the model
if resp.status_code == 200:
    print(resp.json())
else:
    print(f"Request failed with status code {resp.status_code}")
"""
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_predict_custom_trained_model_sample]
from typing import Dict, List, Union

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

from google.oauth2 import service_account

# Define the required SCOPES
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Load credentials from the service account file with the specified SCOPES
cred = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(credentials=cred, client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if isinstance(instances, list) else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))

predict_custom_trained_model_sample(
    project="832139236110",
    endpoint_id="5726003669783019520",
    location="us-central1",
    instances={
            "prompt": "Write a poem about Valencia.",
            "max_length": 200,
            "top_k": 10
        }
)