
# Activation
# source venv/bin/activate

# Deactivation
# deactivate

import matplotlib
import os
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from dotenv import load_dotenv
from matplotlib.axes import Axes
from numpy.typing import NDArray
from typing import List

matplotlib.use('QtAgg')
load_dotenv()
TERMS = int(os.getenv("TERMS"))
N = int(os.getenv("N"))
L = float(os.getenv("L"))
d = float(os.getenv("d"))
w = float(os.getenv("w"))
m0 = 4 * np.pi * 10**-7
M0 = 48 * 10**3
x_buffer = N * L * 0.2
z_buffer = 2 * d * 0.2

def above_field(x, z, terms):
    """
    Calculates the Magnetic Field B above the sample

    Args:
        x: x-coordinate
        z: z-coordinate
        terms: Number of terms provided to the fourier series
    """
    Bx = np.zeros_like(x)
    Bz = np.zeros_like(x)
    for n in range(1, 2 * terms, 2):
        c = 2 * m0 * M0 / (n * np.pi) * (np.exp(-n * np.pi / L * (z - d)) - np.exp(-n * np.pi / L * (z + d)))
        Bx += -c * np.cos(n * np.pi * x / L)
        Bz += c * np.sin(n * np.pi * x / L)
    return (Bx, Bz)


def inside_field(x, z, terms):
    """
    Calculates the Magnetic Field B inside the sample

    Args:
        x: x-coordinate
        z: z-coordinate
        terms: Number of terms provided to the fourier series
    """
    Bx = np.zeros_like(x)
    Bz = np.zeros_like(x)
    for n in range(1, 2 * terms, 2):
        Bx += -2 * m0 * M0 / (n * np.pi) * (np.exp(n * np.pi / L * (z - d)) - np.exp(-1 * n * np.pi / L * (z + d))) * np.cos(n * np.pi * x / L)
        Bz += -2 * m0 * M0 / (n * np.pi) * (np.exp(n * np.pi / L * (z - d)) + np.exp(-1 * n * np.pi / L * (z + d)) - 2) * np.sin(n * np.pi * x / L)
    return (Bx, Bz)


def below_field(x, z, terms):
    """
    Calculates the Magnetic Field B below the sample

    Args:
        x: x-coordinate
        z: z-coordinate
        terms: Number of terms provided to the fourier series
    """
    Bx = np.zeros_like(x)
    Bz = np.zeros_like(x)
    for n in range(1, 2 * terms, 2):
        c = 2 * m0 * M0 / (n * np.pi) * (np.exp(n * np.pi / L * (z - d)) - np.exp(n * np.pi / L * (z + d)))
        Bx += -c * np.cos(n * np.pi * x / L)
        Bz += -c * np.sin(n * np.pi * x / L)
    return (Bx, Bz)


def sample_projection(ax: Axes, unit_domain: NDArray[np.float64], faces: List[List[int]]):
    """
    Creates the sample's Magnetic Field XZ projection subplot

    Args:
        ax: The figure's axis system
        unit_domain: The box representation of a magnetic domain
        faces: A list of lists representing each face of the box-shaped domain
    """
    ax.set_xlim([(N / 2 - 0.2) * L, (N / 2 + 3.2) * L])
    ax.set_ylim([-d / 2 - 0.5 * z_buffer, d / 2 + 0.5 * z_buffer])
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('z (mm)')
    ax.set_title("XZ Projection B(x,z)")
    ax.set_aspect('auto')
    ax.grid()
    for i in range(N):
        offset = i * L
        magnetic_domain = unit_domain + [offset, 0, 0]
        for face in faces:
            x_coords = [magnetic_domain[v][0] for v in face]
            z_coords = [magnetic_domain[v][2] for v in face]
            if i % 2 == 0:
                ax.fill(x_coords, z_coords, alpha=0.3, color='b', edgecolor='b')
            else:
                ax.fill(x_coords, z_coords, alpha=0.3, color='m', edgecolor='m')
    x_up, z_up = np.meshgrid(np.linspace(0, N * L, 186), np.linspace(d / 2, 3 * d / 2, 20))
    Bx_up, Bz_up = above_field(x_up, z_up, TERMS)
    x_in, z_in = np.meshgrid(np.linspace(0, N * L, 186), np.linspace(-d / 2, d / 2, 20))
    Bx_in, Bz_in = inside_field(x_in, z_in, TERMS)
    x_d, z_d = np.meshgrid(np.linspace(0, N * L, 186), np.linspace(-3 * d / 2, -d / 2, 20))
    Bx_d, Bz_d = below_field(x_d, z_d, TERMS)
    ax.quiver(x_in, z_in, Bx_in, Bz_in, scale=1.4)
    # ax.quiver(x_d, z_d, Bx_d, Bz_d)
    # ax.quiver(x_up, z_up, Bx_up, Bz_up)



