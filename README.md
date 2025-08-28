<div align="center">
  <img src="https://raw.githubusercontent.com/chrisov/Magnetic-Induction-Field-Representation/39133463841233210d71938049d8269b641bcc5e/Logo.png" alt="logo" width="300"/>
</div>

<div align="center">

### 🛠 Python
### 🛠 Docker

</div>
<br>

# SrFe<sub>12</sub>O<sub>19</sub> Magnetic Field B(x,z)

This project works as complementary visualization of my Bachelor thesis 'Μagnetization orientation of a rectangular ferromagnet, by displacement of its magnetic walls by a constant external magnetic field´. It utlilizes the formulas developed in the paper to visualize the ferromagnet's magnetic field. The program creates a figure with two subplots, one of the XZ projection of the sample, and a 3D one and it plots the magnetic field B(x,z) produced in the space below, inside and above, in an interactive Qt environment.

## Interactive environment

When run, the Qt environmental framework is fully interactive, where it is possilble to traverse through the grid, rotate, zoom in/out and more, using the corresponding buttons in the menu on the top, as shown in the image below.

![alt text](https://raw.githubusercontent.com/chrisov/Magnetic-Induction-Field-Representation/ce69af2ce0cae1b9dbad89aa9abbcec8e9956095/Example.png)

## Technical details

- The project utilizes the numpy and Matplotlib libraries in its core, in order to make the necessary calculations, as well as plot the results for the magnetic field B(x,z).
- There are distinct functions that calculate B, according to the appropriate formula (see Fig. 2)
- There are distinct functions to plot each subplot in the resulting figure, both painting both the magnetic domains, as well as the vector field B.
- A brief description of a few key variables follows:
  - **magnetic_unit_domain** *(NDArray[np.float64])*: Defines the vertices of a rectangular box, in a 3D coordinate system. Each inner list represents a single vertex (a point in 3D space) with its (x, y, z) coordinates.
  - **magnetic_domain_faces** *(List[List[int]])*: Serves as a blueprint to tell the plotting function how to connect the vertices of a shape to form its surfaces. Each inner list represents a single face of the object and the numbers inside each list are indices that correspond to the positions of vertices in a separate array.
  - **xz_faces** *(List[List[int]])*: Same as 'magnetic_domain_faces', used to create the projected boxes in the first XZ projection subplot.

## Docker Container

The project is developed in a slim Python based docker container, which includes all the necessary dependencies and tools to run and execute. It is noted that a container being a command-line environment by default (headless environment), cannot natively support an interactive 3D graph because it lacks a graphical display server. However, this functionality is enabled by using X11 forwarding, which allows a container to use the host machine's display to render its graphical output. X11 forwarding creates a secure tunnel between the container and the host's X server, allowing the containerized application to draw its windows on the host's screen.

The container runs using the following commands (Linux):

1. Allow the host's X server to accept graphical connections from a Docker container:

```bash
xhost +local:docker
```

2. Run the container:

```bash
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix mag:1.0
```

## .env

The program defines a few useful contants, relative to the experimental process conducted, during the thesis production, in the .env file. The default values describe the actual values used, during the experimental process.

| Picture                | Description       |
|------------------------|-------------------|
| ![Alt text](https://raw.githubusercontent.com/chrisov/Magnetic-Induction-Field-Representation/74e3bee39d4a95351ebb091e92efa870cf927714/Env.png) | - **N**: The number of magnetic domains the sample consists of.<br> - **TERMS**: The number of Fourier terms used for calculating the magnetic field B (*Theory: Fig. 2*).<br> - **L**: The sample's length.<br> - **w**: The sample's width.<br> - **d**: The sample's height.|

## Theory

The ferromagnet is of rectangular shape, with dimensions *70 x 10 x 1 (mm)* (Fig. 1). It is consisted of magnetic domains of alternating magnetization along its length. More simply said, it is like combining multiple magnets of up, down, up, etc polarity one next to the other, in a one rigid body.

<div align="center">
  <img src="https://raw.githubusercontent.com/chrisov/Magnetic-Induction-Field-Representation/5b5f98f92a2903e21c18301c463463a015f24419/Fig1.png" alt="Fig.1" width="600"/><br>
  
  *Fig. 1: Schematic illustration of the experimental setup, which consists of magnetic domains of width L, of alternating magnetization of constant homogeneous intensity.*
</div>
<br>

The formulas developed in the thesis, that describe the Magnetic field B(x,z) are the following:

<div align="center">
  <img src="https://raw.githubusercontent.com/chrisov/Magnetic-Induction-Field-Representation/5b5f98f92a2903e21c18301c463463a015f24419/Fig2.png" alt="Fig.2" width="600"/><br>

  *Fig. 2: Final results for the magnetic field B(x,z) for every sub-space.*
</div>
<br>

The indices I, II, III are used to describe the sub-space, below, inside and above the ferromagnet, respectively. It is necessary to mention that the theoretical analysis conducted in the paper, that resulted into the development of the aforementioned formulas, considers an ideal sample of infinite y-dimension. What this means, is that the visualization is accurate for regions in the respective subspaces that are "far" from any of the sample's borders.
