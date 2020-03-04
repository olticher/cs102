import csv
from normalize import normalize
from bayes import NaiveBayesClassifier

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from db import News, session

model = NaiveBayesClassifier()


def SMS_test():
    with open('SMSSpamCollection') as f:
        data = list(csv.reader(f, delimiter="\t"))

    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

    model.fit(X_train, y_train)
    print('score =', model.score(X_test, y_test))

    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])

    model.fit(X_train, y_train)
    print('sklearn_score =', model.score(X_test, y_test))

    '''
    score = 0.9820574162679426
    sklearn_score = 0.9844497607655502
    '''


def HN_test(train_vector=750):

    s = session()
    X_train, y_train, X_test, y_test = [], [], [], []

    data = s.query(News).filter(News.label != None).all()
    for i, entry in enumerate(data[:train_vector]):
        # X_train.append({})
        # X_train[i]['title'] = entry.title
        X_train.append(entry.title)
        y_train.append(entry.label)

    for i, entry in enumerate(data[train_vector:]):
        # X_test.append({})
        # X_test[i]['title'] = entry.title
        X_test.append(entry.title)
        y_test.append(entry.label)

    model.fit(X_train, y_train)
    print('score =', model.score(X_test, y_test))

    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])

    model.fit(X_train, y_train)
    print('sklearn_score =', model.score(X_test, y_test))

    ''' 1000 entries:
    70/30
    score = 0.736
    sklearn_score = 0.672
    ---
    80/20
    score = 0.725
    sklearn_score = 0.665
    ---
    90/10
    score = 0.75
    sklearn_score = 0.65
    '''


if __name__ == '__main__':
    # print(SMS_test())
    print(HN_test())
