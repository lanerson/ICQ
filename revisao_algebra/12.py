# 12
import matplotlib.pyplot as plt
import numpy as np
def exps(c):
    cs = [c**n for n in range(1,11)]
    x = np.arange(1,11)
    plt.plot(x,cs,label=f"potencias de {c}")
    plt.legend()
    plt.show()
    
exps(2)