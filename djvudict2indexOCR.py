#!/usr/bin/env python3
# virtual environment may be needed !!!

# Janusz S. Bień 2023
# licensed under the Creative Commons Zero v1.0 Universal
# (Creative Commons CC0 Public Domain Dedication)

import os
import re
from PIL import Image
import cv2 
import pytesseract

def escape(s):	
    quote = s.translate(str.maketrans({'"':'""'}))
#     semicolon = quote.translate(str.maketrans({';':'";"'}))
    return '"' + quote + '"'

current_directory = os.getcwd()
directory_name = os.path.basename(current_directory)

# https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
# https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
# https://sparkbyexamples.com/python/python-extract-numbers-from-string/
# https://stackoverflow.com/questions/733454/best-way-to-format-integer-as-string-with-leading-zeros
# https://www.geeksforgeeks.org/how-to-find-width-and-height-of-an-image-using-python/
# A;file:Zaborowski_MBC.djvu;Egzemplarz A; ※ wydanie 1
# ⁊;file:Zaborowski_MBC.djvu?djvuopts=&highlight=442,1338,50,60&page=1;; ※ et
# highlight=x,y,w,h[,color]
# https://nanonets.com/blog/ocr-with-tesseract/

subfolders = [ f.path for f in os.scandir(current_directory) if f.is_dir() ]

indexname = directory_name + ".csv"

# ixf = index file
ixf = open(indexname, "w", encoding="utf8")
# ixf.write("test;test;test;test\n")

custom_config = r'-l lat --psm 8'
# https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
globalcount = 0
subdir_count = 0
for dirname in list(subfolders):
    print(os.path.basename(dirname))
    dirname_base = os.path.basename(dirname)
    dirnumbers = re.findall(r'\d+', dirname)
    subdir_count += 1
#     pageno = dirnumbers[-1]
    pageno = subdir_count  
    filepath = dirname + r"/actions.log"
    lf = open(filepath, "r", encoding="utf8")
    count = 0	
    for line in lf:
        globalcount += 1
        if line.strip() == "Records jb2_start_of_image":
            count += 1
            print("{} {}: {}".format(dirname, count, line.strip()))
        elif line.startswith("Records jb2_new_symbol_add_to_image_and_library:"):
            count += 1
            status = "new"            
            numbers = re.findall(r'\d+', line)
#             print("OK: {} {}".format(numbers, line.strip()))
            result = list(map(int, numbers))
            ident = result[1]
            identstring = f'{ident:05d}'
            imagefile = dirname + "/lib_" + identstring + ".bmp"
            image = Image.open(imagefile)
            # get width and height 
            height1, width1 = image.size
            height = image.height
            width = image.width
#             ocr = pytesseract.image_to_string(img, config='--psm 10')
            ocr = pytesseract.image_to_string(image, config=custom_config).strip()
            print(ocr + "\n")
            image.close()
            print(identstring)
            xcoord = result[2]
            ycoord = result[3]
        elif line.startswith("Records jb2_matched_symbol_with_refinement_add_to_image_and_library:"):
            count += 1
            status = "add"            
            numbers = re.findall(r'\d+', line)
#             print("OK: {} {}".format(numbers, line.strip()))
            result = list(map(int, numbers))
            ident = result[1]
            identstring = f'{ident:05d}'
            imagefile = dirname + "/lib_" + identstring + ".bmp"
            image = Image.open(imagefile)
            # get width and height 
            height, width = image.size
#            ocr = pytesseract.image_to_string(image, config=custom_config).strip()
            print(ocr + "\n")
            image.close()
            print(identstring)
            xcoord = result[2]
            ycoord = result[3]
        elif line.startswith("Records jb2_matched_symbol_copy_to_image_without_refinement:"):
            count += 1
            status = "copy"            
            numbers = re.findall(r'\d+', line)
#             print("OK: {} {}".format(numbers, line.strip()))
            result = list(map(int, numbers))
            ident = result[1]
            identstring = f'{ident:05d}'        
            imagefile = dirname + "/lib_" + identstring + ".bmp"
            image = Image.open(imagefile)
            # get width and height 
            height, width = image.size
            image.close()
            print(identstring)
            xcoord = result[2]
            ycoord = result[3]
        elif line.strip() == "Records jb2_end_of_data":
            count += 1
            print("{} {}: {}".format(dirname, count, line.strip()))
        else:
            print("TO DO: {}".format(line.strip()))
        if count != 1:
            countstring = f'{count:05d}'
            pagenostring = f'{pageno:03d}'
            ycoordl = ycoord - height
            xstring = f'{xcoord:05d}'
            ystring = f'{ycoord:05d}'
            ystringl = f'{ycoordl:05d}'
            wstring = f'{width:05d}'
            hstring = f'{height:05d}'
            ocrstring = " " + "[" + ocr + "]"  
#             print("count {} {} coord {},{},{},{}\n".format(count,globalcount,height,width,xcoord,ycoord))
            entry = escape(directory_name + " " + pagenostring + ":" + identstring  + " " + ocrstring)
            comment =  "{} p {} x {} y {} h {} w {}".format(directory_name + ".djvu", pageno,xcoord,ycoordl, width, height)
            description_static = "※ " +  dirname_base + " "
            description = description_static + countstring + " ({})".format(globalcount) + " " + status 
            coordinates = xstring + "," + ystringl + "," + wstring + "," + hstring + "&page=" + pagenostring	
            snippet = "file:" + "../../DjVu/" + directory_name + ".djvu?djvuopts=&highlight=" + coordinates
            ixf.write(entry + ";" + snippet + ";" + comment + ";" + description + "\n")            
    lf.close()        

ixf.close()
print("Finished {}\n".format(globalcount))
