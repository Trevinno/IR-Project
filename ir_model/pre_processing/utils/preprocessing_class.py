import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from typing import List, Union, Dict, Optional, Tuple
import os
import pickle
from tqdm import tqdm
from nltk.tokenize import word_tokenize
import nltk
import ast
import json


class SentenceTransformerWordEmbeddings:
    def __init__(
        self, 
        model_name: str = "distilbert-base-nli-mean-tokens",
        device: Optional[str] = None,
        batch_size: int = 32
    ):
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        # Load model
        self.model = SentenceTransformer(model_name, device=self.device)
        self.model_name = model_name
        self.batch_size = batch_size

        self.columns_dict = {
            'name': False,
            'tags': True,
            'steps': True,
            'description': False,
            'ingredients': True

        }
        
        # Download NLTK resources if needed
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print('downloading punkt')
            nltk.download('punkt')

        try:
            nltk.data.find('tokenizers/punk_tab')
        except LookupError:
            print('downloading punkt tab')
            nltk.download('punkt_tab')
            
        print(f"Model '{model_name}' loaded on {self.device}")
    
    def change_model(self, model_name: str):
        self.model = SentenceTransformer(model_name, device=self.device)
        self.model_name = model_name
        print(f"Model changed to '{model_name}'")

    def create_word_embeddings(self, tokenized_texts: List[List[str]]) -> List[Dict[str, np.ndarray]]:
        # Flatten list of words for batch processing
        all_words = []
        word_to_doc = []  # Track which document each word came from
        
        for doc_idx, words in enumerate(tokenized_texts):
            unique_words = list(set(words))  # Only process unique words in each document
            all_words.extend(unique_words)
            word_to_doc.extend([doc_idx] * len(unique_words))
        
        # Get embeddings for all words in batches
        word_embeddings = []
        for i in tqdm(range(0, len(all_words), self.batch_size), desc="Embedding words"):
            batch_words = all_words[i:i+self.batch_size]
            with torch.no_grad():
                embeddings = self.model.encode(batch_words, convert_to_numpy=True)
            word_embeddings.append(embeddings)
        
        if word_embeddings:
            all_word_embeddings = np.vstack(word_embeddings)
        else:
            # Handle empty case
            all_word_embeddings = np.array([])
        
        # Group word embeddings by document
        doc_word_embeddings = []
        for i in range(len(tokenized_texts)):
            doc_word_embeddings.append({})
        
        # Map each word embedding back to its document
        for idx, (word, doc_idx) in enumerate(zip(all_words, word_to_doc)):
            doc_word_embeddings[doc_idx][word] = all_word_embeddings[idx]
        
        return doc_word_embeddings

    def save_data(
        self,
        results,
        output_path: [str]
    ):  

        # Save embeddings if output path is provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(results, f)
            print(f"Word embeddings saved to {output_path}")

    def get_word_embeddings(
        self,
        texts: List[str]
    ) -> Dict[str, List]:
        # Tokenize texts
        tokenized_texts = [word_tokenize(text) for text in texts]
        
        # Get word embeddings
        word_embeddings = self.create_word_embeddings(tokenized_texts)
        
        results = {
            "word_embeddings": word_embeddings,
            "tokenized_words": tokenized_texts
        }
            
        return results

    def process_csv(
        self, 
        csv_path: str, 
        text_columns: Union[str, List[str]], 
        output_path: Optional[str] = None,
        sentence_embeddings: bool = True
    ) -> Dict[str, Dict[str, List]]:
        # Read CSV
        df = pd.read_csv(csv_path)
        print(f"CSV loaded with {len(df)} rows")
        
        # Ensure text_columns is a list
        if isinstance(text_columns, str):
            text_columns = [text_columns]
            
        # Validate columns
        for col in text_columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in CSV")
        
        all_results = {}
        


        if sentence_embeddings:
            for index, col in enumerate(text_columns):
                if(self.columns_dict[col]):
                    texts = df[col].apply(lambda x: ' '.join(ast.literal_eval(x)) if isinstance(ast.literal_eval(x), list) else x).fillna("").tolist()
                else:
                    texts = df[col].fillna('').tolist()
                sentence_embedding = self.model.encode(texts, batch_size=self.batch_size, show_progress_bar=True).tolist()
                all_results[col] = {}
                all_results[col]['sentence_embeddings'] = sentence_embedding
                all_results[col]['raw_texts'] = texts
                print('embeddings the lenghts', len(sentence_embedding))
                print('embeddings the lengths', len(texts))
        else:
            # This part is complete legacy, you are not going to use it in theory
            for col in text_columns:
                texts = df[col].fillna("").tolist()
                all_results[col] = self.get_word_embeddings(texts)
        
        # Here is where we create the json style we all know and love
        
        final_json = []
        sample_column = text_columns[0]

        for index, value in enumerate(all_results[col]['sentence_embeddings']):
            new_document = {}
            for col in all_results.keys():
                new_document[col] = {}
                new_document[col]['sentence_embeddings'] = all_results[col]['sentence_embeddings'][index]
                new_document[col]['raw_texts'] = all_results[col]['raw_texts'][index]
            final_json.append(new_document)


        # print('This is a preview of whats inside', final_json[0]['tags'])
        # Save embeddings if output path is provided
        self.save_data(final_json, output_path)
            
        return final_json
