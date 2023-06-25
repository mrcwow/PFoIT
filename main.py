import matplotlib.pyplot as plt
import numpy as np
import cmath
import sympy as sp

e = 0.1
d = 0.5
N = 100
delta = d / N
ae = np.linspace(-10, 10, 100)
zones = N + 1
barrs = [i * delta for i in range(zones)]


def f(ae):
    return ae ** 2 * 0.1 + 1.9


def e_p(ae):
    return f(ae) if 0 < ae <= d else 0


def gamma(ae):
    return 1j * cmath.sqrt(e - e_p(ae))


a0, b0, aI, bI, aI1, bI1, aN, bN = sp.symbols('a0, b0, aI, bI, aI1, bI1, aN, bN')
a0 = aI
b0 = bI
for i in range(zones):
    aei = barrs[i]
    g = gamma(aei - delta / 2)
    g1 = gamma(aei + delta / 2)
    eq1 = aI * sp.exp(g * aei) + bI * sp.exp(-g * aei) - aI1 * sp.exp(g1 * aei) - bI1 * sp.exp(-g1 * aei)
    eq2 = g * aI * sp.exp(g * aei) - g * bI * sp.exp(-g * aei) - g1 * aI1 * sp.exp(g1 * aei) + g1 * bI1 * sp.exp(-g1 * aei)
    answ = sp.solvers.solve((eq1, eq2), (aI, bI))
    a0 = a0.subs(answ)
    a0 = sp.simplify(a0.subs({aI1: aI, bI1: bI}))
    b0 = b0.subs(answ)
    b0 = sp.simplify(b0.subs({aI1: aI, bI1: bI}))

rA0 = sp.simplify(a0.subs({aI: aN, bI: bN}))
rB0 = sp.simplify(b0.subs({aI: aN, bI: bN}))

a0, b0, aN, bN = sp.symbols('a0, b0, aN, bN')
A_0 = 1
B_N = 0
eq1 = (rA0 - a0).subs({a0: A_0, bN: B_N})
eq2 = (rB0 - b0).subs({a0: A_0, bN: B_N})
answ = sp.solvers.solve((eq1, eq2), (b0, aN))
B_0 = answ[b0]
A_N = answ[aN]

D = (abs(A_N)) ** 2
file = open("./result.txt", "w")
file.write(str(D))
file.close()

AB = [[A_0, B_0]]
for i in range(zones):
    aei = barrs[i]
    g = gamma(aei - delta / 2)
    g1 = gamma(aei + delta / 2)
    aI = AB[i][0]
    bI = AB[i][1]
    eq1 = aI * sp.exp(g * aei) + bI * sp.exp(-g * aei) - aI1 * sp.exp(g1 * aei) - bI1 * sp.exp(-g1 * aei)
    eq2 = g * aI * sp.exp(g * aei) - g * bI * sp.exp(-g * aei) - g1 * aI1 * sp.exp(g1 * aei) + g1 * bI1 * sp.exp(-g1 * aei)
    answ = sp.solvers.solve((eq1, eq2), (aI1, bI1))
    AB.append([answ[aI1], answ[bI1]])


def psi(ae, d, AB, delta):
    if ae < 0:
        return sp.re(AB[0][0] * sp.exp(gamma(ae) * ae) + AB[0][1] * sp.exp(-gamma(ae) * ae))
    elif ae > d:
        return sp.re(AB[-1][0] * sp.exp(gamma(ae) * ae) + AB[-1][1] * sp.exp(-gamma(ae) * ae))
    else:
        return sp.re(AB[sp.floor(ae / delta) + 1][0] * sp.exp(gamma(ae) * ae) + AB[sp.floor(ae / delta) + 1][1] * sp.exp(-gamma(ae) * ae))


fig, ax = plt.subplots()
psi = [psi(ae, d, AB, delta) for ae in ae]
ax.plot(ae, psi)
ax.set_xlabel(r'ϰ')
ax.set_ylabel(r'$\Psi$')
fig.savefig('Graphic wave function.jpeg')
