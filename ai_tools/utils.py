from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from deep_translator import GoogleTranslator

def summarize_text(text, sentence_count=4):

    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    summarizer = LsaSummarizer()

    summary = summarizer(
        parser.document,
        sentence_count
    )

    return " ".join(
        str(sentence)
        for sentence in summary
    )
    



# from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests


def translate_text(text, target_language):
    try:
        translated = GoogleTranslator(
            source="auto",
            target=target_language
        ).translate(text)

        return translated

    except TooManyRequests:
        return None
