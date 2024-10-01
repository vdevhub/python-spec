# Import packages and methods
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

dbms = os.environ.get("DBMS")
user_name = os.environ.get("USER_NAME")
password = os.environ.get("PASSWORD")
host = os.environ.get("HOST")
database = os.environ.get("DATABASE")

# Creates an engine object connecting to the database
# Update to use env variables
engine = create_engine(f"{dbms}://{user_name}:{password}@{host}/{database}")

# Makes the session object to make changes
# to the database
Session = sessionmaker(bind=engine)
session = Session()

# Creates a declarative base class
# To pull SQLAlchemy methods and attributes
# So they are available to custom classes
Base = declarative_base()


# Defines the Recipe class
# Inherits from the Base class
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Shows a quick representation of the recipe
    def __repr__(self):
        return (
            "<Recipe ID: "
            + str(self.id)
            + ", Name: "
            + self.name
            + ", Difficulty: "
            + self.difficulty
            + ">"
        )

    # Prints an extended text representation of the recipe
    def __str__(self):
        ingredients_string = "\n>> ".join(self.ingredients.split(", "))
        recipe_string = (
            "\nRecipe ID "
            + str(self.id)
            + " - "
            + self.name
            + "\n"
            + "-" * 30
            + "\nCooking Time (Min): "
            + str(self.cooking_time)
            + "\nDifficulty: "
            + self.difficulty
            + "\n"
            + "-" * 30
            + "\nIngredients"
            + "\n"
            + "-" * 30
            + "\n>> "
            + ingredients_string
        )
        return recipe_string

    # Calcuate the recipe's difficulty
    # based on the recipe's cooking time
    # and the number of ingredients
    def calculate_difficulty(self):
        ingredients_count = len(self.ingredients.split(", "))
        if self.cooking_time < 10:
            if ingredients_count < 4:
                self.difficulty = "Easy"
            else:
                self.difficulty = "Medium"
        elif self.cooking_time >= 10:
            if ingredients_count < 4:
                self.difficulty = "Intermediate"
            else:
                self.difficulty = "Hard"

    # Returns the recipe's ingredients as list
    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        else:
            return self.ingredients.split(", ")


# Creates the defined model(s) as a new table
# in the database
Base.metadata.create_all(engine)

# Main Operations


# Creates a new recipe
def create_recipe():
    # Collect recipe name
    while True:
        name = input("Enter your recipe's name: ")
        if len(name) > 50:
            print("Error: Name too long - max 50 characters. Please try again.")
        elif not name.isalpha():
            print(
                "Error: Name must contain only alphabethical characters. Please try again."
            )
        else:
            break

    # Collect cooking time
    while True:
        cooking_time = input("Enter a cooking time in minutes: ")
        if not cooking_time.isnumeric():
            print("Error: Cooking time must be a numeric value. Please try again.")
        else:
            cooking_time = int(cooking_time)
            break

    # Collect ingredients
    ingredients = []
    while True:
        n = input("How many ingredients you'd like to enter?: ")
        if not n.isnumeric():
            print("Error: You must enter a number. Please try again.")
        else:
            n = int(n)
            break

    print(
        "Sounds good! You'll enter your ingredients one by one now.\nPlease remember that the resulting ingredients list must not exceed 255 characters (around 35-50 words)."
    )
    for loop in range(1, n + 1):
        ingredient = input("Enter ingredient " + str(loop) + ": ")
        ingredient = ingredient.strip().lower().capitalize()
        ingredients.append(ingredient)

    ingredients_str = ", ".join(ingredients)

    # Create new Recipe object
    recipe_entry = Recipe(
        name=name, cooking_time=cooking_time, ingredients=ingredients_str
    )

    # Calculate difficulty for the new recipe
    recipe_entry.calculate_difficulty()

    session.add(recipe_entry)
    session.commit()
    print("Recipe added successfully!")
    print()


