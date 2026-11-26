import numpy as np

def my_gauss(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    N = len(b)
    if A.shape != (N, N): #si no es cuadrada no funciona
        raise ValueError("A debe ser cuadrada (N x N) y b de tamaño N")
    s = np.max(np.abs(A), axis=1)                   
    if np.any(s == 0): #si su determinante es 0 tiene infinitas soluciones y no funciona
        raise ValueError("Matriz singular")

    M = np.column_stack((A, b))                     
    for i in range(N):
        k = i + np.argmax(np.abs(M[i:, i]) / s[i:]) 
        if M[k, i] == 0:
            raise ValueError("Det = 0 y tiene infinitas soluciones")
        M[[i, k]] = M[[k, i]]                        
        s[[i, k]] = s[[k, i]]                        
        M[i] /= M[i, i]                             
        f = M[:, i].copy()
        f[i] = 0                                     
        M -= f[:, None] * M[i]                       
    return M[:, N]      



