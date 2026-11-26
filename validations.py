from scipy.linalg import solve
import numpy as np
import mymath as mm

A = [[1,  1,  1],
     [1,  1, -1],
     [1, -2,  0]]
b = [50000, 15000, 0]

                                 
def np_solve(A, b):
    return np.linalg.solve(A, b)

print(mm.my_gauss(A,b))
print(np_solve(A,b))
      
  
