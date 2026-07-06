import numpy as np
import matplotlib.pyplot as plt
x=np.linspace(0,10,20)
y=np.sin(x)
err=0.2
plt.errorbar(x,y,yerr=err,fmt='o',capsize=4)
plt.show()