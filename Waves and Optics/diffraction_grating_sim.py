import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import Slider

XMIN, XMAX, YMIN, YMAX = -6.0, 6.0, 0.0, 12.0
SCREEN_Y = 9.5 #where the screen is
EPS = 0.001 #avoid div by 0 errors
NX, NY, SNX = 300, 225, 600 #nx and ny are the resolution of the wave grid and snx is the res of the screen
DISPLAY_GAIN = 25 #boosts visibility of wave magnitude 
WAVE_CMAP = LinearSegmentedColormap.from_list('blue_black_red', ['#1e4cff', '#000000', '#ff3a2f'])

#create grids
xs = np.linspace(XMIN, XMAX, NX)
ys = np.linspace(YMIN, YMAX, NY)
X, Y = np.meshgrid(xs, ys)
screen_xs = np.linspace(XMIN, XMAX, SNX)

#stores the adjustable paramaters
state = dict(n_slits=2, slit_sep=2.0, slit_width=0.0, wavelength=0.8, n_src=50, speed=1.5, screen_y=SCREEN_Y)
#n slits - number of slits
#slit_sep - separation between adjacent slits
#slit_width - the width of each slit
#wavelength - wavelength of the initial light
#n_src - number of discrete sources to use for a finite length slit
#speed - wave speed


def build_sources(n_slits, slit_sep, slit_width, n_src):
    #creates the positions of wave sources
    centres = [(s - (n_slits - 1) / 2) * slit_sep for s in range(n_slits)] #slits are centred about 0
    if slit_width == 0 or n_src <= 1:
        return np.array([[c, 0.0] for c in centres])
    offsets = slit_width * (-0.5 + np.linspace(0, 1, n_src)) #for simulating a finite width slit with many sources (n_src)
    return np.array([[c + dx, 0.0] for c in centres for dx in offsets])


def wave_field(sources, k, omega, t):
    #Compute complex wave field from superposed sources.
    psi = np.zeros((NY, NX), dtype=complex)
    for sx, sy in sources:
        r = np.maximum(np.hypot(X - sx, Y - sy), EPS)
        #Sum contributions from each source with proper phase
        psi += np.exp(1j * (k * r - omega * t)) / r
    #Return real part which oscillates
    return np.real(psi)


def screen_intensity(sources, k, screen_y):
    #Calculate diffraction pattern intensity on detection screen
    
    #Uses complex wave representation to properly account for interference through phase relationships. Intensity is phi^2 
    total_wave = np.zeros_like(screen_xs, dtype=complex)

    for sx, sy in sources:
        r = np.hypot(screen_xs - sx, screen_y - sy)
        r = np.maximum(r, EPS)
        #use complex exponential to preserve phase information for interference
        wave = np.exp(1j * k * r) / r
        total_wave += wave

    #intensity is the magnitude of phi squared
    intensity = np.abs(total_wave) ** 2
    return intensity / intensity.max()

#initialises wave sources
sources = build_sources(state['n_slits'], state['slit_sep'], state['slit_width'], state['n_src'])

fig = plt.figure(figsize=(14, 8), facecolor="#111116")
PLOT_B, PLOT_TOP = 0.06, 0.82

#Create side by side subplots for wave field and diffraction pattern
ax_wave = fig.add_axes([0.05, PLOT_B, 0.56, PLOT_TOP - PLOT_B])
ax_screen = fig.add_axes([0.67, PLOT_B, 0.30, PLOT_TOP - PLOT_B])

for ax in (ax_wave, ax_screen):
    ax.set_facecolor("#0a0a0e")

#compute initial wave field
k0 = 2 * np.pi / state['wavelength']
psi0 = wave_field(sources, k0, 2 * state['speed'], 0)
lim = max(np.abs(psi0).max(), 0.01)

#wave field visualisation
wave_im = ax_wave.imshow(DISPLAY_GAIN * psi0, extent=[XMIN, XMAX, YMIN, YMAX], origin='lower', cmap=WAVE_CMAP, vmin=-lim, vmax=lim, aspect='auto')

#screen indicator
screen_line = ax_wave.axhline(state['screen_y'], color='#00ccff', linewidth=2.2, linestyle='-', zorder=6)
screen_label = ax_wave.text(XMIN + 0.15, state['screen_y'] + 0.2, 'screen', color='#00ccff', fontsize=8)

#Mark source positions
src_scatter = ax_wave.scatter(sources[:, 0], sources[:, 1], color='#ffff80', s=14, zorder=4)

ax_wave.set(xlim=(XMIN, XMAX), ylim=(YMIN, YMAX), xlabel='x', ylabel='y', title='Wave field')
ax_wave.tick_params(colors='#666')
for lbl in (ax_wave.xaxis.label, ax_wave.yaxis.label, ax_wave.title):
    lbl.set_color('#aaa' if lbl != ax_wave.title else '#ddd')

