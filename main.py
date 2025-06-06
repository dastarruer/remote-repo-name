from PIL import Image, ImageFilter
import numpy as np
import pyvista as pv
from os import remove, path
import getopt, sys


BASE_DIR = path.dirname(__file__)
topography_img = path.join(BASE_DIR, "images", "topography-image.png")
MODIFIED_TOPOGRAPHY_IMG = path.join(BASE_DIR, "modified-image.png")
FINAL_MODEL_PATH = path.join(BASE_DIR, "model", "model.obj")

FLAGS = ["show", "image="]
OPTIONS = "si:"

def main():
    global topography_img
    
    argument_list = sys.argv[1:]
    arguments, _ = getopt.getopt(argument_list, OPTIONS, FLAGS)

    show = False
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-s", "--show"):
            show = True
        if currentArgument in ("-i", "--image") and path.exists(currentValue):
            topography_img = path.abspath(currentValue)
            
    img = process_image()
    create_model(img, show=show)

    
    

def process_image() -> Image.Image:
    # Reset modified image
    Image.open(topography_img).save(MODIFIED_TOPOGRAPHY_IMG)

    # Convert to grayscale, where brighter values will show as peaks, and darker values will show as lows
    img = Image.open(topography_img).convert('L')
    
    # Downscale the image so the program doesn't crash all the time
    scale_factor = 1
    width, height = int(img.width * scale_factor), int(img.height * scale_factor)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    # Blur image in order to smooth out spikes from adjacent pixels with drastically different values
    blur_strength = 5
    img.filter(ImageFilter.GaussianBlur(radius=blur_strength))

    return img


def create_model(img, show=False) -> None:
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

    if show == True:
        plotter.show()

    # Export the model
    plotter.export_obj(FINAL_MODEL_PATH)

        

if __name__ == "__main__":
    main()