import RLE
from SourceMarkov import SourceMarkov
import sys

file = 'lya'
N = 1
I = SourceMarkov(file, N)
print(I.get_inf(), 'бит')
print(I.get_inf()/8, 'байт')

with open('C:\\Users\\march\\PycharmProjects\\LabaOTICYea\\Frankenstein, by Mary Wollstonecraft (Godwin) Shelley.txt', "rb") as f:
    x = f.read()

print((RLE.codeste(x.decode("utf8"))))
print(RLE.decodeste(RLE.codeste(x.decode("utf8"))))
'''
print((RLE.codeste("qwertyqqqqqwerttttyqwerr")))
print(RLE.decodeste(RLE.codeste("qwertyqqqqqwerttttyqwerr")))
'''