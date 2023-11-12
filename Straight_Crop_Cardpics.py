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
#threshold   = 40 # Threshold value (scale 0-255) for creating a binary image, which is used to find the edge between background and card.
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
print(fileselect)
out_dir = filedialog.askdirectory(title="Please select output folder")
if out_dir == "":
    print("Output folder required.")
    sys.exit()
out_dir += "/"

root.destroy()            
root = Tk()
v = 40 
def set_value():    
    global v
    v = w.get()  # v is set here

canvas = Canvas(root, width = 700, height = 500)
w = Scale(root,from_=0, to=255,length = 255, orient='horizontal')
w.set(40)

w.pack()
Button(root, text='Set', command=set_value).pack()     
Button(root, text='Confirm', command=lambda: lq.final_func(v,fileselect,out_dir, px_buffer)).pack() 
canvas.pack()

root.mainloop()
