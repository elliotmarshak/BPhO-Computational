import numpy as np
import matplotlib.pyplot as plt

import sounddevice as sd


def record_audio(duration_s=5.0, sample_rate=44100):
	num_samples = int(duration_s * sample_rate)
	
	print(f"Recording for {duration_s:.1f} s at {sample_rate} Hz")
	audio = sd.rec(num_samples, samplerate=sample_rate, channels=1, dtype="float32")
	sd.wait()
	print("Recording complete.")
	
	return audio[:, 0] #gchange shape from (N,1) to (N,)


def compute_spectrogram(signal, sample_rate, window_size=2048, hop_size=256):
	if len(signal) < window_size:
		pad = window_size - len(signal)
		signal = np.pad(signal, (0, pad))
		#if the signal is shorter than one FFT window then we pad it with zeros
    
    #use a Hann window to reduce spectral leakage
	window = np.hanning(window_size)
	n_frames = 1 + (len(signal) - window_size) // hop_size #computes how many frames will fit

	spec = np.empty((window_size // 2 + 1, n_frames), dtype=np.float32) #output array with frequency rows amd time cols
	for i in range(n_frames):
		start = i * hop_size
		frame = signal[start : start + window_size] * window
		fft_frame = np.fft.rfft(frame)
		spec[:, i] = np.abs(fft_frame)

	#convert to decibels
	spec_db = 20.0 * np.log10(spec + 1e-10)
	freqs = np.fft.rfftfreq(window_size, d=1.0 / sample_rate) #frequency axis
	times = (np.arange(n_frames) * hop_size) / sample_rate #time axis
	return times, freqs, spec_db


def plot_results(signal, sample_rate, times, freqs, spec_db, max_freq_hz=4000):
	#plot the spectrogram
	t_signal = np.arange(len(signal)) / sample_rate

	fig, (ax_wave, ax_spec) = plt.subplots(2, 1, figsize=(11, 8), constrained_layout=True)

	ax_wave.plot(t_signal, signal, color="tab:blue", linewidth=1.0)
	ax_wave.set_title("Recorded Audio Waveform")
	ax_wave.set_xlabel("Time (s)")
	ax_wave.set_ylabel("Amplitude")

	max_idx = np.searchsorted(freqs, max_freq_hz)
	mesh = ax_spec.pcolormesh(
		times,
		freqs[:max_idx],
		spec_db[:max_idx, :],
		shading="gouraud",
		cmap="magma",
	)
	ax_spec.set_title("FFT Spectrogram")
	ax_spec.set_xlabel("Time (s)")
	ax_spec.set_ylabel("Frequency (Hz)")
	cbar = fig.colorbar(mesh, ax=ax_spec)
	cbar.set_label("Magnitude (dB)")

	plt.show()


duration = input("Recording duration in seconds [default 5]: ").strip()
sample_rate = input("Sample rate in Hz [default 44100]: ").strip()

duration_s = float(duration) if duration else 5.0
sr = int(sample_rate) if sample_rate else 44100

signal = record_audio(duration_s=duration_s, sample_rate=sr)
times, freqs, spec_db = compute_spectrogram(signal, sr)
plot_results(signal, sr, times, freqs, spec_db)

