# 21
import numpy as np
def tensor_prod(A,B):
    a = np.array([A])
    b = np.array([B])
    prod = a.T@b
    ordem = b.size
    return prod.reshape(1,ordem)