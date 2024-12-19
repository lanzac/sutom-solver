import random
from enum import Enum

class LetterCondition(Enum):
        """Represent all possition situation of a letter in the word."""
        NOT_PRESENT = 0   # The letter is not present in the word 
        PRESENT_WRONG_INDEX = 1  # The letter is in the word but not at the given index
        PRESENT_CORRECT_INDEX = 2  # The letter is present at the given index

class Condition:
    """Represent the condition of a letter in the solution"""
    def __init__(self, letter: str,
                       position_index: int,
                       condition: LetterCondition):
        self.letter = letter
        self.position_index = position_index
        self.condition = condition


class Solver:
    def __init__(self, word_length: int, first_letter: str, possible_word_list: list):
        self.word_length = word_length
        self.first_letter = first_letter.lower()
        self.possible_word_list = self._initial_filter_word_list(possible_word_list, word_length, first_letter)
        
        self.conditions_list = list()
        self.conditions_list.append(
            Condition(first_letter, 0, LetterCondition.PRESENT_CORRECT_INDEX))
        

    def _initial_filter_word_list(self, possible_word_list: list, word_length: int, first_letter: str) -> list:
        """Filter the list of words based on the solution word length and first letter

        Args:
            possible_word_list (list): Initial list of words
            word_length (int): Length of the solution word
            first_letter (str): First letter of the solution word

        Returns:
            list: The filtered word list
        """
        # Filter by word_length and start_letter
        return [word for word in possible_word_list if len(word) == word_length and word.startswith(first_letter)]
    
    
    def _get_feedback(self, new_guess: str, SOLUTION: str) -> str:
        """DEBUG mode: Get the feedback of a tested word knowing the solution

        Args:
            new_guess (str): The word being tested
            SOLUTION (str): The solution word

        Returns:
            str: The feedback of the tested word
        """
        feedback = ""
        solution_copy = list(SOLUTION) # Used to mark the letters used
        for i, l in enumerate(new_guess):
            if (l == SOLUTION[i]):
                feedback += '!'
                solution_copy[i] = None # Mark as used
            elif l in solution_copy:
                feedback += '?'
                solution_copy[solution_copy.index(l)] = None # Mark as used
            else: # il y a un pb ici, "_" peut aussi vouloir dire qu'il y a eu n max avant de la même lettre
                feedback += '_'
        return feedback
                
    
    def fill_conditions_list(self, new_guess: str,  feedback: str) -> None:
        """Add new conditions in the conditions list based on each element of
        the feedback

        Args:
            new_guess (str): The word being tested
            feedback (str): The feedback of the word being tested
        """
        if not feedback or  len(feedback) != self.word_length or not all(c in '!?_ ' for c in feedback):
            print(f"Invalid feedback: <<{feedback}>>. Try again.")
        else:
            for i in range(1, self.word_length): # We start at the second letter
                if (feedback[i] == '!'):
                    self.conditions_list.append(
                        Condition(new_guess[i], i, LetterCondition.PRESENT_CORRECT_INDEX))
                elif (feedback[i] == '?'):
                    self.conditions_list.append(
                        Condition(new_guess[i], i, LetterCondition.PRESENT_WRONG_INDEX))
                elif (feedback[i] == '_'):
                    self.conditions_list.append(
                        Condition(new_guess[i], i, LetterCondition.NOT_PRESENT))
    
    def print_conditions(self) -> None:
        """Print all the conditions in human frendly way
        """
        for c in self.conditions_list:
            if (c.is_present_in_word):
                if (c.is_present_at_index):
                    print(f"letter {c.letter} is present at the index {c.position_index}")
                else:
                    print(f"letter {c.letter} is present but not at the index {c.position_index}")
            else:
                print(f"letter {c.letter} not present in the solution.")
    

    def update_possible_words(self) -> None:
        """Update the list of possible words based on current conditions."""
        def matches_conditions(word):
            """ 
            We loop on all the conditions based on feedbacks.
            We only focus on what can exclude the word based on the condition 
            being tested. For example, if a tested condition is that a letter is
            not present in the word, we will just check that this letter 
            is not at the given index (c.position_index) in the tested word. 
            We do not check that this letter appears in the word more times than 
            in the solution.
            Maybe this function needs to be updated
            """
            for c in self.conditions_list:
                if c.condition == LetterCondition.NOT_PRESENT and word[c.position_index] == c.letter:
                    return False
                if c.condition == LetterCondition.PRESENT_WRONG_INDEX:
                    if word[c.position_index] == c.letter or c.letter not in word:
                        return False
                if c.condition == LetterCondition.PRESENT_CORRECT_INDEX:
                    if word[c.position_index] != c.letter:
                        return False
            return True

        self.possible_word_list = [word for word in self.possible_word_list if matches_conditions(word)]

    
    def suggest_next_word_randomly(self):
        """Suggest a random word from the remaining list of valid words."""
        return random.choice(self.possible_word_list)   
                    


def load_word_list(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]



def main(DEBUG=False):
    # Load word list
    initial_word_list = load_word_list('mots.txt')
    
    # Set word length and the first letter
    if (DEBUG):
        SOLUTION = random.choice(initial_word_list)
        word_length = len(SOLUTION)
        first_letter = SOLUTION[0].lower()
        print(f"DEBUG:: The solution is : {SOLUTION}")
    else:
        word_length = int(input("Word length: "))
        first_letter = input("Starting letter: ").strip().lower()
    
    # The solver initiates itself by filtering its word list by lenght and first letter
    solver = Solver(word_length, first_letter, initial_word_list)
    
    # Select a random word
    if (DEBUG):
        next_guess = solver.suggest_next_word_randomly()
        print(f"DEBUG:: We try the word: {next_guess}")
    else:
        next_guess = input(f"Try your word or this one ({solver.suggest_next_word_randomly()}): ")
    
    
    try_count = 0
    
    while True:
        current_guess = next_guess
        
        if (DEBUG):
            feedback = solver._get_feedback(current_guess, SOLUTION)
            print(f"DEBUG:: Feedback: {feedback}")
        else:
            feedback = input("Enter feedback (!=correct position, ?=wrong position, _=not in word): ").strip()
            
        # Fill the condition list based on the new feedback
        solver.fill_conditions_list(current_guess, feedback)
        
        # Remove the guess word if, based on the feedback, it does not match 
        # exactly with the solution.
        if (not all(c == '!' for c in feedback) and current_guess in solver.possible_word_list):
            solver.possible_word_list.remove(current_guess)
        
        try_count += 1
        
        # Update the possible words list based on the new condition list
        solver.update_possible_words()
        
        
        possible_word_list_count = len(solver.possible_word_list)
        
        # If the possible word list is empty, there is a problem
        if (possible_word_list_count == 0):
            print(f"The possible word list is empty, there is a problem!")
            break
        
        print(f"There are {possible_word_list_count} remaining candidates")

        # We find the solution ! 
        if (possible_word_list_count == 1):
            print(f"The solution is {solver.possible_word_list[0]} after {try_count} tries.")
            break
        
        # Randomly suggest a the next word from the remaining valid words
        if (DEBUG):
            next_guess = solver.suggest_next_word_randomly()
            print(f"DEBUG:: We try the word: {next_guess}")
        else:
            next_guess = input(f"Try your word or this one ({solver.suggest_next_word_randomly()}): ")

        
    
if __name__ == "__main__":
    DEBUG = False
    main(DEBUG)