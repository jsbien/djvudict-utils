#!/usr/bin/env python3
# virtual environment may be needed !!!

# Janusz S. Bień 2023
# licensed under the Creative Commons Zero v1.0 Universal
# (Creative Commons CC0 Public Domain Dedication)

import os
import re
from PIL import Image
# import cv2
import subprocess

def escape(s):	
    quote = s.translate(str.maketrans({'"':'""'}))
#     semicolon = quote.translate(str.maketrans({';':'";"'}))
    return '"' + quote + '"'

def find_image(l):
    commented_line = "% " + l
    f.write(commented_line)
    numbers = re.findall(r'\d+', line)
    result = list(map(int, numbers))
    ident = result[1]
    identstring = f'{ident:05d}'
    image_name =  "/lib_" + identstring           
    image_fullname = dirname + "/lib_" + identstring
    image_bmp = image_fullname + ".bmp"
    image_png = image_fullname + ".png"
    my_image = Image.open(image_bmp)
    my_image.save(image_png)
    f.write(identstring + ":\n")
    f.write(r"\includegraphics[width=.05\textwidth,height=0.5\textheight,keepaspectratio]{" + image_name + "}\n")

preamble = (r"\documentclass{article}"
"\n"
"% Output of djvudict2PDF.py by Janusz S. Bień\n"           
r"\usepackage{graphicx}"
            "\n"
r"\newcommand{\mynumber}{\arabic{myimage}\stepcounter{myimage}\ }"
            "\n\n"         
r"\begin{document}"
            "\n"
r"\newcounter{myimage}"
            "\n")
# print(preamble)

postamble = (r"\end{document}"
             "\n"
"%%% Local Variables:\n"
"%%% mode: latex\n"
"%%% TeX-engine: xetex\n"          
"%%% TeX-master: t\n"
"%%% End:\n")
# print(postamble)

tex_page = (r"\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{page.png}" +
            "\n" + r"\newpage" + "\n")

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
# if "auto" in subfolders: subfolders.remove("auto")

# https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
globalcount = 0
subdir_count = 0
for dirname in list(subfolders):
    print(os.path.basename(dirname))
    dirname_base = os.path.basename(dirname)
    if dirname_base == "auto": continue
    base = 	os.path.splitext(dirname_base)[0]
#     dirnumbers = re.findall(r'\d+', dirname)
    subdir_count += 1
#     pageno = dirnumbers[-1]
    pageno = subdir_count
    filename = base +".tex"
    # https://www.w3schools.com/python/python_file_write.asp
    f = open(filename, "w", encoding="utf8")
    #f.write("Woops! I have deleted the content!")
    f.write(preamble)

#     print(os.path.exists(dirname + '/page.png'))
    
    if not os.path.exists(dirname + 'page.png'):
        pimage_fullname = dirname + "/page"
        pimage_bmp = pimage_fullname + ".bmp"
        pimage_png = pimage_fullname + ".png"
        image = Image.open(pimage_bmp)
        image.save(pimage_png)
#         image.save(image_png)
#         page_image = Image.open(dirname + "/page.bmp")
#         page_image.show()
#         page_image.save(dirname + "/page.png")
#         page_image.show()
#             
#         print("Filename: ", page_image.filename)
#         print("Format: ", page_image.format)
#         page_image.close
        
    graphicspath = r"\graphicspath{{" + dirname + "/}}\n"
    f.write(graphicspath)
    f.write(tex_page)
            
    
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
#             status = "new"            
#            numbers = re.findall(r'\d+', line)
#             print("OK: {} {}".format(numbers, line.strip()))
            find_image(line)
        elif line.startswith("Records jb2_matched_symbol_with_refinement_add_to_image_and_library:"):
            count += 1
            status = "add"            
            find_image(line)
        elif line.startswith("Records jb2_matched_symbol_copy_to_image_without_refinement:"):
            count += 1
            status = "copy"            
            find_image(line)
        elif line.strip() == "Records jb2_end_of_data":
            count += 1
            print("{} {}: {}".format(dirname, count, line.strip()))
        else:
            print("TO DO: {}".format(line.strip()))
        if count != 1:
            countstring = f'{count:05d}'
            pagenostring = f'{pageno:03d}'

    f.write(postamble)
    f.close()
    # `xelatex  -file-line-error    -interaction=nonstopmode 0_Ungler1-02_PT03_113.te
    subprocess.call(["xelatex","-file-line-error","-interaction=nonstopmode",filename])        

print("Finished {}\n".format(globalcount))
