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
 
@app.route('/api/explain_code', methods=['POST'])
def explain_code():
    data = request.get_json()
    input_code = data.get('input_code', '')
 
    # Constructing a prompt for code explanation
    explanation_prompt = f"""
   "Provide a step-by-step algorithm for the given logic with well-explained points. Ensure each step is separated by a newline. After proper spacing, give a summary of the logic.give a flowchart also."
    
    {input_code}
    """
 
    # Construct the message for Azure OpenAI chat completion with code explanation request and prompt
    messages = [
        {"role": "user", "content": explanation_prompt}
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
 
        explanation = response_data["choices"][0]["message"]["content"]
    except KeyError:
        explanation = "Error: Unable to explain the code using Azure OpenAI API."
 
    return jsonify({'code_explanation': explanation})
 
if __name__ == '__main__':
    app.run(debug=True, port=5014)