import wikipedia
import transliterate
import multiprocessing as mp
from functools import reduce
import itertools

wikipedia.set_lang("sr")

def get_pages(query, results=2):
  pages = wikipedia.search(transliterate.translit(query, 'sr'), results = results)
  return pages

def sanitize(array, title):
  try:
    wikipedia.page(title)
    array.append(title)
  except:
    print('Error')
  return array

def page_summary(title):
    return wikipedia.summary(title, sentences=2)

a = ['Beograd', 'Košarka', 'Mikroprocesor']

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    x = pool.map(get_pages, a)
    c = list(itertools.chain.from_iterable(x))
    y = reduce(sanitize, c, [])
    z = pool.map(page_summary, y)
    print(z)