from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import numpy as np
import seaborn as sns
import os, statistics, math, sys, csv

#TODO: create the feedback from here or somewhere else?
#importing files for feedback creation
# from Backend.Evaluation.Feedback.HandPositionsFeedback import standardDeviation
# from Backend.Evaluation.Feedback.HandPositionsFeedback import gestureAdvicer


def visualize_hand_positions(raw_data_path, output_path):
    data = csv.DictReader(open(os.path.join(raw_data_path, 'handPositions.csv')), delimiter=',')
    xCoords = []
    yCoords = []
    for d in data:
        xCoords.append(int(d['x']))
        yCoords.append(int(d['y']))

    # string = standardDeviation(xCoords, yCoords)
    # if len(xCoords) == 0 or len(yCoords) == 0:
    #     print("NO HANDS WERE TRACKED. COULD NOT CREATE HAND VISUALIZER GRAPH.")
    #     return False

    # gestureAdvicer(string)
    xMax = 802
    yMax = 539

    x, y = np.mgrid[0:xMax:100j, 0:yMax:100j]
    positions = np.vstack([x.ravel(), y.ravel()])
    values = np.vstack([xCoords, yCoords])

    z = np.sum(values)
    if np.isnan(z) or np.isinf(z):
        print("COULD NOT DETECT ANY HAND MOVEMENTS")
        return False

    kernel = stats.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, x.shape)

    plt.xlim(0,xMax)
    plt.ylim(0,yMax)
    plt.imshow(np.rot90(f), cmap='jet', extent=[0, xMax, 0, yMax])
    plt.scatter(xCoords,yCoords,alpha=0.3)
    plt.gca().set_ylim(plt.gca().get_ylim()[::-1])
    plt.gca().axes.get_xaxis().set_ticks([])
    plt.gca().axes.get_yaxis().set_ticks([])
    plt.title('Hand positions')
    # plt.subplots_adjust(left=0.01, bottom=0, right=0.99, top=1)

    plt.savefig(os.path.join(output_path, 'handposPlot.png'))
    plt.cla()
    plt.clf()
    return xCoords, yCoords

# if __name__ == "__main__":
#     visualize_hand_positions('outputFiles')
