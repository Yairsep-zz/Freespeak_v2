import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import collections

def faceEmotionsPieChart(input_path, output_path):
    df = pd.read_csv(input_path + "\\emotions.csv")
    emotions = df['Emotions']

    labels = np.unique(emotions)
    emotionTocolorMap = {
    "Happy": '#ff9999',
    "Neutral": '#66b3ff',
    "Fearful": '#ffcc99',
    "Angry": '#99ff99',
    "Disgusted": '#ccebc4',
    "Sad": '#fdb462',
    "Surprised": '#fa81ff'
    }

    sizes = []
    colors = []
    for i in range(len(labels)):
        color_counter = 0
        for j in range(len(emotions)):
            if labels[i] ==  emotions[j]:
                color_counter += 1
        sizes.append(color_counter)
        colors.append(emotionTocolorMap.get(labels[i]))

    fig1, ax1 = plt.subplots()
    patches, texts, autotexts = ax1.pie(sizes, colors = colors, autopct='%1.1f%%', startangle=90)
    for text in texts:
        text.set_color('grey')
        for autotext in autotexts:
            autotext.set_color('grey') # Equal aspect ratio ensures that pie is drawn as a circle

    ax1.axis('equal')
    plt.tight_layout()
    plt.legend(labels=labels)
    plt.savefig(output_path + '\\facialEmotionsChart.png')
    plt.cla()
    plt.clf()