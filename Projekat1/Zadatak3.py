from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython.display import HTML
import numpy as np
from queue import Queue
import multiprocessing
from multiprocessing import Value,Queue,Manager

def copyMatrix(a):
    b =[]
    b = a.copy()
    return b

n = 10
repetitions = 15
matrix = np.random.randint(2, size=(n,n))
manager = Manager()
nizMatrica = manager.list()
nizMatrica.append(matrix)
red = [Queue() for i in range(n * n)]
cell_counter = Value('i', 0)
condition = multiprocessing.Condition()
historyQueue = multiprocessing.Queue()

def animate(steps):
    def init():
        im.set_data(steps[0])
        return [im]

    def animate(i):
        im.set_data(steps[i])
        return [im]

    im = plt.matshow(steps[0], interpolation='None', animated=True);

    anim = FuncAnimation(im.get_figure(), animate, init_func=init,
                         frames=len(steps), interval=500, blit=True, repeat=False);
    return anim

def isAlive(celija, brojZivihSuseda):
    if brojZivihSuseda < 2 or brojZivihSuseda > 3:
        return 0
    if celija == 1 and (brojZivihSuseda == 2 or brojZivihSuseda == 3):
        return 1
    if celija == 0 and brojZivihSuseda == 3:
        return 1
    return celija

def izracunaj(x,y,itr,val):
    neighbours = 0
    for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        row = (x + i) % n
        column = (y + j) % n
        red[n * row + column].put(val)

    for i in range(8):
        k = red[n * x + y].get()
        neighbours += k

    val = isAlive(val, neighbours)

    historyQueue.put((x, y, itr, val))
    condition.acquire()
    cell_counter.value += 1

    if cell_counter.value != n * n:
        curr_matrix = nizMatrica[-1]
        curr_matrix[x][y] = val
        nizMatrica[-1] = curr_matrix
        condition.wait()
    else:
        cell_counter.value = 0
        curr_matrix = nizMatrica[-1]
        curr_matrix[x][y] = val
        nizMatrica[-1] = curr_matrix
        nizMatrica.append(curr_matrix)
        condition.notify_all()
    condition.release()

procesi = []
for k in range(repetitions):
    for i in range(n):
        for j in range(n):
            t = multiprocessing.Process(target=izracunaj, kwargs={"x": i, "y": j, "itr": k, "val": nizMatrica[k][i][j]})
            t.start()
            procesi.append(t)

    for t in procesi:
        t.join()

anim = animate(nizMatrica)
HTML(anim.to_html5_video()) #otvoriti u google colabu
#plt.show()