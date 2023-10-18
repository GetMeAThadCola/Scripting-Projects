
Recipe Generator

This Python application is a Recipe Generator that allows users to discover new recipes based on keywords or ingredients they provide. It leverages the Edamam Recipe Search API to fetch random recipes tailored to the user's input. The application features a user-friendly graphical user interface (GUI) built with tkinter, making it easy for users to interact with and find recipe inspiration.

Features:

User-Friendly GUI: The application provides a simple and intuitive interface for users to enter keywords or ingredients.

Random Recipe Generation: Users can input a keyword or ingredient, and the application will fetch a random recipe that matches their input.

Copy Recipe URL: The generated recipe includes a "Copy URL" button, allowing users to copy the recipe URL to their clipboard for easy sharing or reference.

Usage:

Enter a keyword or ingredient in the input field.
Click the "Generate Recipe" button.
The application will fetch a random recipe and display its title and URL.
Use the "Copy URL" button to copy the recipe URL to your clipboard.



Requirements:

Python 3.x
http.client for making HTTP requests
tkinter for the graphical user interface
pyperclip for copying URLs to the clipboard (optional)
API: Edamam Recipe Search API