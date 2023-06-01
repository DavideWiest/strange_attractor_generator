## A project to analyze if a graph is a strange attractor

**See `_seg` for examples of generated graphs.**

### Works in 2d
##### run `generate.py`
Will automatically save graphs that meet predermined criteria (PNG and JSON) until the desired number is met.

### Adjustable selection
##### add the metric function and the selection criterion in their respective lists (generate.py)
Thresholds can be changed easily, the selection algorithm can also be changed.

### Helpful modules like a formula generator
- `FormulaGenerator`: Can generate a lambda function as formula with customizable dimensions, degrees, and generators (e.g. degreeBoolGenerator to decide if x^y will be used in the function, keeping the formula simpler)
- `FormulaParser`: Takes in a formula generated from FormulaGenerator (some limitations, like no division) and parses it into a dictionary (variable**degree represents the key, the factor the value)
- `CoordinatesGenerator`: 
- `Trainingdata_UI`: An example of how to make a small UI where users can label data built with tkinter

### Features several algorithms that indicate a strange-attractor-like behavior
- `Distance-Evaluator`:       Uses numpy to compute the mean distance between the points -> Low distance indicates the graph is stuck in a loop or converges towards an optimum.
- `Vector-Direction-Evaluator`:       Checks if the vectors that point to the next coordinate repeat themselves, (and if, in what number of turns) -> Indication that the graph is in a loop or a simple one.
- `Color-Evaluator`:      Draws a plot with matplotlib, and counts the number of pixels the graph produces with Pillow -> Strange attractors are chaotic, resulting in a large area taken up by connecting lines between two coordinates.

### Most functions will work in other dimensions too, however, many also have to be generalized
- e.g. the coordinates to euclidean distances conversion

### Some training data for the "specialness" of graphs
- `graphBatches/b[1-11]`


.

Note:
I tried to train a small neural network to predict this. It didn't work at all.
