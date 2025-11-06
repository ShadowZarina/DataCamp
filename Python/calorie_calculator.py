import json  # Import the json module to work with JSON files

# Open the nutrition.json file in read mode and load its content into a dictionary
with open('nutrition.json', 'r') as json_file:
    nutrition_dict = json.load(json_file)  # Load the JSON content into a dictionary
    
# Display the first 3 items of the nutrition dictionary
list(nutrition_dict.items())[:3]

'''
Sample Output of Nutrition Dict

[('Cornstarch',
  {'calories': 381,
   'total_fat': 0.1,
   'protein': 0.26,
   'carbohydrate': 91.27,
   'sugars': 0.0}),
 ('Nuts, pecans',
  {'calories': 691,
   'total_fat': 72.0,
   'protein': 9.17,
   'carbohydrate': 13.86,
   'sugars': 3.97}),
 ('Eggplant, raw',
  {'calories': 25,
   'total_fat': 0.2,
   'protein': 0.98,
   'carbohydrate': 5.88,
   'sugars': 3.53})]
'''
