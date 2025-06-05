from PIL import Image, ImageFilter
import numpy as np
import pyvista as pv
from os import remove, path
import getopt, sys
import elevation
import geopandas as gpd


# DEM stands for Distance Elevantion Model
DEM = path.expanduser("~/.cache/elevation/SRTM1/out.tif")

BASE_DIR = path.dirname(__file__)
TEXTURE_PATH = path.join(BASE_DIR, "texture.png")
FINAL_MODEL_PATH = path.join(BASE_DIR, "model", "model.obj")

FLAGS = ["show", "coordinates="]
OPTIONS = "sc:"

def main():
    argument_list = sys.argv[1:]
    arguments, values = getopt.getopt(argument_list, OPTIONS, FLAGS)
    bounds = ()
    
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-c", "--coordinates"):
            bounds = tuple(map(float, currentValue.split(",")))

    elevation.clip(bounds=bounds)
    elevation.clean()

    img = process_image()
    plotter = create_model(img)

    # Export the model
    plotter.export_obj(FINAL_MODEL_PATH)
    
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-s", "--show"):
            plotter.show()


def process_image() -> Image.Image:
    # Convert to grayscale, where brighter values will show as peaks, and darker values will show as lows
    img = Image.open(DEM).convert('L')

    # Downscale the image so the program doesn't crash all the time
    scale_factor = 0.5
    width, height = int(img.width * scale_factor), int(img.height * scale_factor)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    # Blur image in order to smooth out spikes from adjacent pixels with drastically different values
    blur_strength = 5
    img.filter(ImageFilter.GaussianBlur(radius=blur_strength))

    return img


def create_model(img) -> pv.Plotter:
    # Convert to numpy array (0-255)
    heightmap = np.array(img)

    # Normalize heightmap to a smaller scale, e.g. 0 to 50 meters
    max_height = 50
    heightmap = (heightmap / 255.0) * max_height

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
    plotter.add_mesh(grid, cmap="terrain", lighting=True, label="The Gaza strip", render_points_as_spheres=True, texture=texture, render_lines_as_tubes=True)
    return plotter
    
        

if __name__ == "__main__":
    main()