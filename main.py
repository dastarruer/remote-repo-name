from PIL import Image, ImageFilter
import numpy as np
from os import path
import pyvista as pv
import getopt
import sys


BASE_DIR = path.dirname(__file__)
MODIFIED_TOPOGRAPHY_IMG = path.join(BASE_DIR, "modified-image.png")
DEFAULT_IMG = path.join(BASE_DIR, "images", "example-image.png")
FINAL_MODEL_PATH = path.join(BASE_DIR, "model", "model.obj")

FLAGS = ["show", "image=", "scale="]
OPTIONS = "si:"

def main():
    argument_list = sys.argv[1:]
    arguments, _ = getopt.getopt(argument_list, OPTIONS, FLAGS)

    # Default path
    topography_img = DEFAULT_IMG
    show = False
    scale_factor = 1
    for current_argument, current_value in arguments:
        if current_argument in ("-s", "--show"):
            show = True
        if current_argument in ("-i", "--image") and path.exists(current_value):
            topography_img = path.abspath(current_value)
        if current_argument in ("--scale"):
            scale_factor = float(current_value)

    img = process_image(topography_img, scale_factor=scale_factor)
    create_model(img, show=show, topography_img=topography_img)


def process_image(topography_img=DEFAULT_IMG, scale_factor=1.0) -> Image.Image:
    # Reset modified image
    Image.open(topography_img).save(MODIFIED_TOPOGRAPHY_IMG)

    # Convert to grayscale, where brighter values will show as peaks, and 
    # darker values will show as lows
    img = Image.open(topography_img).convert('L')
    # Downscale the image so the program doesn't crash all the time
    width, height = int(img.width * scale_factor), int(img.height * scale_factor)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    # Blur image in order to smooth out spikes from adjacent pixels with 
    # drastically different values
    blur_strength = 5
    img.filter(ImageFilter.GaussianBlur(radius=blur_strength))

    return img


def create_model(img, show=False, topography_img=DEFAULT_IMG) -> None:
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

    # For whatever reason the image will not align with the mesh, meaning that we have to rotate it
    Image.open(topography_img).transpose(Image.Transpose.ROTATE_90).save(MODIFIED_TOPOGRAPHY_IMG)
    
    # TODO: Fix issue where text will be flipped after rotating texture 90 degrees
    # Create the texture
    texture= pv.read_texture(MODIFIED_TOPOGRAPHY_IMG)

    plotter = pv.Plotter()
    plotter.add_mesh(grid, cmap="terrain", lighting=True, label="The Gaza strip", render_points_as_spheres=True, texture=texture, render_lines_as_tubes=True)

    # Export the model
    plotter.export_obj(FINAL_MODEL_PATH)

    if show == True:
        plotter.show()

        

if __name__ == "__main__":
    main()