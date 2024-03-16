from metaphone import doublemetaphone
import Levenshtein


def generate_consecutive_word_pairs(sentence):
    words = sentence.split()
    return [' '.join(words[i:i + 2]) for i in range(len(words) - 1) if 4 <= len(' '.join(words[i:i + 2])) <= 16]


def create_phonetic_dictionary_from_file(file_path):
    """
    Create a dictionary of phonetic representations for words read from a file.

    :param file_path: Path to the file containing custom words.
    :return: A dictionary where keys are words and values are their phonetic representations.
    """
    phonetic_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            phonetic_dict[word] = doublemetaphone(word)
    return phonetic_dict


# File path
file_path = "/home/joshua/extrafiles/projects/WhisperingAssistant/whispering_assistant/assets/docs/phonetic_custom_words.txt"

# Create phonetic dictionary from file
phonetic_dict = create_phonetic_dictionary_from_file(file_path)
print("Phonetic dictionary:", phonetic_dict)


def find_matching_custom_words(sentence, phonetic_dict, fuzzy_match=False):
    """
    Find custom words that phonetically match or are close based on Levenshtein distance, excluding common articles.

    :param sentence: The sentence to be analyzed.
    :param phonetic_dict: A dictionary of custom words and their phonetic representations.
    :param fuzzy_match: Boolean to enable fuzzy matching.
    :return: A list of custom words that have a phonetic match in the sentence.
    """
    ignore_words = {'this', 'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'in', 'on', 'at', 'of', 'to', 'as', 'by',
                    'for'}

    # Split sentence and filter out ignore words
    words = [word for word in sentence.split() if word.lower() not in ignore_words]

    # Generate combinations of consecutive words
    word_combinations = generate_consecutive_word_pairs(sentence.lower()) + words

    sentence_phonetics = [doublemetaphone(word_combo) for word_combo in word_combinations]

    print("Phonetic representations of the sentence (excluding common words):")
    for word, phonetic in zip(word_combinations, sentence_phonetics):
        print(f"{word}: {phonetic}")

    matching_words_with_scores_dict = {}
    for word, word_phonetics in phonetic_dict.items():
        for sent_phonetic in sentence_phonetics:
            if fuzzy_match:
                use_max_distance = 1

                if len(sent_phonetic[0]) > 3 or len(sent_phonetic[1]) > 3:
                    use_max_distance = 2

                if len(sent_phonetic[0]) > 5 or len(sent_phonetic[1]) > 5:
                    use_max_distance = 3

                if word_phonetics[1]:  # If secondary phonetic exists
                    distance_primary = Levenshtein.distance(word_phonetics[0], sent_phonetic[0])
                    distance_secondary = Levenshtein.distance(word_phonetics[1], sent_phonetic[1])
                    score = min(distance_primary, distance_secondary)
                    if score <= use_max_distance:
                        if word not in matching_words_with_scores_dict or score < matching_words_with_scores_dict[word]:
                            matching_words_with_scores_dict[word] = score
                else:  # Only primary phonetic representation
                    distance_primary = Levenshtein.distance(word_phonetics[0], sent_phonetic[0])
                    if distance_primary <= use_max_distance:
                        if word not in matching_words_with_scores_dict or distance_primary < \
                                matching_words_with_scores_dict[word]:
                            matching_words_with_scores_dict[word] = distance_primary
            else:
                if word_phonetics[0] == sent_phonetic[0]:
                    matching_words_with_scores_dict[word] = 0
                    break

    print(matching_words_with_scores_dict)
    # Convert the dictionary back to a list and sort by score
    matching_words_with_scores = sorted(matching_words_with_scores_dict.items(), key=lambda x: x[1])

    # Extract just the words for the final result
    matching_words = [word for word, _ in matching_words_with_scores]

    return matching_words


def get_matching_custom_words(sentence):
    # Define a set of words to ignore (articles, conjunctions, etc.)
    ignore_words = {'this', 'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'can', 'could',
                    'may', 'might', 'must', 'in', 'on', 'at', 'of', 'to', 'as', 'by', 'for', 'with', 'about', 'against',
                    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
                    'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
                    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
                    's', 't', 'can', 'will', 'just', 'don', 'should', 'now'}
    char_length_comparison = 3

    matching_custom_words = find_matching_custom_words(sentence, phonetic_dict, fuzzy_match=True)

    print("BEFORE:", matching_custom_words)

    # Split the input sentence into words, converting them to lowercase, and filter out ignore words
    sentence_words = [word for word in sentence.lower().split() if word not in ignore_words]

    # Generate phonetic representations for the first two letters of each significant word in the sentence
    # Now considering both primary and secondary phonetic codes
    filtered_matching_words = []
    for custom_word in matching_custom_words:
        char_length_comparison = max(3, len(custom_word) // 2)

        custom_word_phonetic_codes = doublemetaphone(custom_word[:char_length_comparison])
        for sentence_word in sentence_words:
            if len(sentence_word) > 1:
                sentence_word_phonetic_codes = doublemetaphone(sentence_word[:char_length_comparison])
                if any(code in custom_word_phonetic_codes for code in sentence_word_phonetic_codes if code):
                    filtered_matching_words.append(custom_word)
                    break

    print("AFTER:", filtered_matching_words)

    # Construct and return the final string if there are any matching words after filtering
    # if filtered_matching_words:
    #     return "topics about " + ", ".join(filtered_matching_words)

    return filtered_matching_words


# Example usage with fuzzy matching enabled
# sentence = "this is a test for when cut and going in throwing carbonite in the city, yurii will help ramoan"
# matching_custom_words = get_matching_custom_words(sentence)
# print("Matching custom words:", matching_custom_words)
