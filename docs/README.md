# Project Overview
A program that exports a satellite image to a 3D model (although technically it does not have to be a satellite image).  

This was made for my Social Studies project because I needed a 3D model of the Gaza strip, but I might need it later so here are some instructions for future me.
## How to use

### Download satellite imagery  
Although there will be an example image in `images/`, you probably want to get your own imagery instead.  

To do so, go to this website: <https://en-gb.topographic-map.com/>  

Here you can find topographic data for every place in the world. It's great because you can also have the country names in the screenshot, which is great if you want a 3D map to impress your teacher or something.  

You can choose any layer, but I used Carto Light. Then, screenshot the area you want, and save it as `images/satellite-image.png` (because I'm lazy and just hardcoded the name). 

Maybe in the future I will use the API instead for ease of use, but for now, this is the workaround. 

### Create the .obj file
Run the install script:
```
chmod +x install.sh
./install.sh
```  
I haven't made it work for any other shell that isn't Fish, so modify `source .venv/bin/activate.fish` if needed.  

Move your downloaded satellite image to the `images/` directory created by the install script, and name it `satellite-image.png` because I'm lazy.  

Then run `main.py`:
```
python3 main.py
```  
You will find the exported `.obj` file in `model/`.  

If you want to impress your teacher on a presentation, upload the model to SketchFab (after zipping `model/`). You can then embed it in Google Sites or something.