#Diffraction pattern on screen
intensity_0 = screen_intensity(sources, k0, state['screen_y'])

#Show intensity as heatmap
screen_im = ax_screen.imshow(np.tile(intensity_0, (60, 1)), extent=[XMIN, XMAX, 0, 0.45], origin='lower', aspect='auto', cmap='inferno', vmin=0, vmax=1)

#Overlay intensity curve
(screen_curve,) = ax_screen.plot(screen_xs, 0.5 + 0.48 * intensity_0, color='#ffaa33', linewidth=1.4)

#Configure screen display
ax_screen.axhline(0.5, color='#444', linewidth=0.5)
ax_screen.set(xlim=(XMIN, XMAX), ylim=(0, 1), xlabel='position on screen', title='Diffraction pattern')
ax_screen.tick_params(colors='#666')
ax_screen.set_yticks([])

for lbl in (ax_screen.xaxis.label, ax_screen.title):
    lbl.set_color('#aaa' if lbl != ax_screen.title else '#ddd')
ax_screen.text(0.02, 0.97, 'intensity', transform=ax_screen.transAxes, color='#aaa', va='top', fontsize=8)
ax_screen.text(0.02, 0.52, 'screen image', transform=ax_screen.transAxes, color='#aaa', va='top', fontsize=8)

#sliders for parameter adjustment
slider_specs = [
    # (parameter_key, label, min, max, initial, step, column, row)
    ('n_slits',    'Num slits',        1,    6,    2,    1,    0,   0),
    ('slit_sep',   'Slit separation',    0.5,  4.0,  2.0,  0.1,  1,   0),
    ('slit_width', 'Slit width',  0.0,  2.0,  0.0,  0.05, 2,   0),
    ('wavelength', 'Wavelength',          0.15, 1.5,  0.8,  0.05, 0,    1),
    ('n_src',      'Src / slit',       1,    100,   50,   1,    1,  1),
    ('speed',      'Speed',            0.5,  4.0,  1.5,  0.25, 2,   1),
    ('screen_y',   'Screen y',         1.0,  11.5, SCREEN_Y, 0.1, 2,   2),
]

#Grid positions for sliders (2 rows 3 columns)
COL_LEFTS   = [0.05, 0.38, 0.70]
ROW_BOTTOMS = [PLOT_TOP + 0.13, PLOT_TOP + 0.085, PLOT_TOP + 0.04]

def create_styled_slider(fig, label, vmin, vmax, valinit, valstep, col, row):
    #creates and styles one slider
    ax_sl = fig.add_axes([COL_LEFTS[col], ROW_BOTTOMS[row], 0.24, 0.025], facecolor="#1e1e26")
    slider = Slider(ax_sl, label, vmin, vmax, valinit=valinit, valstep=valstep, color='#ffaa33', initcolor='#ffaa33')
    slider.label.set(color='#bbb', fontsize=7.5)
    slider.valtext.set(color='#ffaa33', fontsize=7.5)
    slider.track.set_facecolor('#1e1e26')
    return slider

#Create all sliders
sliders = {}
for key, label, vmin, vmax, val, step, col, row in slider_specs:
    sliders[key] = create_styled_slider(fig, label, vmin, vmax, val, step, col, row)

def on_change(_):
    #slider handling
    global sources
    
    #update parameter state from slider values
    state.update({k: (int(sliders[k].val) if k in ('n_slits', 'n_src') else sliders[k].val) for k in sliders})
    
    #rebuild source positions
    sources = build_sources(state['n_slits'], state['slit_sep'], state['slit_width'], state['n_src'])
    src_scatter.set_offsets(sources)
    screen_line.set_ydata([state['screen_y'], state['screen_y']])
    screen_label.set_position((XMIN + 0.15, state['screen_y'] + 0.2))
    
    #update diffraction pattern
    k = 2 * np.pi / state['wavelength']
    intensity = screen_intensity(sources, k, state['screen_y'])
    screen_im.set_data(np.tile(intensity, (60, 1)))
    screen_curve.set_ydata(0.5 + 0.48 * intensity)

for sl in sliders.values():
    sl.on_changed(on_change)

t = [0.0]  #stored in a list as lazy way of passing by ref

def update(_):
    t[0] += 0.05
    
    k = 2 * np.pi / state['wavelength']
    psi = wave_field(sources, k, 2 * state['speed'], t[0])
    wave_im.set_data(DISPLAY_GAIN * psi)
    
    return wave_im, screen_im, screen_curve, src_scatter, screen_line, screen_label

ani = FuncAnimation(fig, update, interval=50, blit=True, cache_frame_data=False)
plt.show()