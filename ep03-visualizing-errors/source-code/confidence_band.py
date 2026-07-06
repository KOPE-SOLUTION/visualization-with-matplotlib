import numpy as np
import matplotlib.pyplot as plt
x=np.linspace(0,10,200)
y=np.sin(x)
err=0.2
plt.plot(x,y)
plt.fill_between(x,y-err,y+err,alpha=0.2)
plt.show()