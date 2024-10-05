# Class Definition

class Recipe(object):
  # Class variable with ingredients of all recipes
  all_ingredients = []

  # Initialize a new recipe
  def __init__(self, name):
    self.name = name
    self.cooking_time = 0
    self.ingredients = []
    self.difficulty = None
  
  # Get the recipe's name
  def get_name(self):
    return self.name
  
  # Get the recipe's cooking time
  def get_cooking_time(self):
    return self.cooking_time
  
  # Set the recipe's name
  def set_name(self, name):
    self.name = name

  # Set the recipe's cooking time
  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time

  # Add ingredients to the recipe
  # And update the list of all ingredients
  def add_ingredients(self, *ingredients):
    [self.ingredients.append(ingredient) for ingredient in ingredients]
    self.update_all_ingredients()

  # Get the recipe's ingredients
  def get_ingredients(self):
    return self.ingredients
  
  # Calcuate the recipe's difficulty
  # Based on the recipe's cooking time
  # and the number of ingredients
  def calculate_difficulty(self):
    if self.cooking_time < 10:
      if len(self.ingredients) < 4:
        self.difficulty = 'Easy'
      else:
        self.difficulty = 'Medium'
    elif self.cooking_time >= 10:
      if len(self.ingredients) < 4:
        self.difficulty = 'Intermediate'
      else:
        self.difficulty = 'Hard'
  
  # Get the recipe's difficulty
  def get_difficulty(self):
    if self.difficulty is None:
      self.calculate_difficulty()
    
    return self.difficulty
  
  # Check if the recipe contains an ingredient
  def search_ingredient(self, ingredient):
    return ingredient in self.ingredients
  
  # Update the all ingredients list
  # with the recipe's ingredients
  def update_all_ingredients(self):
    [Recipe.all_ingredients.append(ingredient) for ingredient in self.ingredients 
     if not ingredient in Recipe.all_ingredients]
  
  # String representation of the recipe
  def __str__(self):
    ingredients_string = '\n'.join(self.ingredients)
    recipe_string = "\nRecipe: " + self.name + \
                    "\nCooking Time (min): " + str(self.cooking_time) + \
                    "\nDifficulty level: " + self.get_difficulty() + \
                    "\n------ Ingredients ------\n" + ingredients_string
    
    return recipe_string

# Search and print recipes
# with a chosen ingredient
def recipe_search(data, search_term):
  for recipe in data:
    if recipe.search_ingredient(search_term):
      print(recipe)


# Main Code

# Initialize recipes
tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
print(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
print(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
print(cake)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)

# Add recipes to a list
recipes_list = [tea, coffee, cake, banana_smoothie]

# Search recipes
searched_ingredients = ["Water", "Sugar", "Bananas"]
for searched_ingredient in searched_ingredients:
  print("\n\nRecipes containing '" + searched_ingredient + "'")
  recipe_search(recipes_list, searched_ingredient)