import numpy as np
from datos import t_vuelo, v_vuelo
t_vuelo = np . linspace (0 , 120 , 121)
v_vuelo = 2500 * (1 / (1 + np.exp ( -0.05 * ( t_vuelo - 60) ) ) ) - 118