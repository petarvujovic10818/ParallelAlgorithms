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
red = [ Queue() for i in range(n * n) ]
currentState = kopirajStanje(steps[0])
repetitions=50
ready = 0
condition = threading.Condition()



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

def komsije(n):
  for x in range(n):
    for y in range(n):
      for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        row = (x + i) % n
        column = (y + j) % n
        red[n*row+column].put(currentState[x][y])

def calculate(x,y):
    global currentState
    global ready
    
    neighbours= 0
    #print(list(red[n*x+y].queue))
    for i in range(8):
        k=red[n*x+y].get()
        neighbours+=k
    currentState[x][y] = willBeAlive(currentState[x][y],neighbours)
    ready+=1

    condition.acquire()
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
komsije(n)
for k in range(repetitions):
  for i in range(n):
      for j in range(n):
        t = threading.Thread(target=calculate, args=(i,j))
        t.start()
        threads.append(t)
  komsije(n)

  for t in threads:
      t.join()



#prikaz
anim = animate(steps);
HTML(anim.to_html5_video())