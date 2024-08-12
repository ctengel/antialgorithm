
import re
import csv
import json
import sklearn
import nltk

STOPWORDS = nltk.corpus.stopwords.words('english')
SCORE_FILE = 'scores.csv'


def tokenize(text):
    return ' '.join([word for word in nltk.tokenize.word_tokenize(re.sub(r'[^a-z\s]', '', text.lower())) if word not in STOPWORDS])


def featurize(entry):
    title_tokens = tokenize(entry['title'])
    #sum_tokens = tokenize(entry['summary'])
    # author
    # feed
    # tags
    return title_tokens

def vectorize(abunch):
    return sklearn.feature_extraction.text.TfidfVectorizer(max_features=262144).fit_transform(abunch).toarray()  # or 1000


def load_all_scored():
    with open(SCORE_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        scorez = list(reader)
    for score in scorez:
        with open(score['hash'] + '.json') as json_file:
            json_data = json.load(json_file)
        score['data'] = json_data
    return scorez

def run_it():
    all_data = load_all_scored()
    labels = [x['score'] for x in all_data]
    features = vectorize([featurize(x['data']) for x in all_data])
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(features, labels, test_size=0.2, random_state=42)
    model = sklearn.svm.SVC(kernel='linear')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Accuracy:", sklearn.metrics.accuracy_score(y_test, y_pred))
    print("Classification Report:\n", sklearn.metrics.classification_report(y_test, y_pred))

run_it()
