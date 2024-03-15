import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer


class TextParser:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.__stemmer_en = SnowballStemmer('english')
        self.__stemmer_ru = SnowballStemmer('russian')
        self.__stop_words_en = set(stopwords.words('english'))
        self.__stop_words_ru = set(stopwords.words('russian'))

    def search_phrases_in_text(self, phrases, text):
        tokens_en = word_tokenize(text, language='english')
        filtered_tokens_en = [word for word in tokens_en if word.lower() not in self.__stop_words_en]
        stemmed_words_en = [self.__stemmer_en.stem(word) for word in filtered_tokens_en]

        tokens_ru = word_tokenize(text, language='russian')
        filtered_tokens_ru = [word for word in tokens_ru if word.lower() not in self.__stop_words_ru]
        stemmed_words_ru = [self.__stemmer_ru.stem(word) for word in filtered_tokens_ru]

        found_phrases = []
        for phrase in phrases:
            phrase_tokens = word_tokenize(phrase)
            stemmed_phrase_tokens_en = [self.__stemmer_en.stem(word) for word in phrase_tokens]
            stemmed_phrase_tokens_ru = [self.__stemmer_ru.stem(word) for word in phrase_tokens]

            en_tokens_found = all(token in stemmed_words_en for token in stemmed_phrase_tokens_en)
            ru_tokens_found = all(token in stemmed_words_ru for token in stemmed_phrase_tokens_ru)

            if en_tokens_found or ru_tokens_found:
                found_phrases.append(phrase)

        return set(found_phrases)


text_parser = TextParser()
