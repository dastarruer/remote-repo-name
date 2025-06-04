from PIL import Image
import numpy as np
import pyvista as pv

# Convert to grayscale and save as .tiff
img = Image.open("images/satellite-image-high.png").convert('L')

# Resize to manageable size (optional)
img = img.resize((300, 300))

# Convert to numpy array (0-255)
heightmap = np.array(img)

# Normalize heightmap to a smaller scale, e.g. 0 to 50 meters
heightmap = (heightmap / 255.0) * 50

# Create grid coordinates
nrows, ncols = heightmap.shape
x = np.arange(ncols)
y = np.arange(nrows)
xv, yv = np.meshgrid(x, y)

# Create 3D terrain mesh using pyvista
grid = pv.StructuredGrid(xv, yv, heightmap)

# Visualize
plotter = pv.Plotter()
plotter.add_mesh(grid, cmap="terrain", lighting="True", label="The Gaza strip", render_points_as_spheres="True")
plotter.show(screenshot="images/output/render.png")
