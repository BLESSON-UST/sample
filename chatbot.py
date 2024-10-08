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


@app.route('/api/sustainability', methods=['POST'])
def generate_requirements():
    data = request.get_json()
    requirements = data.get('requirements', [])
    criteria = data.get('criteria', [])
    refined_requirements = refine_requirements(requirements, criteria)

    response_data = {
        'refined_requirements': refined_requirements
    }

    return jsonify(response_data)


def refine_requirements(requirements, criteria):
    selected_criteria = get_selected_criteria(criteria)
    messages = prepare_messages(requirements)

    response = requests.post(
        AZURE_OPENAI_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY
        },
        json={
            "messages": messages,
            "max_tokens": 3000,
            "temperature": 0.6,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 0.95
        }
    )

    refined_requirement = get_refined_requirement(response)

    return refined_requirement


def get_selected_criteria(criteria):
    selected_criteria = []

    if criteria.get('sustainability_regulations'):
        selected_criteria.append('sustainability regulations')
    if criteria.get('sustainability_impact'):
        selected_criteria.append('sustainability impact')
    if criteria.get('sustainability_risks'):
        selected_criteria.append('sustainability risks')

    return selected_criteria


def prepare_messages(requirements):
    messages = [
        {"role": "system", "content": "\n".join(requirements)},
    ]

    return messages


def get_refined_requirement(response):
    try:
        response_data = response.json()
        app.logger.debug("Azure OpenAI API Response: %s", response_data)

        refined_requirement = response_data["choices"][0]["message"]["content"]
    except KeyError:
        refined_requirement = "Error: Unable to retrieve refined requirements and explanation from Azure OpenAI API."

    return refined_requirement


if __name__ == '__main__':
    app.run(debug=True, port=5052)