# Displays all recipes
def view_all_recipes():
    # Retrieve the list of recipes from the database
    all_recipes = session.query(Recipe).all()

    # If any recipes returned print them out
    # else inform the user that there are
    # no entries and exit the function
    if len(all_recipes):
        for recipe in all_recipes:
            print(recipe)
    else:
        print("No recipes found.")
        return None


# Searches for a recipe by ingredients
def search_by_ingredients():
    recipes_count = session.query(Recipe).count()
    if not recipes_count:
        print("No recipes found. Add some recipes first.")
        return None

    # Fetch the ingredients column
    results = session.query(Recipe.ingredients).all()

    # Initialize all ingredients list
    all_ingredients = []

    # Add unique ingredients to the list
    for ingredients_str in results:
        ingr_list = ingredients_str[0].split(", ")
        for ingredient in ingr_list:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)

    # Display the ingredients list to the user
    for index, ingredient in enumerate(all_ingredients):
        print(str(index) + ". " + ingredient)

    print()

    selected_ingr_indices_str = input(
        "Type the numbers of the ingredients to be searched for, separated by spaces: "
    )
    selected_ingr_indices_list = selected_ingr_indices_str.split()

    # Validate selected ingredients
    # Check if the input can be converted to int (is numbers)
    try:
        selected_ingr_indices = [int(i) for i in selected_ingr_indices_list]
    except ValueError:
        print("Error: Only numbers are allowed.")
        return None

    # Check if the ingredients indices are valid
    if any(i < 0 or i >= len(all_ingredients) for i in selected_ingr_indices):
        print(
            "Error: Invalid selection. Enter numbers from the displayed options only."
        )
        return None

    # Make a list of ingredients to search for
    search_ingredients = []
    for index in selected_ingr_indices:
        search_ingredients.append(all_ingredients[index])

    # Create conditions to search in the database
    conditions = []
    for search_ingredient in search_ingredients:
        like_term = "%" + search_ingredient + "%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Fetch and display matched recipes
    matched_recipes = session.query(Recipe).filter(*conditions).all()
    [print(recipe) for recipe in matched_recipes]


# Edits a recipe
def edit_recipe():
    # Check if any recipe is in the database
    recipes_count = session.query(Recipe).count()
    if not recipes_count:
        print("No recipes found.")
        return None

    # Retrieve recipes' id and name, print out
    results = session.query(Recipe.id, Recipe.name).all()
    for recipe in results:
        print(str(recipe.id) + ". " + recipe.name)
    print()

    # Get user's selection and validate
    selected_recipe_id = input("Enter the ID of the recipe you'd like to edit: ")
    if not selected_recipe_id.isnumeric() or int(selected_recipe_id) not in [
        recipe.id for recipe in results
    ]:
        print(
            "Error: You must select a recipe by its ID. See the listed recipes with their respective IDs and try again."
        )
        return None

    # Retrieve the recipe to be edited
    selected_recipe_id = int(selected_recipe_id)
    recipe_to_edit = session.query(Recipe).filter(Recipe.id == selected_recipe_id).one()

    # Display the recipe's name, ingredients, and cooking time
    print()
    print("Recipe's details:")
    print("1. Name: " + recipe_to_edit.name)
    print("2. Cooking Time (Min): " + str(recipe_to_edit.cooking_time))
    print("3. Ingredients: " + recipe_to_edit.ingredients)
    print()

    # Ask the user which attribute to edit
    attribute_to_edit_sel = input(
        "Select the attribute you'd like to edit by its number - 1, 2, or 3: "
    )
    if not attribute_to_edit_sel in ["1", "2", "3"]:
        print(
            "Error: Incorrect input. You must select one of the three attributes by its number."
        )
        return None

    # Change the recipe's name
    if attribute_to_edit_sel == "1":
        new_name = input("Enter the new name: ")
        if len(new_name) > 50 or not new_name.isalpha():
            print(
                "Error: The name must have max 50 characters and contain only alphabetical characters."
            )
            return None
        recipe_to_edit.name = new_name

    # Change the recipe's cooking time
    if attribute_to_edit_sel == "2":
        new_cooking_time = input("Enter the new cooking time in minutes: ")
        if new_cooking_time < 0 or not new_cooking_time.isnumeric():
            print("Error: The cooking time must be a positive numeric value.")
            return None
        recipe_to_edit.cooking_time = new_cooking_time
        recipe_to_edit.calculate_difficulty()

    # Change the recipe's ingredients
    if attribute_to_edit_sel == "3":
        new_ingredients = []
        n = input("How many ingredients you'd like to enter?: ")
        if int(n) < 1 or not n.isnumeric():
            print("Error: You must enter a postive numeric value.")
            return None

        n = int(n)

        print(
            "Sounds good! You'll enter your ingredients one by one now.\nPlease remember that the resulting ingredients list must not exceed 255 characters (around 35-50 words)."
        )
        for loop in range(1, n + 1):
            ingredient = input("Enter ingredient " + str(loop) + ": ")
            ingredient = ingredient.strip().lower().capitalize()
            new_ingredients.append(ingredient)

        new_ingredients_str = ", ".join(new_ingredients)
        recipe_to_edit.ingredients = new_ingredients_str
        recipe_to_edit.calculate_difficulty()

    session.commit()
    print()
    print("Recipe updated successfully.")


