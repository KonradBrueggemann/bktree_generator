# Konrad Brüggemann
# Universität Potsdam
# Bachelor Computerlinguistik
# 4. Semester


from model.Auxillary import Art
from Controller import Controller
import argparse


def main():
    print(Art.bk_tree_generator)
    # initiating parser to read command line input
    parser = argparse.ArgumentParser(description="processes the input")
    # adding arguments for file, edit distance and mode (demo or normal)
    parser.add_argument("--file", "-f", type=str, required=True,
                        help="the full name of the text file containing the word list")
    parser.add_argument("--mode", "-m", type=str, required=False,
                        help="'demo' only plots the graph but doesnt save the files, "
                             "leaving it blank results in files being saved")
    parser.add_argument("--dist", "-d", type=str, required=False,
                        help="specify which metric for the edit distance you want to use (levenshtein or hamming)")
    args = parser.parse_args()

    # reading the arguments
    file = args.file
    dist = args.dist
    save = args.mode

    # testing if chosen metric is viable
    metrics = ["lev", "ham", "jac", "jar"]
    if dist:
        assert dist[:3] in metrics, \
            "chosen distance metric is not supported. " \
            "choose levenshtein (lev), hamming (ham), " \
            "jaccard (jac) or jaro winkler (jar)"

    # running the controller with the parsed arguments
    controller = Controller(path=file, demo=save, dist=dist)
    controller.main()


if __name__ == "__main__":
    main()
