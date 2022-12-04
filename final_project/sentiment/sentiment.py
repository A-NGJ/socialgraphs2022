from collections import Counter
import re
import string
import typing as t

import nltk
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

        text = [word for word in text if word not in stopwords]

        lemmatizer = nltk.WordNetLemmatizer()
        text = [lemmatizer.lemmatize(word) for word in text]

        text = [word for word in text if re.match(r"^\w+$", word)]

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