# Deletes a recipe
def delete_recipe():
    # Check if any recipe is in the database
    recipes_count = session.query(Recipe).count()
    if not recipes_count:
        print("No recipes found.")
        return None

    # Retrieve recipes' id and name, print out
    results = session.query(Recipe.id, Recipe.name).all()
    for recipe in results:
        print(str(recipe.id) + ". " + recipe.name)
    print()

    # Get user's selection and validate
    selected_recipe_id = input("Enter the ID of the recipe you'd like to delete: ")
    if not selected_recipe_id.isnumeric() or int(selected_recipe_id) not in [
        recipe.id for recipe in results
    ]:
        print(
            "Error: You must select a recipe by its ID. See the listed recipes with their respective IDs and try again."
        )
        return None

    # Retrieve the recipe to be deleted
    selected_recipe_id = int(selected_recipe_id)
    recipe_to_delete = (
        session.query(Recipe).filter(Recipe.id == selected_recipe_id).one()
    )

    # Deletion confirmation
    user_choice = input(
        "Do you want to delete the recipe "
        + str(recipe_to_delete.id)
        + " "
        + recipe_to_delete.name
        + "? Enter y or n: "
    ).lower()

    # Perform final action
    if user_choice == "y":
        session.delete(recipe_to_delete)
        session.commit()
        print("The recipe has been deleted.")
        print()
    elif user_choice == "n":
        print("Cancelling deletion.")
        print()
        return None
    else:
        print("Error: Incorrect input. Enter either 'y' or 'n'.")
        return None


# Displays the main menu
# Calls functions based on the user's choice
def main_menu():
    choice = ""
    while choice != "quit":
        print()
        print("############# MAIN MENU #############")
        print()
        print("## Pick an option:")
        print("-------------------------------------")
        print("   1. Create a new recipe")
        print("   2. View all recipes")
        print("   3. Search for recipes by ingredients")
        print("   4. Edit a recipe")
        print("   5. Delete a recipe")
        print()
        print("## Type 'quit' to exit the application.")
        print()
        choice = input("## Your choice: ")

        if choice == "1":
            print()
            create_recipe()
        elif choice == "2":
            print()
            view_all_recipes()
        elif choice == "3":
            print()
            search_by_ingredients()
        elif choice == "4":
            print()
            edit_recipe()
        elif choice == "5":
            print()
            delete_recipe()
        elif choice == "quit":
            print()
            print("App closed. Goodbye!")
            print()
        else:
            print(
                "Your choice doesn't look correct. Please pick a number from the provided menu or type 'quit' to quit the app."
            )

    # Closes the session and engine
    session.close()
    engine.dispose()


main_menu()
