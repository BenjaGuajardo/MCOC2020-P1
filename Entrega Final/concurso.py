from numpy import *
import scipy as sp
from scipy.integrate import odeint
from leer_eof import leer_eof
from sys import argv
eofname = 'P1.EOF'
eofname_list = ['P1.EOF','P2.EOF','P3.EOF','P4.EOF','P5.EOF','P6.EOF','P7.EOF']
delta_sum = 0

for i in range(7):

    #eofname = argv[1]
    
    tiempo, x, y, z, vx, vy, vz = leer_eof(eofname_list[i])
    
    deltaT = tiempo[-1]
    z0 = [x[0],y[0],z[0],vx[0],vy[0],vz[0]]
    
    ''' PARAMETROS '''
    
    km3 = (1000.)**3
    km5 = (1000.)**5
    km6 = (1000.)**6
    km7 = (1000.)**7
    km8 = (1000.)**8
    
    G = 6.67408e-11
    mt = 5.972e24
    
    μ = 398600.4415*km3
    Ω = 7.2921150e-5
    
    J2 = 1.75552804862579e10*km5
    J3 = -2.61913286025122e11*km6
    J4 = -1.068190333775140e15*km7
    J5 = -9.58077177300831000e17*km8
    
    ''' FUNCION SATELITE '''
    
    def satelite(z,t):
        
        c = cos(Ω*t)
        s = sin(Ω*t)
        
        R = array([
                [c, -s, 0],
                [s,  c, 0],
                [0,  0, 1]])
        
        Rp = Ω*array([
                [-s, -c, 0],
                [ c, -s, 0],
                [ 0,  0, 0]])
        
        Rpp = (Ω**2)*array([
                [-c,  s, 0],
                [-s, -c, 0],
                [ 0,  0, 0]])
        
        x = z[0:3]
        xp = z[3:6] 
        
        r = sqrt(np.dot(x,x))
        
        xc  = R@x
        rnorm = xc/r
        Fg = -(μ/r**2)*rnorm
        
        FJ2 =(J2*xc)/(r**7)
        FJ2[0]=FJ2[0]*(6*xc[2]**2-1.5*(xc[0]**2 + xc[1]**2))
        FJ2[1]=FJ2[1]*(6*xc[2]**2-1.5*(xc[0]**2 + xc[1]**2))        
        FJ2[2]=FJ2[2]*(3*xc[2]**2-4.5*(xc[0]**2 + xc[1]**2))  
        
        FJ3 = zeros(3)
        FJ3[0] = ((J3 * xc[0]*xc[2])/(r**9))*(10*xc[2]**2-7.5*(xc[0]**2 + xc[1]**2))
        FJ3[1] = ((J3 * xc[1]*xc[2])/(r**9))*(10*xc[2]**2-7.5*(xc[0]**2 + xc[1]**2))     
        FJ3[2] = J3*                      (1/(r**9))*(4*xc[2]**2*(xc[2]**2-3*(xc[0]**2 + xc[1]**2))+1.5*((xc[0]**2 + xc[1]**2)))
    
        FJE= zeros(3)
        FJE[0]= -5*J4*xc[0]*(35*xc[2]**4/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**2) - 15*xc[2]**2/(4*(xc[0]**2 + xc[1]**2 + xc[2]**2)) + 0.375)/(xc[0]**2 + xc[1]**2 + xc[2]**2)**(7/2) + J4*(-35*xc[0]*xc[2]**4/(2*(xc[0]**2 + xc[1]**2 + xc[2]**2)**3) + 15*xc[0]*xc[2]**2/(2*(xc[0]**2 + xc[1]**2 + xc[2]**2)**2))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2) - 6*J5*xc[0]*(63*xc[2]**5/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2)) - 35*xc[2]**3/(4*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(3/2)) + 15*xc[2]/(8*sqrt(xc[0]**2 + xc[1]**2 + xc[2]**2)))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**4 + J5*(-315*xc[0]*xc[2]**5/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(7/2)) + 105*xc[0]*xc[2]**3/(4*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2)) - 15*xc[0]*xc[2]/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(3/2)))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**3
        FJE[1]= -5*J4*xc[1]*(35*xc[2]**4/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**2) - 15*xc[2]**2/(4*(xc[0]**2 + xc[1]**2 + xc[2]**2)) + 0.375)/(xc[0]**2 + xc[1]**2 + xc[2]**2)**(7/2) + J4*(-35*xc[1]*xc[2]**4/(2*(xc[0]**2 + xc[1]**2 + xc[2]**2)**3) + 15*xc[1]*xc[2]**2/(2*(xc[0]**2 + xc[1]**2 + xc[2]**2)**2))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2) - 6*J5*xc[1]*(63*xc[2]**5/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2)) - 35*xc[2]**3/(4*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(3/2)) + 15*xc[2]/(8*sqrt(xc[0]**2 + xc[1]**2 + xc[2]**2)))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**4 + J5*(-315*xc[1]*xc[2]**5/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(7/2)) + 105*xc[1]*xc[2]**3/(4*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2)) - 15*xc[1]*xc[2]/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(3/2)))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**3
        FJE[2]= -5*J4*xc[2]*(35*xc[2]**4/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**2) - 15*xc[2]**2/(4*(xc[0]**2 + xc[1]**2 + xc[2]**2)) + 0.375)/(xc[0]**2 + xc[1]**2 + xc[2]**2)**(7/2) + J4*(-35*xc[2]**5/(2*(xc[0]**2 + xc[1]**2 + xc[2]**2)**3) + 25*xc[2]**3/(xc[0]**2 + xc[1]**2 + xc[2]**2)**2 - 15*xc[2]/(2*(xc[0]**2 + xc[1]**2 + xc[2]**2)))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2) - 6*J5*xc[2]*(63*xc[2]**5/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2)) - 35*xc[2]**3/(4*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(3/2)) + 15*xc[2]/(8*sqrt(xc[0]**2 + xc[1]**2 + xc[2]**2)))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**4 + J5*(-315*xc[2]**6/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(7/2)) + 525*xc[2]**4/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(5/2)) - 225*xc[2]**2/(8*(xc[0]**2 + xc[1]**2 + xc[2]**2)**(3/2)) + 15/(8*sqrt(xc[0]**2 + xc[1]**2 + xc[2]**2)))/(xc[0]**2 + xc[1]**2 + xc[2]**2)**3
      
        zp = zeros(6)
        zp[0:3] = xp
        zp[3:6] = R.T@(Fg + FJ2 + FJ3 + FJE - (2*Rp@xp + Rpp@x))
    
        return zp
    
    t = linspace(0, deltaT, len(tiempo))
    z_odeint = odeint(satelite, z0, t)
    
    x_o = z_odeint[:,0]
    y_o = z_odeint[:,1]
    z_o = z_odeint[:,2]
    vx_o = z_odeint[:,3]
    vy_o = z_odeint[:,4]
    vz_o = z_odeint[:,5]
    
    ''' ESCRITURA DE .PRED '''
    
    eof_out = eofname.replace('.EOF', '.PRED')
    
    with open(eof_out, 'w') as fout:
        fout.write('<?xml version="1.0" ?>\n')
        fout.write('<Earth_Explorer_File>\n')
        fout.write('<Data_Block type="xml">\n')
        fout.write(f'  <List_of_OSVs count="{len(tiempo)}">\n')
        for i in range(len(tiempo)):
            fout.write('    <OSV>\n')
            fout.write(f'      <UTC>UTC=2020-07-31T22:59:42.000000</UTC>\n      <X unit="m">{x_o[i]}</X>\n      <Y unit="m">{y_o[i]}</Y>\n      <Z unit="m">{z_o[i]}</Z>\n      <VX unit="m/s">{vx_o[i]}</VX>\n      <VY unit="m/s">{vy_o[i]}</VY>\n      <VZ unit="m/s">{vz_o[i]}</VZ>\n')
            fout.write('    </OSV>\n')
        fout.write('  </List_of_OSVs>\n')
        fout.write('</Data_Block>\n')
        fout.write('</Earth_Explorer_File>')