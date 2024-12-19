# Sutom Solver

A Python program to help solve the word game [SUTOM](https://sutom.nocle.fr). This solver uses filtering based on feedback from your guesses to suggest the word to use for the next try.

## How to Play SUTOM
SUTOM is a French word puzzle game where players must guess a word with feedback provided after each attempt. 

Feedback symbols used in this program :
- `!`: Letter is in the correct positio (lettres entourées d'un carré rouge).
- `?`: Letter is in the word but not in the correct position (lettres entourées d'un cercle jaune).
- `_`: Letter is not in the word (lettres qui restent sur fond bleu).

## Installation
Clone this repository to get started:

```bash
git clone https://github.com/lanzac/sutom-solver.git
cd sutom-solver
```

Make sure Python 3.x is installed on your system.

## Usage

1. Prepare a word list:
   - Use the included `mots.txt` file or provide your own list of valid words.

2. Run the solver:
    ```bash
    python sutom_solver.py
    ```

    Follow the prompts to input feedback after each guess.

    Example if the solution is `BLOQUEUR` the feedback for the word `BLEUIRAI` you must report will be: `!!??_?__`

3. For debug mode (auto-solve with a known solution): Edit the main() function and set DEBUG = True.


## License

This project is open-source and available under the MIT License.

## Credits

SUTOM game by [JonathanMM](https://framagit.org/JonathanMM/sutom).
