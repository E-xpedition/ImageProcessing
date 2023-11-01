# -*- coding: utf-8 -*-
"""                                                                                   
                                            . :::::::..                                   
                                         .:............::.                                
                                        :.................:.     ....                     
                          . :...... .......................:...::.....:.                  
                        .:.............................................::.                
                       .:..........................................:.::::--               
                 --****+:.......::--::......::----:::..........:-----:::::-               
                #+=+****#=::.::------****-----*****-----:::::-::::-----:--.               
       -**##-  #*+*%%###**@ -:******************************-:::::********-               
      %******%=%***#*****#=   ...--..-. ...-**************************-.--.               
      =#********#***%%%%%%                  :-:::::-+-------....-***--.                   
       =#*==+*************%=             -- +-....-+#- ...       ...                      
     ,-=%*++*************###=               +#+==*+##= -                                  
    #=+********+**=******##*#=             #.:...*##--@                                   
     -=%#*****==# = ****++***#=           #.:.:::=##*==@                                  
        %*****+=@%@#***%::%***%          #..-=:::=+##===@                                 
        *==*****%%****%::+*****%     ---#..=:+===####====+-                               
         #+=**********::**::****@  #=:+===:-+....:=#..:+:-=#++-                           
          #*******%*:+*%:::::***#=#=......-:+-:--=:#+:::#++++=#                           
           -%*#*#%*-=   %:::::***%...::++-+=+===+++=-::::=::-=%                           
             -=-        -*::::=***%...::..-*::---++--==:-----+%-                          
                         @:::::****%+==.....-----+==#:-#==+=++==%                         
                         %::::::****%..:==:=::::::-====%=++-==+==%                        
                        @:::::::*****#*--:..=::::::-====+==##++++=%-                      
                        %:::::::=*****#%##+=-==::::--===#*=:---==++@                      
                       @:::::::::******#%##%#-:=++===+#*-*#%%%%%+#=+=                     
                       @:::::::::=*******#**#%#-:-=**==+%#*##*****%+@                     
                       #........::*****###*****%#*--==#%**###***#####%-=                  
                       #...........=**************#%%%******************#%-=              
                    ---#............=**************#######******************#%=           
               --*******#............-***************++++**%%#%%=******=====**=           
             -*+===+****%=.............-************=======*****%+******-===              
          -****++*****===*+..............:==+*%====***++++********##-                     
          -*+======:+**-== =+=::::::::::::::::*=-*+:::==*************##--                 
             =======          ==-**+++++++**-=     =-**+:::==**********#%=                
                                                        ===-*******+===                   
                                                              
Script by Expedition

This script takes your pictures, straightens and crops them so you don't have to use those pesky image editting programms.

Notice:
    
×   It works under the assumption that you take pictures of your cards against a black background, and that they are at least somewhat straight.
×   Both graded and raw cards work for this method.
×   The straightening does not warp your image, it attempts to get the best fit, but it may not be perfect.
×   The script may struggle with black-bordered cards, as these are difficult to differentiate from the background.
×   When you run the script you will be prompted with two selection windows:
    1. Which images to process.
    2. Choose the output directory.
    
"""
#
#@=-                                                                                               
#@@=-            ooo        ooooo                 .o8              oooo                           
#@@@@=-         `88.       .888'                "888              `888                          
#@@@@@@=-       888b     d'888   .ooooo.   .oooo888  oooo  oooo   888   .ooooo.   .oooo.o     
#@@@@@@@@==-   8 Y88. .P  888  d88' `88b d88' `888  `888  `888   888  d88' `88b d88(  "8   
#@@@@@@=-     8  `888'   888  888   888 888   888   888   888   888  888ooo888 `"Y88b.        
#@@@@=-      8    Y     888  888   888 888   888   888   888   888  888    .o o.  )88b         
#@@=-      o8o        o888o `Y8bod8P' `Y8bod88P"  `V88V"V8P' o888o `Y8bod8P' 8""888P'         
#@=-                                                                                          
#####################################################################################################

import cv2
import numpy as np
import houghlines as lq
import imutils as imu
from tkinter import filedialog
from tkinter import *
import os
import sys

