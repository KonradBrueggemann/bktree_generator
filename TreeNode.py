# Konrad Brüggemann
# Universität Potsdam
# Bachelor Computerlinguistik
# 4. Semester


class TreeNode:
    def __init__(self, name: str, weight: int):
        self.children = []
        self.weight = weight
        self.name = name
        self.is_leaf = (self.children is [])

    def add_child(self, name, weight):
        """
        adds a child node to a node's list of children
        :param name: name of the node
        :param weight: weight of the node (will be shown on the edge)
        """
        self.children.append(TreeNode(name, weight))

    def __str__(self, level=0):
        """
        Recursive magic function to print the tree in string format
        :param level: basically the depth of a node (distance to root)
        :return:
        tree in string format
        """
        ret = "\t" * level + repr((self.weight, self.name)) + "\n"
        index = 0
        while index < len(self.children):
            child = self.children[index]
            index += 1
            ret += child.__str__(level + 1)
        return ret
