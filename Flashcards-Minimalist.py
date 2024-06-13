import pandas as pd
import random
import datetime
import os

# Welcome message
print("Vitajte v aplikácii Flashcards Minimalist, ide o náhradu aplikácie Quizlet\n")
print("")


# Specify the file paths
flashcards_file_path = "flashcards.csv"
incorrect_file_path = "incorrect.txt"

# Function to load flashcards from a CSV file
def load_flashcards():
    try:
        flashcards = pd.read_csv(flashcards_file_path)
        return flashcards
    except FileNotFoundError:
        print(f"Súbor '{flashcards_file_path}' nebol nájdený.")
        return None
    except Exception as e:
        print(f"Vyskytla sa chyba: {e}")
        return None

# Function to wait for any keypress (Enter)
def wait_for_any_keypress():
    input()


# Function to prompt the user if they know the answer
def prompt_user_knows_answer():
    while True:
        user_response = input("Vieš odpoveď? ('1' - áno, '0' - nie): ").strip()
        if user_response == "1":
            return 1
        elif user_response == "0":
            return 0
        else:
            print("Neplatný vstup. Prosím, zadajte '1' pre áno alebo '0' pre nie.")

# Main function
def main():
    flashcards = load_flashcards()
    if flashcards is None:
        return  # Exit the program

    total_flashcards = len(flashcards)
    max_flashcards = min(total_flashcards, int(input(f"Zadajte maximálny počet kartičiek, maximum je {total_flashcards}: ")))

    if max_flashcards < 1:
        print("Maximálny počet kartičiek musí byť aspoň 1.")
        return  # Exit the program
    print("------------------------------------------------------------")
    total_responses = 0
    yes_responses = 0
    score = 0  # Initialize the score

    now = datetime.datetime.now()

    with open(incorrect_file_path, "w", encoding="utf-8") as result_file:
        result_file.write(f"Dátum a čas: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        result_file.write("Nesprávne odpovede:\n")
        result_file.write("------------------------------------------------------------\n")
        
    flashcards_indices = random.sample(range(total_flashcards), max_flashcards)
    flashcards_to_show = flashcards.iloc[flashcards_indices]

    for index, row in flashcards_to_show.iterrows():
        front, back, source = row["Front"], row["Back"], row.get("Source", "")
        print("\n" + front)
        wait_for_any_keypress()
        print(back)

        if source:
            print("\nSource: " + source)
        print("\n------------------------------------------------------------")
        user_knew_answer = prompt_user_knows_answer()
        total_responses += 1
        print("\n------------------------------------------------------------")
        # Update the score based on user's response
        if user_knew_answer == 1:
            score += 1

        if not user_knew_answer:
            with open(incorrect_file_path, "a", encoding="utf-8") as incorrect_file:
                incorrect_file.write(f"{front}\nSprávna odpoveď: {back}\n")
                if source:
                    incorrect_file.write(f"Zdroj: {source}\n")  # Write the source when the answer is incorrect
                incorrect_file.write("------------------------------------------------------------\n")  # Add a separator whether there is a source or not
                yes_responses += 1

    print("Nesprávne odpovede boli uložené do súboru 'incorrect.txt'.")
    print(f"Skóre: {score}/{total_responses}")  # Display the score

    if total_responses > 0:
        if yes_responses > 0:
            percentage = ((total_responses - yes_responses) / total_responses) * 100
            formatted_percentage = f"{percentage:.1f}".rstrip('0').rstrip('.')
            print(f"Dosiahli ste {formatted_percentage}%")
        else:
            print("Dosiahli ste 100%")
    else:
        print("No responses found in the incorrect answers file.")



    if os.path.exists(incorrect_file_path):
        os.system(f"notepad {incorrect_file_path}")  # Open the incorrect answers file in Notepad
    else:
        print(f"The file '{incorrect_file_path}' does not exist.")

if __name__ == "__main__":
    main()
