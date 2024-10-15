import sqlite3
import random

# Connect to the database and create flashcards table with level and set_id fields
con = sqlite3.connect("flashcards.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS flashcards (
    id INTEGER PRIMARY KEY,
    front TEXT,
    back TEXT,
    level INTEGER DEFAULT 1,
    set_id INTEGER DEFAULT 1
)""")
con.commit()

# Class to represent a flashcard
class Flashcard:
    def __init__(self, front, back, level, set_id):
        self.front = front
        self.back = back
        self.level = level
        self.set_id = set_id

    def __str__(self) -> str:
        return f"Front: {self.front}\nBack: {self.back}\nLevel: {self.level}\nSet ID: {self.set_id}"

# Add a new flashcard to the database
def add_flashcard(front, back, set_id=1):
    cur.execute("INSERT INTO flashcards (front, back, level, set_id) VALUES (?, ?, 1, ?)", (front, back, set_id))
    con.commit()

# Retrieve flashcards from the database
def get_flashcards(set_id=1):
    cur.execute("SELECT id, front, back, level FROM flashcards WHERE set_id = ?", (set_id,))
    rows = cur.fetchall()
    return [Flashcard(row[1], row[2], row[3], set_id) for row in rows], rows

# Remove a flashcard by ID
def remove_flashcard(card_id):
    cur.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
    con.commit()

# Update the level of a flashcard
def update_flashcard_level(card_id, new_level):
    cur.execute("UPDATE flashcards SET level = ? WHERE id = ?", (new_level, card_id))
    con.commit()

# Allow users to study flashcards, using spaced repetition
def study(set_id=1):
    cards, raw_cards = get_flashcards(set_id)
    if not cards:
        print("No flashcards available.")
        return

    # Group flashcards by level for spaced repetition
    flashcards_by_level = {1: [], 2: [], 3: []}
    for card in raw_cards:
        if card[3] <= 3:  # Limit to level 3 for simplicity
            flashcards_by_level[card[3]].append(card)

    score = 0
    for level in [1, 2, 3]:  # Show lower-level cards more frequently
        if flashcards_by_level[level]:
            card = random.choice(flashcards_by_level[level])
            print(f"Level {level}: {card[1]}")
            answer = input("Answer: ")

            if answer == card[2]:
                print("Correct!")
                score += 1
                if card[3] < 3:  # If not already at max level
                    update_flashcard_level(card[0], card[3] + 1)  # Move card to next level
            else:
                print("Incorrect, try again.")
                while answer != card[2]:
                    answer = input("Incorrect, try again: ")
                print("Correct!")
                if card[3] > 1:  # Move card back one level
                    update_flashcard_level(card[0], card[3] - 1)

    print("Your score was ", score, "/", len(cards))

# Main program loop
def main():
    while True:
        response = input("Actions: study, add, remove, change_set, quit\n")

        if response == "add":
            front = input("Front of card: ")
            back = input("Back of card: ")
            set_id = int(input("Enter set ID (default is 1): ") or 1)
            add_flashcard(front, back, set_id)
            print("Flashcard added!")

        elif response == "study":
            set_id = int(input("Enter set ID (default is 1): ") or 1)
            study(set_id)

        elif response == "remove":
            set_id = int(input("Enter set ID (default is 1): ") or 1)
            cards, raw_cards = get_flashcards(set_id)
            if not cards:
                print("No flashcards available.")
                continue

            for card in raw_cards:
                print(f"{card[0]}: Front: {card[1]}, Back: {card[2]}, Level: {card[3]}")
            
            try:
                card_id = int(input("Enter the ID of the flashcard you want to remove: "))
                remove_flashcard(card_id)
                print("Flashcard removed!")
            except ValueError:
                print("Invalid ID. Please try again.")

        elif response == "change_set":
            print("Changing the active flashcard set. You can now add or study cards from a different set.")

        elif response == "quit":
            print("Goodbye!")
            break

        else:
            print("Invalid action. Please try again.")

    con.close()

if __name__ == "__main__":
    main()