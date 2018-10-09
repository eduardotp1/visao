#imports
import cv2 as cv
import os
import glob
import numpy as np
import operations_helper as oph
import codeword
import pickle



#todas as imagens devem ter a mesma resolução
folder_path = './back3'

data_path = os.path.join(folder_path,'*g')
files = glob.glob(data_path)

#list with all images of the trainning
data = []

print('Reading images...')
for f1 in files:
    img = cv.imread(f1)
    data.append(img)

width,height, whatever = data[0].shape
print('width', width)
print('height', height)

print("Constructing codebook...")
codebook = [[0 for j in range(height)] for k in range(width)]



print("Total de imagens: {0}".format(len(data)))
e = 12 #epsolon aceito na variação rgb
a = 0.5
b = 1.2
t = 0
counter = 0
for img_bgr in data:
    counter +=1
    print("Imagem {0}".format(counter))
    t+=1
    img = img_bgr.copy()
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    for row in range(0,len(img)):
        for column in range(0,len(img[row])):
            pixel = img[row][column]
            brightness =  (pixel[0]**2 + pixel[1]**2 + pixel[2]**2)**(0.5)
            cb = codebook[row][column]
            now_codeword = codeword.codeword((pixel[0], pixel[1], pixel[2]), brightness, brightness,1, t-1, t,t)

            if(cb != 0):
                is_new_cw = True
                for cw in cb:
                    colorDist  = oph.get_color_distortion(pixel, cw.get_v())
                    color_condition = colorDist <=  e
                
                    ilow = cw.get_imax() * a
                    ihi = min(b*cw.get_imax(),cw.get_imin()/a)
                    brightness_condition  = (brightness >= ilow) and (brightness <= ihi)

                    if(brightness_condition and color_condition):
                        is_new_cw = False
                        f = cw.get_f()
                        new_rgb = oph.update_rgb(pixel, cw.get_v(), f)
                        imin = min(brightness,cw.get_imin())
                        imax = max(brightness,cw.get_imax())
                        f = f + 1
                        lb = max(cw.get_lb(),t-cw.get_q())
                        q = t
                        cw.set_v(new_rgb)
                        cw.set_imin(imin)
                        cw.set_imax(imax)
                        cw.set_f(f)
                        cw.set_lb(lb)
                        cw.set_q(q)
                
                if(is_new_cw):
                    codebook[row][column].append(now_codeword)
            else:
                rgb= [pixel[0], pixel[1], pixel[2]]
                codebook[row][column] = [now_codeword]



print("Cleaning codebook...")

n =  len(data)

for i in codebook:
    for j in i:
        cleanedCodeword  = [];
        for k in j:
            if(k.get_lb() >= n/2 ):
                cleanedCodeword.append(k)
        j = cleanedCodeword


pickle.dump( codebook, open( "save3.pickle", "wb" ) )

print("Codebook constructed and saved.")
