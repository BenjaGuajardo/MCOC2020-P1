import scipy as sp
from scipy.integrate import odeint
import matplotlib.pylab as plt

#Parametros

Ω = (7.27 * 10 ** -5)/(1/3600) # rad / h , rotacion de la tierra
mt = 5.972e24 # kg , masa de la tierra
G = (6.674e-11)*(1e-9)*(3600.**2) # G = 6.67408e-11 m3 kg-1 s-2 -> km3 kg-1 h-2

def satelite(z,t):
    
    zp = sp.zeros(6)
    
    zp[0:3] = z[3:6]
    
    R = sp.array([[sp.cos(Ω * t), -sp.sin(Ω * t), 0],[sp.sin(Ω * t), sp.cos(Ω * t), 0],[0, 0, 1]])
    Rp = Ω * sp.array([[-sp.sin(Ω * t), -sp.cos(Ω * t), 0],[sp.cos(Ω * t), -sp.sin(Ω * t), 0],[0, 0, 0]])
    Rpp = (Ω ** 2) * sp.array([[-sp.cos(Ω * t), sp.sin(Ω * t), 0],[-sp.sin(Ω * t), -sp.cos(Ω * t), 0],[0, 0, 0]])
    
    r = sp.sqrt(z[0]**2+z[1]**2+z[2]**2) #distancia entre la tierra y el satelite.
    z1 = z[0:3]
    z2 = z[3:6]    
    cte = -G * mt / (r ** 3)
    
    zp[3:6] = cte * z1 - R.T @ Rpp @ z1 - 2 * R.T @ Rp @ z2
    
    return zp

#vector de tiempo en horas
horas = 3.31 #h   t* ≈ 3.3 h
t = sp.linspace(0, horas, 10000)

#parte en 6371+700 km, con vi = X km/h

x0 = 700.
vi = 24550.55 #km/h  vi* ≈ 24550.55 km/h

z0 = sp.array([6371.+x0, 0, 0, 0, vi, 0])

sol = odeint(satelite, z0, t)

#GRAFICOS

plt.figure(1)

x = sol[:,0]
y = sol[:,1]
z = sol[:,2]

plt.subplot(3,1,1)
plt.plot(t, x, color = 'red')
#plt.hlines(6371.+80, 0., horas, color = 'red', linestyle = '--')
plt.xlabel('t [h]')
plt.ylabel('x(t) [km]')
plt.xlim(0,horas)
plt.grid()

plt.subplot(3,1,2)
plt.plot(t, y, color = 'red')
#plt.hlines(6371.+80, 0., horas, color = 'red', linestyle = '--')
plt.xlabel('t [h]')
plt.ylabel('y(t) [km]')
plt.xlim(0,horas)
plt.grid()

plt.subplot(3,1,3)
plt.plot(t, z, color = 'red')
plt.xlabel('t [h]')
plt.ylabel('z(t) [km]')
plt.xlim(0,horas)
plt.grid()

plt.tight_layout() 

plt.savefig('figura 1.png')

plt.figure(2) #figura de la tierra y orbita

r = sp.sqrt(x**2+y**2+z**2)
plt.plot(t, r, color = 'red', label = '$Satélite$')
plt.xlabel('t [h]')
plt.ylabel('r(t) [km]')
plt.hlines(6371.+80, 0., horas, color = 'dodgerblue', linestyle = '--',label = '$Atmósfera$')
plt.hlines(6371., 0., horas, color = 'brown', label = '$Tierra$')
plt.xlim(0,horas)
plt.grid()
plt.legend(loc = 1)
plt.tight_layout()

plt.savefig('figura 2.png')

plt.figure(3)

plt.plot(x, y, color = 'red', label = '$Satélite$')
angulo = sp.linspace(0, 2*sp.pi, 1000)
xtierra = 6371. * sp.cos(angulo)
ytierra = 6371. * sp.sin(angulo)
xatm = (6371.+80) * sp.cos(angulo)
yatm = (6371.+80) * sp.sin(angulo)
plt.plot(xatm, yatm, color="dodgerblue", linestyle = '--',label = '$Atmósfera$')
plt.plot(xtierra, ytierra, color="brown", label = '$Tierra$')
plt.axis('equal')
plt.grid()
plt.legend(loc = 1)
plt.tight_layout() 

plt.savefig('figura 3.png')

plt.show()