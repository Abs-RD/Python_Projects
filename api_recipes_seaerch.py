print('\033c')


import requests
import json
from termcolor import colored
from tabulate import tabulate


# global variables
HEALTH_LABELS = ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Alcohol-Free', 'Nut-Free']


# function for recipe search
def recipe_search(ingredient):
    app_id = '816481c4'
    app_key = 'd78e6f927c479252b36011214e9708ea'
    result = requests.get(f'https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}')
    data = result.json()

    # Check if 'hits' is in the data
    if 'hits' in data:
        return data['hits']
    else:
        return []
    

# function to save results to a file named "recipe.txt"
def save_to_file(results):
    with open('recipes.txt', 'w') as file:
        for result in results:
            recipe = result['recipe']
            file.write(recipe['label'] + '\n')
            file.write(recipe['url'] + '\n')       

        # Check if 'health labels' exists in the recipe data and write them
            if 'healthLabels' in recipe and recipe['healthLabels']:
                health_labels = ', '.join([label for label in recipe['healthLabels'] if label in HEALTH_LABELS])
                if health_labels:  
                    file.write(f"Health Labels: {health_labels}\n")
            file.write('\n')

    print(colored("\nRecipes saved to recipes.txt", "green"))


# function to save the chosen recipe to a new file named "chosen_recipe.txt"
def save_selected_to_file(recipe, nutrition_info = None):
    with open('chosen_recipe.txt', 'w') as file:
        
        # Writing the label
        file.write(f"Recipe Name: {recipe['label']}\n\n")

        # Writing the number of servings
        file.write(f"Number of Servings: {int(recipe['yield'])}\n")

        # Extracting and writing total weight
        total_weight = nutrition_info.get('totalWeight', 0)
        file.write(f"Total Weight: {total_weight:.2f} g\n\n")

        # Check if 'diet labels' exists in the recipe data and writing them to file
        if 'dietLabels' in recipe and recipe['dietLabels']:
            file.write("Diet Labels:\n")
            for label in recipe['dietLabels']:
                file.write(f"- {label}\n")
            file.write("\n")

        # Check if nutrition_info is provided and writing it to file
        if nutrition_info:
            file.write("Nutrition Analysis:\n")

            # Extracting nutritional components
            total_nutrients = nutrition_info.get('totalNutrients', {})
            calories = nutrition_info.get('calories', 0)
            carbohydrates = total_nutrients.get('CHOCDF', {}).get('quantity', 0)
            fat = total_nutrients.get('FAT', {}).get('quantity', 0)
            cholesterol = total_nutrients.get('CHOLE', {}).get('quantity', 0)
            
            # Writing nutritional components to file
            file.write(f"- Total Calories: {calories} kcal\n")
            file.write(f"- Total Carbohydrates: {carbohydrates:.2f} g\n")
            file.write(f"- Total Fat: {fat:.2f} g\n")
            file.write(f"- Cholesterol: {cholesterol:.2f} mg\n\n")

        # Writing the list of ingredients
        file.write("\nIngredients:\n")
        for ingredient in recipe['ingredientLines']:
            file.write(f"- {ingredient}\n")

        # Writing the URL
        file.write("\n\nFor full recipe and preparation go to " + recipe['url'] + "\n")
           

    print(colored("\nSelected recipe and nutrition analysis saved to chosen_recipe.txt\n", "light_yellow"))


