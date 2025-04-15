from BERT import cosine_similarity
from BM25 import BM25
import json
import numpy as np

def calculate_similarity_scores(documents_data,
                                query,
                                word_weights=None,
                                k1=1.2, 
                                b=0.75,
                                max_results=10):
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

    bm25 = BM25(texts, k1, b, word_weights)
    bm25_scores = bm25.get_scores(query)

    reference_embedding = embeddings[0]  # Using first document as reference
    bert_scores = [cosine_similarity(reference_embedding, emb) for emb in embeddings]

    results = []
    for i, (text, bm25_score, bert_score) in enumerate(zip(texts, bm25_scores, bert_scores)):
        index, column = document_indices[i]
        
        combined_score = 0.5 * bm25_score + 0.5 * bert_score
        
        results.append({
            'document_index': index,
            'column': column,
            'text': text,
            'bm25_score': bm25_score,
            'bert_score': bert_score,
            'combined_score': combined_score
        })

    results.sort(key=lambda x: x['combined_score'], reverse=True)
    
    return results[:max_results]

json_data_path= '../../data/processed/word_embeddings.json'
query = 'Chicken Fajitas with Pasta and Cheese'

word_weights = {
        "meal": 4,
        "chicken": 2,
        "pasta": 15
    }

k1= 1
b=0.75
max_results=10

with open(json_data_path, 'r') as f:
    documents_data = json.load(f)


# Calculate similarity scores
results = calculate_similarity_scores(
    documents_data=documents_data, 
    query=query, 
    word_weights=word_weights,
    k1=k1,
    b=b,
    max_results=max_results
)

results = [doc for doc in results if doc.get('column') == 'ingredients']

print("Top results for 'good chicken':")
for i, result in enumerate(results):
    print('Result {}:'.format(i + 1))
    print('Document: {}, Column: {}'.format(result['document_index'], result['column']))
    print('Text: {}'.format(result['text']))
    print('BM25 Score: {}'.format(result['bm25_score']))
    print('BERT Score: {}'.format(result['bert_score']))
    print('Combined Score: {}'.format(result['combined_score']))
    print()
