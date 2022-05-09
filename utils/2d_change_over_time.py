import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
from render_video import render_video

fileName = "../kapapala_tracking.csv"
print("USAGE", sys.argv[0], "[input_csv]")
if len(sys.argv) > 1:
    fileName = sys.argv[0]

data = pd.read_csv(fileName)

print(data.head())

fig, ax = plt.subplots()
ax.set_title("ROD Spread")

ax.set_xticklabels([""]*100)
ax.set_yticklabels([""]*100)
cm = plt.cm.get_cmap('RdYlGn')
timesteps = len(data.iloc[1, 4:])

sc = ax.scatter(x=data["POINT_X"], y=data["POINT_Y"], c=data.iloc[:, 3], cmap=cm)
cb = plt.colorbar(sc)
cb.ticks = ["healthy", "damaged", "infected", "deteriorating", "dead"]

for i in range(timesteps):
    sc = ax.scatter(x=data["POINT_X"], y=data["POINT_Y"], c=data.iloc[:, 3+i], cmap=cm)
    tx = plt.text(251101,2143120, data.columns[3+i])
    plt.pause(0.01)
    plt.savefig("../images/2d/{}.png".format(i))
    tx.remove()

render_video("../videos/rod_2d.avi", "../images/2d/")