def magnetic_field(ax: Axes, unit_domain: NDArray[np.float64], faces: List[List[int]]):
    """
    Creates the sample's Magnetic Field 3D representaion subplot

    Args:
        ax: The figure's axis system
        unit_domain: The box representation of a magnetic domain
        faces: A list of lists representing each face of the box-shaped domain
    """
    ax.set_xlim([-x_buffer, N * L + x_buffer])
    ax.set_ylim([0, w])
    ax.set_zlim([-d / 2 - z_buffer, d / 2 + z_buffer])
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_zlabel('z (mm)')
    ax.set_title("Magnetic Induction Field B(x,y,z)")
    for i in range(N):
        offset = i * L
        magnetic_domain = unit_domain + [offset, 0, 0]
        if i % 2 == 0:
            box_faces = Poly3DCollection([magnetic_domain[face] for face in faces], linewidths=1, edgecolors='b', alpha=.25)
        else:
            box_faces = Poly3DCollection([magnetic_domain[face] for face in faces], linewidths=1, edgecolors='m', alpha=.25)
        ax.add_collection3d(box_faces)
    x = np.linspace(0, N * L, 25)
    y = np.linspace(0, w, 3)
    z = np.linspace(-d / 2, d / 2, 3)
    # x_up, y_up, z_up = np.meshgrid(x, y, np.linspace(d / 2, 3 * d / 2, 20))
    # Bx_up, Bz_up = above_field(x_up, z_up, int(os.getenv("TERMS")))
    x_in, y_in, z_in = np.meshgrid(x, y, z)
    Bx_in, Bz_in = inside_field(x_in, z_in, TERMS)
    ax.quiver(x_in, y_in, z_in, Bx_in, np.zeros_like(x_in), Bz_in, length=0.001, color='k')


def main():
    magnetic_unit_domain = np.array([
        [0, 0, -d / 2], [L, 0, -d / 2], [L, w, -d / 2], [0, w, -d / 2],  # Bottom face
        [0, 0, d / 2], [L, 0, d / 2], [L, w, d / 2], [0, w, d / 2]])   # Top face

    magnetic_domain_faces = [
        [0, 1, 2, 3],  # Bottom face
        [0, 1, 5, 4],  # Front face
        [1, 2, 6, 5],  # Right face
        [2, 3, 7, 6],  # Back face  
        [3, 0, 4, 7]]  # Left face

    xz_faces = [
        [0, 1, 5, 4], # Front face (projected)
        [1, 2, 6, 5], # Right face (projected)
        [2, 3, 7, 6], # Back face (projected)
        [3, 0, 4, 7]  # Left face (projected)
    ]

    fig = plt.figure(figsize=(21, 7))
    ax2 = fig.add_subplot(1, 2, 1)
    sample_projection(ax2, magnetic_unit_domain, xz_faces)
    ax3 = fig.add_subplot(1, 2, 2, projection='3d')
    magnetic_field(ax3, magnetic_unit_domain, magnetic_domain_faces)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()