from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue
import threading

def copyMatrix(a):
    b =[]
    b = a.copy()
    return b

n = 20
matrix = np.random.randint(2, size=(n,n))
nizMatrica = []
nizMatrica.append(matrix)
curr_state = copyMatrix(nizMatrica[0])
cell_counter = 0
red = [Queue() for i in range(n * n)]
uslov = threading.Condition()
it = 50

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

def popuniNiz(n):
    for x in range(n):
        for y in range(n):
            for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                row = (x + i) % n
                column = (y + j) % n
                red[n * row + column].put(curr_state[x][y])

def izracunaj(x,y):
    global curr_state
    global cell_counter

    neighbours = 0
    for i in range(8):
        k = red[n * x + y].get()
        neighbours += k
    curr_state[x][y] = isAlive(curr_state[x][y], neighbours)
    cell_counter += 1
    uslov.acquire()
    if cell_counter != n * n:
        uslov.wait()
    else:
        nizMatrica.append(copyMatrix(curr_state))
        cell_counter = 0
        uslov.notifyAll()
    uslov.release()

threads = []
popuniNiz(n)
for k in range(it):
    for i in range(n):
        for j in range(n):
            t = threading.Thread(target=izracunaj, args=(i, j))
            t.start()
            threads.append(t)
    popuniNiz(n)

for t in threads:
    t.join()

anim = animate(nizMatrica)
plt.show()