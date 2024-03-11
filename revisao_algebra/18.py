# 18
import numpy as np

def dot_prod(A,B):
    a = np.array(A)
    b = np.array(B)
    return a @ b.T

dot_prod([1,2,3],[1,1,1])