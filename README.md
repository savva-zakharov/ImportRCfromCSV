ImportRCfromCSV
---
**Description** 

This is a simple Blender addon for importing camera positions from Reality Scan (formerly Reality Capture) from CSV file. It reads the source file, positions the cameras at the correct locations, applies rotational transformation, sets the correct focal lenght and optionally imports the images as backgrounds 

**Use Instructions** 
1. In Reality Scan, with the right component selected, choose Alignment > Export > Registration
2. Choose to save as type "Internal/External camera parameters"
3. Save the .csv file in a convenient location.
4. (Make sure to install and enable the addon in Blender)
5. In Blender, go to File > Import > Import RC camera CSV (.csv)
6. The file selection diologue will appear. Go to the location where you saved the .csv file and select it. The side bar offers a check box to import the images as backgrounds (default on). By default, it will search the same folder for matching images, overwise you can specify optional file path for the images in the side bar.
7. Click Import
