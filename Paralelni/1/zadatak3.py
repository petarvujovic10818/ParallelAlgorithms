from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython.display import HTML
import numpy as np
import multiprocessing
from multiprocessing import Queue, Value, Manager, Array, Condition
import copy


def kopirajStanje(a): 
    b =[] 
    b = copy.copy(a) 
    return b 

#globalne
n = 10
repetitions=15
manager = Manager()
steps = manager.list()
steps.append((np.random.rand(n ** 2).reshape(n, n) > 0.5).astype(np.int8))
red = [ Queue() for i in range(n * n) ]
ready = Value('i', 0)
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

def willBeAlive(vrednost,brojZivihKomsija):
   if (brojZivihKomsija < 2) or (brojZivihKomsija > 3): 
      return 0 
   if vrednost  == 1:
      return 1 
   if brojZivihKomsija == 3: 
      return 1
   return vrednost
  

def calculate(x,y,itr,val):
    
    neighbours= 0
    for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        row = (x + i) % n
        column = (y + j) % n
        red[n*row+column].put(val)

    
    for i in range(8):
        k=red[n*x+y].get()
        neighbours+=k

    val = willBeAlive(val,neighbours)

    historyQueue.put((x,y,itr,val))

    condition.acquire()
    ready.value+=1
    
    if ready.value == n ** 2:
      ready.value = 0
      matrix = steps[-1]
      matrix[x][y] = val
      steps[-1] = matrix
      steps.append(matrix)
      condition.notify_all()
      condition.release()
    else:
      matrix = steps[-1]
      matrix[x][y] = val
      steps[-1] = matrix
      condition.wait()
      condition.release()


#main
procesi=[]
for k in range(repetitions):
  for i in range(n):
      for j in range(n):
        t = multiprocessing.Process(target=calculate, kwargs={"x": i, "y": j,"itr": k, "val": steps[k][i][j]})
        t.start()
        procesi.append(t)

  for t in procesi:
      t.join()



#prikaz
anim = animate(steps);
HTML(anim.to_html5_video())