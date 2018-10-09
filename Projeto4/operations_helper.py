def get_color_distortion(incomeRGB,codebookRGB):
  x = incomeRGB[0]**2 + incomeRGB[1]**2 + incomeRGB[2]**2

  v = codebookRGB[0]**2 + codebookRGB[1]**2 + codebookRGB[2]**2

  a1 = float(incomeRGB[0])*float(codebookRGB[0])
  a2 = float(incomeRGB[1])*float(codebookRGB[1])
  a3 = float(incomeRGB[2])*float(codebookRGB[2])
  xv = (a1 + a2 +a3)**2

  if(v <=  0):
    v = 1

  p = float(xv)/float(v)
  if(p > x):
    p = x
  colordist = (float(x)-p)**0.5
  return colordist


def update_rgb(new_pixel,codewordRGB, f):

    r = (f*codewordRGB[0] + new_pixel[0])/(f+1)
    g = (f*codewordRGB[1] + new_pixel[1])/(f+1)
    b = (f*codewordRGB[2] + new_pixel[2])/(f+1)

    if((r > 255 ) or (g > 255 ) or (b > 255 )):
      print('new_pixel: ', new_pixel)
      print('codepixel: ', codewordRGB)
      print('f: ', f)
      print('\n')
    return [r,g,b]
