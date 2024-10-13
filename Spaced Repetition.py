class Flashcard:
    def __init__(self, front, back):
        self.front = front
        self.back = back

    def __str__(self) -> str:
        return f"Front: {self.front}\nBack: {self.back}"
    
response = input("Actions: study, add, remove\n")

if response == "add":
    front = input("Front of card: ")
    back = input("Back of card: ")
    card1 = Flashcard(front, back)

