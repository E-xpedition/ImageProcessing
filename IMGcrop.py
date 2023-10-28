
"""                                                                                   
                                                            
                             . ......                       
                           ..........:.                     
                 ...... ...............:........            
                :.............................:::.          
           .:===.....::::.....:::::.......::-::::-          
     .::  :*+****+::------------------::::::---:-:          
    +***#=%**#*#** .::-:::.::------------------:-:          
    -#*******###%-          .:::::--:--:...:-:.             
   .:+*++********#+        : +#--=#* .                      
   +******++:+**##*+        -::.:*#=#.                      
     +***+=#@+*%:%**=      =:--::+#+=+                      
     :++***#**#:=+**#- ::-*-:==--*#=--=-:.                  
      :*****#+=*=:-**%=+.-..-+::--#-:+++++                  
        =*+--:  +:::***..:-:+=-==+-:::-:-#                  
                =:::=***--..:----==+=+====*:                
                +::::***+.--:-::::===*+====+.               
                +::::+***%**--=-::-==++=+=++#               
               @::::::****####+-=+*+*+*####*+*              
               %:...::=***##**##+=-=*#*##**##%=-            
               #.......-**********##************#==-        
          :-=+**-.......-**************####+***+++**-       
       .:++++****.........-+*******+===+*****===:-.         
       ++++++=+-=-=-:::::::::-=+-===++*******#=:.           
         ----.      -:=-----=:-   --==++=++++##==           
                                        ----:               

Script by Expedition

This script returns quadrants of images, useful as close-ups.
    
"""
from PIL import Image

number      = 2256 # Directory where input image(s) is located
number2     = 1903 # If only 1 image, same as number. If attempting multiple images of ascending image number, final image number
directory   = "F:\\Pokemon\\Processing\\" # Directory where input image(s) is located
out_dir     = "F:\\Pokemon\\Processing\\" # Directory where the result is saved to

for picture in range(number,number2+1):
    try:
        im = Image.open(directory+"IMG_"+str(number)+".jpg")
 
        # Size of the image in pixels (size of original image)
        width, height = im.size
         
        # Setting the points for cropped image
        left = 0
        top = 0
        right = width / 2
        bottom = height / 2
         
        # Crop immage into 4 quadrants
        im1 = im.crop((left, top, right, bottom))
        im2 = im.crop((left, bottom, right, height))
        im3 = im.crop((right, top, width, bottom))
        im4 = im.crop((right, bottom, width, height))
        
        im1 = im1.save(out_dir+"IMG_"+str(number)+"-1.jpg")
        im2 = im2.save(out_dir+"IMG_"+str(number)+"-2.jpg")
        im3 = im3.save(out_dir+"IMG_"+str(number)+"-3.jpg")
        im4 = im4.save(out_dir+"IMG_"+str(number)+"-4.jpg")
    except:
        print("Unsuccesful with IMG_"+str(picture)+" , better luck next time!")
