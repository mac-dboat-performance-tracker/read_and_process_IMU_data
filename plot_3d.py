import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def make_paddle():
    y = np.linspace(0, 0.82, 10)
    points_add = np.column_stack([np.zeros_like(y), y, np.zeros_like(y)])
    a = np.linspace(-0.08, 0, 3)
    b = np.linspace(0, 0.08, 3)
    points_add_1 = np.column_stack([a, a, np.zeros_like(a)])
    points_add_2 = np.column_stack([b, a[::-1], np.zeros_like(a)])
    c = np.linspace(-0.48, -0.08, 8)
    points_add_3 = np.column_stack([-0.08*np.ones_like(c), c, np.zeros_like(c)])
    points_add_4 = np.column_stack([0.08*np.ones_like(c), c, np.zeros_like(c)])
    d = np.linspace(-0.08, 0.08, 5)
    points_add_5 = np.column_stack([d, -0.48*np.ones_like(d), np.zeros_like(d)])
    points = np.vstack((points_add, points_add_1, points_add_2, points_add_3, points_add_4, points_add_5)).T
    return points

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
point_initial = make_paddle()
points = point_initial
scat = ax.scatter(points[0], points[1], points[2], c='green', s=15)
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
x_limits = [points[0].min(), points[0].max()]
y_limits = [points[1].min(), points[1].max()]
z_limits = [points[2].min(), points[2].max()]
max_range = max(
    x_limits[1] - x_limits[0],
    y_limits[1] - y_limits[0],
    z_limits[1] - z_limits[0]
) / 2.0
mid_x = np.mean(x_limits)
mid_y = np.mean(y_limits)
mid_z = np.mean(z_limits)
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)
ax.set_box_aspect([1, 1, 1])
plt.ion()
plt.show()

port = 'COM9'
baud = 9600
ser = serial.Serial(port, baud, timeout=1)
time.sleep(2)
while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            roll, pitch = map(float, line.split(','))
            yaw = 0
            # rotation around the x-axis (roll)
            R_x = np.array([[1,0,0],[0,np.cos(roll),-np.sin(roll)],[0,np.sin(roll),np.cos(roll)]])
            # rotation around the y-axis (pitch)
            R_y = np.array([[np.cos(pitch),0,np.sin(pitch)],[0,1,0],[-np.sin(pitch),0,np.cos(pitch)]])
            # rotation around the z-axis (yaw)
            R_z = np.array([[np.cos(yaw),-np.sin(yaw),0],[np.sin(yaw),np.cos(yaw),0],[0,0,1]])
            # create rotation matrix
            R = R_z @ R_y @ R_x
            points = R @ point_initial
            scat._offsets3d = (points[0], points[1], points[2])
            plt.draw()
            plt.pause(0.02)
        except ValueError:
            continue
