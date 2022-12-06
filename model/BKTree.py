# Konrad Brüggemann
# Universität Potsdam
# Bachelor Computerlinguistik
# 4. Semester


from model.Auxillary import Methods, Config
from model.Distances import LevenshteinDistance, HammingDistance, JaccardDistance, JaroWinklerDistance
from model.Visualizer import Visualizer
from TreeNode import TreeNode
from threading import Thread, Lock
from multiprocessing import Process, Manager


class BKTree:
    def __init__(self, word_list, edit_dist):
        # used for status messages
        self.count = 0
        self.fix_count = []
        self.word_list = Methods.clean_list(word_list)
        self.edit_dist = edit_dist
        self.length = len(self.word_list)
        # defining the tree root as the first word of the list
        self.root = TreeNode(name=self.word_list[0], weight=0)
        # splitting the word list into chunks
        self.chunks = Methods.chunkify(self.word_list[1:])
        # creating a dictionary with each word and its distance to the root
        self.dist_to_root = self._distances_to_root()
        self.tree = self.create_bktree()
        self.graph = self.get_graph()
        self.max_depth = self._get_max_depth()

    def _distances_to_root(self):
        print("Calculating root distance for every word...")
        if len(self.chunks) == Methods.thread_count():
            distances = self._multiprocessing()
        else:
            distances = {}
            self._distance_to_root(L=self.chunks, dist_dict=distances)
        print("Done.")
        return distances

    def _distance_to_root(self, L: list, dist_dict: dict):
        root = self.word_list[0]
        index = 0
        while index < len(L):
            word = L[index]
            dist_dict[word] = self.get_distance(word, root)
            index += 1

    def _multiprocessing(self):
        # creating a value dictionary
        manager = Manager()
        distances = manager.dict()
        # each chunk of the word list will be processed by a separate process
        processes = [Process(target=self._distance_to_root, args=(chunk, distances)) for chunk in self.chunks]
        for process in processes:
            process.daemon = True
            process.start()
        for process in processes:
            process.join()
        return distances

    def create_bktree(self):
        """
        calls the _create_bktree_recursive function which actually builds the tree
        if the word list is long enough it will call the function in multiple threads to save time
        short lists will be processed in a single thread
        :return: tree object
        """
        chunks = self.chunks
        if len(chunks) == Methods.thread_count():
            return self._multithreading(chunks)
        else:
            self._create_bktree_recursive(self.word_list[1:])
            return self.root

    def _multithreading(self, chunks):
        # creating a thread for each chunk
        threads = [Thread(target=self._create_bktree_recursive, args=(chunk,)) for chunk in chunks]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self.root

    def _create_bktree_recursive(self, L):
        """
        recursive function that builds the tree with help of bk_parent
        :param L: word list
        :return: tree object
        """
        # the object is locked whenever a thread is modifying it to avoid clashing
        locker = Lock()
        index = 0
        while index < len(L):
            word = L[index]
            with locker:
                self.count += 1
                # bk_parent function is called to find the node to which the word has to bind to
                self._find_parent_node(word, self.root)
            # for every 1000 words being processed a status message is printed
            if self.count % 10000 == 0 and self.count not in self.fix_count:
                self.fix_count.append(self.count)
                print(f"{self.count} / {self.length} words parsed.")
                print(Methods.progress_bar(self.count, self.length))
            index += 1
        return self.root

    def _find_parent_node(self, word, root, level=0):
        """
        recursive function that finds the right parent for a word and adds it to its children
        :param word: the currently processed word
        :param root: the node that's being looked at, not always the root of the entire tree
        :return: word becomes child node of the parent that was determined
        """
        current_node = root
        if level == 0:
            dist_to_current = self.dist_to_root[word]
        else:
            dist_to_current = self.get_distance(word, current_node.name)
        if not current_node.is_leaf:
            index = 0
            while index < len(current_node.children):
                node = current_node.children[index]
                index += 1
                # if there already is an edge with the same distance,
                # recursively iterate through the children of that node
                if node.weight == dist_to_current:
                    current_node = node
                    return self._find_parent_node(word, current_node, level + 1)
        # once the right parent node is found, the new distance is calculated
        # and the word is added to the children of that node
        dist_to_current = self.get_distance(word, current_node.name)
        current_node.add_child(name=word, weight=dist_to_current)

    def get_distance(self, w1, w2):
        """
        calls the respective function to calculate the chosen distance metric of the pair of words
        :return: the calculated edit distance
        """
        if self.edit_dist.startswith("lev"):
            return LevenshteinDistance.dist(w1, w2)
        elif self.edit_dist.startswith("ham"):
            return HammingDistance.dist(w1, w2)
        elif self.edit_dist.startswith("jac"):
            return JaccardDistance.J(w1, w2)
        elif self.edit_dist.startswith("jar"):
            return JaroWinklerDistance.jaro_Winkler(w1, w2)
        else:
            raise TypeError

    def get_graph(self):
        if len(self.word_list) >= Config.max_items:
            print("The word list is too long for a graph to be generated. "
                  "Limit is 30. However the tree will be stored "
                  "in a text file.")
        else:
            vis = Visualizer(self.tree)
            return vis.graph

    def _get_max_depth(self) -> int:
        max_depth = 0
        depth_of_current_branch = 0

        node_depth_tuple = [(self.tree, depth_of_current_branch)]

        # traversing through the tree
        while node_depth_tuple:
            current_neighbour = node_depth_tuple.pop()
            current_children = current_neighbour[0].children
            depth_of_current_branch = current_neighbour[1]
            depth_of_current_branch += 1

            if len(current_children) == 0:
                max_depth = depth_of_current_branch if depth_of_current_branch > max_depth else max_depth
            else:
                for child in current_children:
                    node_depth_tuple.append((child, depth_of_current_branch))

        return max_depth - 1
