import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import traceback
import os
import json

from modules.constants import *

class CloseUIEvent(Exception):
    pass

class TrainingDataUI():
    def __init__(self, master: tk.Tk, batchName: str, outerDirLoc: str):
        self.cl = CoordinatesLoader(batchName, outerDirLoc, RECOGNIZE_EXISTING_RATINGS)
        self.rs = RatingSaver(batchName, outerDirLoc, ALLOW_RATING_OVERWRITE)

        self.master = master
        master.title("Function Graph")

        # Create a Figure object and add a subplot
        self.fig = plt.figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Create a canvas widget for Matplotlib graph display
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        # Generate a sample function graph
        self.loadNextGraph()

        # Create a label and integer input field
        self.label = ttk.Label(self.master, text="Specialness Rating (0 to 10):")
        self.label.pack()
        self.rating_value = tk.IntVar()
        self.rating_entry = ttk.Entry(self.master, textvariable=self.rating_value)
        self.rating_entry.pack()
        self.rating_entry.focus_set()

        # Create a counter
        self.counter = tk.IntVar()
        self.counter.set(0)

        # Create a label for the counter
        self.counter_label = ttk.Label(self.master, text="Rating Count: ")
        self.counter_label.pack()

        # Bind the Enter key press event to the rating entry field
        self.rating_entry.bind("<Return>", self.save_rating)

    # Generate a sample function graph
    def loadNextGraph(self):
        xyList = self.cl.getNextCoordinates()
        x, y = zip(*xyList)

        self.ax.clear()
        self.ax.scatter(x, y)
        self.ax.plot(x, y)
        self.canvas.draw()

    # Function to handle Enter key press event
    def save_rating(self, event):
        try:
            if self.rating_value.get() == "":
                print("Enter pressed, but rating empty")
                return
        except tk.TclError:
            print("Enter pressed, but rating empty")
            return
        
        rating = int(self.rating_value.get())/10
        # Save the rating and perform desired actions
        self.rs.saveRatingToFile(rating)

        self.rating_entry.delete(0, tk.END)
        self.rating_entry.focus_set()
        self.counter.set(self.counter.get() + 1)

        # Check if all ratings are completed
        if self.cl.index > len(self.cl.graphInfoFiles)-1:
            self.rating_entry.configure(state=tk.DISABLED)  # Disable rating entry field when all ratings are completed
            raise CloseUIEvent("Closing Ui: Whole batch has been rated")

        self.loadNextGraph()

        # Update counter label to display current/end
        self.counter_label["text"] = f"Rating Count: {self.counter.get()+1}/{len(self.cl.graphInfoFiles)}"

    def finishRatingProcess(self):
        self.rs.loadAndDistributeRatings()

class CoordinatesLoader():
    def __init__(self, batchName: str, outerDirLoc: str, recognizeExistingRatings: bool):
        self.batchName = batchName
        self.outerDirLoc = outerDirLoc
    
        self.graphInfoFiles = getAllGraphFilesInDir(self.outerDirLoc + "/" + self.batchName)
        self.dest = outerDirLoc + "/" + batchName + "/" + GENERAL_RATING_FILENAME

        if recognizeExistingRatings:
            with open(self.dest, "r") as f:
                self.index = f.read().split("\n")
        else:
            self.index = 0
        
    def getNextCoordinates(self):
        if self.index > len(self.graphInfoFiles)-1:
            raise IndexError("There is no next graph info file in line. Maybe the directory doenst contain any graph files.")
        fileLoc = self.outerDirLoc + "/" + self.batchName + "/" + self.graphInfoFiles[self.index]
        with open(fileLoc, "r") as f:
            file = json.load(f)

        self.index += 1
        return file["coordinates"]

class RatingSaver():
    def __init__(self, batchName: str, outerDirLoc: str, allowRatingOverwrite: bool):
        self.batchName = batchName
        self.outerDirLoc = outerDirLoc
        self.dest = outerDirLoc + "/" + batchName + "/" + GENERAL_RATING_FILENAME
        self.allowRatingOverwrite = allowRatingOverwrite

    def saveRatingToFile(self, rating):
        with open(self.dest, "a") as f:
            f.write(str(rating) + "\n")

    def loadAndDistributeRatings(self):
        with open(self.dest, "r") as f:
            ratings = f.read().split("\n")[:-1]
        
        filenames = getAllGraphFilesInDir(self.outerDirLoc + "/" + self.batchName)
        
        for rating, filename in zip(ratings, filenames):
            fileLoc = self.outerDirLoc + "/" + self.batchName + "/" + filename
            with open(fileLoc, "r") as f:
                contents = json.load(f)
            if not self.allowRatingOverwrite and contents.get("rating") != None:
                print(f"Not overwriting rating for file {filename}")
                continue
            contents["rating"] = float(rating)
            with open(fileLoc, "w") as f:
                json.dump(contents, f, indent=4)


def getAllGraphFilesInDir(dir: str) -> list[str]:
    return sorted([
    filename
    for filename in os.listdir(dir)
    if filename.endswith(".json") and filename not in (GENERAL_INFO_FILENAME, GENERAL_RATING_FILENAME)
    ], key= lambda x: int(x.split(".")[0]))


def testRatingSaverDistribution():
    rs = RatingSaver("first", "graphBatches", True)
    rs.loadAndDistributeRatings()


if __name__ == "__main__":
    # Create a Tkinter window
    window = tk.Tk()

    # Create the TrainingDataUI instance
    training_ui = TrainingDataUI(window, BATCHNAME, OUTERDIRLOC)

    try:
        # Start the Tkinter event loop
        window.mainloop()
    # except CloseUIEvent as e:
    #     pass
    except:
        # unexpected bahavior
        traceback.format_exc()

    training_ui.finishRatingProcess()
    print("Rating process finished: Ratings saved and distributed")
