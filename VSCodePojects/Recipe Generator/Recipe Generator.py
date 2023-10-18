import http.client
import json
import random
import tkinter as tk
from tkinter import messagebox
from urllib.parse import quote
import pyperclip

# Replace with your Edamam API credentials
APP_ID = 'fd2eae03'
APP_KEY = 'a47fa08895edfb55ad21242eaa06be39'

def get_recipe(keyword):
    # Encode the keyword to ensure it's URL-safe
    encoded_keyword = quote(keyword)
    
    connection = http.client.HTTPSConnection("api.edamam.com")
    endpoint = f"/search?q={encoded_keyword}&app_id={APP_ID}&app_key={APP_KEY}"

    connection.request("GET", endpoint)
    response = connection.getresponse()

    if response.status == 200:
        data = json.loads(response.read().decode('utf-8'))
        if 'hits' in data and data['hits']:
            random_recipe = random.choice(data['hits'])
            recipe = random_recipe['recipe']
            return recipe
        else:
            return "No recipes found for the keyword."
    else:
        return "Failed to retrieve a recipe."

def copy_recipe_url(url):
    pyperclip.copy(url)
    messagebox.showinfo("Copy URL", "Recipe URL has been copied to your clipboard.")

def generate_recipe():
    keyword = keyword_entry.get()
    recipe = get_recipe(keyword)
    
    if isinstance(recipe, dict):
        recipe_url = recipe['url']
        messagebox.showinfo("Random Recipe", f"Title: {recipe['label']}\nURL: {recipe_url}")
        copy_button = tk.Button(root, text="Copy URL", command=lambda: copy_recipe_url(recipe_url))
        copy_button.pack()
    else:
        messagebox.showinfo("Recipe Not Found", recipe)

# Create a GUI window
root = tk.Tk()
root.title("Recipe Generator")

# Create and configure widgets
keyword_label = tk.Label(root, text="Enter a Keyword or Ingredient:")
keyword_label.pack()

keyword_entry = tk.Entry(root, width=40)
keyword_entry.pack()

generate_button = tk.Button(root, text="Generate Recipe", command=generate_recipe)
generate_button.pack()

# Start the GUI application
root.mainloop()
