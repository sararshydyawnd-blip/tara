import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from collections import deque
import csv
import time


# ============================================================
# ECG SIMULATOR
# ============================================================
# Educational / simulation software.
# This program DOES NOT provide medical diagnosis.
# ============================================================


class ECGConfig:
    def __init__(self):
        self.sample_rate = 250
        self.duration = 10.0

        self.bpm = 72
        self.amplitude = 1.0

        self.noise_enabled = True
        self.noise_level = 0.025

        self.baseline_enabled = True
        self.baseline_amplitude = 0.04

        self.grid_major_x = 0.2
        self.grid_minor_x = 0.04

        self.grid_major_y = 0.5
        self.grid_minor_y = 0.1


class ECGGenerator:
    """
    Generates a synthetic ECG signal using Gaussian components
    representing P, Q, R, S and T waves.
    """

    def __init__(self, config):
        self.config = config

    def gaussian(self, x, center, width, amplitude):
        return amplitude * np.exp(
            -0.5 * ((x - center) / width) ** 2
        )

    def single_beat(self, t):
        """
        Generate one synthetic cardiac cycle.
        """

        # P wave
        p = self.gaussian(
            t,
            center=0.18,
            width=0.025,
            amplitude=0.12
        )

        # Q wave
        q = self.gaussian(
            t,
            center=0.36,
            width=0.012,
            amplitude=-0.16
        )

        # R wave
        r = self.gaussian(
            t,
            center=0.40,
            width=0.010,
            amplitude=1.20
        )

        # S wave
        s = self.gaussian(
            t,
            center=0.44,
            width=0.014,
            amplitude=-0.28
        )

        # T wave
        tw = self.gaussian(
            t,
            center=0.66,
            width=0.055,
            amplitude=0.30
        )

        return p + q + r + s + tw

    def generate(self, duration=None):
        if duration is None:
            duration = self.config.duration

        fs = self.config.sample_rate

        t = np.arange(
            0,
            duration,
            1 / fs
        )

        beat_duration = 60.0 / self.config.bpm

        phase = np.mod(t, beat_duration)

        normalized_phase = (
            phase / beat_duration
        )

        signal = self.single_beat(
            normalized_phase
        )

        signal *= self.config.amplitude

        if self.config.baseline_enabled:
            baseline = (
                self.config.baseline_amplitude
                * np.sin(2 * np.pi * 0.25 * t)
            )

            signal += baseline

        if self.config.noise_enabled:
            noise = np.random.normal(
                0,
                self.config.noise_level,
                len(t)
            )

            signal += noise

        return t, signal

    def generate_long(self, duration):
        return self.generate(duration)


class ECGFilter:
    """
    Simple moving-average filter.
    """

    @staticmethod
    def moving_average(signal, window=5):

        if window < 2:
            return signal.copy()

        kernel = np.ones(window) / window

        return np.convolve(
            signal,
            kernel,
            mode="same"
        )


class RPeakDetector:

    @staticmethod
    def detect(signal, sample_rate, threshold=None):

        if len(signal) == 0:
            return []

        if threshold is None:
            threshold = (
                np.mean(signal)
                + 0.5 * np.std(signal)
            )

        peaks = []

        minimum_distance = int(
            sample_rate * 0.25
        )

        last_peak = -minimum_distance

        for i in range(1, len(signal) - 1):

            if signal[i] <= threshold:
                continue

            if (
                signal[i] > signal[i - 1]
                and signal[i] >= signal[i + 1]
            ):

                if (
                    i - last_peak
                    >= minimum_distance
                ):
                    peaks.append(i)
                    last_peak = i

        return peaks

    @staticmethod
    def calculate_bpm(
        peak_indices,
        sample_rate
    ):

        if len(peak_indices) < 2:
            return 0

        intervals = np.diff(
            peak_indices
        ) / sample_rate

        intervals = intervals[
            intervals > 0
        ]

        if len(intervals) == 0:
            return 0

        average_interval = np.mean(
            intervals
        )

        if average_interval <= 0:
            return 0

        return 60.0 / average_interval


class ECGStorage:

    def __init__(self):
        self.time = []
        self.signal = []

    def set_data(self, t, signal):
        self.time = list(t)
        self.signal = list(signal)

    def clear(self):
        self.time.clear()
        self.signal.clear()

    def export_csv(self, filename):

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "time_seconds",
                "ecg_amplitude"
            ])

            for t, value in zip(
                self.time,
                self.signal
            ):
                writer.writerow([
                    t,
                    value
                ])


