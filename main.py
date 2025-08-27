
# Activation
# source venv/bin/activate

# pip install numpy matplotlib PyQt6 python-dotenv

# Deactivation
# deactivate

import matplotlib
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from dotenv import load_dotenv

matplotlib.use('QtAgg')
load_dotenv()
N = int(os.getenv("N"))
L = float(os.getenv("L"))
d = float(os.getenv("d"))
w = float(os.getenv("w"))
m0 = 4 * np.pi * 10**-7
M0 = 48 * 10**3

def above_field(x, z, terms):
    Bx = np.zeros_like(x)
    By = np.zeros_like(x)
    Bz = np.zeros_like(x)

    for n in range(1, 2 * terms, 2):
        Bx += -2 * m0 * M0 / (n * np.pi) * (np.exp(n * np.pi / L * (z - L)) - np.exp(n * np.pi / L * (z + L))) * np.cos(n * np.pi * x / L)
        Bz += -2 * m0 * M0 / (n * np.pi) * (np.exp(n * np.pi / L * (z - L)) - np.exp(n * np.pi / L * (z + L))) * np.sin(n * np.pi * x / L)
    return (Bx, By, Bz)

def inside_field(x, z, terms):
    Bx = np.zeros_like(x)
    By = np.zeros_like(x)
    Bz = np.zeros_like(x)

    for n in range(1, 2 * terms, 2):
        Bx += -2 * m0 * M0 / (n * np.pi) * (np.exp(n * np.pi / L * (z - d)) - np.exp(-1 * n * np.pi / L * (z + d))) * np.cos(n * np.pi * x / L)
        Bz += -2 * m0 * M0 / (n * np.pi) * (np.exp(n * np.pi / L * (z - d)) + np.exp(-1 * n * np.pi / L * (z + d)) - 2) * np.sin(n * np.pi * x / L)
    return (Bx, By, Bz)

# def square_wave_fourier(x, terms):
#     """Calculates the Fourier series approximation of a square wave."""
#     y = np.zeros_like(x)
#     for n in range(1, 2 * terms, 2):  # n = 1, 3, 5, ...
#         y += (4 / (np.pi * n)) * np.sin(n * x)
#     return y

fig = plt.figure(figsize=(14, 6))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')

# Define the vertices of a magnetic domain
magnetic_unit_domain = np.array([
    [0, 0, -d / 2], [L, 0, -d / 2], [L, w, -d / 2], [0, w, -d / 2],  # Bottom face
    [0, 0, d / 2], [L, 0, d / 2], [L, w, d / 2], [0, w, d / 2]   # Top face
])

# Define the faces of the magnetic domain, excluding the top face
magnetic_domain_faces = [
    [0, 1, 2, 3],  # Bottom face
    [0, 1, 5, 4],  # Front face
    [1, 2, 6, 5],  # Right face
    [2, 3, 7, 6],  # Back face  
    [3, 0, 4, 7]   # Left face
]

x = np.linspace(0, N * L, 40)
y = np.linspace(0, w, 5)
x1, y1, z1 = np.meshgrid(x, y, np.linspace(d / 2, d, 30))
U1, V1, W1 = above_field(x1, z1, int(os.getenv("TERMS")))
x2, y2, z2 = np.meshgrid(x, y, np.linspace(-d / 2, d / 2, 30))
U2, V2, W2 = inside_field(x2, z2, int(os.getenv("TERMS")))

for i in range(N):
    offset = i * L
    magnetic_domain = magnetic_unit_domain + [offset, 0, 0]

    if i % 2 == 0:
        box_faces = Poly3DCollection([magnetic_domain[face] for face in magnetic_domain_faces], linewidths=1, edgecolors='b', alpha=.25)
    else:
        box_faces = Poly3DCollection([magnetic_domain[face] for face in magnetic_domain_faces], linewidths=1, edgecolors='m', alpha=.25)
    ax1.add_collection3d(box_faces)

ax2 = fig.add_subplot(1, 2, 2)

# Define the vertices for the 2D xz-projection of the bottom face
# This is a square on the xz plane
xz_faces = [
    [0, 1, 5, 4], # Front face (projected)
    [1, 2, 6, 5], # Right face (projected)
    [2, 3, 7, 6], # Back face (projected)
    [3, 0, 4, 7]  # Left face (projected)
]


# Plot the xz projection of the four side faces
for i in range(N):
    offset = i * L
    magnetic_domain = magnetic_unit_domain + [offset, 0, 0]

    # Plot the 2D faces of the boxes
    for face in xz_faces:
        x_coords = [magnetic_domain[v][0] for v in face]
        z_coords = [magnetic_domain[v][2] for v in face]
        if i % 2 == 0:
            ax2.fill(x_coords, z_coords, alpha=0.3, color='b', edgecolor='b')
        else:
            ax2.fill(x_coords, z_coords, alpha=0.3, color='m', edgecolor='m')

x_buffer = N * L * 0.2
z_buffer = 2 * d * 0.2

# 1st subplot
# Set axis limits and labels
ax1.set_xlim([-x_buffer, N * L + x_buffer])
ax1.set_ylim([0, w])
ax1.set_zlim([-d / 2 - z_buffer, d / 2 + z_buffer])
ax1.set_xlabel('X-axis')
ax1.set_ylabel('Y-axis')
ax1.set_zlabel('Z-axis')
ax1.set_title("Magnetic Induction Field B(x,y,z)")
# ax1.quiver(x, y, z, U2, V2, W2, length=0.1)

# 2nd subplot
# Set axis limits and labels
ax2.set_xlim([-x_buffer, N * L + x_buffer])
ax2.set_ylim([-d / 2 - z_buffer, d / 2 + z_buffer])
ax2.set_xlabel('X-axis')
ax2.set_ylabel('Z-axis')
ax2.set_title("XZ Projection B(x,z)")
ax2.set_aspect('auto')
ax2.grid()
ax2.quiver(x1[y1 == 0], z1[y1 == 0], U1[y1 == 0], W1[y1 == 0])
ax2.quiver(x2[y1 == 0], z2[y1 == 0], U2[y1 == 0], W2[y1 == 0])

plt.tight_layout() # Adjust subplots to fit in figure area
plt.show()
# plt.savefig('my_plot.png')
# plt.savefig('my_plot.png')
# print("Image saved as 'my_plot.png'")
