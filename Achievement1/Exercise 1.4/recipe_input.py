import pickle

recipes_list = []
all_ingredients = []

def take_recipe():
  name = input("Enter the name of your recipe: ").strip().lower().capitalize()
  cooking_time = int(input("Enter the cooking time of your recipe in minutes: ").strip())
  ingredients = input("Enter the ingredients for your recipe with each ingredient separated by a comma: ").strip().split(',')
  print()

  ingredients = [ingredient.strip().lower().capitalize() for ingredient in ingredients]

  recipe = {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients,
    'difficulty': calc_difficulty(cooking_time, ingredients)
  }

  return recipe

def calc_difficulty(cooking_time, ingredients):
  difficulty = ''

  if cooking_time < 10:
    if len(ingredients) < 4:
      difficulty = 'Easy'
    else:
      difficulty = 'Medium'
  elif cooking_time >= 10:
    if len(ingredients) < 4:
      difficulty = 'Intermediate'
    else:
      difficulty = 'Hard'
  
  return difficulty



filename = input("Enter the filename (with .bin extension) where your recipes are stored: ")
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
except FileNotFoundError:
    data = {
      'recipes_list': [],
      'all_ingredients': []
    }
except:
    data = {
      'recipes_list': [],
      'all_ingredients': []
    }
else:
    file.close()
finally:
    recipes_list, all_ingredients = data['recipes_list'], data['all_ingredients']


n = int(input("How many recipes would you like to enter?: "))

for i in range(0,n):
  recipe = take_recipe()

  for ingredient in recipe.get('ingredients'):
    if ingredient not in all_ingredients:
      all_ingredients.append(ingredient)
  
  recipes_list.append(recipe)


data = {
   'recipes_list': recipes_list,
   'all_ingredients': all_ingredients
}

with open(filename, 'wb') as file:
   pickle.dump(data, file)

print('Recipes saved successfully!')