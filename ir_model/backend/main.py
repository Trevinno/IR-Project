import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pre_processing.utils import SentenceTransformerWordEmbeddings

from .BERT import cosine_similarity
from .BM25 import BM25
import json
import numpy as np
import pandas as pd

processor = SentenceTransformerWordEmbeddings(model_name="distilbert-base-nli-mean-tokens")


def minmax_normalize(scores):     
    minimum_score = min(scores)
    maximum_score = max(scores)
    score_range = maximum_score - minimum_score
    
    if score_range == 0:
        return [0.5] * len(scores)
    
    return [(score - minimum_score) / score_range for score in scores]


def calculate_similarity_scores(documents_data,
                                query,
                                word_weights=None,
                                k1=1.2, 
                                b=0.75):
    if word_weights is None:
        word_weights = {}
        
    texts = []
    embeddings = []
    document_indices = []
    
    for index, doc in enumerate(documents_data):
        for column in doc.keys():
            if 'raw_texts' in doc[column] and 'sentence_embeddings' in doc[column]:
                if doc[column]['raw_texts'] and doc[column]['sentence_embeddings']:
                    texts.append(doc[column]['raw_texts'])
                    embeddings.append(doc[column]['sentence_embeddings'])
                    document_indices.append((index, column))

    # Obtain BM25 Scores
    bm25 = BM25(texts, k1, b, word_weights)
    bm25_scores = bm25.get_scores(query)

    # Create query into word embedding
    reference_embedding = processor.simple_transformation(query)

    # Obtain Bert Scores
    bert_scores = [cosine_similarity(reference_embedding, emb) for emb in embeddings]

    bert_scores = minmax_normalize(bert_scores)
    bm25_scores = minmax_normalize(bm25_scores)

    results = []
    for index, (text, bm25_score, bert_score) in enumerate(zip(texts, bm25_scores, bert_scores)):
        index, column = document_indices[index]
        
        combined_score = 0.60 * bm25_score + 0.40 * bert_score
        
        results.append({
            'document_index': index,
            'column': column,
            'text': text,
            'bm25_score': bm25_score,
            'bert_score': bert_score,
            'combined_score': combined_score
        })

    results.sort(key=lambda x: x['combined_score'], reverse=True)
    
    return results

def combine_document_scores(results, column_weights):
    document_scores = {}
    for result in results:
        doc_index = result['document_index']
        column = result['column']
        
        if doc_index not in document_scores:
            document_scores[doc_index] = {
                'document_index': doc_index,
                'columns': {},
                'combined_document_score': 0.0
            }

        document_scores[doc_index]['columns'][column] = {
            'text': result['text'],
            'bm25_score': result['bm25_score'],
            'bert_score': result['bert_score'],
            'combined_score': result['combined_score']
        }

    for doc_index, doc_data in document_scores.items():
        weighted_score = 0
        
        for column_id, column_dict in doc_data['columns'].items():
            weighted_score += column_dict['combined_score'] * column_weights[column_id]
        
        
        doc_data['combined_document_score'] = weighted_score

    result_list = list(document_scores.values())
    result_list.sort(key=lambda x: x['combined_document_score'], reverse=True)
    
    return result_list


def fetch_results(query, data_path, max_results_to_fetch, diet=[], cuisine=[]):

    complement_to_query = ', '.join(diet + cuisine)

    # Could add dietery requierments
    word_weights = {key: 3 for key in diet + cuisine}

    # Make sure these add up to 100 percent
    column_weights = {
        'ingredients': 0.3,
        'name': 0.2,
        'description': 0.1,
        'tags': 0.25,
        'steps': 0.15,
    }

    k1 = 1
    b = 0.75

    print('Reading the database...')
    with open(data_path, 'r') as f:
        documents_data = json.load(f)
    print('Finished reading the database.')

    # Calculate similarity scores
    print('Calculating the cosine similarity scores plus BM25 scores...')
    results = calculate_similarity_scores(
        documents_data=documents_data, 
        query=query + complement_to_query, 
        word_weights=word_weights,
        k1=k1,
        b=b
    )
    print('Finished calculating the cosine similarity scores plus BM25 scores.')

    print('Combining the scores...')
    combined_results = combine_document_scores(results, column_weights)
    print('Finished combining the scores.')
    
    combined_results = combined_results
    return combined_results[:max_results_to_fetch]
