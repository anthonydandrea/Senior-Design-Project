import random as rd


class Keyboard:
    def __init__(self):
        self.keys = [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m"],
        ]

    def getTypo(self, k):
        shouldUpper, isUpper = False, k == k.upper()
        if isUpper:
            shouldUpper = rd.random() < 0.8

        k = k.lower()

        for r in range(len(self.keys)):
            if k in self.keys[r]:
                c = self.keys[r].index(k)

                waiting = True
                tr = tc = None

                while waiting:
                    tr, tc = r + rd.randint(-1, 1), c + rd.randint(-1, 1)

                    if tr == r and tc == c:
                        pass
                    elif tr < 0 or tr >= len(self.keys):
                        pass
                    elif tc < 0 or tc >= len(self.keys[tr]):
                        pass
                    else:
                        val = self.keys[tr][tc]
                        return val.upper() if shouldUpper else val

        # k is not a letter
        return k 

