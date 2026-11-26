from scipy.linalg import solve
import numpy as np

A = [[1,  1,  1],
     [1,  1, -1],
     [1, -2,  0]]
b = [50000, 15000, 0]

def my_gauss(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    N = len(b)
    if A.shape != (N, N):
        raise ValueError("A debe ser cuadrada (N x N) y b de tamaño N")
    s = np.max(np.abs(A), axis=1)                    
    if np.any(s == 0):
        raise ValueError("Matriz singular")

    M = np.column_stack((A, b))                     
    for i in range(N):
        k = i + np.argmax(np.abs(M[i:, i]) / s[i:])  
        if M[k, i] == 0:
            raise ValueError("Matriz singular")
        M[[i, k]] = M[[k, i]]                      
        s[[i, k]] = s[[k, i]]                        
        M[i] /= M[i, i]                              
        f = M[:, i].copy()
        f[i] = 0                                     
        M -= f[:, None] * M[i]                      
    return M[:, N]                                  
def np_solve(A, b):
    return np.linalg.solve(A, b)

print(my_gauss(A,b))
print(np_solve(A,b))
      
  