#
#@=-               ooooo                                        .                   
#@@=-             `888'                                      .o8            
#@@@@=-           888  ooo. .oo.   oo.ooooo.  oooo  oooo  .o888oo           
#@@@@@@=-        888  `888P"Y88b   888' `88b `888  `888    888                
#@@@@@@@@==-    888   888   888   888   888  888   888    888                
#@@@@@@=-      888   888   888   888   888  888   888    888 .               
#@@@@=-      o888o o888o o888o  888bod8P'  `V88V"V8P'   "888"         
#@@=-                          888                                     
#@=-                         o888o                                          
#####################################################################################################
    
px_buffer   = 100 # Amount of pixels to buffer the sides with on the output image
threshold   = 40 # Threshold value (scale 0-255) for creating a binary image, which is used to find the edge between background and card.
                 # Default is set to 40, a number between 30 and 50 generally gives best results.

#
#@=-               .oooooo..o                     o8o                 .         
#@@=-            d8P'    `Y8                     `"'               .o8         
#@@@@=-          Y88bo.       .ooooo.  oooo d8b oooo  oo.ooooo.  .o888oo     
#@@@@@@=-        `"Y8888o.  d88' `"Y8 `888""8P `888   888' `88b   888      
#@@@@@@@@==-        `"Y88b 888        888      888   888   888   888    
#@@@@@@=-     oo     .d8P 888   .o8  888      888   888   888   888 .      
#@@@@=-      8""88888P'  `Y8bod8P' d888b    o888o  888bod8P'   "888"        
#@@=-                                             888                      
#@=-                                            o888o                       
#####################################################################################################
root = Tk()
root.withdraw()
fileselect = filedialog.askopenfilenames(
                                    initialdir= os.getcwd(),
                                    title= "Please select file(s):",
                                    filetypes= [("image files", "*.jpg *.jpeg *.png *.bmp")])
out_dir = filedialog.askdirectory(title="Please select output folder")
if out_dir == "":
    print("Output folder required.")
    sys.exit()
out_dir += "/"
n = -1
for picture in fileselect:
    n += 1
    try:
        # Import the photo, assumed photoname based on camera counting and jpg-extension
        color = cv2.imread(picture, cv2.IMREAD_COLOR)
        
        # Retrieve imagename
        imagename = picture.rsplit('/',1)[1]
        
        # Call function to get the fitted lines
        crooked_lines = lq.GetLines(color,out_dir,imagename,threshold)
        
        # Finding the rotation of the card compared to straight
        av1=[]
        angle_fix = crooked_lines[crooked_lines[:,0,1].argsort()]
        for w in range(len(angle_fix)):
            if w > 2:
                av1.append(angle_fix[w,0,1])
        average_rot = sum(av1)/len(av1)
        
        # Fixing the angle
        if average_rot > 3:
            rotated = imu.rotate(color, 180+average_rot*(180/np.pi))
        elif average_rot > 1:
            rotated = imu.rotate(color, 270+average_rot*(180/np.pi))
        # Export the rotated image - remove the # in front of the next line if you wish to save
        #cv2.imwrite(out_dir+"r_"+imagename, rotated)
        
        # Part 2, redo with straightened image
        straight_lines = lq.GetLines(rotated,out_dir,imagename,threshold)
        
        # Get intersect locations
        intersect_pts = lq.hough_lines_intersection(straight_lines, rotated.shape)
        
        # Buffer intersection points
        min_x=min([p[0] for p in intersect_pts])-px_buffer
        max_x=max([p[0] for p in intersect_pts])+px_buffer
        min_y=min([p[1] for p in intersect_pts])-px_buffer
        max_y=max([p[1] for p in intersect_pts])+px_buffer
        
        # Crop and save the newly cropped and rotated image
        cropped = rotated[min_y:max_y,min_x:max_x]
        cv2.imwrite(out_dir+"X_"+imagename, cropped)
        print("Succesfully exported to "+out_dir+"X_"+imagename)
    except:
        print("Unsuccesful with "+str(picture)+" , better luck next time!")
root.destroy()
