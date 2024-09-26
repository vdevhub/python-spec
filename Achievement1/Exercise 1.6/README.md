# Databases in Python - MySQL
Instead of working with standard files to store data, Python supports working with databases which are more structured and more robust for handling data. In this version of the Recipe app, a local MySQL database is used to create a table with recipes and their respective attributes. All queries are executed via a dedicated connection to the database initiated through `mysql.connector` module. A cursor object is then initiated through the connection object.

## Details
1. When the app is launched, the main menu is printed on the screen that consists of 4 options: create a recipe, search for a recipe by ingredient, update a recipe, and delete a recipe.
2. The menu is being displayed until the user types 'quit' in the terminal.
3. For the recipe creation, the user is asked to provide their recipe name, cooking time, and ingredients through a series of prompts. Difficulty is calculated based on the cooking time and the number of ingredients.
4. For the recipe search, the user is provided a list of unique ingredients distilled from the database and asked to select the number of the ingredient to be searched for. Once provided, the app looks for such recipes and prints them out on the screen once found.
5. For the recipe update, the user is provided a list of all recipes and asked to select the number of the recipe to update. Then they are prompted to enter the column name to update, and the new value. If a change is made to the cooking time or the ingredients, the recipe's difficulty is automatically recalculated and updated in the database as well.
6. For the recipe deletion, the user is provided a list of all recipes and asked to select the number of the recipe to be deleted. Once selected, the recipe is removed from the database.

## Database Operations
- After every update, changes are committed to the database using the connection's method `commit()`.
- When the user terminates the program, a commit is executed again and the connection is closed using the connection's method `close()`.
- To search for recipes by ingredient, the `LIKE` keyword is used with the `%` operator as ingredients are stored as a string in the database. This allows the query to look for the ingredient within the string instead of comparing the whole string against the searched ingredient which would always result in no recipe found.
