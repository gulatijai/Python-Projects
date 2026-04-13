import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

app= Flask(__name__)
bootstrap=Bootstrap5(app)

BASE_URL= "https://www.themealdb.com/api/json/v1/1/"

def get_api_data(endpoint):
    response= requests.get(BASE_URL+endpoint)
    return response.json()

def get_ingredients(meal):
    ingredients =[]
    for i in range(1,21):
        ingredient= meal.get(f'strIngredient{i}')
        measure= meal.get(f'strMeasure{i}')
        if ingredient and ingredient.strip():
            ingredients.append(f'{measure.strip()} {ingredient.strip()}')
    return ingredients

@app.route('/')
def home():
    data= get_api_data('random.php')
    random_meal= data['meals'][0]
    categories =get_api_data('categories.php')['categories']
    return render_template('index.html', meal= random_meal, categories =categories)

@app.route('/search')
def search():
    query= request.args.get('q')
    data= get_api_data(f'search.php?s={query}')
    meals= data['meals'] if data['meals'] else[]
    return render_template('results.html', meals= meals, query=query)

@app.route('/meal/<meal_id>')
def meal_detail(meal_id):
    data= get_api_data(f'lookup.php?i={meal_id}')
    meal= data['meals'][0]
    ingredients= get_ingredients(meal)
    return render_template('meal.html', meal=meal, ingredients= ingredients)

@app.route('/category/<category_name>')
def category(category_name):
    data= get_api_data(f'filter.php?c={category_name}')
    meals= data['meals'] if data['meals'] else []
    return render_template('category.html', meals= meals, category= category_name)

@app.context_processor
def inject_categories():
    categories = get_api_data('categories.php')['categories']
    return dict(categories=categories)

if __name__ == '__main__':
    app.run(debug=True)