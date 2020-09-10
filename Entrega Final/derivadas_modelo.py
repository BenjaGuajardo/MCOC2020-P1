from sympy import Symbol, diff, sqrt
from legendre_np import legendre
x = Symbol('xc[0]')
y = Symbol('xc[1]')
z = Symbol('xc[2]')
J4 = Symbol('J4')
J5 = Symbol('J5')

r = sqrt(x**2+y**2+z**2)
sinθ = z/r

u = J4*(legendre(0,4,sinθ))/(r**5) + J5*(legendre(0,5,sinθ))/(r**6)

Fx = u.diff(x)
Fy = u.diff(y)
Fz = u.diff(z)

print (Fx)
print (Fy)
print (Fz)