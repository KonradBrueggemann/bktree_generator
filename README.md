# BKTree GeneratorVisualizer

This project aims to provide an algorithm that creates a Burkhard-Keller-Tree based on a given list of words, with the weights of the edges between two words being their distance in a string metric of choice. The word list may contain more than 200.000 words, however only trees containing up to 30 words can be visualized graphically. In addition, the program has an interactive mode in which the user can input a word and a maximum distance and the program will return all words from the list that have a distance less or equal to the maximum distance given.

## Repository

The Repository contains 9 files. The runnable file is called `main.py`. `Auxillary.py` contains a few static methods needed by the other classes. In `Distances.py`, the classes for the different string metrics (Levenshtein, Hamming, Jaccard and Jaro-Winkler) are implemented and `TreeNode.py` contains the class for the tree nodes which are used by `BKTree.py` to actually build the Burkhard-Keller-Tree. Using `Visualizer.py` that tree will be visualized graphically. The interactive mode is implemented in `View.py` and `Controller.py` contains the class that actually controlls the procedure of the program.


## Getting started

It is assumed that you are using Python 3.
To run the files, networkx library must be installed in the project folder, using ```pip install networkx```. 
Once installed, the file that needs to be started is 'main.py'. To run it, simply write "python main.py" followed by an argument -f containing the path to the word list and an optional argument -d which specifies the string metric (default is levenshtein) into the command line. 
Examples:
```
python main.py -f wordlist_de.txt -d lev
python main.py -f wordlists/demo_list.txt 
python main.py -f C:/user/test/Desktop/Uni/txt/demo.txt -d levenshtein
```
The tree will be stored in pickle format and the graph will be stored as a png. If you don't want any files to be stored, add '-m demo' to the command:
```
python main.py -f wordlist_de.txt -d lev -m demo
```

## Building the tree

The tree is built using a simple recursive approach which can be found in the `BKTree` class. The word list will be read and filtered of any duplicates or words that contain anything that arent letters, the remaining words will be passed to the function `create_bktree` and will be parsed there. In very long lists, for every 5000 words that are parsed, a status message will be printed to the console. The first word of the list is determined as the root of the tree. 

## Visualization

Once the tree is generated, if the length of the word list does not exceed 30, it will be passed onto the Visualizer class, which graphically visualizes it using networkx and matplotlib. Trivially, for each node in the tree, a node in the graph will be generated, and with each edge of the tree, those nodes will be connected. The functions `add_node` and `add_edge` of networkx are used for that. The final graph will be plotted in a new window and saved in a .png file. When the window is closed, the program automatically moves on to the interactive mode.

## Interactive Mode

In the interactive mode, the user gets the option to input a query word and a maximum distance. The program then traverses through the tree to find all words that have a distance less or equal to the max. distance to the query word. A list of all matches will be returned. A potential use case of this would be a grammar correction tool, where the tree is built on a massive corpus of correctly spelled words and the query word might be misspelled. So a list of very closely related, correct words would be returned and suggested to the user. 

## Saving files

The tree will be stored in `pickle` format and can later be reused. Additionally, a written version of the tree will also be stored in a `.txt` file and if a graph was created, it will be stored as a `.png`. If a word list is loaded which has already been used, the corresponding pickle file containing the tree will be read and the interactive mode will run immediately.

## Tests

Unit tests for the string metrics can be found in `tests.py`. There is also a function to check if a tree was built correctly, so when a tree is loaded from a pickle file, it will go through that test to make sure everything is correct.