class ECGApplication:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "ECG Simulator"
        )

        self.root.geometry(
            "1200x750"
        )

        self.config = ECGConfig()

        self.generator = ECGGenerator(
            self.config
        )

        self.filter = ECGFilter()

        self.detector = RPeakDetector()

        self.storage = ECGStorage()

        self.running = False

        self.animation = None

        self.current_time = 0

        self.visible_seconds = 6

        self.setup_style()
        self.setup_variables()
        self.setup_ui()

        self.generate_signal()

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "TButton",
            font=("Arial", 10)
        )

        style.configure(
            "TLabel",
            font=("Arial", 10)
        )

        style.configure(
            "Title.TLabel",
            font=("Arial", 18, "bold")
        )

    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    def setup_variables(self):

        self.bpm_var = tk.IntVar(
            value=self.config.bpm
        )

        self.amplitude_var = tk.DoubleVar(
            value=self.config.amplitude
        )

        self.noise_var = tk.BooleanVar(
            value=self.config.noise_enabled
        )

        self.baseline_var = tk.BooleanVar(
            value=self.config.baseline_enabled
        )

        self.filter_var = tk.BooleanVar(
            value=False
        )

        self.bpm_display = tk.StringVar(
            value="72 BPM"
        )

        self.status_var = tk.StringVar(
            value="Ready"
        )

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def setup_ui(self):

        main = ttk.Frame(
            self.root,
            padding=10
        )

        main.pack(
            fill=tk.BOTH,
            expand=True
        )

        title = ttk.Label(
            main,
            text="ECG / EKG Simulator",
            style="Title.TLabel"
        )

        title.pack(
            pady=(0, 10)
        )

        control_frame = ttk.LabelFrame(
            main,
            text="Controls",
            padding=10
        )

        control_frame.pack(
            fill=tk.X
        )

        # BPM
        ttk.Label(
            control_frame,
            text="Heart Rate:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.bpm_scale = ttk.Scale(
            control_frame,
            from_=40,
            to=180,
            variable=self.bpm_var,
            command=self.on_bpm_change
        )

        self.bpm_scale.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )

        ttk.Label(
            control_frame,
            textvariable=self.bpm_display
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        # Amplitude
        ttk.Label(
            control_frame,
            text="Amplitude:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.amplitude_scale = ttk.Scale(
            control_frame,
            from_=0.2,
            to=2.0,
            variable=self.amplitude_var,
            command=self.on_amplitude_change
        )

        self.amplitude_scale.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5
        )

        # Noise
        ttk.Checkbutton(
            control_frame,
            text="Noise",
            variable=self.noise_var,
            command=self.generate_signal
        ).grid(
            row=0,
            column=3,
            padx=10
        )

        # Baseline
        ttk.Checkbutton(
            control_frame,
            text="Baseline",
            variable=self.baseline_var,
            command=self.generate_signal
        ).grid(
            row=1,
            column=3,
            padx=10
        )

        # Filter
        ttk.Checkbutton(
            control_frame,
            text="Filter",
            variable=self.filter_var,
            command=self.update_plot
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        control_frame.columnconfigure(
            1,
            weight=1
        )

        # Buttons
        button_frame = ttk.Frame(
            main
        )

        button_frame.pack(
            fill=tk.X,
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Start",
            command=self.start
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Stop",
            command=self.stop
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Regenerate",
            command=self.generate_signal
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_csv
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_plot
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        ttk.Label(
            button_frame,
            textvariable=self.status_var
        ).pack(
            side=tk.RIGHT,
            padx=10
        )

        # ECG display
        graph_frame = ttk.LabelFrame(
            main,
            text="ECG Monitor",
            padding=5
        )

        graph_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.figure = plt.Figure(
            figsize=(10, 5),
            dpi=100
        )

        self.ax = self.figure.add_subplot(
            111
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

        self.setup_plot()

    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------

    def setup_plot(self):

        self.ax.set_facecolor(
            "#fffafa"
        )

        self.ax.set_xlabel(
            "Time (seconds)"
        )

        self.ax.set_ylabel(
            "Amplitude (mV)"
        )

        self.ax.set_xlim(
            0,
            self.visible_seconds
        )

        self.ax.set_ylim(
            -0.6,
            1.5
        )

        self.setup_grid()

        self.line, = self.ax.plot(
            [],
            [],
            color="#111111",
            linewidth=1.5
        )

        self.peak_scatter = self.ax.scatter(
            [],
            [],
            color="red",
            s=35,
            zorder=5
        )

        self.canvas.draw()

    def setup_grid(self):

        self.ax.grid(
            which="major",
            color="#e6aaaa",
            linewidth=0.8
        )

        self.ax.grid(
            which="minor",
            color="#f2dada",
            linewidth=0.4
        )

        self.ax.minorticks_on()

    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    def update_config(self):

        self.config.bpm = int(
            self.bpm_var.get()
        )

        self.config.amplitude = float(
            self.amplitude_var.get()
        )

        self.config.noise_enabled = (
            self.noise_var.get()
        )

        self.config.baseline_enabled = (
            self.baseline_var.get()
        )

    def generate_signal(self):

        self.update_config()

        self.status_var.set(
            "Generating ECG..."
        )

        self.root.update_idletasks()

        t, signal = (
            self.generator.generate(
                20
            )
        )

        self.storage.set_data(
            t,
            signal
        )

        self.current_time = 0

        self.update_plot()

        self.status_var.set(
            "ECG generated"
        )

    # --------------------------------------------------------
    # PLOT UPDATE
    # --------------------------------------------------------

    def update_plot(self):

        if not self.storage.time:
            return

        t = np.array(
            self.storage.time
        )

        signal = np.array(
            self.storage.signal
        )

        if self.filter_var.get():

            display_signal = (
                self.filter.moving_average(
                    signal,
                    5
                )
            )

        else:
            display_signal = signal

        peaks = self.detector.detect(
            display_signal,
            self.config.sample_rate
        )

        # Keep only visible data
        end = min(
            len(t),
            int(
                (
                    self.current_time
                    + self.visible_seconds
                )
                * self.config.sample_rate
            )
        )

        start = max(
            0,
            int(
                self.current_time
                * self.config.sample_rate
            )
        )

        visible_t = t[start:end]

        visible_signal = (
            display_signal[start:end]
        )

        self.line.set_data(
            visible_t,
            visible_signal
        )

        visible_peaks = [
            p
            for p in peaks
            if start <= p < end
        ]

        peak_x = t[
            visible_peaks
        ]

        peak_y = display_signal[
            visible_peaks
        ]

        self.peak_scatter.set_offsets(
            np.column_stack(
                (peak_x, peak_y)
            )
            if len(peak_x)
            else np.empty((0, 2))
        )

        if len(visible_t):

            left = visible_t[0]

            right = (
                left
                + self.visible_seconds
            )

            self.ax.set_xlim(
                left,
                right
            )

        measured_bpm = (
            self.detector.calculate_bpm(
                peaks,
                self.config.sample_rate
            )
        )

        if measured_bpm > 0:

            self.bpm_display.set(
                f"{self.config.bpm} BPM "
                f"(detected: "
                f"{measured_bpm:.0f})"
            )

        else:

            self.bpm_display.set(
                f"{self.config.bpm} BPM"
            )

        self.canvas.draw_idle()

    # --------------------------------------------------------
    # ANIMATION
    # --------------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.status_var.set(
            "Monitoring..."
        )

        self.current_time = 0

        self.animation = FuncAnimation(
            self.figure,
            self.animate,
            interval=40,
            cache_frame_data=False
        )

        self.canvas.draw_idle()

    def stop(self):

        self.running = False

        self.status_var.set(
            "Stopped"
        )

        if self.animation:

            self.animation.event_source.stop()

            self.animation = None

    def animate(self, frame):

        if not self.running:
            return

        self.current_time += 0.04

        total_time = (
            self.storage.time[-1]
            if self.storage.time
            else 20
        )

        if (
            self.current_time
            + self.visible_seconds
            >= total_time
        ):

            self.generate_signal()

        self.update_plot()

    # --------------------------------------------------------
    # CONTROLS
    # --------------------------------------------------------

    def on_bpm_change(self, value):

        bpm = int(
            float(value)
        )

        self.bpm_var.set(
            bpm
        )

        self.config.bpm = bpm

        self.generate_signal()

    def on_amplitude_change(self, value):

        amplitude = float(value)

        self.config.amplitude = amplitude

        self.generate_signal()

    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------

    def export_csv(self):

        if not self.storage.time:

            messagebox.showwarning(
                "Warning",
                "No ECG data available."
            )

            return

        filename = filedialog.asksaveasfilename(
            title="Save ECG Data",
            defaultextension=".csv",
            filetypes=[
                (
                    "CSV files",
                    "*.csv"
                )
            ]
        )

        if not filename:
            return

        try:

            self.storage.export_csv(
                filename
            )

            messagebox.showinfo(
                "Success",
                "ECG data exported successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    def clear_plot(self):

        self.stop()

        self.storage.clear()

        self.line.set_data(
            [],
            []
        )

        self.peak_scatter.set_offsets(
            np.empty((0, 2))
        )

        self.ax.set_xlim(
            0,
            self.visible_seconds
        )

        self.canvas.draw_idle()

        self.status_var.set(
            "Plot cleared"
        )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():

    root = tk.Tk()

    app = ECGApplication(
        root
    )

    root.protocol(
        "WM_DELETE_WINDOW",
        root.destroy
    )

    root.mainloop()


if __name__ == "__main__":
    main()

