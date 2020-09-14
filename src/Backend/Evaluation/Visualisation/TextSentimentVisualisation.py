import matplotlib.pyplot as plt
import logging
import math
import os
def visualize_text_sentiment(magnitude, score, output_path):
    logging.info('start plotting textEmotions')
    x = ['magnitude', 'score']
    values = [magnitude, score]
    scale = 1
    if magnitude >= 10:
        scale = math.floor(magnitude / 10) + 1

    if magnitude < 1:
        scale = 0.5

    x_pos = [scale*0, scale*1]
    ax = plt.gca()

    plt.barh(x_pos, values, 0.3*scale, color=['#2300A8', '#00A658'], alpha=0.5)
    plt.title("Text emotions analysis", y=1.6)
    plt.yticks(x_pos, x)

    ax.set_aspect('equal')
    ax.grid(True, which='both', alpha=0.4)

    #removing top and right borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.axvline(x=0, color='black', alpha=0.7)

    scoreScale = -1*scale
    magnitudeScale = -1.5*scale
    if magnitude < 1:
        scoreScale += 0.1
        magnitudeScale += 0.1

    plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9)
    plt.savefig(os.path.join(output_path, 'textEmotions.png'))
    logging.info('plotting textEmotions done')