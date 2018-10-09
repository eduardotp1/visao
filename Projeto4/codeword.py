class codeword:
  def __init__(self, v, imin, imax, f, lb, p,q):
    self.__imin = imin
    self.__imax = imax
    self.__f = f
    self.__lb = lb
    self.__p = p
    self.__q = q
    self.__v = v

#getters
  
  def get_imin(self):
    return self.__imin

  def get_imax(self):
    return self.__imax

  def get_f(self):
    return self.__f

  def get_lb(self):
    return self.__lb

  def get_q(self):
    return self.__q

  def get_p(self):
    return self.__p 

  def get_v(self):
    return self.__v



# setters

  def set_v(self, values):
    self.__v = values

  def set_imin(self, value):
    self.__imin = value

  def set_imax(self, value):
    self.__imax = value

  def set_f(self, value):
    self.__f = value

  def set_lb(self, value):
    self.__lb = value

  def set_q(self, value):
    self.__q = value

