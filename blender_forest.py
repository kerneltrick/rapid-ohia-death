import bpy
import os
import csv
import numpy as np

class DataLoader:

    def __init__(self, filename):

        self.filename = filename
        self.data = None

    def load_data(self):

        pass



if __name__ == "__main__":
    filename = "kapapala_tracking.csv"
    loader = DataLoader(filename)
