# Konrad Brüggemann
# Universität Potsdam
# Bachelor Computerlinguistik
# 4. Semester


import multiprocessing as mp
from itertools import cycle
from string import punctuation


class Methods:

    @staticmethod
    def clean_list(L):
        """
        :param L: the original word list
        :return: word list without special characters and no duplicates
        """
        assert isinstance(L, list), "not a list"
        assert len(L) > 1, "not enough words"
        for word in range(len(L) - 1):
            for _ in punctuation:
                if _ in L[word]:
                    L.remove(L[word])
        return list(sorted(set([w for w in L if w.isalpha()])))

    @staticmethod
    def chunkify(L):
        """
        divides the word list into chunks if its very long
        so that the tree can be generated through multithreading
        :param L: list of words
        :return: either list of chunks or original list
        """
        if len(L) > 1000:
            no_of_chunks = Methods.thread_count()
            chunks = [[] for _ in range(no_of_chunks)]
            for element, chunk in zip(L, cycle(chunks)):
                chunk.append(element)
            print(f"Generated {no_of_chunks} chunks with an average size of {len(chunks[0])} items.")
            return chunks
        else:
            return L

    @staticmethod
    def thread_count():
        return mp.cpu_count()

    @staticmethod
    def progress_bar(curr, total):
        if total > 200000:
            curr /= 4
            total /= 4
        elif total > 100000:
            curr /= 2
            total /= 2
        curr, total = curr//1000, total//1000
        progress = round(curr/total, 4) * 100
        text = "[" + "▓" * int(curr) + "░" * int(total-curr) + "]" + f" {progress}%"
        return text


class Config:
    max_items: int = 30


class Art:
    bk_tree_generator = """
    ___  _  _    ___ ____ ____ ____    ____ ____ _  _ ____ ____ ____ ___ ____ ____ 
    |__] |_/  __  |  |__/ |___ |___    | __ |___ |\ | |___ |__/ |__|  |  |  | |__/ 
    |__] | \_     |  |  \ |___ |___    |__] |___ | \| |___ |  \ |  |  |  |__| |  \ 
                                                                               """

    interactive_mode = """
    _ _  _ ___ ____ ____ ____ ____ ___ _ _  _ ____    _  _ ____ ___  ____ 
    | |\ |  |  |___ |__/ |__| |     |  | |  | |___    |\/| |  | |  \ |___ 
    | | \|  |  |___ |  \ |  | |___  |  |  \/  |___    |  | |__| |__/ |___ 
    """
