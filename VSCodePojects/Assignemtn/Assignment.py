import random

# Initialize empty dictionary to store flashcards
flashcards = {}
print ("Welcome to Hunter's Flashcard Program")
# Main program loop
while True:
    # Display menu options
    print("\n=== Flashcard Program ===")
    print("1. Add a flashcard")
    print("2. Delete a flashcard")
    print("3. Review flashcards")
    print("4. Quiz mode")
    print("5. Exit")
    
    # Get user choice
    choice = input("\nEnter your choice (1-5): ")
    
    # Option 1: Add a flashcard
    if choice == "1":
        term = input("Enter the term: ")
        definition = input("Enter the definition: ")
        flashcards[term] = definition
        print("Flashcard added successfully!")
    
    # Option 2: Delete a flashcard
    elif choice == "2":
        if flashcards:
            print("\nAvailable terms:")
            for term in flashcards:
                print(f"- {term}")
            term_to_delete = input("\nEnter the term to delete: ")
            if term_to_delete in flashcards:
                del flashcards[term_to_delete]
                print("Flashcard deleted successfully!")
            else:
                print("Term not found!")
        else:
            print("No flashcards to delete!")
    
    # Option 3: Review flashcards
    elif choice == "3":
        if flashcards:
            print("\nAll Flashcards:")
            for term, definition in flashcards.items():
                print(f"\nTerm: {term}")
                print(f"Definition: {definition}")
        else:
            print("No flashcards to review!")
    
    # Option 4: Quiz mode
    elif choice == "4":
        if flashcards:
            # Randomly select a term
            random_term = random.choice(list(flashcards.keys()))
            print(f"\nTerm: {random_term}")
            user_answer = input("Enter the definition: ")
            
            # Check if answer is correct
            if user_answer.lower() == flashcards[random_term].lower():
                print("Correct!")
            else:
                print(f"Incorrect. The correct definition is: {flashcards[random_term]}")
        else:
            print("No flashcards available for quiz!")
    
    # Option 5: Exit program
    elif choice == "5":
        print("Thank you for using the Flashcard Program!")
        break
    
    # Handle invalid input
    else:
        print("Invalid choice! Please select a number between 1 and 5.")