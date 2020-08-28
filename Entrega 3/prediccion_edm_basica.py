import scipy as sp
from scipy.integrate import odeint
from datetime import datetime

#Parametros

Ω = 7.27e-5 # rad / s , rotacion de la tierra
mt = 5.972e24 # kg , masa de la tierra
G = 6.67408e-11 # G = 6.67408e-11 m3 kg-1 s-2

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

ti = '2020-07-31T22:59:42.000000'
ti = ti.split("T")
ti = "{} {}".format(ti[0],ti[1])
ti = datetime.strptime(ti, '%Y-%m-%d %H:%M:%S.%f')

tf = '2020-08-02T00:59:42.000000'
tf = tf.split("T")
tf = "{} {}".format(tf[0],tf[1])
tf = datetime.strptime(tf, '%Y-%m-%d %H:%M:%S.%f')

deltaT = (tf-ti).total_seconds()

t = sp.linspace(0, deltaT, 10000)

# INICIO

x_i=397366.988406# m
y_i=2221745.734184# m
z_i=-6712844.599103# m
vx_i=2338.335745# m/s
vy_i=-6872.261583# m/s
vz_i=-2137.043046# m/s

z0 = sp.array([x_i,y_i,z_i,vx_i,vy_i,vz_i])

sol = odeint(satelite, z0, t)

final_estimado = sol[-1,:3] #m

x_f =1822794.314710# m
y_f = 6837567.652326# m
z_f = -103204.079648# m

final_real = [x_f,y_f,z_f] #m

diferencia = sp.sqrt(sp.dot((final_real-final_estimado),(final_real-final_estimado))) #m

print (diferencia)

# INICIO
#    <OSV>
#      <TAI>TAI=2020-07-31T23:00:19.000000</TAI>
#      <UTC>UTC=2020-07-31T22:59:42.000000</UTC>
#      <UT1>UT1=2020-07-31T22:59:41.791778</UT1>
#      <Absolute_Orbit>+22721</Absolute_Orbit>
#      <X unit="m">397366.988406</X>
#      <Y unit="m">2221745.734184</Y>
#      <Z unit="m">-6712844.599103</Z>
#      <VX unit="m/s">2338.335745</VX>
#      <VY unit="m/s">-6872.261583</VY>
#      <VZ unit="m/s">-2137.043046</VZ>
# FINAL
#    <OSV>
#      <TAI>TAI=2020-08-02T01:00:19.000000</TAI>
#      <UTC>UTC=2020-08-02T00:59:42.000000</UTC>
#      <UT1>UT1=2020-08-02T00:59:41.792925</UT1>
#      <Absolute_Orbit>+22737</Absolute_Orbit>
#      <X unit="m">1822794.314710</X>
#      <Y unit="m">6837567.652326</Y>
#      <Z unit="m">-103204.079648</Z>
#      <VX unit="m/s">1504.405694</VX>
#      <VY unit="m/s">-503.962104</VY>
#      <VZ unit="m/s">-7429.411565</VZ>