import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft

l1 = 12.34968539104614
l2 = 0.7470061799879233
c1 = 0.00001129485861537885
c2 = 0.000012076179949636138
r1 = 112.5937626787764
r2 = 38.8059391938039
r3 = 1017.89986650661
r4 = 514.4844215282689
countN = 8192
dt = 0.019634954084936207
harmonicnumber = 4
pathsignalfile = "9.txt"


def zc(w, c):
    return 1 / (1j * w * c)


def zl(w, l):
    return 1j * w * l


def zr(r):
    return r


def zleft(w):
    return zc(w, c1) + zr(r2) + zl(w, l2) + zr(r3)


def zright(w):
    return zr(r4) + zc(w, c2)


def zgen(w):
    return zl(w, l1) + zr(r1) + (zleft(w) * zright(w)) / (zleft(w) + zright(w))


def H(w):
    return (zright(w) * zr(r3)) / (zgen(w) * (zleft(w) + zright(w)))


def AH(w):
    return abs(H(w))


fig, ax = plt.subplots()
plt.plot([AH(w) for w in range(1, 100)])
ax.set_xlabel(r'$\omega$')
ax.set_ylabel(r'A($\omega$)')
fig.savefig('Frequency response.jpeg')

signalvalue = []
signaltime = []
with open(pathsignalfile) as f:
    for i, line in enumerate(f):
        signalvalue.append(list(map(float, line.split()))[0])
        signaltime.append(i * dt)
f.close()
fig, ax = plt.subplots()
plt.plot(signaltime, signalvalue)
ax.set_xlabel('t')
ax.set_ylabel('U')
fig.savefig('Graphic signal.jpeg')

signalspectr = abs(fft(signalvalue))
h_signalspectr = signalspectr[:(countN // 2)]
fig, ax = plt.subplots()
plt.plot(h_signalspectr)
ax.set_xlabel('n')
ax.set_ylabel('U')
fig.savefig('Graphic harmonic.jpeg')

freqU = [[2 * np.pi * i * (1 / (countN * dt)), h_signalspectr[i]] for i in range(len(h_signalspectr))]
x = [i[0] for i in freqU]
y = [i[1] for i in freqU]
fig, ax = plt.subplots()
plt.plot(x, y)
ax.set_xlabel(r'$\omega$')
ax.set_ylabel('U')
fig.savefig('Graphic spectr.jpeg')

[w, U] = list(filter(lambda x: x[1] > 22500, freqU))[0]
# print(freqU)
print('w: ', w)
print('U: ', U)
# print('4: ', U * AH(w))
print(AH(w))
f = open('./result.txt', 'w')
f.write(str(AH(w)))
f.close()
