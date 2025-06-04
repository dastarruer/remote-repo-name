from PIL import Image
import numpy as np
import pyvista as pv
from os import remove

def main():
    img = process_image()
    plotter = create_model(img)

    # Save as a screenshot once closed
    plotter.show(screenshot="images/output/render.png")

def process_image() -> Image:
    # Convert to grayscale and save as .tiff
    img = Image.open("images/satellite-image-high.png").convert('L')

    # Rotate the image so that it will show properly when put on the mesh
    return img

def create_model(img):
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

    # Create the texture
    img.transpose(Image.ROTATE_90).save("texture.png")
    texture= pv.read_texture("texture.png")

    # Delete the texture
    remove("texture.png")

    # Delete the 
    # Visualize
    plotter = pv.Plotter()
    plotter.add_mesh(grid, cmap="terrain", lighting="True", label="The Gaza strip", render_points_as_spheres="True", texture=texture)
    return plotter
    

if __name__ == "__main__":
    main()