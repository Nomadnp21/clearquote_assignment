import os
from flask import Flask, request, jsonify, render_template
import pandas as pd
import openai

# Load the dataset
df = pd.read_csv(r"C:\Users\kkpan\Downloads\Data Analyst Exercise - May 2024 - Dataset.csv")

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Define a function to process the query and return results
def process_query(query):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=query,
        max_tokens=50
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    query = request.form['query']
    response = process_query(query)
    
    # For simplicity, directly using the interpreted result as a SQL-like query
    try:
        result = df.query(response).to_dict(orient='records')
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
