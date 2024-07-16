import re
from nltk.stem import WordNetLemmatizer
from pattern.en import lemma, lexeme

# Reading and processing the text file
def read_file(file_path):
    with open(file_path, 'r', encoding="utf8") as f:
        text_data = f.read().lower()
    words = re.findall(r'\w+', text_data)
    return set(words)

# Counting words
def count_words(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

# Calculating probabilities
def calculate_probabilities(word_count_dict):
    probs = {}
    total_words = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / total_words
    return probs

# Lemmatizing words
def lemmatize_word(word):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)

# Deleting letters from the words
def delete_letter(word):
    delete_list = []
    for i in range(len(word)):
        delete_list.append(word[:i] + word[i+1:])
    return delete_list

# Switching two letters in a word
def switch_letters(word):
    switch_list = []
    for i in range(len(word) - 1):
        switch_list.append(word[:i] + word[i+1] + word[i] + word[i+2:])
    return switch_list

# Replacing letters in a word
def replace_letter(word):
    replace_list = []
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(word)):
        for letter in alphabets:
            replace_list.append(word[:i] + letter + word[i+1:])
    return replace_list

# Inserting letters into a word
def insert_letter(word):
    insert_list = []
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(word) + 1):
        for letter in alphabets:
            insert_list.append(word[:i] + letter + word[i:])
    return insert_list

# Collecting all the words
def edit_one_letter(word, allow_switches=True):
    edits = set()
    edits.update(delete_letter(word))
    if allow_switches:
        edits.update(switch_letters(word))
    edits.update(replace_letter(word))
    edits.update(insert_letter(word))
    return edits

# Collecting words using two edits
def edit_two_letters(word, allow_switches=True):
    edits = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edits.update(edit_one_letter(w, allow_switches=allow_switches))
    return edits

# Getting corrections for the word
def get_corrections(word, probs, vocab, n=2):
    suggestions = (word in vocab and [word]) or list(edit_one_letter(word).intersection(vocab)) or list(edit_two_letters(word).intersection(vocab))
    best_suggestions = sorted([(s, probs.get(s, 0)) for s in suggestions], key=lambda x: x[1], reverse=True)
    return best_suggestions[:n]

# Main function
def main():
    # Load vocabulary
    vocab = read_file('data/final.txt')

    # Count words and calculate probabilities
    word_count = count_words(vocab)
    probs = calculate_probabilities(word_count)

    # Input word
    my_word = input("Enter any word: ").strip().lower()

    # Get corrections
    corrections = get_corrections(my_word, probs, vocab, 2)
    if corrections:
        for word, prob in corrections:
            print(f"Suggested correction: {word} (Probability: {prob:.4f})")
    else:
        print("No suggestions found.")

if __name__ == "__main__":
    main()
