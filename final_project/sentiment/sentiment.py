from collections import (
    Counter,
    defaultdict,
)
import re
import string
import typing as t

import nltk
import numpy as np
import pandas as pd


class SentimentAnalyzer:
    def __init__(self):
        self.data = None

    def load_sentiment_data(self, path: str):
        self.data = pd.read_csv(path, delimiter="\t", na_values="--")

    @staticmethod
    def normalize_text(text: t.Iterable[str]) -> t.List[str]:
        """
        Normalizes text with the following steps:
        * set everything lowercase
        * remove english stopwords and punctuation
        * lemmatize words
        * remove words which contain signs other than letters

        Returns
        -------
        List[str] :
            normalized text
        """

        text = [word.lower() for word in text]

        stopwords = nltk.corpus.stopwords.words("english")
        stopwords.extend(string.punctuation)
        stopwords.extend(
            [
                "would",
                "could",
                "although",
                "however",
                "also",
                "told",
            ]
        )

        text = [word for word in text if word not in stopwords]

        lemmatizer = nltk.WordNetLemmatizer()
        text = [lemmatizer.lemmatize(word) for word in text]

        text = [word for word in text if re.match(r"^[A-Za-z_\-]+$", word)]

        return text

    def calc_sentiment(self, text: t.Iterable[str]) -> float:
        """
        Calculates sentiment of input text.

        Returns
        -------
        float :
            sentiment score in range [0, 10], the higher the happier text
        """
        text = [token for token in text if token in self.data.word.values]
        freq_dist = Counter(text)
        if sum(freq_dist.values()) == 0:
            print("empty frequency distribution for input text")
            return 0

        sum_sentiment = sum(
            self.data[self.data.word == token].happiness_average.values[0]
            * freq_dist[token]
            for token in freq_dist
        )
        return sum_sentiment / sum(freq_dist.values())

    def in_wordlist(self, tokens: t.Iterable[str]) -> dict:
        """
        Find tokens that are present in word list.

        Returns
        -------
        dict :
            Dictionary in format {Token: sentiment} of matched tokens
        """

        tokens_in_wordlist = {}
        for token in tokens:
            if token in self.data.word.values:
                tokens_in_wordlist[token] = self.data[
                    self.data.word == token
                ].happiness_average.values[0]

        return tokens_in_wordlist


def term_freq(text: t.List[str]) -> defaultdict:
    """
    Term frequency for each document in given text DO DPY

    Parameters
    ----------
    text:
        Tokenized text

    Returns
    -------
    defaultdict(int) :
        term frequency
    """
    term_freqs = defaultdict(int)
    for word in text:
        term_freqs[word] += 1 / len(text)
    return term_freqs


def inv_doc_freq(corpus: t.List[t.List[str]]) -> defaultdict:
    """
    Calculate inverse document frequency for each word in a corpus

    Parameters
    ----------
    corpus:
        list of tokenized documents

    Returns
    -------
        inverse document term frequency
    """
    words_idf = {}
    words_count = defaultdict(int)
    for text in corpus:
        words_in_text = set()
        for word in text:
            if word not in words_in_text:
                words_in_text.add(word)
                words_count[word] += 1

    for word in words_count:
        words_idf[word] = np.log(len(corpus) / (1 + words_count[word]))

    return words_idf
