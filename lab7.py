import numpy as np
import time
import random
from matplotlib import pyplot as plt
from matplotlib import style
import csv
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import PIL

#1
m1 = [random.randint(-100000, 100000) for _ in range(1000000)]
m2 = [random.randint(-100000, 100000) for _ in range(1000000)]

n1 = np.array([random.randint(-100000, 100000) for _ in range(1000000)])
n2 = np.array([random.randint(-100000, 100000) for _ in range(1000000)])

t_start_n = time.perf_counter()
n = np.multiply(n1, n2)
all_time_n = time.perf_counter() - t_start_n


t_start_m = time.perf_counter()
for i in range(1000000):
    m = m1[i] * m2[i]

all_time_m = time.perf_counter() - t_start_m

if all_time_n<all_time_m:
    print(" яльно ")

#2
data = pd.read_csv('./data1.csv', sep=r'\s*;\s*', header=0, encoding='ansi', engine='python')

style.use('ggplot')

y = data['Положение дроссельной заслонки (%)'].to_numpy()
x = data['Время'].to_numpy()

plt.plot(x, y)

y = data['Угол опережения зажигания (°ПКВ)'].to_numpy()
x = data['Время'].to_numpy()

plt.xlabel('Время')
plt.ylabel('Положение дроссельной заслонки (%)/Угол опережения зажигания (°ПКВ)')

plt.title('График')

plt.plot(x, y)

plt.show()

#3 axes3d у меня не работал совсем((
fig = plt.figure()
ax_3d = fig.add_subplot(projection='3d')
x = np.arange(-10, 10, 0.01)
y = np.arange(-0.5, 0.5, 0.001)
xgrid, ygrid = np.meshgrid(x, y)
zgrid = np.tan(xgrid + ygrid)
ax_3d.set_xlabel('x')
ax_3d.set_ylabel('y')
ax_3d.set_zlabel('z')
ax_3d.plot_wireframe(xgrid, ygrid, zgrid)
plt.show()

#extra






