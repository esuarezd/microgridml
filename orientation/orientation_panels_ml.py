import matplotlib.pyplot as plt
import numpy as np

# Parámetros
azimut = np.radians(45)  # Convertir a radianes
inclinación = np.radians(15)  # Convertir a radianes

# Coordenadas esféricas a cartesianas
r = 1  # Radio
x = r * np.sin(inclinación) * np.cos(azimut)
y = r * np.sin(inclinación) * np.sin(azimut)
z = r * np.cos(inclinación)

# Dibujo
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(0, 0, 0, x, y, z, color='r', label='Panel')
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.legend()
plt.show()
