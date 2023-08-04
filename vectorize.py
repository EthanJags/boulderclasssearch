import openai
import pandas as pd
# from openai.embeddings_utils import get_embedding
import requests
import json

openai.api_key = "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"
import ast


# def get_vectors():
#     vector = openai.Embedding.retrieve(id="text-embedding-ada-002")
#     return vector
count = 0
def get_embedding(input_text, engine):
    global count
    count = count + 1
    print(count)
    print(input_text)
    # Define the API endpoint
    endpoint = "https://api.openai.com/v1/embeddings"
    
    # Set your OpenAI API key
    api_key = "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"

    # Prepare the headers for the request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload for the request
    data = {
        "model": engine,
        "input": input_text
    }
    
    # Make the POST request
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    # print(response.json())
    # print("formatted")
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # In a real-world scenario, you might want to add error handling here
        return None


# Load the data from the CSV file
df = pd.read_csv('CUScrape copy.csv', encoding='latin-1')
print("opened")
# Apply the get_embedding function to each row in the 'Class Code' column
# This will create a new Series (column) in pandas where each row contains the embedding of the corresponding 'Class Code'


def extract_embeddings_from_json(json_data):
    holder = json_data['data'][0]['embedding']
    print("formatted: ", holder)
    return holder

df['Embeddings'] = df.apply(lambda row: extract_embeddings_from_json(get_embedding(row['Class Name'] if pd.isna(row['Class Description']) else row['Class Name'] + ": " + row['Class Description'], engine='text-embedding-ada-002')), axis=1)

# Save the DataFrame, including the new 'embedding' column, to a new CSV file
df.to_csv('CUScrape_with_embeddingsformatted.csv', index=False, encoding='latin-1')