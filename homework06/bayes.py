"""
Naive Bayes classifier
"""
from collections import Counter, defaultdict
from math import log
from text import clean


class NaiveBayesClassifier:
    """ Naive Bayes classifier """

    def __init__(self, alpha=1.0):
        self.factor = alpha
        self.classes = defaultdict(lambda: defaultdict(int))
        self.words = defaultdict(lambda: defaultdict(int))
        self.classes_counter = {}
        self.words_counter = {}
        self.pairs_counter = {}

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        all_words = []
        pairs = []
        self.classes_counter = dict(Counter(y))
        for title, class_ in zip(X, y):
            words_list = clean(title)
            for word in words_list:
                all_words.append(word)
                pairs.append((word, class_))
                self.classes[class_]['appearances'] += 1
        for class_ in self.classes:
            self.classes[class_]['prior'] = self.classes_counter[class_]/len(y)
        self.words_counter = dict(Counter(all_words))
        self.pairs_counter = dict(Counter(pairs))
        d = len(self.words_counter)
        for word in self.words_counter:
            for class_ in self.classes:
                self.words[word][class_] = (
                    self.pairs_counter.get((word, class_), 0) + self.factor) / (self.classes[class_]['appearances'] + self.factor * d)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        classification = []
        for title in X:
            words_list = clean(title)
            p_list = []
            for class_ in self.classes:
                ln_p_class = log(self.classes[class_]['prior'])
                for word in words_list:
                    if self.words[word][class_]:
                        ln_p_class += log(self.words[word][class_])
                p_list.append((class_, ln_p_class))
            classification.append(max(p_list, key=lambda x: x[1]))
        return classification

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        count = 0
        for record, label in zip(self.predict(X_test), y_test):
            if record[0] == label:
                count += 1
        return count / len(y_test)
