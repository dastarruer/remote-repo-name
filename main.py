from PIL import Image
import numpy as np
import pyvista as pv
from os import remove

SATELLITE_IMG="images/satellite-image-high.png"
TEXTURE_PATH="texture.png"
FINAL_MODEL_PATH="model.obj"

def main():
    img = process_image()
    plotter = create_model(img)

    # Show the model
    plotter.show()
    
    # Save the model
    plotter.save("terrain.obj")


def process_image() -> Image:
    # Convert to grayscale and save as .tiff
    img = Image.open(SATELLITE_IMG).convert('L')

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
    img.transpose(Image.ROTATE_90).save(TEXTURE_PATH)
    texture= pv.read_texture(TEXTURE_PATH)
    
    grid.extract_surface().save(FINAL_MODEL_PATH)

    # Delete the texture
    remove(TEXTURE_PATH)

    plotter = pv.Plotter()
    plotter.add_mesh(grid, cmap="terrain", lighting="True", label="The Gaza strip", render_points_as_spheres="True", texture=texture, render_lines_as_tubes="True")
    return plotter
    

if __name__ == "__main__":
    main()