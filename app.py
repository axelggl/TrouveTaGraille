from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from urllib.parse import unquote, urlencode

# Create Flask app
app = Flask(__name__, template_folder='src')

# Get API key from .env file
load_dotenv('.env')
api_key = os.getenv('API_KEY')

# Define the base URL for the API
url = 'https://api.spoonacular.com/recipes/findByIngredients'

# Define the main route for the app
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If a form was submitted, get the form data
        query = request.form.get('search_query', '')
        # Perform a search for recipes with the given ingredients
        recipes = get_recipes(query)
        # Return the main page
        return render_template('index.html', recipes=recipes, search_query=query)
    
    # If it's a GET request or no form data was submitted, return the homepage
    search_query = request.args.get('search_query', '')
    decoded_query = unquote(search_query)
    # Perform a search for recipes with the given ingredients
    recipes = get_recipes(decoded_query)
    # Return the main page
    return render_template('index.html', recipes=recipes, search_query=decoded_query)

# Function to search for recipes with the given ingredients
def get_recipes(ingredients: str) -> dict:
    # Replace spaces with ',+'
    formatted_ingredients = ingredients.replace(' ', ',+')
    # Manually construct the query string to avoid encoding issues
    query_string = f"ingredients={formatted_ingredients}&apiKey={api_key}"
    api_url = f"{url}?{query_string}"
    
    # Make a GET request to the API
    response = requests.get(api_url)
    print(response.url)
    # Return the JSON response
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data['results']
        else:
            return []
    else:
        return []

# Route to view a recipe
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Get the search query from the URL
    search_query = request.args.get('search_query', '')
    # Build the URL to get information about the specific recipe
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': api_key
    }

    # Send a GET request to the API
    response = requests.get(url, params=params)
    # If the API call is successful, display the recipe
    if response.status_code == 200:
        recipe = response.json()
        return render_template('recipe.html', recipe=recipe, search_query=search_query)
    else:
        return "Recipe not found!", 404

# Run the app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
