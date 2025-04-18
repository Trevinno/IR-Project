print('hello first')

from utils import SentenceTransformerWordEmbeddings
import numpy as np
import json
import pickle

processor = SentenceTransformerWordEmbeddings(model_name='distilbert-base-nli-mean-tokens', device='cpu')

text_columns =['name', 'tags', 'steps', 'description', 'ingredients']

# Process CSV
embeddings_results = processor.process_csv(
    csv_path='../../data/raw/RAW_recipes_test.csv',
    text_columns=text_columns,
    output_path='../../data/processed/word_embeddings.json',
    sentence_embeddings=True
)
