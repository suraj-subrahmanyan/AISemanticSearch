import jsonlines
import nltk
import spacy
import contractions
import string

#nltk.download("stopwords")

# 1. make lowercase 2. expand contractions 3. remove punctuation 4. tokenize 5. lemmatize 6. remove stopwords

from nltk.corpus import stopwords

def removePunctuation(text):
    punctuationString = string.punctuation
    #Replace with space so that Hello-World --> Hello World
    translation_table = str.maketrans(punctuationString, " " * len(punctuationString), "") 
    text = text.translate(translation_table)
    #For Hello: World --> Hello  World, we can remove all whitespace and then add one space between each
    text = ' '.join(text.split())
    return text

def removeStopwords(text):
    noStopwords = []
    stopwords_list = stopwords.words("english") #ex. something because
    split_string = text.split() #list ["something", "because"]

    for words in split_string: #for each word "something", "because", etc. that is not stopword, add to list
        if words not in stopwords_list:
            noStopwords.append(words)

    text = " ".join(noStopwords) #join them back to be tokenized with spacy
    return text    

def lemmatizer(text):
    lemmatized_list = []
    model = spacy.load("en_core_web_sm")
    doc = model(text)
    for tokens in doc:
        lemmatized_list.append(tokens.lemma_)
    return lemmatized_list

if __name__ == '__main__':
    final_list = []
    with jsonlines.open('processed_papers_final.jsonl', 'r') as reader:
        line_count = 0
        for lines in reader:
            s = lines["title"]
            s = s.lower() #ex. Bob --> bob
            s = contractions.fix(s) #ex. it's --> it is
            s = removePunctuation(s) #ex. Hello: World --> Hello World
            s = removeStopwords(s)
            final_list.append(lemmatizer(s))
            
            with jsonlines.open('new_preprocessed_text.jsonl', 'w') as writer:
                writer.write_all(final_list)
            
            #Testing
            # if (line_count >= 200):
            #     break
            # line_count += 1