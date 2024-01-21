from flask import Flask, render_template, request

import json
import requests
app = Flask(__name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
  'x-rapidapi-key': "815abe79damsh508dd88101127e1p140d1ajsnf54e52aadad1",
  }

random_joke = "food/jokes/random"
find = "recipes/findByIngredients"
randomFind = "recipes/random"

@app.route('/')
def search_page():
  joke_response = "LOL" #str(requests.request("GET", url + random_joke, headers=headers).json()['text'])
  return render_template('search.html', joke=joke_response)

@app.route('/recipes')
def get_recipes():
  time = int(request.args['time']).strip()
  if (time <10):
     return render_template('error.html')
  if (str(request.args['ingridients']).strip() != ""):
      # If there is a list of ingridients -> list
      querystring = {"number":"20","ranking":"2","ignorePantry":"false","ingredients":request.args['ingridients']}
      response = requests.request("GET", url + find, headers=headers, params=querystring).json()
      for recipe in response:
         if( recipe['readyInMinutes']!=""):
            recipe_time=recipe['readyInMinutes']
            if (time> recipe_time):
              response.remove(recipe)
      if len(response) == 0:
         return render_template('error.html')
      return render_template('recipes.html', recipes=response)
  else:
      # Random recipes
      querystring = {"number":"5"}
      response = requests.request("GET", url + randomFind, headers=headers, params=querystring).json()
      print(response)
      return render_template('recipes.html', recipes=response['recipes'])
  
@app.route('/recipe')
def get_recipe():
  recipe_id = request.args['id']
  recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
  ingedientsWidget = "recipes/{0}/ingredientWidget".format(recipe_id)
  equipmentWidget = "recipes/{0}/equipmentWidget".format(recipe_id)
  summary = "recipes/{0}/summary".format(recipe_id)


  recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers).json()
    
  recipe_headers = {
      'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
      'x-rapidapi-key': "815abe79damsh508dd88101127e1p140d1ajsnf54e52aadad1",
      'accept': "text/html"
  }
  querystring = {"defaultCss":"true", "showBacklink":"false"}

  recipe_info['inregdientsWidget'] = requests.request("GET", url + ingedientsWidget, headers=recipe_headers, params=querystring).text
  recipe_info['equipmentWidget'] = requests.request("GET", url + equipmentWidget, headers=recipe_headers, params=querystring).text
    
  recipe_info['instructionss'] = requests.request("GET", url + summary, headers=recipe_headers, params=querystring).text

  return render_template('recipe.html', recipe=recipe_info)


if __name__ == '__main__':
  app.run()

