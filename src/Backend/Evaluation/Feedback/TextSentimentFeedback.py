import logging
import os

def generate_text_sentiment_feedback(score, magnitude, output_path):
    logging.info('start textEmotionExplanation')

    # if magnitude == 0 and score == 0:
    #     print("NO TEXT WAS DETECTED, COULD NOT CREATE GRAPH FOR TEXT EMOTIONS ANALYSIS")
    #     return False

    result = 'Overall Sentiment: positivity of {} with strength of {}'.format(
        score, magnitude) + "\n"
    string = ""

    if score > 0 and magnitude >= 5:
        string += "Your speech text shows positive emotions and is very emotional. That means that your speech text is overall really positive."
    elif score > 0 and magnitude < 5:
        string += "Your speech text shows positive emotions, but is not really emotional. That means that your speech text has a few positive emotions."
    elif score < 0 and magnitude < 5:
        string += "Your speech text shows negative emotions, but is not really emotional. That means that your speech text has a few negative emotions."
    elif score < 0 and magnitude >= 5:
        string += "Your speech text shows negative emotions and is very emotional. That means that your speech text is overall really negative"
    elif score == 0 and magnitude < 5:
        string += "Your speech text is not emotional at all, it is very neutral."
    elif score == 0 and magnitude >= 5:
        string += "Your speech shows equally distributed positive and negative emotions."

    with open(os.path.join(output_path, 'textEmotionsExplanation.txt'), "w") as text_file:
        text_file.write(result + string)
        logging.info('textEmotionsExplanation done')

