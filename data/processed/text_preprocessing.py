import jsonlines
import nltk
import spacy
import contractions
import string

#nltk.download("stopwords")

# 1. make lowercase 2. expand contractions 3. remove punctuation 4. tokenize 5. lemmatize 6. remove stopwords

model = spacy.load("en_core_web_sm")

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
    doc = model(text)
    for tokens in doc:
        lemmatized_list.append(tokens.lemma_)
    return lemmatized_list

if __name__ == '__main__':
    with jsonlines.open('processed_papers_final.jsonl', 'r') as reader:
        with jsonlines.open('nlp_text.jsonl', 'w') as writer:
            # line_count = 0
            for lines in reader:
                temp_dict = {}

                #id
                temp_dict['id'] = lines['id']

                #Titles
                t_nlp = lines['title']
                t_nlp = t_nlp.lower() #ex. Bob --> bob
                t_nlp = contractions.fix(t_nlp) #ex. it's --> it is
                t_nlp = removePunctuation(t_nlp) #ex. Hello: World --> Hello World
                t_nlp = removeStopwords(t_nlp)
                temp_dict['title'] = lemmatizer(t_nlp)

                #Summaries
                s_nlp = lines['summary']
                s_nlp = s_nlp.lower()
                s_nlp = contractions.fix(s_nlp)
                s_nlp = removePunctuation(s_nlp)
                s_nlp = removeStopwords(s_nlp)
                temp_dict['summary'] = lemmatizer(s_nlp)

                writer.write(temp_dict)
                print("line complete")

                #Testing
                # if (line_count >= 50):
                #     break
                # line_count += 1                