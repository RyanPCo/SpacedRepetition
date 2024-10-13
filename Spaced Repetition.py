import sqlite3
class Flashcard:
    def __init__(self, front, back):
        self.front = front
        self.back = back

    def __str__(self) -> str:
        return f"Front: {self.front}\nBack: {self.back}"
    
cards = []
score = 0

while True:
    response = input("Actions: study, add, remove\n")

    if response == "add":
        front = input("Front of card: ")
        back = input("Back of card: ")
        cards.append(Flashcard(front, back))
    elif response == "study":
        for i in cards:
            print(i.front)
            answer = input("Answer: ")
            if answer == i.back:
                score = score + 1
            while answer != i.back:
                answer = input("Incorrect, try again: ")
            print("Correct!")
        print("Your score was ", score, "/", len(cards))
    elif response == "remove":
        for i in cards:
            print(i)
        answer = input(f"Here is a list of your flashcards, which one would you like to remove?\n")
        cards.remove(answer)