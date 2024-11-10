import pandas as pd
import json
from collections import defaultdict
import re
import bkit
import argparse

def annotate_sentence(text, lemma, pos):
    words = text.split()
    return ' '.join([f"{word}[{pos}]" if word == lemma else word for word in words])

def main(input_file, output_file):
    pos_mapping = {
        'ADJ': 'adjective',
        'NNP': 'noun',
        'INTJ': 'interjection',
        'PART': 'part',
        'PRO': 'pronoun',
        'VF': 'verb',
        'PUNCT': 'punctuation',
        'PP': 'postposition',
        'DET': 'noun',
        'VNF': 'verb',
        'CONJ': 'conjunction',
        'QF': 'others',
        'NNC': 'noun',
        'OTH': 'others',
        'ADV': 'adverb'
    }

    bangla_punct_num_pattern = r'[^\u0980-\u09FF\u0900-\u097F\u0041-\u007A\u0041-\u005A]'
    english_punct_pattern = r'[!"#$%&\'()*+,\-./:;<=>?@[\\]^_`{|}~0-9]'
    bangla_number_pattern = r'[\u09E6-\u09EF]'  # Pattern to match Bangla numbers

    df = pd.read_csv(input_file)
    lemma_data = defaultdict(lambda: defaultdict(lambda: {"frequency": 0, "text": set()}))

    for index, row in df.iterrows():
        text = row['text']
        tokens = row['validation']
        
        tokens = json.loads(tokens.replace("'", "\""))

        for token_data in tokens:
            token_idx = token_data['token']
            original_pos = token_data['label']
            word = text.split()[token_idx]

            mapped_pos = pos_mapping.get(original_pos, original_pos)
            lemma_word = bkit.lemmatizer.lemmatize(word)
            # if want to lemmatize using POS
            # lemma_word = bkit.lemmatizer.lemmatize_word(word, pos)


            if re.search(bangla_punct_num_pattern, lemma_word) or re.search(english_punct_pattern, lemma_word) or re.search(bangla_number_pattern, lemma_word):
                continue  

            modified_text = annotate_sentence(text, word, original_pos)
            
            #use lemmma_word replace of word if you want to store lemma instead of word
            lemma_data[word][original_pos]["frequency"] += 1
            lemma_data[word][original_pos]["text"].add(modified_text)

    output_data = []
    for lemma, pos_info in lemma_data.items():
        total_frequency = sum(details["frequency"] for details in pos_info.values())
        variations = len(pos_info)
        first_entry = True
        for pos, details in pos_info.items():
            frequency = details["frequency"]
            text_examples = "; ".join(details["text"])
            output_data.append({
                "word": lemma if first_entry else "",
                "pos": pos,
                "text": text_examples,
                "frequency": frequency,
                "total_frequency": total_frequency if first_entry else "",
                "variations": variations if first_entry else ""
            })
            first_entry = False

    output_df = pd.DataFrame(output_data)
    output_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a CSV file to generate word frequency data.")
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument('--output_file', type=str, required=True, help="Path to the output CSV file.")
    args = parser.parse_args()

    main(args.input_file, args.output_file)
