use reqwest;
use std::fs::File;
use std::io::Read;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // URL of the API endpoint
    let url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/a1f0d138-2887-4cd6-bef3-52459e71f411/classify/iterations/Iteration2/image";

    // Set the headers
    let client = reqwest::Client::new();
    let mut headers = reqwest::header::HeaderMap::new();
    headers.insert("Prediction-Key", "57c7f62e201e40218c4bebe0047e97a0".parse()?);
    headers.insert(reqwest::header::CONTENT_TYPE, "application/octet-stream".parse()?);

    // Load your image file
    let mut image_file = File::open("models/btr90.jpg")?;
    let mut image_data = Vec::new();
    image_file.read_to_end(&mut image_data)?;

    // Make the POST request
    let response = client.post(url)
        .headers(headers)
        .body(image_data)
        .send()
        .await?;

    // Check if the request was successful
    if response.status().is_success() {
        println!("Request was successful.");
        println!("Response: {:?}", response.json::<serde_json::Value>().await?);
    } else {
        println!("Request failed.");
        println!("Status code: {}", response.status());
        println!("Response: {:?}", response.text().await?);
    }

    Ok(())
}

