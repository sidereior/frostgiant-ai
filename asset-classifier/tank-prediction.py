import requests

# URL of the API endpoint
url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/a1f0d138-2887-4cd6-bef3-52459e71f411/classify/iterations/Iteration2/image"

# Set the headers
headers = {
    'Prediction-Key': '57c7f62e201e40218c4bebe0047e97a0',
    'Content-Type': 'application/octet-stream'
}

# Load your image file
with open('btr90.jpg', 'rb') as image_file:
    image_data = image_file.read()

# Make the POST request
response = requests.post(url, headers=headers, data=image_data)

# Check if the request was successful
if response.status_code == 200:
    print("Request was successful.")
    print("Response:", response.json())
else:
    print("Request failed.")
    print("Status code:", response.status_code)
    print("Response:", response.text)
