Learn more or give us feedback
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def normalize(text):
    wnl = WordNetLemmatizer()
    stopWords = set(stopwords.words('english')) 
    word_list = []
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    text = text.lower().split()
    for word in text:
        lemma = wnl.lemmatize(word)
        if lemma not in stopWords:
            word_list.append(lemma)

    return word_list 
