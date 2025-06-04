from PIL import Image
import numpy as np
import pyvista as pv

# Convert to grayscale and save as .tiff
img = Image.open("images/satellite-image-high.png").convert('L')
# Rotate the image so that it will show properly when put on the mesh
img.transpose(Image.ROTATE_90).save("images/output/flipped.png")

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
grid.texture_map_to_plane(inplace=True)

# Visualize
plotter = pv.Plotter()
texture= pv.read_texture("images/output/flipped.png")
plotter.add_mesh(grid, cmap="terrain", lighting="True", label="The Gaza strip", render_points_as_spheres="True", texture=texture)

# Save as a screenshot once closed
plotter.show(screenshot="images/output/render.png")
