import base64
import requests



# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "btr90.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I have given you a picture of a BTR-90 armored vehicle. There is a red cross in this image that overlaps with a certain part of the vehicle. I want you to tell me what part of the vehicle the red cross overlaps with. For example, if it overlaps with the left side of the turret, you would say 'left side turret'. If it overlaps with the front right wheel, you would say 'front right wheel'. If it overlaps with the hull of the vehicle and towards the front right, you would say 'front right side of hull'. Be as specific as possible when identifing what part the vehicle the red cross overlaps with and an example full response could be something like: 'front right side of hull, from a front on view in the top right corner of the upper place' Identify the armor plate and positioning where possible. just be as specific as possible.."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())