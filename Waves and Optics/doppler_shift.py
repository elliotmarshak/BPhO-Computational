import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.widgets import Button, Slider


XMIN, XMAX = -20.0, 20.0
YMIN, YMAX = -10.0, 10.0
WAVE_SPEED = 8.0  #propagation speed in the medium
DT = 0.03


state = {
	"f0": 1.2,      #source frequency (Hz)
	"vs": 2.0,      #source speed (m/s)
	"vo": 0.0,      #observer speed
}



def observed_frequency(f0, c, xs, xo, vs, vo):
	observer_toward_source = vo * np.sign(xs - xo)
	source_toward_observer = vs * np.sign(xo - xs)
	return max(0.0, f0 * (c + observer_toward_source) / (c - source_toward_observer))


fig = plt.figure(figsize=(12.5, 8), facecolor="#111116")
ax_main = fig.add_axes([0.06, 0.30, 0.70, 0.64])
ax_hist = fig.add_axes([0.06, 0.08, 0.70, 0.16])

for ax in (ax_main, ax_hist):
	ax.set_facecolor("#0a0a0e")
	ax.tick_params(colors="#9a9a9a")
	for spine in ax.spines.values():
		spine.set_color("#333")


ax_main.set_xlim(XMIN, XMAX)
ax_main.set_ylim(YMIN, YMAX)
ax_main.set_title("Doppler Effect Simulation", color="#e6e6e6")
ax_main.set_xlabel("x", color="#b8b8b8")
ax_main.set_ylabel("y", color="#b8b8b8")
ax_main.axhline(0, color="#2f2f39", linewidth=0.8)

ax_hist.set_title("Observed Frequency Over Time", color="#e6e6e6", fontsize=10)
ax_hist.set_xlabel("time (s)", color="#b8b8b8")
ax_hist.set_ylabel("f_obs (Hz)", color="#b8b8b8")
ax_hist.set_xlim(0, 12)
ax_hist.set_ylim(0, 4)


#The moving objects
source_dot, = ax_main.plot([], [], "o", color="#ff7043", markersize=10, label="Source")
observer_dot, = ax_main.plot([], [], "o", color="#66bb6a", markersize=10, label="Observer")
ax_main.legend(loc="upper right", facecolor="#111116", edgecolor="#333", labelcolor="#ddd")

info_text = ax_main.text(
	0.02,
	0.97,
	"",
	transform=ax_main.transAxes,
	va="top",
	color="#dddddd",
	fontsize=10,
)

hist_t = []
hist_f = []
hist_line, = ax_hist.plot([], [], color="#f7c948", linewidth=1.8)


#Simulation state
t = 0.0
source_x, source_y = -12.0, 0.0
observer_x, observer_y = 10.0, 0.0
emit_accum = 0.0
wavefronts = []  #each item: {"t_emit": float, "x_emit": float, "patch": Circle}


def emit_wavefront(current_t):
	patch = Circle((source_x, source_y), 0.0, fill=False, linewidth=1.0, edgecolor="#4fc3f7", alpha=0.35)
	ax_main.add_patch(patch)
	wavefronts.append({"t_emit": current_t, "x_emit": source_x, "patch": patch})


def clear_wavefronts():
	for wf in wavefronts:
		wf["patch"].remove()
	wavefronts.clear()


def reset(_):
	global t, source_x, observer_x, emit_accum
	t = 0.0
	source_x = -12.0
	observer_x = 10.0
	emit_accum = 0.0
	hist_t.clear()
	hist_f.clear()
	clear_wavefronts()


def on_slider_change(_):
	state["f0"] = float(sl_f0.val)
	state["vs"] = float(sl_vs.val)
	state["vo"] = float(sl_vo.val)


ax_f0 = fig.add_axes([0.80, 0.66, 0.16, 0.03], facecolor="#1e1e26")
ax_vs = fig.add_axes([0.80, 0.57, 0.16, 0.03], facecolor="#1e1e26")
ax_vo = fig.add_axes([0.80, 0.48, 0.16, 0.03], facecolor="#1e1e26")
ax_reset = fig.add_axes([0.82, 0.38, 0.12, 0.05], facecolor="#1e1e26")

sl_f0 = Slider(ax_f0, "f0 (Hz)", 0.4, 3.0, valinit=state["f0"], valstep=0.05, color="#f7c948")
sl_vs = Slider(ax_vs, "source v", -7.0, 7.0, valinit=state["vs"], valstep=0.1, color="#f7c948")
sl_vo = Slider(ax_vo, "observer v", -7.0, 7.0, valinit=state["vo"], valstep=0.1, color="#f7c948")
for sl in (sl_f0, sl_vs, sl_vo):
	sl.label.set_color("#d0d0d0")
	sl.valtext.set_color("#f7c948")
	sl.track.set_facecolor("#1e1e26")
	sl.on_changed(on_slider_change)

btn_reset = Button(ax_reset, "Reset", color="#2a2f3a", hovercolor="#3a4150")
btn_reset.label.set_color("#f0f0f0")
btn_reset.on_clicked(reset)


def update(_):
	global t, source_x, observer_x, emit_accum
	t += DT

	f0 = state["f0"]
	vs = state["vs"]
	vo = state["vo"]

	#Move source and observer and wrap around edges
	source_x += vs * DT
	observer_x += vo * DT
	if source_x > XMAX:
		source_x = XMIN
	if source_x < XMIN:
		source_x = XMAX
	if observer_x > XMAX:
		observer_x = XMIN
	if observer_x < XMIN:
		observer_x = XMAX

	#emit new crests at the source frequency
	emit_accum += DT
	emit_period = 1.0 / max(f0, 1e-6)
	while emit_accum >= emit_period:
		emit_wavefront(t)
		emit_accum -= emit_period

	#update wavefront radii and remove old ones
	max_radius = 45.0
	keep = []
	for wf in wavefronts:
		r = WAVE_SPEED * (t - wf["t_emit"])
		if r <= max_radius:
			wf["patch"].center = (wf["x_emit"], source_y)
			wf["patch"].radius = r
			keep.append(wf)
		else:
			wf["patch"].remove()
	wavefronts[:] = keep

	f_obs = observed_frequency(f0, WAVE_SPEED, source_x, observer_x, vs, vo)
	hist_t.append(t)
	hist_f.append(f_obs)
	if len(hist_t) > 500:
		hist_t.pop(0)
		hist_f.pop(0)

	#Keep history panel focused on recent times
	t0 = max(0.0, t - 12.0)
	ax_hist.set_xlim(t0, t0 + 12.0)
	y_top = max(4.0, max(hist_f) * 1.2)
	ax_hist.set_ylim(0.0, y_top)

	source_dot.set_data([source_x], [source_y])
	observer_dot.set_data([observer_x], [observer_y])
	hist_line.set_data(hist_t, hist_f)

	shift_pct = 100.0 * (f_obs - f0) / max(f0, 1e-6)
	info_text.set_text(
		f"f0 = {f0:.2f} Hz\n"
		f"f_obs = {f_obs:.2f} Hz\n"
		f"shift = {shift_pct:+.1f}%\n"
		f"wave speed c = {WAVE_SPEED:.1f}"
	)

	return [source_dot, observer_dot, hist_line, info_text, *[wf["patch"] for wf in wavefronts]]


ani = FuncAnimation(fig, update, interval=int(DT * 1000), blit=False, cache_frame_data=False)
plt.show()
