from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

recipes = [
    {
        "title": "Pasta Carbonara",
        "cuisine": "Italian",
        "diet": ["Vegetarian"],
        "ingredients": ["Pasta", "Egg", "Parmesan", "Pepper"],
        "steps": ["Boil pasta", "Mix ingredients", "Serve hot"]
    },
    {
        "title": "Vegan Salad",
        "cuisine": "Turkish",
        "diet": ["Vegan"],
        "ingredients": ["Lettuce", "Tomato", "Cucumber"],
        "steps": ["Chop ingredients", "Mix them", "Add olive oil"]
    }
]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    results = [r for r in recipes if query in r['title'].lower()]
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
