import openai
import pandas as pd
from openai.embeddings_utils import get_embedding

openai.api_key = "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"

# Load the data from the CSV file
df = pd.read_csv('CUScrape.csv', encoding='latin-1')

# Apply the get_embedding function to each row in the 'Class Code' column
# This will create a new Series (column) in pandas where each row contains the embedding of the corresponding 'Class Code'
df['embedding'] = df['Class Code'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))

# Save the DataFrame, including the new 'embedding' column, to a new CSV file
df.to_csv('CUScrape_with_embeddings.csv', index=False, encoding='latin-1')