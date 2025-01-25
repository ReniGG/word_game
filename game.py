import random

class Letter:

    def __init__(self, letter = str, in_word:bool = False, in_correct_place:bool=False):
        self.letter = letter
        self.in_word = in_word
        self.in_correct_place = in_correct_place

    def is_in_word(self):
        return self.in_word

    def is_in_correct_place(self):
        return self.in_correct_place

    def __str__(self):
        return self.letter


class Bot:
    def __init__(self, game, guess: str = None):
        self.words = game.get_words()
        self.guess = guess
        self.available_letters = self.get_available_letters()

    def get_available_letters(self):
        # Initialize available letters from the words in the game
        available_letters = []
        for word in self.words:
            available_letters.extend(list(word))
        return list(set(available_letters))

    def make_guess(self):
        if not self.available_letters: #f self.available_letters is empty (which can happen if all letters are removed), calling random.choice() will raise an error
            print("No available letters left.")
            return None  # or raise an exception if needed
        self.guess = random.choice(self.available_letters)
        self.guess = random.choice(self.available_letters)
        return self.guess

    def record_guesses(self, l_guess):
        if not l_guess.in_word and l_guess.letter in self.available_letters:
            self.available_letters.remove(l_guess.letter)
            print(f'Removed letter {l_guess.letter} from available letters.')



class Game:

    def __init__(self):
        try:
            with open('wordlist.txt', 'r') as file:
                self.words = file.read().splitlines()
        except FileNotFoundError:
            print("The word file was not found.")
            self.words = []
        self.list_letters_chosen_word = []
        self.list_letters_guess = []

    def get_words(self):
        return self.words

    def choose_a_word(self):
        self.list_letters_chosen_word = []

        chosen_word = random.choice(self.words)
        for l in range(len(chosen_word)):
            letter_chosen_word = Letter(chosen_word[l])
            self.list_letters_chosen_word.append(letter_chosen_word)
        return self.list_letters_chosen_word


    
    def transform_guess(self, guess):
        self.list_letters_guess = []

        for l in range(len(guess)):
            letter_guess = Letter(guess[l])
            self.list_letters_guess.append(letter_guess)
        return self.list_letters_guess


    def compare_letters(self, bot):
        for index, (l_chosen, l_guess) in enumerate(zip(self.list_letters_chosen_word, self.list_letters_guess)):
            # Check if the letter from chosen_word is in the guess
            is_in_guess = any(l_guess.letter == letter.letter for letter in self.list_letters_chosen_word)

            chosen = ''.join([str(letter) for letter in self.list_letters_chosen_word])

            if l_chosen.letter == l_guess.letter:
                l_guess.in_word = True
                l_guess.in_correct_place = True
                print(f'Letter {l_guess.letter} is in the chosen word {chosen} and they match at index {index}')
            elif is_in_guess and l_chosen.letter != l_guess.letter:
                l_guess.in_word = True
                print(f'Letter {l_guess.letter} is in the chosen word {chosen} but they do not match at index {index}')
            else:
                print(f'Letter {l_guess.letter} is not in the chosen word {chosen}.')
                bot.record_guesses(l_guess)


# Main execution
game = Game()
bot = Bot(game)

# 1. Game chooses a word
chosen_word = game.choose_a_word()
print("Chosen word: " + ''.join([str(letter) for letter in chosen_word]))

# 2. Bot makes 5 guesses
for i in range(10):  # Loop 5 times
    print(f"\n--- Guess {i + 1} ---")

    # 3. Bot makes a guess
    guess = bot.make_guess()
    print(f"Bot's guess: {guess}")

    # 4. Transform the guess into `Letter` objects
    game.transform_guess(guess)

    # 5. Compare the chosen word with the guess
    game.compare_letters(bot)