# function asking user if they want to select a specific recipe from the printed list
def ask_for_choice(results):
    
    while True:
        choice = input("Would you like to select a recipe from the list? (yes/no) - ").strip().lower()
        
        if choice == "yes":
            print(colored("\nLIST OF RECIPES", "cyan", attrs=['underline'])) 
            for index, result in enumerate(results, 1):
                print(f"{index}. {result['recipe']['label']}")

            while True:
                try:
                    selected = int(input("\nEnter the number of the recipe you want to choose: "))
                    if 1 <= selected <= len(results):
                        chosen_recipe = results[selected-1]['recipe']
                        return chosen_recipe
                    else:
                        print(f"Invalid choice. Please choose a number between 1 and {len(results)}.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == "no":
            print(colored("\nThank you! Have a great day!👋\n", "light_yellow"))
            return None
        else:
            print(colored("\nInvalid choice. Please enter 'yes' or 'no'", "dark_grey", attrs=['bold']))


# function to get 'traffic_light_color' nutrient labelling system
def get_traffic_light_color(value, nutrient):
    thresholds = {
        "total_fat": (3, 17.5),
        "saturates": (1.5, 5),
        "sugars": (5, 22.5),
        "salt": (0.3, 1.5),
    }
    
    lower, upper = thresholds[nutrient]
    if value > upper:
        return '\033[91m' 
    elif value > lower:
        return '\033[93m' 
    else:
        return '\033[92m' 
    

# function to output nutrition analysis for chosen recipe
def analyze_recipe_nutrition(recipe):
    # define the API endpoint and credentials
    api_url = 'https://api.edamam.com/api/nutrition-details'
    nutrition_app_id = '6ca583ba'  
    nutrition_app_key = '890338c1300e2aae83f828cbba387098'
    
    # set headers and parameters for the request
    headers = {'Content-Type': 'application/json'}
    params = {'app_id': nutrition_app_id, 'app_key': nutrition_app_key}
    data = json.dumps(recipe)
    
    response = requests.post(api_url, headers=headers, params=params, data=data)
    
    # check if the request was successful (HTTP Status Code 200)
    if response.status_code == 200:
        nutrition_info = response.json()
        print(colored("\n\nNutrition Analysis Per 100g Serving:", 'cyan'))

        # Extracting and printing total weight
        total_weight = nutrition_info.get('totalWeight', 0)
        print(f"Total Weight (of an adult's reference intake): {total_weight:.2f} g\n")


        # Extracting and printing nutritional components
        total_nutrients = nutrition_info.get('totalNutrients', {})
        
        # Per 100g serving
        calories = nutrition_info.get('calories', 0)
        fat = total_nutrients.get('FAT', {}).get('quantity', 0) / 100                       
        saturated_fat = total_nutrients.get('FASAT', {}).get('quantity', 0) / 100           
        sugars = total_nutrients.get('SUGAR', {}).get('quantity', 0) / 100                 
        salt = total_nutrients.get('NA', {}).get('quantity', 0) / 1000             
        protein = total_nutrients.get('PROCNT', {}).get('quantity', 0)
        carbohydrates = total_nutrients.get('CHOCDF', {}).get('quantity', 0)
        fiber = total_nutrients.get('FIBTG', {}).get('quantity', 0)


        # Using the function to get color codes
        fat_color = get_traffic_light_color(fat, "total_fat")
        saturated_fat_color = get_traffic_light_color(saturated_fat, "saturates")
        sugars_color = get_traffic_light_color(sugars, "sugars")
        salt_color = get_traffic_light_color(salt, "salt")

   
    # Displaying the extracted nutritional information in a table
        # Organizing data into a table
        nutrient_names = ["Calories", "Fat", "Saturates", "Sugars", "Salt", "Protein", "Carbohydrates", "Fiber"]
        nutrient_values = [
            f"{calories} kcal",
            f"{fat_color}{fat:.2f} g\033[0m",
            f"{saturated_fat_color}{saturated_fat:.2f} g\033[0m",         
            f"{sugars_color}{sugars:.2f} g\033[0m",
            f"{salt_color}{salt:.2f} g\033[0m",
            f"{protein:.2f} g",
            f"{carbohydrates:.2f} g",
            f"{fiber:.2f} g"
        ]
        
        # Combining names and values into a table
        table = [nutrient_names, nutrient_values]

        # Print the table using tabulate with the 'simple_outline' table format
        print(tabulate(table, tablefmt='simple_outline', headers='firstrow'))
        
    # Return the parsed JSON data
        return nutrition_info
    else:
        # Print an error message if the request was not successful
        print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
        print(f"Message: {response.text}")
        # Return None to indicate that the function did not successfully retrieve the data
        return None


# function to ask user for an ingredient, searches for recipes and prints them out
def run():
    print(colored("Are you ready to have fun cooking? Provide an ingredient and see the fun recipes you can use!", attrs=['bold']))   
    
    # User inputs an ingredient
    ingredient = input('\nEnter an ingredient: ')
    print()
    
    # Fetch and display recipes using the ingredient
    results = recipe_search(ingredient)
    if not results:
        print("No recipes found for that ingredient.\n")
        return

    # printing list of recipes related to entered ingredient
    for index, result in enumerate(results, start=1):
        recipe = result['recipe']
        print(colored(f"{index}. {recipe['label']}", "cyan"))                             
        print(recipe['url'])                                               
                                             

        # only print if there are any health labels present
        if 'healthLabels' in recipe and recipe['healthLabels']:
            health_labels = ', '.join([label for label in recipe['healthLabels'] if label in HEALTH_LABELS])
            if health_labels:                                               
                print(colored("Health Labels: ", "light_magenta") + health_labels)
       
        print()


    # Save recipe results to a file
    save_to_file(results)


    # Ask the user if they want to select a specific recipe
    selected_recipe = ask_for_choice(results)
    
    if selected_recipe:
        print("You chose: " + colored(f"{selected_recipe['label']}", "light_magenta"))
        sample_recipe = {
            "title": selected_recipe['label'],
            "ingr": selected_recipe['ingredientLines']
        }
        nutrition_info = analyze_recipe_nutrition(sample_recipe)
        

        # Save the selected recipe and its nutritional information
        save_selected_to_file(selected_recipe, nutrition_info)

run()

