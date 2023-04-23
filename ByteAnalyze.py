import math

class ByteAnalyze:
    def __init__(self, X, Alph):
        self.X = X
        self.EnFile = []
        self.Alph = Alph.copy()
        j = 0
        for i in range(len(X)):
            i = j
            for j in range(i, len(X) + 1):
                if X[i:j] in Alph:
                    self.EnFile.append(X[i:j])
                    break
        self.EnCounter = {}

    def X_in_alph_size(self):
        return len(self.EnFile)

    def Alph_in_X(self):
        for elem in self.Alph:
            if self.EnFile.count(elem) != 0:
                self.EnCounter[str(elem)] = self.EnFile.count(elem)
        return self.EnCounter

    def PinX(self):
        PinX = {}
        len = self.X_in_alph_size()
        for key, value in self.EnCounter.items():
            PinX[key] = value / len
        return PinX

    def InfX(self):
        InfX = {}
        len = self.X_in_alph_size()
        for key, value in self.EnCounter.items():
            InfX[key] = -math.log2(value / len)
        return InfX

    def InfSumX(self):
        InfSum = 0
        len = self.X_in_alph_size()
        for key, value in self.EnCounter.items():
            InfSum += -math.log2(value / len)
        return InfSum

    def ReturnSortedEnFile(self):
        SortedEnfile = self.Alph.copy()
        returned = []
        for i in range(len(SortedEnfile)):
            if SortedEnfile[i] in self.EnFile:
                returned.append(SortedEnfile[i])
        return returned

    def ReturnSortedPinX(self):
        return dict(sorted(self.EnCounter.items(), key=lambda x: x[1], reverse=True))

    def ReturnOketsInFile(self):
        Alph_Bytes = []
        for i in range(256):
            Alph_Bytes.append((bytes([i])))
        analyze_fo_return = ByteAnalyze(self.X, Alph_Bytes)
        analyze_fo_return.Alph_in_X()
        return analyze_fo_return.ReturnSortedPinX()
