# pos-word-variation-analysis

## Installation
```bash
pip install -r requirements.txt
```
## Usage
Run this script to analyze the frequency and variations of words based on POS tags:
```bash
python pos_word_frequency.py --input_file PATH_TO_INPUT_CSV --output_file PATH_TO_OUTPUT_CSV
```
### output:
* `Word`: Unique words
* `POS`: The part-of-speech tag
* `frequency`: Frequency of the word with the specific POS tag.
* `text:` Annotated sentences with POS tags.
* `total_frequency:` Total frequency of the lemma word.
* `variations:` Number of POS variations for the word.


Run this script to analyze the words based on POS tags:
```bash
python pos_tag_extractor.py --input_file INPUT_CSV --output_file OUTPUT_CSV ----pos_tag POS_TAG(EX- OTH,NNC..)
```
### output
* `word`: Specific POS tag word
* `Sentence`: Sentence of a specific word
* `Group_id`: Group id of sentence



