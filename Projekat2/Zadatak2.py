from functools import reduce
import re


def unos_texta():
    text = input('Enter text: ')
    text = text.lower()
    text = re.sub('\W+', ' ', text)
    return text


def metoda(array, text):
    words = text.split()
    x = []
    for word in words:
        if word in array:
            continue
        else:
            array.append(word)
            x.append((word, 0))
    return x


def contr_map(word):
    return word, 1


text = unos_texta()
text2 = unos_texta()

text3 = text + ' ' + text2

a = text.split()
aa = text2.split()
aaa = text3.split()
#x = list(reduce(metoda, aaa, []))
x = metoda([], text3)
#print(x)

c = list(map(contr_map, a))
cc = list(map(contr_map, aa))
ccc = list(map(contr_map, aaa))

c_sort = sorted(c, key=lambda x: x[0])
cc_sort = sorted(cc, key=lambda x: x[0])
ccc_sort = sorted(ccc, key=lambda x: x[0])

def key_add(array, value):
    if array and array[-1][0] == value[0]:
        array[-1] = array[-1][0], array[-1][1] + value[1]
    else:
        array.append(value)
    return array


reduced = reduce(key_add, c_sort, [])
reduced2 = reduce(key_add, cc_sort, [])
reduced3 = reduce(key_add, ccc_sort, [])


print(reduced)
print(reduced2)
print(reduced3)