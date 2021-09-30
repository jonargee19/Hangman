import random
import time
import os
import pickle

class Hangman:

    def __init__(self):
        self._word_list = "cat dog".split()
        self._guesses = 0
        self._win_status = "Playing"
        self._spaces = ""
        self._word = ""
        self._letters_guessed = ""
        self._score = 0
        self._player_name = ""
        self.load_scores()
#        self._high_scores = {1:["", 0], 2:["", 0], 3:["", 0], 4:["", 0], 5:["", 0]}

    def get_word_list(self):
        """get method for word_list"""
        return self._word_list

    def get_guesses(self):
        """get method for guesses"""
        return self._guesses

    def get_win_status(self):
        return self._win_status

    def decrement_guesses(self):
        """Reduces number of guesses by one."""
        self._guesses -= 1
        if self._guesses > 0:
            return True
        else:
            return False

    def validate_letter(self, letter):
        """Makes sure input is valid."""
        if len(letter) == 1:
            if letter.isalpha():
                return True
        return False

    def check_against_word(self, letter):
        """Checks guessed letter against word."""
        return letter in self._word

    def update_game(self, letter, guess_bool):
        """Updates the amount of guesses left and the progress of the word to be guessed."""
        self._letters_guessed += letter
        if guess_bool:
            for i in range(len(self._word)):
                if letter == self._word[i]:
                    spaces_list = list(self._spaces)
                    spaces_list[i*2] = letter
                    self._spaces = "".join(spaces_list)  
            if "_" not in self._spaces:
                self._win_status = "Won"          
        elif self.decrement_guesses():
            return
        else:
            self._win_status = "Lost"

    def manage_high_scores(self, player, score):
        """Takes a player name and their score and checks it against the current high score. If the score
        is great enough to make the list (a dictionary of lists), then it will be added."""
 #       new_high_scores = self._high_scores
        end_of_dict = len(self._high_scores)
        for key in self._high_scores:
            if score >= self._high_scores[key][1]:
                for el in range(end_of_dict, key, -1):
                    self._high_scores[el] = self._high_scores[el-1]
 #                   new_high_scores[el] = self._high_scores[el-1]
                self._high_scores[key] = [player, score]
 #               self._high_scores[key] = score
 #               new_high_scores[key][0] = player
 #               new_high_scores[key][1] = score
 #               self._high_scores = new_high_scores
                self.save_scores()
                break
 
    def win_lose(self):
        """Determines what happens if a player wins or loses."""
        if self._win_status == "Lost":
            self.manage_high_scores(self._player_name, self._score)           
            print(f"Sorry, you don't have any guesses left. You lost! \nYour score was {self._score}")
            print("HIGH SCORES:")
            for el in self._high_scores:
                print(f"{el}: {self._high_scores[el]}")
            print("Would you like to play again? ('y' for yes and 'n' for no)")
            choice = input()
            if choice == "y":
                print()
                self.clear_board(False)
                self.play()
            else:
                return
        if self._win_status == "Won":
            self._score += 1
            os.system('cls')
            print(self._spaces)
            print(f"You guessed it! \nYour score is: {self._score} \nWould you like to play again? ('y' for yes and 'n' for no)")
            choice = input()
            if choice == "y":
                print()
                self.clear_board(True)
                self.play()
            else:
                return

    def introduction(self):
        """Introduces the game."""
        os.system('cls')
        print("Welcome to Hangman!")
        print()
        time.sleep(1)
        print("Coded by Jon Ramm")
        print()
        time.sleep(1)
        print("See how many you can get in a row!")
        print()
        print("What is your name?")
        self._player_name = input()
        print(f"I hope you know some words, {self._player_name}...")
        time.sleep(1)
        os.system('cls')
        

    def clear_board(self, won):
        """Resets game state, word, spaces, and guesses."""
        self._guesses = 0
        self._win_status = "Playing"
        self._word = ""
        self._spaces = ""
        self._letters_guessed = ""
        if won is False:
            self._score = 0
        os.system('cls')

    def save_scores(self):
        """Saves high scores via pickling."""
        with open("high_scores.pickle", "wb") as file:
            pickle.dump(self._high_scores, file)

    def load_scores(self):
        """Un-pickles high scores."""
        with open("high_scores.pickle", "rb") as file:
            self._high_scores = pickle.load(file)

    def play(self):
        """method for playing the game"""
        self._word = self._word_list[random.randint(0, len(self._word_list)-1)]
        self._guesses = len(self._word)
        if self._win_status == "Playing":
            for letter in self._word:
                    self._spaces += "_ "
            while self._win_status == "Playing" and self._guesses != 0:
                os.system('cls')
                print(self._spaces, "\n")
                print("Score: ", self._score)
                print("Letters guessed: ", self._letters_guessed)
                print("Guesses remaining: ", self._guesses)
                print("Guess a letter: ")
                guessed_letter = input()
                if self.validate_letter(guessed_letter) is False:
                    print("Input invalid, please try again.")
                    time.sleep(.75)
                    continue
                elif self.check_against_word(guessed_letter):
                    if guessed_letter not in self._spaces:
                        print(f"The letter '{guessed_letter}' is in the word, good job!")
                        time.sleep(.75)
                        self.update_game(guessed_letter, True)
                        continue
                    else:
                        print(f"You already guessed '{guessed_letter}', try again.")
                        time.sleep(.75)
                        self.update_game(guessed_letter, False)
                        continue
                else:
                    print(f"The letter '{guessed_letter}' is not in the word, try again.")
                    time.sleep(.75)
                    self.update_game(guessed_letter, False)
                    continue
            self.win_lose()
            

if __name__ == "__main__":
    game = Hangman()
 #   game.save_scores()
    game.introduction()
    game.play()
