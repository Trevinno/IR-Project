from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ir_model.backend import fetch_results
app = Flask(__name__)
CORS(app)

local_data_path = '../data/processed/word_embeddings.json'


s3_data = False

if s3_data:
    data_path = s3_data_path
else:
    data_path = local_data_path

recipes = [
    {
        'document_index': 1,
        'columns': {
            'name': {
                'text': 'arriba baked winter squash mexican style',
                'bm25_score': 0.0,
                'bert_score': np.float64(1.0),
                'combined_score': np.float64(0.5)
            },
            'ingredients': {
                'text': 'winter squash mexican seasoning mixed spice honey butter olive oil salt',
                'bm25_score': 0.0,
                'bert_score': np.float64(0.859762083856304),
                'combined_score': np.float64(0.429881041928152)
            },
            'steps': {
                'text': 'make a choice and proceed with recipe depending on size of squash , cut into half or fourths remove seeds for spicy squash , drizzle olive oil or melted butter over each cut squash piece season with mexican seasoning mix ii for sweet squash , drizzle melted honey , butter , grated piloncillo over each cut squash piece season with sweet mexican spice mix bake at 350 degrees , again depending on size , for 40 minutes up to an hour , until a fork can easily pierce the skin be careful not to burn the squash especially if you opt to use sugar or butter if you feel more comfortable , cover the squash with aluminum foil the first half hour , give or take , of baking if desired , season with salt',
                'bm25_score': 0.0,
                'bert_score': np.float64(0.666948999530292),
                'combined_score': np.float64(0.333474499765146)
            },
            'tags': {
                'text': '60-minutes-or-less time-to-make course main-ingredient cuisine preparation occasion north-american side-dishes vegetables mexican easy fall holiday-event vegetarian winter dietary christmas seasonal squash',
                'bm25_score': 0.0,
                'bert_score': np.float64(0.6796339551919633),
                'combined_score': np.float64(0.3398169775959817)
            },
            'description': {'text': 'autumn is my favorite time of year to cook! this recipe \r\ncan be prepared either spicy or sweet, your choice!\r\ntwo of my posted mexican-inspired seasoning mix recipes are offered as suggestions.', 
            'bm25_score': 0.0,
            'bert_score': np.float64(0.5729694140786755),
            'combined_score': np.float64(0.28648470703933776)
            }
        },
        'combined_document_score': 0.0
    }
]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    query_diet = request.args.getlist('diet')
    query_cusine = request.args.getlist('cuisine')

    recipes = fetch_results(query, data_path, 10, query_diet, query_cusine)

    return jsonify({'results': recipes})

if __name__ == '__main__':
    app.run(debug=True)
