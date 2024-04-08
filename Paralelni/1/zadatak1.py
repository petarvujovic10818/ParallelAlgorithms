from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython.display import HTML
import numpy as np
from queue import Queue, Empty
import threading


def kopirajStanje(a): 
    b =[] 
    b = a.copy() 
    return b 

#globalne
n = 10
steps = [(np.random.rand(n ** 2).reshape(n, n) > 0.5).astype(np.int8)]
currentState = kopirajStanje(steps[0])
repetitions=50
ready = 0
condition = threading.Condition()
semafori = [[threading.Semaphore(0)] * n for i in range(n * n)]
brojaci = [[0] * n for _ in range(n)]
sinhSemafor = threading.Semaphore(1)
kljuc = threading.Lock()



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

def willBeAlive(vrednost,brojZivihKomsija):
   if (brojZivihKomsija < 2) or (brojZivihKomsija > 3): 
      return 0 
   if vrednost  == 1:
      return 1 
   if brojZivihKomsija == 3: 
      return 1
   return vrednost

def calculate(x,y):
    global n
    global steps
    global currentState
    global ready
    global condition
    global semafori
    global brojaci
    global sinhSemafor
    global kljuc
    
    neighbours = 0
    
    for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        row = (x + i) % n
        column = (y + j) % n
        neighbours += currentState[row][column]
        
        sinhSemafor.acquire() #sinhronizacija suseda koji menjaju vrednost brojaca
        brojaci[row][column]+=1 #lista brojaca suseda
        if brojaci[row][column]==8: 
          brojaci[row][column]=0
          semafori[row][column].release() #poslednji sused budi semaforom
        sinhSemafor.release()

    semafori[x][y].acquire() #kad je semafor pustio moze da upise novu vrednost
    currentState[x][y] = willBeAlive(currentState[x][y],neighbours)
    

     
    condition.acquire() #conditionom zasticen i brojac celija
    ready+=1

    if ready == n ** 2:
      steps.append(kopirajStanje(currentState))
      ready = 0
      condition.notifyAll()
      condition.release()
    else:
      condition.wait()
      condition.release()
    


#main
threads=[]

for k in range(repetitions):
  for i in range(n):
    for j in range(n):
      t = threading.Thread(target=calculate, args=(i,j))
      t.start()
      threads.append(t)

for t in threads:
  t.join()



#prikaz
anim = animate(steps);
HTML(anim.to_html5_video())