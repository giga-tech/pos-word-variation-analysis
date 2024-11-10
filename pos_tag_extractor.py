import pandas as pd
import ast
import argparse

def extract_tagged_data(row, pos_tag):
    validation_data = ast.literal_eval(row['validation'])
    tagged_tokens = [d['token'] for d in validation_data if d['label'] == pos_tag]
    words = row['text'].split()
    tagged_words = [words[token] for token in tagged_tokens]
    
    return [{'word': word, 'sentence': row['text'], 'group_id': row['group_id']} for word in tagged_words]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and filter data by POS tag.")
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument('--output_file', type=str, required=True, help="Path to the output CSV file.")
    parser.add_argument('--pos_tag', type=str, required=True, help="POS tag to filter (e.g., 'OTH').")
    
    args = parser.parse_args()

    df = pd.read_csv(args.input_file)
    filtered_data = df.apply(lambda row: extract_tagged_data(row, args.pos_tag), axis=1).explode().dropna().reset_index(drop=True)
    result_df = pd.DataFrame(filtered_data.tolist())
    
    result_df.to_csv(args.output_file, index=False)
