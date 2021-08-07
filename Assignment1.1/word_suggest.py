from nltk import corpus
from nltk.tokenize import word_tokenize
from nltk.corpus import words, brown, stopwords
from nltk.probability import FreqDist

stopwords_set = set(stopwords.words('english'))
stopwords_set = set()
freq_buckets = dict()

for word in brown.words():
    word = word.lower()
    if word not in stopwords_set:
        bucket_key = word[0]
        if bucket_key not in freq_buckets:
            freq_buckets[bucket_key] = FreqDist()

        freq_buckets[bucket_key][word] += 1


def last_word(text: str):
    words = word_tokenize(text)

    if len(words) == 0:
        return ""

    return words[-1]


def reco(string: str):
    if len(string) == 0:
        return list()

    bucket_key = string[0]
    if bucket_key not in freq_buckets:
        return list()

    freq_bucket = freq_buckets[bucket_key]

    recos = list()
    
    for key in freq_bucket:
        if str(key).startswith(string):
            recos.append((key, freq_bucket.get(key)))

    recos.sort(key=lambda x:x[1], reverse=True)

    return recos

if __name__ == "__main__":
    while True:
        reco(input())
