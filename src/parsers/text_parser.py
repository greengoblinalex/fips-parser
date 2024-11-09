import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer


class TextParser:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stemmers = {
            'english': SnowballStemmer('english'),
            'russian': SnowballStemmer('russian')
        }
        self.stop_words = {
            'english': set(stopwords.words('english')),
            'russian': set(stopwords.words('russian'))
        }

    def preprocess_text(self, text, language):
        tokens = word_tokenize(text, language=language)
        filtered_tokens = [word for word in tokens if word.isalnum() and word.lower() not in self.stop_words[language]]
        return [self.stemmers[language].stem(word) for word in filtered_tokens]

    def search_phrases_in_text(self, phrases, text, languages=['english', 'russian']):
        found_phrases = set()
        for language in languages:
            stemmed_words = self.preprocess_text(text, language)
            for phrase in phrases:
                phrase_tokens = word_tokenize(phrase, language=language)
                stemmed_phrase_tokens = [self.stemmers[language].stem(word) for word in phrase_tokens]
                if all(token in stemmed_words for token in stemmed_phrase_tokens):
                    found_phrases.add(phrase)
        return found_phrases


text_parser = TextParser()
