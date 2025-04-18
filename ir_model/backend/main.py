import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pre_processing.utils import SentenceTransformerWordEmbeddings

from .BERT import cosine_similarity
from .BM25 import BM25
import json
import numpy as np

processor = SentenceTransformerWordEmbeddings(model_name="distilbert-base-nli-mean-tokens")


def minmax_normalize(scores):
    if not scores:
        return []
        
    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score
    
    if score_range == 0:
        return [0.5] * len(scores)
    
    return [(score - min_score) / score_range for score in scores]


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

    bm25 = BM25(texts, k1, b, word_weights)
    bm25_scores = bm25.get_scores(query)

    #reference_embedding = embeddings[0]

    # Create query into word embedding
    reference_embedding = processor.simple_transformation(query)


    bert_scores = [cosine_similarity(reference_embedding, emb) for emb in embeddings]


    bert_scores = minmax_normalize(bert_scores)
    bm25_scores = minmax_normalize(bm25_scores)

    results = []
    for i, (text, bm25_score, bert_score) in enumerate(zip(texts, bm25_scores, bert_scores)):
        index, column = document_indices[i]
        
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
        # print(doc_data)

    result_list = list(document_scores.values())
    result_list.sort(key=lambda x: x['combined_document_score'], reverse=True)
    
    return result_list


def fetch_results(query, data_path, max_results_to_fetch, diet=[], cuisine=[]):

    # data_path= '../../data/processed/word_embeddings.json'
    # query = 'sex'

    complement_to_query = ', '.join(diet + cuisine)

    # Could add dietery requierments
    word_weights = {key: 3 for key in diet + cuisine}

    print(word_weights)

    # Make sure these add up to 100 percent
    column_weights = {
        'ingredients': 0.3,
        'name': 0.05,
        'description': 0.1,
        'tags': 0.4,
        'steps': 0.15,
    }

    k1 = 1
    b = 0.75

    with open(data_path, 'r') as f:
        documents_data = json.load(f)

    # Calculate similarity scores
    results = calculate_similarity_scores(
        documents_data=documents_data, 
        query=query + complement_to_query, 
        word_weights=word_weights,
        k1=k1,
        b=b
    )

    combined_results = combine_document_scores(results, column_weights)

    
    combined_results = combined_results
    return combined_results[:max_results_to_fetch]


# Test pipeline

# combined_results = fetch_results(
#                         'cut shortening into dry ingredients', 
#                         '../../data/processed/word_embeddings.json',
#                         10,
#                         ['course', 'weeknight', 'non-stick', 'apart'],
#                         ['vanilla', 'single', 'yummy', 'miniature', 'patties'])


# ['columns'][<col>]['text']
# print(combined_results[1]['columns']['name'])
# print('\n')
# print(combined_results[1]['columns']['ingredients'])
# print('\n')
# print(combined_results[1]['columns']['steps'])
# print('\n')
# print(combined_results[1]['columns']['tags'])
# print('\n')
# print(combined_results[1]['columns']['description'])




# for i, combined_result in enumerate(combined_results):
#     print('Result {}:'.format(i + 1))
#     print('Document: {}'.format(combined_result['document_index']))
#     for column in combined_result['columns'].keys():
#         print('--------------------------------------------------------------')
#         print('{}: {}'.format(column, combined_result['columns'][column]['text']))
#     print('--------------------------------------------------------------')
#     print('Combined Score: {}'.format(combined_result['combined_document_score']))
#     print('\n')


