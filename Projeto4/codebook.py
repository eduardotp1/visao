#imports
import cv2 
import os
import glob
import numpy as np
import pickle


def get_dist(pixelRGB,cbRGB):
  x = pixelRGB[0]**2 + pixelRGB[1]**2 + pixelRGB[2]**2
  v = cbRGB[0]**2 + cbRGB[1]**2 + cbRGB[2]**2
  xv = (float(pixelRGB[0])*float(cbRGB[0]) + float(pixelRGB[1])*float(cbRGB[1]) + float(pixelRGB[2])*float(cbRGB[2]))**2
  if(v <=  0):
    v = 1
  p = float(xv)/float(v)
  if(p > x):
    p = x
  colordist = (float(x)-p)**0.5
  return colordist


def get_new_rgb(pixelRGB,codewordRGB, f):
    r = ((f*codewordRGB[0])+ pixelRGB[0])/(f+1)
    g = ((f*codewordRGB[1]) + pixelRGB[1])/(f+1)
    b = ((f*codewordRGB[2]) + pixelRGB[2])/(f+1)
    return [r,g,b]


folder_path = './backgrounds'
 
data_path = os.path.join(folder_path,'*g')
files = glob.glob(data_path)

images = []

for file_in in files:
    img = cv2.imread(file_in)
    images.append(img)

w,h, s = images[0].shape

codebook = [[0 for j in range(h)] for k in range(w)]


epsolon = 12
alfa = 0.7
beta = 1.1
t = 1

##-------------COLINHA ------------------------
#[ (R,G, B), (Imin,Imax, Frequency, lambda, p , q)]
##---------------------------------------------

progress = 0 


for img in images:
    progress += 1
    print('Imagem {0}/{1}'.format(progress,len(images)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for i in range(0,len(img)):
        for j in range(0,len(img[i])):
            nowPixel = img[i][j]
            brightness =  (nowPixel[0]**2 + nowPixel[1]**2 + nowPixel[2]**2)**(0.5)
            cb = codebook[i][j]
            codeword = [[nowPixel[0], nowPixel[1], nowPixel[2]], [brightness, brightness,1, t-1, t,t]]
            if(cb != 0):
                append = True
                for cw in cb:
                    #distoraoo RGB
                    colorDist  = get_dist(nowPixel, cw[0])
                    firstBool = colorDist <=  epsolon
                    #brilhos
                    imin = cw[1][1] * alfa
                    imax = min(beta*cw[1][1], cw[1][0]/alfa)
                    secondBool  = (brightness >= imin) and (brightness <= imax)
                    if(firstBool and secondBool):
                        append = False
                        f = cw[1][2]
                        new_rgb = get_new_rgb(nowPixel, cw[0], f)
                        imin = min(brightness,cw[1][0])
                        imax = max(brightness,cw[1][1])
                        f = f + 1
                        lbda = max(cw[1][3],t-cw[1][5])
                        q = t
                        #update existing codeword
                        cw[0] = new_rgb
                        cw[1][0] = imin
                        cw[1][1] = imax
                        cw[1][2] = f
                        cw[1][3] = lbda
                        cw[1][5] = q
                
                if(append):
                    codebook[i][j].append(codeword)
            else:
                codebook[i][j] = [codeword]
    t+=1

size =  len(images)

for i in codebook:
    for j in i:
        filteredCodeword  = [];
        for k in j:
            if(k[1][3] >= size/2 ):
                filteredCodeword.append(k)
        j = filteredCodeword
        
print('Terminou')


pickle.dump( codebook, open( "treinamento.pickle", "wb" ) )
