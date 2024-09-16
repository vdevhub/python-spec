# File Handling in Python

Python offers multiple ways of file handling with text files being the most simple and binary files serving to store more complex structures. Here, the pickle module is used to work with binary files both to read and load data. 

Error handling (try-except-else-finally) is implemented to ensure reading and writing binary files doesn't cause the script to terminate unexpectedly or crash.

## Details
### Recipe Input
1. Pickle is imported to the script due to writing to binary files.
2. The script takes input from the user about how many recipes they want to enter.
3. For each recipe, the user is asked to provide its name, cooking time in minutes, and list of ingredients.
4. The difficulty of each recipe is calculated from its cooking time and the number of ingredients and the resulting value (`Easy`, `Medium`, `Intermediate`, or `Hard`) is stored with the recipe.
5. Recipes are then stored in a `recipes_list` while all unique ingredients are appended to an `all_ingredients` list.
6. Both lists are compiled into a dictionary which is then stored as a binary file locally.

### Recipe Search
1. Pickle is imported to the script due to reading binary files.
2. The script asks the user what binary file they store their recipes in.
3. If the file is found, the data from it is loaded and unpacked into 2 lists: `recipes_list`, `all_ingredients`.
4. All ingredients are printed on the screen as a numbered list.
5. The user is prompted to enter the number of the ingredient they want to search recipes for.
6. If they enter a number from the list, the respective recipes are printed on the screen.
7. If the input is incorrect, the user is notified and the script terminates.
8. If the file with recipes is not found, the user is also notified and the script terminates.
