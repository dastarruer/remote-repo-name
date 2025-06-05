from PIL import Image, ImageFilter
import numpy as np
import pyvista as pv
from os import remove

SATELLITE_IMG="images/satellite-image.png"
TEXTURE_PATH="texture.png"
FINAL_MODEL_PATH="model/model.obj"

def main():
    img = process_image()
    plotter = create_model(img)

    # Export the model
    plotter.export_obj(FINAL_MODEL_PATH)


def process_image() -> Image.Image:
    # Convert to grayscale, where brighter values will show as peaks, and darker values will show as lows
    img = Image.open(SATELLITE_IMG).convert('L')

    # Blur image in order to smooth out spikes from adjacent pixels with drastically different values
    blur_strength = 35
    img.filter(ImageFilter.GaussianBlur(radius=blur_strength))

    return img


def create_model(img) -> pv.Plotter:
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

    # Rotate the image so that it will show properly when put on the mesh, and save the texture file
    img.transpose(Image.Transpose.ROTATE_90).save(TEXTURE_PATH)

    # Create the texture
    texture= pv.read_texture(TEXTURE_PATH)
    
    # Delete the texture file
    remove(TEXTURE_PATH)

    plotter = pv.Plotter()
    plotter.add_mesh(grid, cmap="terrain", lighting="True", label="The Gaza strip", render_points_as_spheres="True", texture=texture, render_lines_as_tubes="True")
    return plotter
    

if __name__ == "__main__":
    main()