from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import threading

def copyMatrix(a):
    b = []
    b = a.copy()
    return b

n = 20
matrix = np.random.randint(2, size=(n,n))
nizMatrica = []
nizMatrica.append(matrix)
curr_state = copyMatrix(nizMatrica[0])
uslov = threading.Condition() 
brojaci = [[0] * n for _ in range(n)] 
semaforx = threading.Semaphore(0)
mutex = threading.Semaphore(1)
iter = 50
cell_counter = 0

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

def izracunaj(x,y, it = 50):
    global n
    global matrix
    global curr_state
    global cell_counter

    for i in range(it):
        neighbours = 0
        for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]: 
            row = (x + i) % n 
            column = (y + j) % n 
            neighbours += curr_state[row][column] 
            mutex.acquire()
            brojaci[row][column] += 1
            if brojaci[row][column] == 8:
                brojaci[row][column] = 0
                semaforx.release()
            mutex.release()

        semaforx.acquire()
        curr_state[x][y] = isAlive(curr_state[x][y],neighbours)

        uslov.acquire()
        cell_counter += 1

        if cell_counter != n*n:
            uslov.wait()
        else:
            nizMatrica.append(copyMatrix(curr_state))
            cell_counter = 0
            uslov.notifyAll()
        uslov.release()

threads = []

for i in range(n):
    for j in range(n):
        t = threading.Thread(target=izracunaj, args=(i, j))
        threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

anim = animate(nizMatrica)
plt.show()