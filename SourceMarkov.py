import math


class SourceMarkov:
    def __init__(self, file_name, N):
        self.N = N + 1  # размерность источника маркова
        self.alph = self.get_alph()  # первичный алфавит
        self.X = self.file_open(file_name)  # содержимое файла
        # self.X = bytes('AABCBABCKFKFVEJVCNEICJW;FKEPWOJFIERNVMEIFNWENDOIEWJFKCDCDKJFKJAAAJAIFJWOEFJFKEFKWEFMLKCMWKVNCABBBBC'.encode('utf8'))
        self.v_ij = self.get_v_ij()
        self.v_j = self.get_v_j()
        self.p_ai = self.get_p_ai()
        self.p_aiaj = self.get_p_aiaj()
        self.inf = self.get_inf()

    # поиск вхождений
    def find_count(self, string):
        count = 0
        index = -1
        while True:
            index = self.X.find(string, index + 1)
            if index == -1:
                return count
            count += 1

    # получить первичный алфавит
    def get_alph(self):
        alph = []
        for i in range(256):
            alph.append(chr(i).encode('utf8'))
        return alph

    def file_open(self, file_name):
        with open(file_name, 'rb') as file:
            return file.read()

    # количество вхождений каждой подстроки длины N+1
    def get_v_ij(self):
        d = {}
        for i in range(len(self.X) - self.N):
            key = self.X[i:i + self.N]
            if key not in d:
                value = self.find_count(key)
                if value != 0:
                    d[key] = value
                if key[-self.N + 1:] == self.X[-self.N + 1:]:
                    key = key[-self.N + 1:] + bytes(' +EOF'.encode('utf8'))
                    d[key] = 1
        return d
    # количество вхождений любой подстроки длины N + 1, начинающихся с aiajak...a(n-1)*
    def get_v_j(self):
        d = {}
        for key, value in self.v_ij.items():
            key_new = key[:self.N - 1] + bytes('*'.encode('utf8'))
            v = 0
            if bytes(' +EOF'.encode('utf8')) in key:
                v = 1
            d[key_new] = v

        for key, value in self.v_ij.items():
            key_new = key[:self.N - 1] + bytes('*'.encode('utf8'))
            d[key_new] += value
        return d

    # абсолютная вероятность
    def get_p_ai(self):
        p_ai = {}
        for i in range(len(self.alph)):
            if self.alph[i] in self.X:
                key = self.alph[i]
                value = round(1 / len(self.alph), 6)
                p_ai[key] = value
        return p_ai

    # условная вероятность
    def get_p_aiaj(self):
        d = {}
        for key_ij, value_ij in self.v_ij.items():
            for key_j, value_j in self.v_j.items():
                if key_j[:self.N - 1] == key_ij[:self.N - 1]:
                    key = key_ij
                    value = round(value_ij / value_j, 6)
                    d[key] = value
        return d

    def get_inf(self):
        inf = 0
        for key, value in self.p_aiaj.items():
            inf += round(-math.log2(value), 3)
        for key, value in self.p_ai.items():
            inf += round(-math.log2(value), 3)
        return inf
