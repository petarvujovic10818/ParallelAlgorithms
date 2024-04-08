import numpy as np
import math
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule


  
mod = SourceModule("""
      #define TILE_WIDTH 32

      __global__ void multiply(float * A, float * B, float * C,
                  int numARows, int numAColumns,
                  int numBRows, int numBColumns,
                  int numCRows, int numCColumns) {

          __shared__ float ds_M[TILE_WIDTH][TILE_WIDTH];
          __shared__ float ds_N[TILE_WIDTH][TILE_WIDTH];
          int bx = blockIdx.x, by = blockIdx.y,
            tx = threadIdx.x, ty = threadIdx.y,
            Row = by * TILE_WIDTH + ty,
            Col = bx * TILE_WIDTH + tx;
          float Pvalue = 0;

          for (int m = 0; m < (numAColumns-1)/TILE_WIDTH+1; ++m) {
            if (Row < numARows && m*TILE_WIDTH+tx < numAColumns)
                ds_M[ty][tx] = A[Row*numAColumns + m*TILE_WIDTH+tx];
            else
                ds_M[ty][tx] = 0;
            if (Col < numBColumns && m*TILE_WIDTH+ty < numBRows)
                ds_N[ty][tx] = B[(m*TILE_WIDTH+ty)*numBColumns+Col];
            else
                ds_N[ty][tx] = 0;

            __syncthreads();
            for (int k = 0; k < TILE_WIDTH; ++k)
                Pvalue += ds_M[ty][k] * ds_N[k][tx];
            __syncthreads();
          }
          if (Row < numCRows && Col < numCColumns)
            C[Row*numCColumns+Col] = Pvalue;
      }
   """)

# Matrica A
a_rows = np.int32(437)
a_cols = np.int32(352)
a = np.random.rand(a_rows,a_cols).astype(dtype=np.float32)
a = np.round(a, 1)
print("Matrica A:\n", a)

# Matrica B
b_rows = np.int32(352)
b_cols = np.int32(379)
b = np.random.rand(b_rows,b_cols).astype(dtype=np.float32)
b = np.round(b, 1)
print("Matrica B:\n", b)

# Rezultujuca matrica
c_rows = a_rows
c_cols = b_cols
pom = np.random.rand(c_rows,c_cols).astype(dtype=np.float32)
#pom = np.round(pom,1)
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
func(a_gpu,b_gpu,c_gpu,a_rows,a_cols,b_rows,b_cols,c_rows,c_cols, block=(32,32,1), grid=(math.ceil(c.shape[1]/32), math.ceil(c.shape[0]/32), 1))  

# provera
result = np.matmul(a,b)
result = np.round(result,2)
print("Correct result:\n",result)
# kopiranje Device TO Host
cuda.memcpy_dtoh(c, c_gpu)  
c = np.round(c, 2)
print("My result:\n", c)


np.allclose(result,c)
