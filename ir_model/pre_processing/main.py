from utils import SentenceTransformerWordEmbeddings
import numpy as np
import json
import pickle

csv_path = '../../data/raw/RAW_recipes_test.csv'
s3_path = '/RAW/RAW_recipes_test.csv'

output_path = '../../data/processed/word_embeddings.json'
s3_output_path = 's3://open-bucket-ir-qmul/PROCESSED/word_embeddings.json'

processor = SentenceTransformerWordEmbeddings(model_name='distilbert-base-nli-mean-tokens', device='cpu')

text_columns =['name', 'tags', 'steps', 'description', 'ingredients']

# Process CSV
embeddings_results = processor.process_csv(
    csv_path=csv_path,
    text_columns=text_columns,
    output_path=output_path,
    sentence_embeddings=True,
    online_hosting=False
)
