# Konrad Brüggemann
# Universität Potsdam
# Bachelor Computerlinguistik
# 4. Semester


import numpy
from math import floor, ceil


class LevenshteinDistance:

    @staticmethod
    def dist(w1, w2):
        """
        This method calculates the Levenshtein distance between two words
        by creating a matrix that contains the distances between all the prefixes of the two words
        using a dynamic programming approach
        :param w1: word of parent node
        :param w2: word of child node (interchangeable)
        :return: Levenshtein distance between the two words
        """

        # initiating the matrix
        matrix = numpy.zeros((len(w1) + 1, len(w2) + 1))

        # first row is filled with values starting from 0
        for i in range(len(w1) + 1):
            matrix[i][0] = i
        # first column is filled with values starting from 0
        for j in range(len(w2) + 1):
            matrix[0][j] = j

        # iterating through each cell of the matrix excluding first row and column
        for i in range(1, len(w1) + 1):
            for j in range(1, len(w2) + 1):
                # inside the loops the distances are calculated for all combinations of prefixes from the two words
                # if the two characters are equal,
                # the distance is equal to that of the cell to the top left of the current cell
                if w1[i - 1] == w2[j - 1]:
                    matrix[i][j] = matrix[i - 1][j - 1]
                else:
                    # if the two characters are not equal,
                    # the distance is the minimum of the cell bordering it to the left, top left, and top middle
                    # with an added cost of 1
                    a = matrix[i][j - 1]
                    b = matrix[i - 1][j]
                    c = matrix[i - 1][j - 1]
                    low = min(a, b, c)
                    matrix[i][j] = low + 1

        # the Levenshtein distance is then located at the bottom-right corner of the matrix
        return int(matrix[len(w1)][len(w2)])


class HammingDistance:

    @staticmethod
    def dist(w1, w2):
        """
        :param w1: word of parent node
        :param w2: word of child node (interchangeable)
        This method calculates the Hamming distance between two given words
        using a simple iteration approach
        in contrary to the original hamming distance which only works for words of same length,
        this method also accounts for words that differ in length
        :return: calculated Hamming distance as integer
        """

        res = 0

        # if one word contains the other, the difference in length is their distance
        if w1 in w2:
            return len(w2) - len(w1)
        if w2 in w1:
            return len(w1) - len(w2)

        # for words of same length, each letter that is not identical increases distance by 1
        if len(w1) == len(w2):
            for i in range(len(w1)):
                if w1[i] != w2[i]:
                    res += 1
            return res

        # for words of different length
        elif len(w1) != len(w2):

            # the distance is at least the difference in length
            res = max(len(w1), len(w2)) - min(len(w1), len(w2))

            # then each letter which is not identical further increases the distance by 1
            for i in range(min(len(w1), len(w2))):
                if w1[i] != w2[i]:
                    res += 1
            return res
        else:
            # if two words arent of different length but not of same length either, something must be wrong
            raise TypeError


class JaccardDistance:

    @staticmethod
    def J(w1, w2):
        """
        :param w1: word of parent node
        :param w2: word of child node (interchangeable)
        This method calculates the Jaccard Index for the distance between two words
        Jaccard Distance doesnt account for order of letters but merely for amount of shared letters
        between both words
        """
        # for each word a list is generated containing all letters
        set_A = [l for l in w1]
        set_B = [l for l in w2]

        # calculating the intersection of the two lists
        temp = set(set_B)
        intersection = [value for value in set_A if value in temp]

        # if the intersection is empty, return 0
        if len(intersection) == 0:
            return 0

        # concatenate both lists
        union = set(set_A + set_B)

        # jaccard distance is defined as 1 - J(A, B) where J(A, B) is the intersection divided by the union
        # of the two samples A and B, in our case the letters of word 1 and word 2
        # to make it more user friendly, the distance is multiplied by 1000
        return int(1000 * round(len(intersection) / len(union), 3))


class JaroWinklerDistance:

    @staticmethod
    def jaro(s1, s2):
        # If the s are equal
        if s1 == s2:
            return 1.0

        # Length of two s
        len1 = len(s1)
        len2 = len(s2)

        # Maximum distance upto which matching
        # is allowed
        max_dist = floor(max(len1, len2) / 2) - 1

        # Count of matches
        match = 0

        # Hash for matches
        hash_s1 = [0] * len(s1)
        hash_s2 = [0] * len(s2)

        # Traverse through the first word
        for i in range(len1):

            # Check if there is any matches
            for j in range(max(0, i - max_dist),
                           min(len2, i + max_dist + 1)):

                # If there is a match
                if s1[i] == s2[j] and hash_s2[j] == 0:
                    hash_s1[i] = 1
                    hash_s2[j] = 1
                    match += 1
                    break

        # If there is no match
        if match == 0:
            return 0.0

        # Number of transpositions
        t = 0
        point = 0

        # Count number of occurrences
        # where two characters match but
        # there is a third matched character
        # in between the indices
        for i in range(len1):
            if hash_s1[i]:

                # Find the next matched character
                # in second
                while hash_s2[point] == 0:
                    point += 1

                if s1[i] != s2[point]:
                    t += 1
                point += 1
        t = t // 2

        # Return the Jaro Similarity
        return (match / len1 + match / len2 +
                (match - t) / match) / 3.0

    @staticmethod
    def jaro_Winkler(s1, s2):

        jaro_dist = JaroWinklerDistance.jaro(s1, s2)

        # If the jaro Similarity is above a threshold
        if jaro_dist > 0.7:

            # Find the length of common prefix
            prefix = 0

            for i in range(min(len(s1), len(s2))):

                # If the characters match
                if s1[i] == s2[i]:
                    prefix += 1

                # Else break
                else:
                    break

            # Maximum of 4 characters are allowed in prefix
            prefix = min(4, prefix)

            # Calculate jaro winkler Similarity
            jaro_dist += 0.1 * prefix * (1 - jaro_dist)

        return int(1000 * (1 - round(jaro_dist, 4)))
