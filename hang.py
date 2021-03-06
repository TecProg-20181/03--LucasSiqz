import random
import string
import logging

WORDLIST_FILENAME = "words.txt"

logging.basicConfig(filename='hangman.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

class File():

    def open_file(self, file):
        try:
            inFile = open(file, 'r', 0)
            logging.info('File opened')
        except:
            print("Error opening the file!\nShutting down...")
            logging.info('Error opening file')
            exit(1)

        return inFile

    def read_file(self, inFIle):
        logging.info('File read')
        return inFile.readline()

    def close_file(self, inFile):
        logging.info('File closed')
        inFile.close()


class Word():

    def create_word_list(self, line):
        logging.info('Create word list')
        return string.split(line)

    def validate_word(self, wordList):
        secretWord = random.choice(wordList)

        if secretWord.isalpha() == False:
            print("Invalid word finded!\nShutting down...")
            exit(1)
        logging.info('Word has been validated')

        return secretWord

    def calc_different_letters(self, secretWord):
        self.differentLetters = 0
        for letter in string.ascii_lowercase:
            if letter in secretWord:
                self.differentLetters += 1
        logging.info('Different letters has been calculated')
        return self.differentLetters

    def choose_word(self, differentLetters, secretWord, wordList):
        if differentLetters > 8:
            choise = raw_input('Do you want to change the secret word? (Y to yes & N to no): ')
            while(choise.lower() != 'y' and choise.lower() != 'n'):
                choise = raw_input("invalid option. Do you want to change the secret word? (Y to yes & N to no): ")

            if choise == 'Y' or choise == 'y':
                word = Word()
                secretWord = word.validate_word(wordList)
                differentLetters = self.calc_different_letters(secretWord)
                game = Game()
                game.print_welcome_message(secretWord, differentLetters)
                secretWord = self.choose_word(differentLetters, secretWord, wordList)

        return secretWord


class Game():

    def print_welcome_message(self, secretWord, differentLetters):
            logging.info('The game has started')
            print 'Welcome to the game, Hangam!'
            print '-------------'
            print 'I am thinking of a word that is', len(secretWord), 'letters long with', differentLetters, 'differents letters.'
            print '-------------'

    def is_word_guessed(self, secretWord, lettersGuessed):
        for letter in secretWord:
            if letter in lettersGuessed:
                pass
            else:
                return False

        return True

    def get_guessed_word(self):
         self.guessed = ''
         for letter in secretWord:
             if letter in self.lettersGuessed:
                 self.guessed += letter
             else:
                 self.guessed += '_ '

         return self.guessed

    def get_available_letters(self, lettersGuessed):
        # 'abcdefghijklmnopqrstuvwxyz'
        self.available = string.ascii_lowercase
        for letter in self.available:
            if letter in lettersGuessed:
                self.available = self.available.replace(letter, '')

        return self.available

    def hangman(self, secretWord):
        self.guesses = 8
        self.lettersGuessed = []

        while  self.is_word_guessed(secretWord, self.lettersGuessed) == False and self.guesses > 0:
            print 'You have ', self.guesses, 'guesses left.'

            self.availabe = self.get_available_letters(self.lettersGuessed)

            print 'Available letters', self.available
            letter = raw_input('Please guess a letter: ')

            while letter.isalpha() == False or len(letter) > 1:
                letter = raw_input('This is not a letter!  Please guess a letter: ')

            if letter.lower() in self.lettersGuessed:
                self.guessed = self.get_guessed_word()
                print 'Oops! You have already guessed that letter: ', self.guessed
                logging.info('Letter already guessed')

            elif letter.lower() in secretWord:
                self.lettersGuessed.append(letter.lower())
                self.guessed = self.get_guessed_word()
                print 'Good Guess: ', self.guessed
                logging.info('Guessed letter in the word')

            else:
                self.guesses -= 1
                self.lettersGuessed.append(letter.lower())
                self.guessed = self.get_guessed_word()
                print 'Oops! That letter is not in my word: ',  self.guessed
                logging.info('Guessed wrong')

            print '------------'

        else:
            if self.is_word_guessed(secretWord, self.lettersGuessed) == True:
                print 'Congratulations, you won!'
                logging.info('Won the game')
            else:
                print 'Sorry, you ran out of guesses. The word was', secretWord, '.'
                logging.info('Lose the game')
            logging.info('Finished the game')

file = File()
inFile = file.open_file(WORDLIST_FILENAME)
line = file.read_file(inFile)
file.close_file(inFile)

word = Word()
wordList = word.create_word_list(line)
secretWord = word.validate_word(wordList)
differentLetters = word.calc_different_letters(secretWord)

game = Game()
game.print_welcome_message(secretWord, differentLetters)
game.hangman(word.choose_word(differentLetters, secretWord, wordList))
