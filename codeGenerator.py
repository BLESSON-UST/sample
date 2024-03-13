from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the logging level to debug for detailed logs
app.logger.setLevel(logging.DEBUG)

# Define the Azure OpenAI endpoint
AZURE_OPENAI_ENDPOINT = "https://gen-ai-demo.openai.azure.com/openai/deployments/open-ai-gpt35/chat/completions?api-version=2023-07-01-preview"

# Replace 'your_azure_openai_api_key' with your actual Azure OpenAI API key
AZURE_OPENAI_API_KEY = 'f39237474a6546c8ad3f14d3931ff7d7'

def generate_code(input_code, target_language):
    # Construct the message for Azure OpenAI chat completion with code generation request
    messages = [
        {"role": "user", "content": f"Generate complete code that can be run without any errors with all the necessary components and include exception handling, validation, or proper error handling in {target_language} based on the following input:\n\n{input_code}\n\n"}
    ]

    # Make a POST request to Azure OpenAI
    response = requests.post(
        AZURE_OPENAI_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY
        },
        json={"messages": messages}
    )

    # Parse the response and handle errors
    try:
        response_data = response.json()
        app.logger.debug("Azure OpenAI API Response: %s", response_data)  # Log the response for debugging

        generated_code = response_data["choices"][0]["message"]["content"]
    except KeyError:
        generated_code = "Error: Unable to generate code using Azure OpenAI API."

    return generated_code

@app.route('/api/generate_code', methods=['POST'])
def generate_code_endpoint():
    data = request.get_json()
    input_code = data.get('input_code', '')
    target_language = data.get('target_language', '')

    # Validate input parameters as needed

    # Generate code based on user input
    generated_code = generate_code(input_code, target_language)

    return jsonify({'generated_code': generated_code})

if __name__ == '__main__':
    app.run(debug=True, port=5023)
