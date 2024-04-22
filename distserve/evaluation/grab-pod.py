# curl --request POST \
#   --header 'content-type: application/json' \
#   --url 'https://api.runpod.io/graphql?api_key=${YOUR_API_KEY}' \
#   --data 
  
# {"input":{"cloudType":"SECURE","containerDiskInGb":20,"volumeInGb":0,"deployCost":1.48,"gpuCount":2,"gpuTypeId":"NVIDIA GeForce RTX 4090","minMemoryInGb":62,"minVcpuCount":16,"startJupyter":true,"startSsh":true,"templateId":"runpod-torch-v21","volumeKey":null,"ports":"8888/http,22/tcp","dataCenterId":"US-OR-1","networkVolumeId":"dg0br51h50","name":"spider-test"}}

# {"operationName":"Mutation","variables":{"input":{"cloudType":"SECURE","containerDiskInGb":1024,"volumeInGb":0,"deployCost":4.58,"gpuCount":2,"gpuTypeId":"NVIDIA A100-SXM4-80GB","minMemoryInGb":250,"minVcpuCount":32,"startJupyter":true,"startSsh":true,"templateId":"xbivg6n3b6","volumeKey":null,"ports":"8080/http,22/tcp,8000/tcp","dataCenterId":"US-OR-1","networkVolumeId":"dg0br51h50","name":"spider-test"}},"query":"mutation Mutation($input: PodFindAndDeployOnDemandInput) {\n  podFindAndDeployOnDemand(input: $input) {\n    id\n    imageName\n    env\n    machineId\n    machine {\n      podHostId\n      __typename\n    }\n    __typename\n  }\n}"}
  
import os, sys
import argparse
import requests
import time

def request_pod(api_key, public_key):
    data = '{"query": "mutation { podFindAndDeployOnDemand( input: { cloudType: SECURE, gpuCount: 8, volumeInGb: 0, containerDiskInGb: 512, minVcpuCount: 64, minMemoryInGb: 512, gpuTypeId: \\"NVIDIA A100-SXM4-80GB\\", name: \\"distserve-evaluation\\", startJupyter: false, startSsh: true, templateId: \\"xbivg6n3b6\\", volumeKey: null, dockerArgs: \\"\\", ports: \\"8080/http,22/tcp,8000/tcp\\", dataCenterId: \\"US-OR-1\\", volumeMountPath: \\"/workspace\\", networkVolumeId:\\"dg0br51h50\\", env: [{ key: \\"PUBLIC_KEY\\", value: \\"' + public_key + '\\" }] } ) { id imageName env machineId machine { podHostId } } }"}'
    response = requests.post('https://api.runpod.io/graphql?api_key=' + api_key, headers={'content-type': 'application/json'}, data=data)
    print(response.text)
    json_data = response.json()
    if "errors" in json_data:
        error = json_data["errors"][0]
        msg = error["message"]
        if msg != "There are no longer any instances available with the requested specifications. Please refresh and try again.":
            print("Alert! Unknown error: ", error)
            sys.exit(1)
    else:
        assert "data" in json_data
        print("Pod deployed successfully")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", type=str, required=True, help="API key")
    parser.add_argument("--public-key", type=str, required=True, help="Public key")
    args = parser.parse_args()
    
    while True:
        request_pod(args.api_key, args.public_key)
        time.sleep(2)
    