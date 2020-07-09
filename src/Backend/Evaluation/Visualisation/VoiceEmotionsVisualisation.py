import numpy as np
import logging
import matplotlib.pyplot as plt

def voiceEmotionsVisualisation(input_data, output_path):
    logging.info('start plotting speechEmotions')
    labels = np.unique(input_data)
    emotionToColorMap = {
    "happy": '#ff9999',
    "neutral": '#66b3ff',
    "fearful": '#ffcc99',
    "calm": '#99ff99'
    }

    sizes = []
    colors = []
    for i in range(len(labels)):
        color_counter = 0
        for j in range(len(input_data)):
            if labels[i] ==  input_data[j]:
                color_counter += 1
        sizes.append(color_counter)
        colors.append(emotionToColorMap.get(labels[i]))

    fig1, ax1 = plt.subplots()
    patches, texts, autotexts = ax1.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=90)
    for text in texts:
        text.set_color('grey')
        for autotext in autotexts:
            autotext.set_color('grey')# Equal aspect ratio ensures that pie is drawn as a circle

    ax1.axis('equal')
    plt.tight_layout()
    plt.legend(labels=labels)
    plt.savefig(output_path + '\\speechEmotionsChart.png')

    plt.cla()
    plt.clf()
    logging.info('plotting speechEmotions done')