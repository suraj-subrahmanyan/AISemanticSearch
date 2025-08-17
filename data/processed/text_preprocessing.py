import jsonlines
import nltk
import spacy

# 1. make lowercase 2. expand contractions 3. remove punctuation 4. tokenize 5. lemmatize 6. remove stopwords
#write functions to do manually instead of libraries
#deal with possessive nouns like occam's using nltk's POS (part of speech) tagging

#nltk.download("punkt_tab")

from nltk.tokenize import word_tokenize

with jsonlines.open('processed_papers_final.jsonl', 'r') as reader:
    line_count = 0
    for lines in reader:
        s = lines["title"]
        s = s.replace(':', '')
        s = s.replace('-', '')  
        s = s.replace("'s", '')     
        stemming = spacy.load("en_core_web_sm")
        s = stemming(s)
        print(s)
        if (line_count >= 10):
            break
        line_count += 1

if __name__ == '__main__':
    pass