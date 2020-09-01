import scipy as sp
from scipy.integrate import odeint
import matplotlib.pylab as plt

m = 1. #kg
f = 1. #Hz
chi = 0.2
w = 2*sp.pi*f
k = m*w**2
c = 2*chi*w*m

def eulerint(zp,z0,t,Nsubdivisiones=1):
    
    Nt = len(t)
    Ndim = len(sp.array(z0))
    z = sp.zeros((Nt,Ndim))

    z[0,:] = z0
    
    # z(i+1) = zp_i * dt + z_i
    for i in range(1,Nt):
        
        t_anterior = t[i-1]
        dt = (t[i] - t[i-1])/Nsubdivisiones
        z_temp = z[i-1,:].copy()
        
        for k in range(Nsubdivisiones):          
            z_temp += dt * zp(z_temp,t_anterior + k*dt)
        
        z[i,:] = z_temp
    
    return z

def zp(z,t):
    
    zp = sp.zeros(2)
    zp[0] = z[1]
    
    x = z[0]
    xp = z[1]
    
    zp[1] = -k*x/m - c*xp/m
    
    return zp

# x(0)=1 ; x'(0)=1
z0 = [1,1]

# tiempo entre 0 y 4
t = sp.linspace(0,4,100)

#Solucion real - Lo calcule en la TI
c1 = (sp.sqrt(c**2-4*k*m)*m-(c+2*m)*m)/(sp.sqrt(c**2-4*k*m)*m-c*m)
c2 = (2*m*m)/(sp.sqrt(c**2-4*k*m)*m-c*m)
z_real = c2*sp.exp(((sp.sqrt(c**2-4*k*m))/(2*m)-c/(2*m))*t)+c1*sp.exp(((-sp.sqrt(c**2-4*k*m))/(2*m)-c/(2*m))*t)

#Solucion con odeint
z_odeint = odeint(zp,z0,t)

#Solucion con el metodo de euler para diferentes subdivisiones.
z_euler_1 = eulerint(zp,z0,t, Nsubdivisiones=1)
z_euler_10 = eulerint(zp,z0,t, Nsubdivisiones=10)
z_euler_100 = eulerint(zp,z0,t, Nsubdivisiones=100)

plt.figure()
plt.xlim(0,4)
plt.xlabel('t')
plt.ylabel('x(t)')

plt.plot(t,z_real,label='real',color='black',linewidth=2)
plt.plot(t,z_odeint[:,0],label='odeint', color='dodgerblue')
plt.plot(t,z_euler_1[:,0],label='eulerint 1', color='green', linestyle='--')
plt.plot(t,z_euler_10[:,0],label='eulerint 10', color='red', linestyle='--')
plt.plot(t,z_euler_100[:,0],label='eulerint 100', color='orange', linestyle='--')

plt.legend()
plt.savefig('Entrega4.png')
plt.show()