import math
from collections import Counter
import time

# Reading a text file with line-separated values
with open('data.txt', 'r') as file:
    # Read lines and strip whitespace
    word = [line.strip() for line in file.readlines()]

def calculate_entropy(valid, guess_pattern):
    """Calculate entropy based on possible word patterns."""
    pattern_counts = Counter(
        ''.join([w[i] if guess_pattern[i] != '_' else '_' for i in range(len(w))])
        for w in valid
    )
    total_words = len(valid)
    entropy = sum(
        -p * math.log2(p)
        for p in (count / total_words for count in pattern_counts.values())
    )
    return entropy

def top_letter(valid, guessed):
    """Select the letter with the highest frequency in valid words."""
    letter_counts = Counter()
    for word in valid:
        for letter in set(word):
            if letter not in guessed:
                letter_counts[letter] += 1
    return letter_counts.most_common(1)[0][0] if letter_counts else None

valid_words, guessed_letters, daWord = word.copy(), set(), ""

# Get the target word from the user
while daWord not in word:
    daWord = input("Provide word in dataset: ")

teem = time.time()

# Initialize the guess with underscores
guess = ["_"] * len(daWord)

wrong_attempts, reps = 0, 0

# Main guessing loop
while "".join(guess) != daWord and wrong_attempts < 8:
    current = top_letter(valid_words, guessed_letters)  # Choose the letter based on frequency

    if not current:  # If no valid letter is found, break
        break

    guessed_letters.add(current)

    if current in daWord:
        # Update the guess for every occurrence of the guessed letter in daWord
        for i in range(len(daWord)):
            if daWord[i] == current:
                guess[i] = current
    else:
        wrong_attempts += 1

    # Filter valid words based on the current guess
    valid_words = [w for w in valid_words if len(w) == len(daWord) and all(guess[i] == "_" or guess[i] == w[i] for i in range(len(guess)))]

    # Print the current state for debugging
    print(f"Iteration {reps + 1}: Guessed Letter = '{current}', Current Guess = '{''.join(guess)}', Wrong Attempts = {wrong_attempts}")

    reps += 1

# Final result
if "".join(guess) == daWord:
    print(f"WON! The word was '{daWord}'.")
else:
    print(f"LOSS! The word was '{daWord}'.")
print(f"Time Elapsed: {time.time()-teem:.2f} seconds")
