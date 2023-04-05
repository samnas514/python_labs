import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax_3d = fig.add_subplot(projection='3d')
x = np.arange(-10, 10, 0.01)
y = np.arange(-0.5, 0.5, 0.001)
xgrid, ygrid = np.meshgrid(x, y)
zgrid = np.tan(xgrid + ygrid)
ax_3d.plot_wireframe(xgrid, ygrid, zgrid)
plt.show()