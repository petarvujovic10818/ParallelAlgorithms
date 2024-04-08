import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

mod = SourceModule("""
     __global__ void multiply(float *a, float *b, float *c, int widthA, int widthB, int widthC, int heightC)
     {
          
          int tx = threadIdx.x; // kolona
          int ty = threadIdx.y; // vrsta

          if((ty < heightC) && (tx < widthC)) // zbog blocka i grida, kad je poslednji block < 32x32 da ne gleda ostale
          {
            float Rvalue = 0;
            for(int k=0; k < widthA; k++)
            {
              float Aelement = a[ty*widthA +k];
              float Belement = b[k*widthB +tx];
              Rvalue += Aelement * Belement;
            }
            c[ty*widthC + tx] = Rvalue;
          }
      }
   """)

# Matrica A
a = np.random.rand(2,7).astype(dtype=np.float32)
a = np.round(a, 1)
print("Matrica A:\n", a)

# Matrica B
b = np.random.rand(7,4).astype(dtype=np.float32)
b = np.round(b, 1)
print("Matrica B:\n", b)

# Rezultujuca matrica
pom = np.random.rand(2,4).astype(dtype=np.float32)
c = np.zeros_like(pom)

# alociranje CUDA memorije
a_gpu = cuda.mem_alloc(a.nbytes)  
b_gpu = cuda.mem_alloc(b.nbytes)
c_gpu = cuda.mem_alloc(c.nbytes)

# kopiranje Host TO Device
cuda.memcpy_htod(a_gpu, a)  
cuda.memcpy_htod(b_gpu, b)
cuda.memcpy_htod(c_gpu, c)

# priprema kernela za izvrsavanje
func = mod.get_function("multiply")  

# izrvrsavanje kernela... block=(x,y,z)
wa = np.int32(7)
wb = np.int32(4)
wc = np.int32(4)
hc = np.int32(2)
func(a_gpu,b_gpu,c_gpu,wa,wb,wc,hc, block=(4,2,1), grid=(1, 1, 1))  

# kopiranje Device TO Host
cuda.memcpy_dtoh(c, c_gpu)  
c = np.round(c, 2)
print("Rezultujuca matrica:\n", c)

# provera
result = np.matmul(a,b)
result = np.round(result,2)

np.allclose(result,c)
