import sqlite3

con = sqlite3.connect("flashcards.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS flashcards (id INTEGER PRIMARY KEY, front TEXT, back TEXT)")
con.commit()
class Flashcard:
    def __init__(self, front, back):
        self.front = front
        self.back = back

    def __str__(self) -> str:
        return f"Front: {self.front}\nBack: {self.back}"

def add_flashcard(front, back):
    cur.execute("INSERT INTO flashcards (front, back) VALUES (?, ?)", (front, back))
    con.commit()

def get_flashcards():
    cur.execute("SELECT id, front, back FROM flashcards")
    rows = cur.fetchall()
    return [Flashcard(row[1], row[2]) for row in rows], rows

def remove_flashcard(card_id):
    cur.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
    con.commit()

score = 0

while True:
    response = input("Actions: study, add, remove, quit\n")

    if response == "add":
        front = input("Front of card: ")
        back = input("Back of card: ")
        add_flashcard(front, back)
        print("Flashcard added!")

    elif response == "study":
        cards, raw_cards = get_flashcards()
        if not cards:
            print("No flashcards available.")
            continue

        for i in cards:
            print(i.front)
            answer = input("Answer: ")
            if answer == i.back:
                score += 1
            while answer != i.back:
                answer = input("Incorrect, try again: ")
            print("Correct!")
        print("Your score was ", score, "/", len(cards))

    elif response == "remove":
        cards, raw_cards = get_flashcards()
        if not cards:
            print("No flashcards available.")
            continue

        for card in raw_cards:
            print(f"{card[0]}: Front: {card[1]}, Back: {card[2]}")
        
        try:
            card_id = int(input("Enter the ID of the flashcard you want to remove: "))
            remove_flashcard(card_id)
            print("Flashcard removed!")
        except ValueError:
            print("Invalid ID. Please try again.")

    elif response == "quit":
        print("Goodbye!")
        break

    else:
        print("Invalid action. Please try again.")

con.close()