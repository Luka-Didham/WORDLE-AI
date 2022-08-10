__author__ = "<Luka Didham>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<didlu343@student.otago.ac.nz>"

import re
import copy

class WordleAgent():
   """
       A class that encapsulates the code dictating the
       behaviour of the Wordle playing agent

       ...

       Attributes
       ----------
       dictionary : list
           a list of valid words for the game
       letter : list
           a list containing valid characters in the game
       word_length : int
           the number of letters per guess word
       num_guesses : int
           the max. number of guesses per game
       mode: str
           indicates whether the game is played in 'easy' or 'hard' mode

       Methods
       -------
       AgentFunction(percepts)
           Returns the next word guess given state of the game in percepts
       """

   def __init__(self, dictionary, letters, word_length, num_guesses, mode):
      """
      :param dictionary: a list of valid words for the game
      :param letters: a list containing valid characters in the game
      :param word_length: the number of letters per guess word
      :param num_guesses: the max. number of guesses per game
      :param mode: indicates whether the game is played in 'easy' or 'hard' mode
      """
      self.master_dictionary = dictionary
      self.dictionary = copy.deepcopy(dictionary)
      self.letters = letters
      self.word_length = word_length
      self.num_guesses = num_guesses
      self.mode = mode
      self.dictionary_frequency = {} # stores each letters frequency score in alphabet
      self.regex_master = [] # regex list holding regex strings actually converted
      self.regex_state_master = [] # regex state if character is Not in the position or is in postion
      self.regex_values_master = [] # regex values without formatting ued below
      self.regex_match_counter = 0 # tracks how many regex matches (1's in letter states)
      self.regex_letters = '' # letters used in regex
      i = 0
      while(i < self.word_length): # fills regex lists to size required by 'word_length'
         self.regex_master.insert(i, '.')
         self.regex_state_master.insert(i, 0)
         self.regex_values_master.insert(i, '')
         i = i+1

   #ranks frequencies of letters within the dictionary
   def LetterFrequencies(self):
      for i in self.dictionary:
         list_of_letters = list(i)
         for x in list_of_letters:
            if x in self.dictionary_frequency:
               self.dictionary_frequency[x] = 1 + self.dictionary_frequency.get(x, 1)
            else:
               self.dictionary_frequency[x] = 1

   #ranks the best word in the remaining dictionary based on "dictionary_frequency" weightings
   #Also runs easy mode gussing in certain scenarios
   def ChooseBestWord(self):
      self.LetterFrequencies()  # does frequency calculation for each alphabet letter
      max_word_score = 0 # highest scoring word from filtered dictionary based on letter frequency
      max_word = '' # Actual word with highest word score
      word_score = 0 # current word score
      uncommon_letters = '' # used in easy mode gussing to find letters not common to all remaining limited dictionary
      #below if statment was calibrated to only start easy mode gussing when a sufficent amount of regex matches are found and
      # When dictionary is suffeciently small enough adjusted through observations.
      if self.mode == 'easy' and self.regex_match_counter/self.word_length > 0.3 and len(self.dictionary)/self.word_length < 6 and len(self.dictionary)>3: #threshold to start easy mode guessing
         temp_dictionary = copy.deepcopy(self.master_dictionary)
         for i in self.dictionary:
            for x in i:
               if (self.regex_letters.find(x) == -1): # uncommon letter found
                  uncommon_letters = uncommon_letters + x
         set_uncommon  = set(uncommon_letters)
         uncommon_letters = str(set_uncommon)
         for i in temp_dictionary:
            list_of_letters = list(i)
            set_of_letters = set(list_of_letters)  # remove repeats
            for x in set_of_letters:
               if uncommon_letters.find(x) != -1: #do find uncommon letter
                  word_score = word_score + 1
            if word_score > max_word_score:
               max_word = i
               max_word_score = word_score
            word_score = 0
      else:
         for i in self.dictionary:
            list_of_letters = list(i)
            set_of_letters = set(list_of_letters) #remove repeats
            for x in set_of_letters:
               word_score = word_score + self.dictionary_frequency.get(x, 0)
            if word_score > max_word_score:
               max_word = i
               max_word_score = word_score
            word_score = 0
      if(max_word in self.dictionary):
         self.dictionary.remove(max_word)
      return max_word

   def AgentFunction(self, percepts):

      """Returns the next word guess given state of the game in percepts

      :param percepts: a tuple of three items: guess_counter, letter_indexes, and letter_states;
               guess_counter is an integer indicating which guess this is, starting with 0 for initial guess;
               letter_indexes is a list of indexes of letters from self.letters corresponding to
                           the previous guess, a list of -1's on guess 0;
               letter_states is a list of the same length as letter_indexes, providing feedback about the
                           previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                           letter was not found in the solution), -1 (the correspond letter is found in the
                           solution, but not in that spot), 1 (the corresponding letter is found in the solution
                           in that spot).
      :return: string - a word from self.dictionary that is the next guess
      """
      # This is how you extract three different parts of percepts.
      guess_counter, letter_indexes, letter_states = percepts
      list_len = len(letter_states) #states and indexes list same length


      if(guess_counter==0):
         #below code resets everything between rounds
         self.dictionary = copy.deepcopy(self.master_dictionary)
         self.regex = copy.deepcopy(self.regex_master)
         self.regex_state = copy.deepcopy(self.regex_state_master)
         self.regex_values = copy.deepcopy(self.regex_values_master)
         self.letters_excluded = '' #letters not in word
         self.letters_included = ''  #letters in word
         self.regex_match_counter = 0 #how many letter state '1' matches are found. Used for easy mode gussing thresholds
         self.regex_letters = ''
         self.easy_mode_ran = False
         # rank best word in remaining dictionary
         return self.ChooseBestWord()  # does frequency stuff
      else:
         print(self.dictionary_frequency)
         #below code adds letters to letters_needed, letters_excluded, and regex
         i = 0
         while i < list_len:
            if(letter_states[i]==1): # exsits in correct position
               self.regex[i] = self.letters[letter_indexes[i]] #adds to regex
               self.regex_state[i] = 1 #ensures regex character CANT be changed
               self.regex_match_counter = self.regex_match_counter + 1
               self.regex_letters += self.letters[letter_indexes[i]] #adding letters to regex list
               if (self.letters_included.find(self.letters[letter_indexes[i]]) == -1):  # stop repeats in letters_included list
                  self.letters_included += self.letters[letter_indexes[i]] # adds word to letters included list
            if (letter_states[i] == -1): #exsists but in wrong position
               self.regex_values[i] = self.regex_values[i] + self.letters[letter_indexes[i]] #adds to regex
               self.regex_state[i] = -1 #ensures regex can be changed and is a [not] list
               if (self.letters_included.find(self.letters[letter_indexes[i]]) == -1):  # stop repeats in letters_included list
                  self.letters_included += self.letters[letter_indexes[i]] # adds word to letters included list
            if(letter_states[i]==0): # letter does not exsist in word
               if(self.letters_excluded.find(self.letters[letter_indexes[i]])==-1): #stop repeats in letters excluded list
                  self.letters_excluded += self.letters[letter_indexes[i]] #adds word to letters excluded list
            i = i+1

      #below code checks to ensure letters_excluded does not contain letters from letters_included list
      for x in self.letters_excluded:
         if (self.letters_included.find(x) != -1): #we do find matching letter in letters_included
            self.letters_excluded = self.letters_excluded.replace(x,"")

      #below code properly formats regex [not] syntax
      i = 0 #reset counter i
      while i < len(self.regex):
         if self.regex_state[i] == -1:
            self.regex[i] = "[^" + self.regex_values[i] + "]"
         i = i+1
      #below code removes words from dictionary depending on regex, and letters included/excluded lists
      pattern = re.compile(''.join(self.regex))
      temp_dictionary = copy.deepcopy(self.dictionary)
      for i in self.dictionary:
         removed = False
         if not(pattern.match(i)):
            temp_dictionary.remove(i)
            continue
         for x in self.letters_included:
            if (i.find(x)==-1): #is not found
               temp_dictionary.remove(i)
               removed = True
               break
         if removed:
            continue
         else:
            for x in self.letters_excluded:
               if (i.find(x)>-1): #is found
                  temp_dictionary.remove(i)
                  break

      self.dictionary = temp_dictionary
      return self.ChooseBestWord()  # does letter frequency allocation


