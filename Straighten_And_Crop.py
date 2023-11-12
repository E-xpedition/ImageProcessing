import PySimpleGUI as sg
import cv2
import os
import numpy as np
import imutils as imu
import warnings

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
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

"""



warnings.filterwarnings("ignore", category=RuntimeWarning)


def polar2cartesian(rho: float, theta_rad: float, rotate90: bool = False):
    """
    Converts line equation from polar to cartesian coordinates

    Args:
        rho: input line rho
        theta_rad: input line theta
        rotate90: output line perpendicular to the input line

    Returns:
        m: slope of the line
           For horizontal line: m = 0
           For vertical line: m = np.nan
        b: intercept when x=0
    """
    x = np.cos(theta_rad) * rho
    y = np.sin(theta_rad) * rho
    m = np.nan
    if not np.isclose(x, 0.0):
        m = y / x
    if rotate90:
        if m is np.nan:
            m = 0.0
        elif np.isclose(m, 0.0):
            m = np.nan
        else:
            m = -1.0 / m
    b = 0.0
    if m is not np.nan:
        b = y - m * x

    return m, b


def solve4x(y: float, m: float, b: float):
    """
    From y = m * x + b
         x = (y - b) / m
    """
    if np.isclose(m, 0.0):
        return 0.0
    if m is np.nan:
        return b
    return (y - b) / m


def solve4y(x: float, m: float, b: float):
    """
    y = m * x + b
    """
    if m is np.nan:
        return b
    return m * x + b


def intersection(m1: float, b1: float, m2: float, b2: float, lines1: float, lines2: float):
    # Consider y to be equal and solve for x
    # Solve:
    #   m1 * x + b1 = m2 * x + b2
    x = (b2 - b1) / (m1 - m2)
    # Use the value of x to calculate y
    y = m1 * x + b1
    if np.isnan(m1):
        x = lines1
        y = m2 * x + b2
    if np.isnan(m2):
        x = lines2
        y = m1 * x +b1
    try:
        return int(round(x)), int(round(y))
    except:
        return np.nan,np.nan



def hough_lines_intersection(lines: np.array, image_shape: tuple):
    """
    Returns the intersection points that lie on the image
    for all combinations of the lines
    """
    if len(lines.shape) == 3 and \
            lines.shape[1] == 1 and lines.shape[2] == 2:
        lines = np.squeeze(lines)
    lines_count = len(lines)
    intersect_pts = []
    for i in range(lines_count - 1):
        for j in range(i + 1, lines_count):
            m1, b1 = polar2cartesian(lines[i][0], lines[i][1], True)
            m2, b2 = polar2cartesian(lines[j][0], lines[j][1], True)
            x, y = intersection(m1, b1, m2, b2, lines[i][0],lines[j][0])
            if point_on_image(x, y, image_shape):
                intersect_pts.append([x, y])
    return np.array(intersect_pts, dtype=int)


def point_on_image(x: int, y: int, image_shape: tuple):
    """
    Returns true is x and y are on the image
    """
    return 0 <= y < image_shape[0] and 0 <= x < image_shape[1]

def drawHoughLines(image, lines, output):
    out = image.copy()
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 10000 * (-b))
        y1 = int(y0 + 10000 * (a))
        x2 = int(x0 - 10000 * (-b))
        y2 = int(y0 - 10000 * (a))
        cv2.line(out, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imwrite(output, out)

def GetLines(image,filepath,imagename,threshold):
    # Blur image to reduce false positive edges
    blurred = cv2.blur(image, (9,9))
    # RGB to gray
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    # Threshold the image to binary
    th, im_th = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    # Copy the thresholded image
    im_floodfill_inv = cv2.bitwise_not(im_th)
    im_base = im_floodfill_inv.copy()
    # Mask used for flood filling
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
     
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill_inv, mask, (0,0), 255);
     
    # Invert floodfilled image
    im_inv = cv2.bitwise_not(im_floodfill_inv)
     
    # Combine the two images to get the foreground
    im_out = im_base | im_inv
    # Export the binary image - remove the # in front of the next line if you wish to export
    #cv2.imwrite(filepath+imagename, im_out)

    # Edge detection   
    edges = cv2.Canny(im_out, 50, 120, apertureSize=3)
    # Export the detected edges - remove the # in front of the next line if you wish to export
    #cv2.imwrite(filepath+imagename, edges)
    
    # Fit lines to detected edges
    polar_lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    
    # Reduce all detected lines to only strongest 4
    strong_lines = np.zeros([4,1,2])
    n2 = 0
    for n1 in range(0,len(polar_lines)):
        for rho,theta in polar_lines[n1]:
            if n1 == 0:
                strong_lines[n2] = polar_lines[n1]
                n2 = n2 + 1
            else:
                """
                if rho < 0:
                   rho*=-1
                   theta-=np.pi
                """
                closeness_rho = np.isclose(rho,strong_lines[0:n2,0,0],atol = 500)
                closeness_theta = np.isclose(theta,strong_lines[0:n2,0,1],atol = np.pi/18)
                closeness = np.all([closeness_rho,closeness_theta],axis=0)
                if not any(closeness) and n2 < 4:
                    strong_lines[n2] = polar_lines[n1]
                    n2 = n2 + 1
    # Export the detected strong line fits for edge-detection - remove the # in front of the next line if you wish to export   
    #drawHoughLines(image, strong_lines, filepath+"p"+imagename)
    return strong_lines

def final_func(threshold,fileselect,out_dir,px_buffer):
    n = -1
    for picture in fileselect:
        n += 1
        try:
            # Import the photo, assumed photoname based on camera counting and jpg-extension
            color = cv2.imread(picture, cv2.IMREAD_COLOR)
            
            # Retrieve imagename
            imagename = picture.rsplit('/',1)[1]
            
            # Call function to get the fitted lines
            crooked_lines = GetLines(color,out_dir,imagename,threshold)
            
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
            #cv2.imwrite(directory+"IMG_"+str(picture)+"_rotated.jpg", rotated)
            
            # Part 2, redo with straightened image
            straight_lines = GetLines(rotated,out_dir,imagename,threshold)
            
            # Get intersect locations
            intersect_pts = hough_lines_intersection(straight_lines, rotated.shape)
            
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
            
def main():
    sg.theme("Black")
    thumb = None
    # Define the window layout
    layout = [
        [sg.Image(size=(500,10),filename="", key="-IMAGE-")],
        [sg.Text("Image File"), sg.Input(size=(25, 1), key="-FILE-"), sg.FileBrowse(file_types=file_types),sg.Button("Load image"),],
        [sg.Text("Output Location"), sg.Input(size=(25, 1), key="-OUTDIR-"), sg.FolderBrowse(),],
        [sg.Text("Threshold value (ensure the entire card is white, but background is mostly black)", size=(60, 1), justification="left")],
        [sg.Slider((0, 255),40,1,orientation="h",size=(40, 15),key="-THRESH SLIDER-",)],
        [sg.Text("Buffer around output image in pixels:", size=(25, 1), justification="left"),sg.Input('100',size=(10,1), enable_events=True, key='-BUFFER-', justification="left")],
        [sg.Button("Exit", size=(10, 1)),sg.Button("Continue", size = (10,1))],
    ]

    # Create the window and show it without the plot
    window = sg.Window("Straighten And Crop", layout, location=(200, 100))

    #cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        filename = values["-FILE-"]
        outdir = values["-OUTDIR-"]
        if event == '-BUFFER-':
            if len(values['-BUFFER-'])>0:
                if values['-BUFFER-'][-1] not in ('0123456789'):
                    sg.popup("Only digits allowed")
                    window['-BUFFER-'].update(values['-BUFFER-'][:-1])
        if event == "Load image":
            if os.path.exists(filename):
                thumb = cv2.imread(values["-FILE-"])
                thumb = imu.resize(thumb,500)
        
        if os.path.exists(filename) and thumb is not None:
            #frame = cv2.imread(values["-FILE-"])
            #frame = imutils.resize(frame,500)
            frame = cv2.cvtColor(thumb, cv2.COLOR_BGR2GRAY)
            frame = cv2.threshold(frame, values["-THRESH SLIDER-"], 255, cv2.THRESH_BINARY_INV)[1]
            #copy threshed image
            im_floodfill_inv = cv2.bitwise_not(frame)
            im_base = im_floodfill_inv.copy()
            # Mask used for flood filling
            h, w = frame.shape[:2]
            mask = np.zeros((h+2, w+2), np.uint8)
     
            # Floodfill from point (0, 0)
            cv2.floodFill(im_floodfill_inv, mask, (0,0), 255);
     
            # Invert floodfilled image
            im_inv = cv2.bitwise_not(im_floodfill_inv)
     
            # Combine the two images to get the foreground
            frame = im_base | im_inv
            
            #image.thumbnail((400, 400))
            #bio = io.BytesIO()
            #imgbytes.save(bio, format="PNG")
            
            #cv2.cvtColor(image, cv2.COLOR_BGR2LAB)[:, :, 0]
            
            #window["-IMAGE-"].update(data=bio.getvalue())
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            #imgbytes = cv2.imencode(".png", image)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes) 
        if event == "Continue":
            tempfix = [filename]
            if values["-BUFFER-"] == '':
                values["-BUFFER-"] = '0'
            if os.path.exists(outdir):
                outdir += r"/"
                final_func(values["-THRESH SLIDER-"], tempfix,outdir, int(values["-BUFFER-"]))
            else:
                outdir = filename.rsplit('/',1)[0] + r"/"
                final_func(values["-THRESH SLIDER-"], tempfix,outdir, int(values["-BUFFER-"]))
    window.close()
    
if __name__ == "__main__":
    main()