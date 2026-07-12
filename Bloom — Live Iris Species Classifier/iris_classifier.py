"""
Bloom — Live Iris Species Classifier
A small, aesthetic desktop app that predicts an Iris flower's species
in real time as you adjust its measurements.

Install dependencies (one-time):
    pip install customtkinter scikit-learn

Run:
    python iris_classifier_gui.py
"""

import customtkinter as ctk
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# =========================================================
# TRAIN THE MODEL (runs once on startup)
# =========================================================
iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names
class_names = ["Setosa", "Versicolor", "Virginica"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_scaled, y_train)
MODEL_ACCURACY = accuracy_score(y_test, model.predict(X_test_scaled))

# Sensible slider ranges based on the real dataset's min/max per feature
FEATURE_RANGES = [(float(X[:, i].min()), float(X[:, i].max())) for i in range(4)]
FEATURE_LABELS = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]

# =========================================================
# COLOR PALETTE — botanical, not corporate-blue
# =========================================================
BG = "#0e1512"
PANEL = "#161f1a"
CARD = "#1b251f"
TEXT = "#e8f2ec"
TEXT_MUTED = "#7d9488"
ACCENT = "#5fd97a"
ACCENT_SOFT = "#2b3d31"

SPECIES_COLORS = {
    "Setosa": "#c99bfa",
    "Versicolor": "#4fd6c4",
    "Virginica": "#7c6bf0",
}


class PetalIcon(ctk.CTkCanvas):
    """A tiny hand-drawn flower glyph that recolors per predicted species."""

    def __init__(self, master, size=110, **kwargs):
        super().__init__(master, width=size, height=size, bg=CARD,
                          highlightthickness=0, **kwargs)
        self.size = size
        self.draw("#c99bfa")

    def draw(self, color):
        self.delete("all")
        s = self.size
        cx, cy = s / 2, s / 2
        r = s * 0.20

        # Four petals as overlapping ellipses
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in offsets:
            px = cx + dx * r * 0.9
            py = cy + dy * r * 0.9
            self.create_oval(
                px - r, py - r, px + r, py + r,
                fill=color, outline="", stipple="", width=0
            )
        # Center
        cr = s * 0.14
        self.create_oval(
            cx - cr, cy - cr, cx + cr, cy + cr,
            fill="#ffe9a8", outline=""
        )


