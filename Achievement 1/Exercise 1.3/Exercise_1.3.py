recipes_list = []
ingredients_list = []

n = int(input("How many recipes would you like to enter?: "))

def take_recipe():
  name = input("Enter the name of your recipe: ").strip().lower().capitalize()
  cooking_time = int(input("Enter the cooking time of your recipe in minutes: ").strip())
  ingredients = input("Enter the ingredients for your recipe with each ingredient separated by a comma: ").strip().split(',')
  print()
  
  ingredients = [ingredient.strip().lower().capitalize() for ingredient in ingredients]

  recipe = {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients
  }

  return recipe

for i in range(0,n):
  recipe = take_recipe()

  for ingredient in recipe.get('ingredients'):
    if ingredient not in ingredients_list:
      ingredients_list.append(ingredient)
  
  recipes_list.append(recipe)

for recipe in recipes_list:
  difficulty = ''

  if recipe.get('cooking_time') < 10:
    if len(recipe.get('ingredients')) < 4:
      difficulty = 'Easy'
    else:
      difficulty = 'Medium'
  elif recipe.get('cooking_time') >= 10:
    if len(recipe.get('ingredients')) < 4:
      difficulty = 'Intermediate'
    else:
      difficulty = 'Hard'
  
  print("Recipe: " + recipe.get('name'))
  print("Cooking Time (min): " + str(recipe.get('cooking_time')))
  print("Ingredients:")
  for ingredient in recipe.get('ingredients'):
    print(ingredient)
  print("Difficulty level: " + difficulty)
  print()

ingredients_list.sort()
print("Ingredients Available Across All Recipes")
print("----------------------------------------")
for ingredient in ingredients_list:
  print(ingredient)