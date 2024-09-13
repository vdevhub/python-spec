import pickle

def display_recipe(recipe):
  print("Recipe: " + recipe.get('name'))
  print("Cooking Time (min): " + str(recipe.get('cooking_time')))
  print("Ingredients:")
  for ingredient in recipe.get('ingredients'):
    print(ingredient)
  print("Difficulty level: " + recipe.get('difficulty'))
  print()

def search_ingredient(data):
  for index, ingredient in enumerate(data['all_ingredients']):
    print(str(index) + ' - ' + ingredient)
  
  try:
    ingredient_number = int(input("Which ingredient would you like to search for? Enter the number: "))
    ingredient_searched = data['all_ingredients'][ingredient_number]
  except:
    print("The input is incorrect. You have to type the number of an ingredient from the ingredients listed.")
  else:
    for recipe in data['recipes_list']:
      if ingredient_searched in recipe['ingredients']:
        display_recipe(recipe)

filename = input("Enter the filename (with .bin extension) where your recipes are stored: ")
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
except:
    print("The file hasn't been found - exiting.")
else:
    search_ingredient(data)
    file.close()