class ConfidenceBar(ctk.CTkFrame):
    """A labeled, colored probability bar for one species."""

    def __init__(self, master, label, color, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.color = color

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x")

        self.name_label = ctk.CTkLabel(
            top, text=label, font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT, anchor="w",
        )
        self.name_label.pack(side="left")

        self.pct_label = ctk.CTkLabel(
            top, text="0%", font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED,
        )
        self.pct_label.pack(side="right")

        self.bar = ctk.CTkProgressBar(
            self, height=10, corner_radius=6,
            fg_color=ACCENT_SOFT, progress_color=color,
        )
        self.bar.pack(fill="x", pady=(6, 0))
        self.bar.set(0)

    def update_value(self, value):
        self.bar.set(value)
        self.pct_label.configure(text=f"{value * 100:.0f}%")


class FeatureSlider(ctk.CTkFrame):
    """A slider with a live numeric readout, styled to feel tactile."""

    def __init__(self, master, label, min_val, max_val, default, unit, on_change, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_change = on_change

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(
            top, text=label, font=ctk.CTkFont(size=13),
            text_color=TEXT, anchor="w",
        ).pack(side="left")

        self.value_label = ctk.CTkLabel(
            top, text=f"{default:.1f} {unit}", font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ACCENT,
        )
        self.value_label.pack(side="right")

        self.unit = unit
        self.slider = ctk.CTkSlider(
            self, from_=min_val, to=max_val, number_of_steps=200,
            command=self._on_slide, progress_color=ACCENT,
            button_color=ACCENT, button_hover_color="#78e690",
            fg_color=ACCENT_SOFT,
        )
        self.slider.set(default)
        self.slider.pack(fill="x", pady=(8, 0))

    def _on_slide(self, value):
        self.value_label.configure(text=f"{value:.1f} {self.unit}")
        self.on_change()

    def get(self):
        return self.slider.get()

    def set(self, value):
        self.slider.set(value)
        self.value_label.configure(text=f"{value:.1f} {self.unit}")


class BloomApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bloom — Live Species Classifier")
        self.geometry("980x620")
        self.minsize(860, 560)
        self.configure(fg_color=BG)

        self._build_header()
        self._build_body()

        self.after(300, self.predict_live)

    # -----------------------------------------------------
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=PANEL, height=70, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=24, fill="y")

        ctk.CTkLabel(
            left, text="🌸", font=ctk.CTkFont(size=22),
        ).pack(side="left", padx=(0, 10), pady=14)

        title_box = ctk.CTkFrame(left, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box, text="Bloom", font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT, anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box, text="Live species classifier", font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED, anchor="w",
        ).pack(anchor="w")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=24, fill="y")

        acc_box = ctk.CTkFrame(right, fg_color="transparent")
        acc_box.pack(pady=10)

        ctk.CTkLabel(
            acc_box, text=f"{MODEL_ACCURACY * 100:.1f}%",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=ACCENT,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            acc_box, text="MODEL\nACCURACY", font=ctk.CTkFont(size=10, weight="bold"),
            text_color=TEXT_MUTED, justify="left", anchor="w",
        ).pack(side="left")

    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color=BG)
        body.pack(fill="both", expand=True, padx=22, pady=20)

        # --- Left: sliders ---
        left_panel = ctk.CTkFrame(body, fg_color=PANEL, corner_radius=16)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 12))

        ctk.CTkLabel(
            left_panel, text="MEASUREMENTS (cm)", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_MUTED, anchor="w",
        ).pack(fill="x", padx=24, pady=(22, 14))

        self.sliders = []
        defaults = [5.8, 3.0, 4.3, 1.3]  # roughly the dataset's mean values
        for label, (lo, hi), default in zip(FEATURE_LABELS, FEATURE_RANGES, defaults):
            s = FeatureSlider(
                left_panel, label, lo, hi, default, "cm",
                on_change=self.predict_live,
            )
            s.pack(fill="x", padx=24, pady=12)
            self.sliders.append(s)

        btn_row = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_row.pack(fill="x", padx=24, pady=(20, 24))

        ctk.CTkButton(
            btn_row, text="🎲  Try Random Sample", command=self.randomize,
            fg_color=ACCENT_SOFT, hover_color="#38493e", text_color=TEXT,
            corner_radius=10, height=38,
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            btn_row, text="↺  Reset", command=self.reset_defaults,
            fg_color=ACCENT_SOFT, hover_color="#38493e", text_color=TEXT,
            corner_radius=10, height=38, width=90,
        ).pack(side="right")

        # --- Right: prediction card ---
        right_panel = ctk.CTkFrame(body, fg_color=PANEL, corner_radius=16, width=340)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        ctk.CTkLabel(
            right_panel, text="PREDICTION", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_MUTED, anchor="w",
        ).pack(fill="x", padx=24, pady=(22, 10))

        card = ctk.CTkFrame(right_panel, fg_color=CARD, corner_radius=14)
        card.pack(fill="x", padx=24, pady=(0, 20))

        self.icon = PetalIcon(card, size=100)
        self.icon.pack(pady=(20, 8))

        self.species_label = ctk.CTkLabel(
            card, text="Setosa", font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT,
        )
        self.species_label.pack()

        self.latin_label = ctk.CTkLabel(
            card, text="Iris setosa", font=ctk.CTkFont(size=12, slant="italic"),
            text_color=TEXT_MUTED,
        )
        self.latin_label.pack(pady=(0, 20))

        ctk.CTkLabel(
            right_panel, text="CONFIDENCE", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_MUTED, anchor="w",
        ).pack(fill="x", padx=24, pady=(4, 10))

        self.bars = {}
        for name in class_names:
            bar = ConfidenceBar(right_panel, name, SPECIES_COLORS[name])
            bar.pack(fill="x", padx=24, pady=8)
            self.bars[name] = bar

    # -----------------------------------------------------
    LATIN = {"Setosa": "Iris setosa", "Versicolor": "Iris versicolor", "Virginica": "Iris virginica"}

    def predict_live(self):
        values = np.array([[s.get() for s in self.sliders]])
        scaled = scaler.transform(values)

        proba = model.predict_proba(scaled)[0]
        pred_idx = int(np.argmax(proba))
        pred_name = class_names[pred_idx]

        self.species_label.configure(text=pred_name)
        self.latin_label.configure(text=self.LATIN[pred_name])
        self.icon.draw(SPECIES_COLORS[pred_name])

        for name, p in zip(class_names, proba):
            self.bars[name].update_value(float(p))

    def randomize(self):
        idx = np.random.randint(0, len(X))
        sample = X[idx]
        for slider, val in zip(self.sliders, sample):
            slider.set(float(val))
        self.predict_live()

    def reset_defaults(self):
        defaults = [5.8, 3.0, 4.3, 1.3]
        for slider, val in zip(self.sliders, defaults):
            slider.set(val)
        self.predict_live()


if __name__ == "__main__":
    app = BloomApp()
    app.mainloop()
