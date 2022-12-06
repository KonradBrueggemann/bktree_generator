# Konrad Brüggemann
# Universität Potsdam
# Bachelor Computerlinguistik
# 4. Semester


from model.Distances import LevenshteinDistance, HammingDistance, JaccardDistance, JaroWinklerDistance


class View:

    def __init__(self, tree, dist):
        self.tree = tree
        self.dist = dist
        self._dynamic_matches = {}

    def main(self):
        print("Now you will be asked to input a word and a maximum distance. "
              "Every word in the tree that has a distance to your word that is lower than the max. distance "
              "will be returned.")
        # user can do this as many times as he wants until he ends the program by inputting a space bar
        while True:
            self.run()

    def run(self):
        """
        function for the interactive mode
        user can input a word and a max distance
        then get_matches() will be run to find the matching words
        """
        word: str = input("Enter a word: ")
        # a space bar terminates the program
        if word.startswith(" "):
            quit("Program finished.")
        try:
            d: int = int(input("Enter the maximum distance: "))
        # catching bad inputs
        except ValueError:
            print("max. distance must be integer and cannot be empty!")
            return
        # finding all matches
        result = self.get_matches(word, d)
        if not result:
            print("No matches found.")
        else:
            # print the list in a more pretty way
            if len(result) > 1:
                print(f"{len(result)} matches were found:")
            else:
                print("1 Match was found.")
            print(*result, sep=", ", end=".\n")

    def distance(self, w1, w2):
        """ returns respective dist of word pair """
        if self.dist.startswith("lev"):
            return LevenshteinDistance.dist(w1, w2)
        elif self.dist.startswith("ham"):
            return HammingDistance.dist(w1, w2)
        elif self.dist.startswith("jar"):
            return JaroWinklerDistance.jaro_Winkler(w1, w2)
        elif self.dist.startswith("jac"):
            return JaccardDistance.J(w1, w2)
        else:
            raise TypeError

    def _check_for_previous_matches(self, word, d):
        result = {}
        matches = self._dynamic_matches
        pair = (word, d)
        # checking if this exact input has been used before
        if pair in matches.keys():
            print("Matches for this input have been calculated previously.")
            # True because a perfect match has been found
            return matches[pair], True
        else:
            # going through the stored matches to see if the queue word has been used before
            # but with a higher distance
            for pair in matches.keys():
                if pair[0] == word and int(pair[1]) > d:
                    print("Matches for this word with a larger distance have been calculated previously. "
                          "Returning those that fit this input...")
                    for word, dist in matches[pair].items():
                        # all words that matched the queue word previously but have a distance
                        # that also satisfies the current input will be returned
                        if dist <= d:
                            result[word] = dist
            # updating the class variable
            self._dynamic_matches[word] = result
            return (result, True) if result else (result, False)

    def get_matches(self, word, d):
        """
        checks if a similar queue has been used before
        and if that is the case, matches will be obtained from that previous queue
        if not, calls the recursive function _get_matches()
        and sorts the matches by increasing edit dist
        """
        result = self._check_for_previous_matches(word, d)
        # if the second value (index 1) of the result is TRUE, that means that from a previous input queue
        # the matches were obtained and did not have to be recalculated
        if result[1]:
            # sorting the results by increasing distance, so that words closer to the queue show up first
            result = sorted(result[0], key=result[0].get)
        else:
            # if there was no related previous queue, matches have to be calculated from scratch
            result = self._get_matches(word, d, self.tree)
            # updating the dictionary
            self._dynamic_matches[(word, d)] = result
            result = sorted(result, key=result.get)
        try:
            # if the queue word is actually in the tree, it ends up in the list of matches with a distance of 0,
            # which places it at index 0
            # but it should not be shown in that case
            if result[0] == word:
                result = result[1:]
            return result
        # an Index Error will occur if no matches have been found, but the program should not terminate because of that
        except IndexError:
            pass

    def _get_matches(self, word: str, d: int, node):
        """
        function to find all words that have less or equal dist than the max. dist d to a given word
        :param word: the word the user put in
        :param d: maximum distance chosen by user
        :param node: the current node the function is looking at
        :return: dictionary in which the keys are the matches and the values are the edit dist to the queue word
        """

        # dictionary with the matches and their distance so that later the output can be sorted increasingly
        list_of_matches = {}

        current_node = node
        # distance between user word and current node
        dist_to_current = self.distance(word, current_node.name)
        # if its lower or equal to the maximum distance d, it can be appended to the result list right away
        if dist_to_current <= d:
            list_of_matches[current_node.name] = dist_to_current
        # iterating through its children
        index = 0
        while index < len(current_node.children):
            child = current_node.children[index]
            dist = child.weight
            # look at all nodes that have a distance with a difference of d
            # to the distance between the parent and user word
            if (dist_to_current - d) <= dist <= (dist_to_current + d):
                # add node to list of matches if distance to user word is lower or equal to the max dist
                if self.distance(child.name, word) <= d:
                    list_of_matches[child.name] = dist
                # run function recursively if not looking at a leaf
                if not child.is_leaf:
                    list_of_matches.update(self._get_matches(word, d, node=child))
            index += 1
        # return the final dictionary
        return list_of_matches
