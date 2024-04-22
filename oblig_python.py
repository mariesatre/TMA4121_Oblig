import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


#Konstanter, grenser og skrittstørrelse(med mulighet for ulike x- og y-verdier, selv om jeg bruker samme for begge)
c = 1

X_min = -5
X_max = 5
Y_min = -5
Y_max = 5
t_max = 10

X_nmr_of_steps = 50
Y_nmr_of_steps = 50
t_nmr_of_steps = 200

#Arrays for x, y og t, og skrittlengde mellom to steg
x = np.linspace(X_min, X_max, X_nmr_of_steps)
y = np.linspace(Y_min, Y_max, Y_nmr_of_steps)
t = np.linspace(0, t_max, t_nmr_of_steps)
dx = x[1] - x[0]
dy = y[1] - y[0]
dt = t[1] - t[0]

#Omgjør x- og y-vektorene til matriser med np.meshgrid, resulterer i koordinatsystemet vist i plotet under:

x, y = np.meshgrid(x, y)

plt.plot(x, y, marker='o', color='k', linestyle='none')
plt.show()

#Initialbetingelser(Selvvalgte, synes eksponentfunksjonen gir det kuleste resultatet, har også med en sinusfunksjon og en konstant for noen veldig ulike resultater)

def inital(x, y):
    return np.exp(-4 * (x**2 + y**2))
    #return 0.5*np.sin(x) + 0.5*np.cos(y)
    #return 0.5

def initial_dt(x, y):
    return 0



#En if-else som sjekker om løsningen er stabil etter CFL-kravet med de valgte steglengdene
if ((c*dt)/dx + (c*dt)/dy <= 1):
    print("Method is stable with chosen step sizes.")
else:
    print("Method is unstable with chosen step sizes.")




#Oppretter en tom matrise for funksjonen til bølgen u. Ordner deretter initalkrav for både selve bølgen og dens deriverte. Fyller deretter opp matrisen med en for-løkke
#som implementerer formelen for u_k+1 gitt av sentraldifferansen. Løser altså likningen numerisk i hvert punkt.
u = np.zeros((X_nmr_of_steps, Y_nmr_of_steps, t_nmr_of_steps))
u[:, :, 0] = inital(x,y)
u[:, :, 1] = u[:, :, 0] + dt * initial_dt(x, y)
 
for k in range(1, t_nmr_of_steps-1):
    for i in range(1, X_nmr_of_steps-1):
        for j in range(1, Y_nmr_of_steps-1):
            u[i, j, k+1] = (2*u[i, j, k] - u[i, j, k-1] + (c*dt/dx)**2 * (u[i+1, j, k] - 2*u[i, j, k] + u[i-1, j, k]) + (c*dt/dy)**2 * (u[i, j+1, k] - 2*u[i, j, k] + u[i, j-1, k]))

#Animasjon

#Setter opp figuren, aksene(som 3D) med grenser og plotet for første tidssteg
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surface = ax.plot_surface(x, y, u[:, :, 0], cmap='viridis')

ax.set_xlim([X_min, X_max])
ax.set_ylim([Y_min, Y_max])
ax.set_zlim([-0.75, 0.75])

#Lager funksjon for å animere for flere tidssteg
def update(frame):
    ax.clear()
    surface = ax.plot_surface(x, y, u[:, :, frame], cmap='viridis')
    ax.set_xlim([X_min, X_max])
    ax.set_ylim([Y_min, Y_max])
    ax.set_zlim([-0.75, 0.75])
    ax.set_title(f"Time step {frame}")
    return surface

# Plotter som animasjon og viser til slutt
ani = FuncAnimation(fig, update, frames=np.arange(0, t_nmr_of_steps))

plt.show()
