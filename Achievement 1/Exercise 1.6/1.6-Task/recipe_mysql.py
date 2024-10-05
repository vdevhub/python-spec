import mysql.connector

# Initialize a database connection object
conn = mysql.connector.connect(
  host = 'localhost',
  user = 'cf-python',
  password = 'password'
)

# Initialize a cursor object
cursor = conn.cursor()

# Create a new task_database unless exists
# Access the database
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

# Create a Recipes table unless exists
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
                    id            INT PRIMARY KEY AUTO_INCREMENT,
                    name          VARCHAR(50),
                    ingredients   VARCHAR(255),
                    cooking_time  INT,
                    difficulty    VARCHAR(20)
                  )
              ''')

# Displays the main menu
# Calls functions based on the user's choice
def main_menu(conn, cursor):
  choice = ""
  while (choice != 'quit'):
    print("Main Menu")
    print("##########################################")
    print("Pick an option:")
    print("1. Create a new recipe")
    print("2. Search for a recipe by ingredient")
    print("3. Update an existing recipe")
    print("4. Delete a recipe")
    print("Type 'quit' to exit the program.")
    choice = input("Your choice: ")
  
    if choice == '1':
      create_recipe(conn, cursor)
    elif choice == '2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      delete_recipe(conn, cursor)
  
  quit_conn(conn)
  print("Program ended. Goodbye!")

# Terminates the DB connection
def quit_conn(conn):
  conn.commit()
  conn.close()

# Creates a new recipe
def create_recipe(conn, cursor):
  # Get user input - recipe name, cooking time, ingredients
  name = input("Enter the name of your recipe: ").strip().lower().capitalize()
  cooking_time = int(input("Enter the cooking time of your recipe in minutes: ").strip())
  ingredients = input("Enter the ingredients for your recipe with each ingredient separated by a comma: ").strip().split(',')
  print()
  
  # Normalize ingredients
  # Create ingredients string for the SQL query
  ingredients = [ingredient.strip().lower().capitalize() for ingredient in ingredients]
  ingredients_string =  ", ".join(ingredients)

  # Get recipe's difficulty
  difficulty = calculate_difficulty(cooking_time, ingredients)

  # Prepare the SQL query and values
  sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
  vals = (name, ingredients_string, cooking_time, difficulty)

  # Execute the query and commit changes
  cursor.execute(sql, vals)
  conn.commit()

# Calculates a recipe's difficulty
# based on its cooking time and number of ingredients
def calculate_difficulty(cooking_time, ingredients):
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


def search_recipe(conn, cursor):
  all_ingredients = []
  
  # Fetch all ingredients rows
  cursor.execute("SELECT ingredients FROM Recipes")
  results = cursor.fetchall()

  # Add unique ingredients to the list
  for ingredient_rows in results:
    for ingredients_string in ingredient_rows:
      ingredients_list = ingredients_string.split(', ')
      for ingredient in ingredients_list:
        if not ingredient in all_ingredients:
          all_ingredients.append(ingredient)

  print("Ingredients List")
  print("##########################################")
  for index, ingredient in enumerate(all_ingredients):
    print(str(index) + '. ' + ingredient)
  
  try:
    search_ingredient = all_ingredients[int(input("Select the number of ingredient to search for: "))]
  except:
    print("You entered the wrong number or your input is not a number.")
  else:
    sql = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    val = ('%' + search_ingredient + '%', )
    cursor.execute(sql, val)
    matched_recipes = cursor.fetchall()

    print("Found the Following Recipes")
    print("##########################################")
    print()
    for recipe in matched_recipes:
      display_recipe(recipe)

# Displays one recipe
def display_recipe(recipe):
  print("Recipe: " + recipe[1])
  print("Cooking Time (min): " + str(recipe[3]))
  print("Ingredients:")
  for ingredient in recipe[2].split(', '):
    print(ingredient)
  print("Difficulty level: " + recipe[4])
  print()

# Updates a recipe
def update_recipe(conn, cursor):
  cursor.execute("SELECT * FROM Recipes")
  all_recipes = cursor.fetchall()

  print("Recipes List")
  print("##########################################")
  print()
  for recipe in all_recipes:
    print(str(recipe[0]) + '. ' + recipe[1])
    
  recipe_to_update_num = int(input("Select the number of the recipe you want to update: "))
  column_to_update = input("Type the column that you want to update (name, cooking_time, ingredients): ")
  new_value = input("Enter the new value, please: ")

  def update_difficulty(id):
    cursor.execute(f"SELECT * FROM Recipes WHERE id = %s", (id, ))
    recipe_to_update = cursor.fetchall()

    cooking_time = recipe_to_update[0][3]
    ingredients = recipe_to_update[0][2].split(', ')

    updated_difficulty = calculate_difficulty(cooking_time, ingredients)
    cursor.execute(f"UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, id))

  if column_to_update == 'name':
    cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_value, recipe_to_update_num))
  elif column_to_update == 'cooking_time':
    cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_value, recipe_to_update_num))
    update_difficulty(recipe_to_update_num)
  elif column_to_update == 'ingredients':
    ingredients = [ingredient.strip().lower().capitalize() for ingredient in new_value]
    ingredients_string =  ", ".join(ingredients)
    cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (ingredients_string, recipe_to_update_num))
    update_difficulty(recipe_to_update_num)

  conn.commit()
  print("Updated successfully.")

def delete_recipe(conn, cursor):
  cursor.execute("SELECT * FROM Recipes")
  all_recipes = cursor.fetchall()

  print("Recipes List")
  print("##########################################")
  print()
  for recipe in all_recipes:
    print(str(recipe[0]) + '. ' + recipe[1])
    
  recipe_to_delete_num = int(input("Select the number of the recipe you want to delete: "))
  cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_to_delete_num, ))
  print("Recipe deleted!")
  print()

  conn.commit()


# Main code
main_menu(conn, cursor)
