# Python Data Structures

This part documents Python data type considerations and selection for a recipe app using a command line interface.

## Details
1. A single recipe is a `dictionary` data type with the following keys:
   - `name (str)`: name of the recipe
   - `cooking_time (int)`: cooking time in minutes
   - `ingredients (list)`: ingredients, each of the str data type
  
   - *Reason*: A dictionary is suitable for a single recipe object as it stores data in key-value pairs which helps to describe different values as opposed to storing just values without meaning. Additionally, a dictionary can be easily updated and expanded. The ingredients key is a nested list because each of the values is going to be the same type (String), these don't need specific descriptive keys, and a list will support easy searching and modification of the ingredients too.
  
2. The outer structure called `all_recipes` is a list containing all recipe objects.

   - *Reason*: A list is suitable for the all_recipes object as it can be easily modified and new recipes can easily be added as well as removed. This structure is also sequential and allows for sorting, searching, and selection of elements.
