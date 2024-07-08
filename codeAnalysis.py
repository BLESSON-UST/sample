import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

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
    """
    Handle the explanation of provided code.
    """
    data = request.get_json()
    input_code = data.get('input_code', '')

    explanation = get_code_explanation(input_code)
    return jsonify({'code_explanation': explanation})


def get_code_explanation(input_code):
    """
    Get the explanation for the provided code using Azure OpenAI API.
    """
    explanation_prompt = construct_explanation_prompt(input_code)
    messages = [{"role": "user", "content": explanation_prompt}]

    response = make_azure_openai_request(messages)
    
    explanation = parse_response(response)
    return explanation


def construct_explanation_prompt(input_code):
    """
    Construct the prompt for code explanation.
    """
    explanation_prompt = f"""
        "Provide a step-by-step algorithm for the given logic with well-explained points.
        Ensure each step is separated by a newline. After proper spacing, give a summary of the logic.
        Give a flowchart also."

        {input_code}
    """
    return explanation_prompt


def make_azure_openai_request(messages):
    """
    Make a POST request to Azure OpenAI API.
    """
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json={"messages": messages})
    return response


def parse_response(response):
    """
    Parse the response from Azure OpenAI API.
    """
    try:
        response_data = response.json()
        app.logger.debug("Azure OpenAI API Response: %s", response_data)  # Log the response for debugging

        explanation = response_data["choices"][0]["message"]["content"]
    except (KeyError, ValueError):
        explanation = "Error: Unable to explain the code using Azure OpenAI API."

    return explanation


if __name__ == '__main__':
    app.run(debug=True, port=5014)