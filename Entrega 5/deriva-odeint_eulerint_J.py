from time import perf_counter
ti = perf_counter()
import scipy as sp
from scipy.integrate import odeint
from leer_eof import leer_eof
from matplotlib import pyplot as plt

fname = 'S1B_OPER_AUX_POEORB_OPOD_20200821T111155_V20200731T225942_20200802T005942.EOF'
eof_list = leer_eof(fname)

tiempo = eof_list[0]
x = eof_list[1]
y = eof_list[2]
z = eof_list[3]
vx = eof_list[4]
vy = eof_list[5]
vz = eof_list[6]

z0 = [x[0],y[0],z[0],vx[0],vy[0],vz[0]]
final_real = [x[-1],y[-1],z[-1]]
deltaT = tiempo[-1]

#Parametros

Ω = 7.27e-5 # rad / s , rotacion de la tierra
mt = 5.972e24 # kg , masa de la tierra
G = 6.67408e-11 # G = 6.67408e-11 m3 kg-1 s-2
J2 = 1.75553e10*(1000**5) # km5 -s2 -> m5
J3 = -2.61913e11*(1000**6) # km6 s-2 -> m6

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

    # Se incluye J2
    zp[3] = zp[3] + J2*z[0]*(6*z[2]**2-3*(z[0]**2+z[1]**2)/2)/(r**7)
    zp[4] = zp[4] + J2*z[1]*(6*z[2]**2-3*(z[0]**2+z[1]**2)/2)/(r**7)
    zp[5] = zp[5] + J2*z[2]*(3*z[2]**2-9*(z[0]**2+z[1]**2)/2)/(r**7)

    # Se icluye J3
    zp[3] = zp[3] + J3*z[0]*z[2]*(10*z[2]**2-15*(z[0]**2+z[1]**2)/2)/(r**9)
    zp[4] = zp[4] + J3*z[1]*z[2]*(10*z[2]**2-15*(z[0]**2+z[1]**2)/2)/(r**9)
    zp[5] = zp[5] + J3*((4*z[2]**2*z[2]**2-3*(z[0]**2+z[1]**2))+1.5*(z[0]**2+z[1]**2)**2)/(r**9)
    
    return zp

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

t = sp.linspace(0, deltaT, len(tiempo))

t1=perf_counter()
z_odeint = odeint(satelite, z0, t)
t2=perf_counter()
z_eulerint = eulerint(satelite,z0,t, Nsubdivisiones=1)
t3=perf_counter()

t_odeint = t2-t1
t_eulerint = t3-t2

print (f'tiempo odeint = {t_odeint} s')
print (f'tiempo eulerint = {t_eulerint} s')

x_o = z_odeint[:,0]
y_o = z_odeint[:,1]
z_o = z_odeint[:,2]

x_e = z_eulerint[:,0]
y_e = z_eulerint[:,1]
z_e = z_eulerint[:,2]

''' DERIVA ODEINT - EULERINT '''

deriva = sp.zeros(len(tiempo))

for i in range(len(tiempo)):
    deriva[i] = sp.sqrt(sp.dot((z_odeint[i,:3] - z_eulerint[i,:3]), (z_odeint[i,:3] - z_eulerint[i,:3])))

z_of = sp.sqrt(sp.dot(z_odeint[-1,:3],z_odeint[-1,:3]))
error = sp.round_(deriva[-1]/z_of,1)

print (f'Error = {error*100} %')

dist_max = sp.round_(sp.amax(deriva)/1000,1)

plt.figure(1)

plt.title(f'Distancia entre eulerint y odeint, $δ_m$ = {dist_max} (km)')
plt.ylabel('Deriva, δ [KM]')
plt.xlabel('Tiempo, $t$ [h]')
plt.plot(t/3600,deriva/1000)
plt.tight_layout()
plt.savefig('pregunta4_deriva.png')

tf= perf_counter()

ttotal = tf-ti

print (f'Código demora {ttotal} s')
plt.show()