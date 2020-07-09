from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def analyze(raw_data_path):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    with open(raw_data_path, 'r') as review_file:
    content = review_file.read()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    # data for evaluation
    return magnitude, score