import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.rcParams["figure.figsize"] = (8, 8)
plt.rcParams["font.size"] = 14
plt.style.use('dark_background') # dark theme


def CalculatePhaseFromFocus(x, y, e):
    return np.sqrt(np.sum((e.r-np.array([x, y]))**2))*(2*np.pi/e.lambda0)


class Emitter():

    def __init__(self, x, y, c, f, phi, rMax=100, color="tab:blue", alpha=0.6):
        self.r, self.c, self.f, self.rMax, self.alpha = np.array(
            [x, y]), c, f, rMax, alpha
        self.color = color
        self.SetUp()
        self.SetPhase(phi)

    def Increment(self, dt):
        self.t += dt
        if self.t < self.t0:
            return
        for i, circle in enumerate(self.circles):
            r = i*self.lambda0 + self.Wrap(self.lambda0*self.phi/(2*np.pi) +
                                           self.c * self.t, self.lambda0)
            circle.set_height(2*r)
            circle.set_width(2*r)
            circle.set_alpha(self.alpha if i < ((self.t-self.t0)/self.T) else 0)

    def SetPhase(self, phi):
        self.phi = self.Wrap(phi, 2*np.pi)
        self.t0 = self.T*(1-self.phi/(2*np.pi))
        self.t = 0

    def SetUp(self):
        self.lambda0 = self.c/self.f
        self.T = 1./self.f
        self.N = np.int(np.ceil(self.rMax/self.lambda0))
        self.circles = [plt.Circle(xy=tuple(self.r), fill=False, lw=2,
                                   radius=0, alpha=self.alpha,
                                   color=self.color)
                        for i in range(self.N)]

    def Wrap(self, x, x_max):
        if x >= 0:
            return x - np.floor(x/x_max) * x_max
        if x < 0:
            return x_max - (-x - np.floor(-x/x_max) * x_max)


class EmitterArray():

    def __init__(self):
        self.emitters = []

    def AddEmitter(self, e):
        self.emitters.append(e)

    def Increment(self, dt):
        for emitter in self.emitters:
            emitter.Increment(dt)

    def GetCircles(self):
        """Get all the circles from all the emitters"""
        circles = []
        for emitter in self.emitters:
            circles.extend(emitter.circles)
        return circles

    def RemoveOffset(self):
        """Only run this one time after all emitters have been added"""
        offsets = []
        for emitter in self.emitters:
            offsets.append(emitter.t0)
        offset_min = np.min(offsets)
        for emitter in self.emitters:
            emitter.Increment(offset_min)

    @property
    def circles(self):
        return self.GetCircles()


FPS = 30
X, Y = 100, 100
c, f = 3, 0.2
lambda0 = c/f

N = 10

emitter_array = EmitterArray()

# ########################################################
# # DEMO 1 - Linear Array of Emitters
# xs = np.linspace(-lambda0/4, lambda0/4, N)
# ys = np.zeros_like(xs)
# phi = np.linspace(0,np.pi/2,N)
# for i in range(N):
#     e = Emitter(xs[i], ys[i], c, f, phi[i])
#     emitter_array.AddEmitter(e)
# #######################################################

# ########################################################
# # DEMO 2 - Linear Array of Emitters
# r = np.linspace(-lambda0/4, lambda0/4, N)
# angle = np.pi/4
# xs = r*np.cos(angle)
# ys = r*np.sin(angle)
# phi = np.linspace(0 , np.pi/2, N)
# for i in range(N):
#     e = Emitter(xs[i], ys[i], c, f, phi[i])
#     emitter_array.AddEmitter(e)
# #######################################################

# ########################################################
# # DEMO 3 - Focussed Array
xs = np.linspace(-lambda0, lambda0, N)
ys = np.zeros_like(xs)
for i in range(N):
    e = Emitter(xs[i], ys[i], c, f, 0)
    phase = CalculatePhaseFromFocus(0, 20, e)
    e.SetPhase(phase)
    emitter_array.AddEmitter(e)
# #######################################################

# ########################################################
# # DEMO 4 - Dual Frequency Emitters
# xs = np.linspace(-lambda0/4, lambda0/4, N)
# ys = np.zeros_like(xs)
# phi = np.linspace(0,np.pi/2,N)
# for i in range(N):
#     e = Emitter(xs[i], ys[i], c, f, phi[i])
#     emitter_array.AddEmitter(e)

# for i in range(N):
#     e = Emitter(xs[i], ys[i], c, 0.5*f, -phi[i], color = "red")
#     emitter_array.AddEmitter(e)
# #######################################################

# # ########################################################
# # # DEMO 5 - Focussed Array
# xs = np.linspace(-lambda0, lambda0, N)
# ys = np.zeros_like(xs)
# for i in range(N):
#     e = Emitter(xs[i], ys[i], c, f, 0)
#     phase = CalculatePhaseFromFocus(0, 20, e)
#     e.SetPhase(phase)
#     emitter_array.AddEmitter(e)

# for i in range(N):
#     e = Emitter(xs[i], ys[i], c, 0.8*f, 0, color = "red")
#     phase = CalculatePhaseFromFocus(-20, 30, e)
#     e.SetPhase(phase)
#     emitter_array.AddEmitter(e)
# # #######################################################

# # # ########################################################
# # # # DEMO 6 - Focussed Array Random
# xs = np.random.uniform(-lambda0/2, lambda0/2, N)
# ys = np.random.uniform(-lambda0/2, lambda0/2, N)
# for i in range(N):
#     e = Emitter(xs[i], ys[i], c, f, 0)
#     phase = CalculatePhaseFromFocus(0, 20, e)
#     e.SetPhase(phase)
#     emitter_array.AddEmitter(e)
# # # #######################################################

# # # ########################################################
# # # # DEMO 7 - Focussed Array Random
# N = 20
# xs = np.random.uniform(-lambda0*2, lambda0*2, N)
# ys = np.random.uniform(-lambda0*2, lambda0*2, N)
# for i in range(N):
#     e = Emitter(xs[i], ys[i], c, f, 0)
#     phase = CalculatePhaseFromFocus(0, 20, e)
#     e.SetPhase(phase)
#     emitter_array.AddEmitter(e)
# # # #######################################################


emitter_array.RemoveOffset()

fig, ax = plt.subplots()
ax.set_xlim([-X/2, Y/2])
ax.set_ylim([-X/2, Y/2])
ax.set_aspect(1)
ax.grid(alpha=0.2)
fig.tight_layout()

for circle in emitter_array.circles:
    ax.add_patch(circle)

for emitter in emitter_array.emitters:
    ax.add_patch(plt.Circle(tuple(emitter.r), 0.4, color="purple"))


def init():
    return tuple(emitter_array.circles)


def update(frame_number):
    emitter_array.Increment(1/FPS)
    return tuple(emitter_array.circles)


if __name__ == "__main__":
    ani = FuncAnimation(fig, update, init_func=init,
                        interval=1000/FPS, blit=True)
    plt.show()
