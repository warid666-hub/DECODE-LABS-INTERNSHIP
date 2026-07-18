"""
Vantage — Live Tech Stack & Career Path Recommender

Pick the skills you have (or want to use), and Vantage instantly ranks
the career paths that best match them — using TF-IDF vectorization and
cosine similarity, the same math behind real-world recommendation engines.

Install dependencies (one-time):
    pip install customtkinter scikit-learn

Run:
    python vantage_recommender.py
"""

import customtkinter as ctk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# =========================================================
# DATA: job roles -> required skills (acts as "raw_skills.csv")
# =========================================================
JOB_ROLES = {
    "Data Scientist": {
        "skills": ["python", "sql", "machine_learning", "statistics", "data_analysis", "pandas"],
        "blurb": "Turns raw data into predictive models and business insight.",
        "glyph": "◆",
    },
    "DevOps Engineer": {
        "skills": ["aws", "docker", "kubernetes", "ci_cd", "automation", "linux"],
        "blurb": "Automates infrastructure and keeps deployments fast and reliable.",
        "glyph": "▲",
    },
    "Backend Developer": {
        "skills": ["java", "python", "sql", "apis", "data_structures", "git"],
        "blurb": "Builds the server-side logic and APIs that power applications.",
        "glyph": "■",
    },
    "Frontend Developer": {
        "skills": ["javascript", "react", "css", "html", "ui_design", "git"],
        "blurb": "Crafts the interfaces users see and interact with directly.",
        "glyph": "●",
    },
    "Machine Learning Engineer": {
        "skills": ["python", "machine_learning", "tensorflow", "data_structures", "cloud", "statistics"],
        "blurb": "Ships ML models into production systems that scale.",
        "glyph": "◆",
    },
    "Cloud Architect": {
        "skills": ["aws", "cloud", "docker", "kubernetes", "automation", "security"],
        "blurb": "Designs scalable, resilient cloud infrastructure end to end.",
        "glyph": "▲",
    },
    "Cybersecurity Analyst": {
        "skills": ["security", "networking", "linux", "python", "automation", "sql"],
        "blurb": "Defends systems and data against threats and vulnerabilities.",
        "glyph": "◈",
    },
    "Data Engineer": {
        "skills": ["python", "sql", "cloud", "data_structures", "automation", "docker"],
        "blurb": "Builds the pipelines that move and shape data at scale.",
        "glyph": "◆",
    },
    "Mobile Developer": {
        "skills": ["java", "javascript", "ui_design", "apis", "git", "css"],
        "blurb": "Builds the apps people carry in their pockets every day.",
        "glyph": "●",
    },
    "QA / Test Engineer": {
        "skills": ["automation", "python", "git", "data_structures", "sql", "ci_cd"],
        "blurb": "Catches what breaks before your users ever do.",
        "glyph": "■",
    },
    "UI/UX Designer": {
        "skills": ["ui_design", "css", "html", "javascript", "statistics", "networking"],
        "blurb": "Shapes how a product looks, feels, and flows for real people.",
        "glyph": "●",
    },
    "Product Manager": {
        "skills": ["data_analysis", "statistics", "sql", "ui_design", "apis", "automation"],
        "blurb": "Bridges business goals, engineering, and user needs.",
        "glyph": "◈",
    },
}

# Skill chips grouped into categories for a curated, scannable layout
SKILL_CATEGORIES = [
    ("Languages", [
        ("Python", "python"), ("Java", "java"), ("JavaScript", "javascript"), ("SQL", "sql"),
    ]),
    ("Data & ML", [
        ("Machine Learning", "machine_learning"), ("TensorFlow", "tensorflow"),
        ("Statistics", "statistics"), ("Data Analysis", "data_analysis"), ("Pandas", "pandas"),
    ]),
    ("Cloud & DevOps", [
        ("AWS", "aws"), ("Cloud", "cloud"), ("Docker", "docker"), ("Kubernetes", "kubernetes"),
        ("CI/CD", "ci_cd"), ("Automation", "automation"), ("Linux", "linux"),
    ]),
    ("Web & Design", [
        ("React", "react"), ("CSS", "css"), ("HTML", "html"), ("UI Design", "ui_design"),
    ]),
    ("Engineering & Security", [
        ("APIs", "apis"), ("Data Structures", "data_structures"), ("Git", "git"),
        ("Security", "security"), ("Networking", "networking"),
    ]),
]

# =========================================================
# BUILD THE TF-IDF SPACE (runs once on startup)
# =========================================================
role_names = list(JOB_ROLES.keys())
corpus = [" ".join(JOB_ROLES[r]["skills"]) for r in role_names]

vectorizer = TfidfVectorizer()
role_vectors = vectorizer.fit_transform(corpus)


def recommend(selected_tokens):
    """Return roles ranked by cosine similarity to the selected skill set."""
    if not selected_tokens:
        return []
    query = " ".join(selected_tokens)
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, role_vectors)[0]
    ranked = sorted(zip(role_names, scores), key=lambda x: x[1], reverse=True)
    return ranked


# =========================================================
# COLOR PALETTE — light & clean, with bold vibrant accents
# =========================================================
BG = "#f8f7fc"
PANEL = "#ffffff"
CARD = "#ffffff"
CARD_BORDER = "#e8e4f3"
TEXT = "#241c38"
TEXT_MUTED = "#867cA0"
ACCENT = "#ff4d97"
ACCENT_DIM = "#c23570"
ACCENT_SOFT = "#ffe3ef"
CHIP_OFF = "#f1eef9"
CHIP_ON = "#ff4d97"
RANK_COLORS = ["#ff4d97", "#00b4d8", "#e0a300"]
SECTION_LABEL = "#a89dc7"

CATEGORY_COLORS = ["#ff4d97", "#00b4d8", "#4caf3d", "#e0a300", "#8b5cf6"]


class VantageMark(ctk.CTkCanvas):
    """A small mountain-peak glyph — the vantage point — used as the logo."""

    def __init__(self, master, size=40, **kwargs):
        super().__init__(master, width=size, height=size, bg=PANEL,
                          highlightthickness=0, **kwargs)
        self.size = size
        self.draw(ACCENT)

    def draw(self, color):
        self.delete("all")
        s = self.size
        base_y = s * 0.74
        # Horizon line
        self.create_line(s * 0.08, base_y, s * 0.92, base_y, fill="#d8d2ec", width=1)
        # Back peak (secondary vibrant accent)
        self.create_polygon(
            s * 0.30, base_y, s * 0.58, s * 0.22, s * 0.86, base_y,
            fill="#00b4d8", outline="",
        )
        # Front peak (primary vibrant accent)
        self.create_polygon(
            s * 0.10, base_y, s * 0.42, s * 0.14, s * 0.74, base_y,
            fill=color, outline="",
        )
        # Vantage point marker at the summit
        cx, cy = s * 0.42, s * 0.14
        self.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="#ffffff", outline="")


class SkillChip(ctk.CTkButton):
    """A toggleable pill-shaped skill tag."""

    def __init__(self, master, label, token, on_toggle, **kwargs):
        self.token = token
        self.selected = False
        self.on_toggle = on_toggle
        super().__init__(
            master, text=label, command=self._toggle,
            fg_color=CHIP_OFF, hover_color="#e6e1f5", text_color=TEXT_MUTED,
            corner_radius=16, height=32, font=ctk.CTkFont(size=12),
            border_width=1, border_color="#e8e4f3",
            **kwargs,
        )

    def _toggle(self):
        self.selected = not self.selected
        if self.selected:
            self.configure(fg_color=CHIP_ON, text_color="#ffffff",
                            border_color=CHIP_ON,
                            font=ctk.CTkFont(size=12, weight="bold"))
        else:
            self.configure(fg_color=CHIP_OFF, text_color=TEXT_MUTED,
                            border_color="#e8e4f3",
                            font=ctk.CTkFont(size=12))
        self.on_toggle()


class MatchCard(ctk.CTkFrame):
    """A ranked recommendation card showing role, blurb, and match %."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CARD, corner_radius=14,
                          border_width=1, border_color=CARD_BORDER, **kwargs)

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=18, pady=(16, 2))

        self.badge = ctk.CTkLabel(
            top, text="1", font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff", fg_color=ACCENT, corner_radius=12,
            width=24, height=24,
        )
        self.badge.pack(side="left", padx=(0, 10))

        name_box = ctk.CTkFrame(top, fg_color="transparent")
        name_box.pack(side="left", fill="x", expand=True)

        self.role_label = ctk.CTkLabel(
            name_box, text="Role Name", font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT, anchor="w",
        )
        self.role_label.pack(anchor="w")

        self.pct_label = ctk.CTkLabel(
            top, text="0%", font=ctk.CTkFont(size=16, weight="bold"),
            text_color=ACCENT,
        )
        self.pct_label.pack(side="right")

        self.bar = ctk.CTkProgressBar(
            self, height=7, corner_radius=4,
            fg_color=ACCENT_SOFT, progress_color=ACCENT,
        )
        self.bar.pack(fill="x", padx=18, pady=(10, 10))
        self.bar.set(0)

        self.blurb_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED,
            anchor="w", justify="left", wraplength=280,
        )
        self.blurb_label.pack(fill="x", padx=18, pady=(0, 16))

    def update_data(self, rank, role, score, blurb, color):
        self.badge.configure(text=str(rank), fg_color=color)
        self.role_label.configure(text=role)
        self.pct_label.configure(text=f"{score * 100:.0f}%", text_color=color)
        self.bar.configure(progress_color=color)
        self.bar.set(min(score, 1.0))
        self.blurb_label.configure(text=blurb)


class VantageApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vantage — Career Path Matcher")
        self.geometry("1080x700")
        self.minsize(900, 600)
        self.configure(fg_color=BG)

        self.chips = []
        self._build_header()
        self._build_body()
        self.after(200, self.refresh)

    # -----------------------------------------------------
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=PANEL, height=76, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        accent_line = ctk.CTkFrame(self, fg_color=ACCENT, height=2, corner_radius=0)
        accent_line.pack(fill="x", side="top")

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=26, fill="y")

        self.logo = VantageMark(left, size=38)
        self.logo.pack(side="left", padx=(0, 12), pady=19)

        title_box = ctk.CTkFrame(left, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(
            title_box, text="Vantage", font=ctk.CTkFont(size=19, weight="bold"),
            text_color=TEXT, anchor="w",
        ).pack(anchor="w", pady=(14, 0))
        ctk.CTkLabel(
            title_box, text="Find the career path your skills point to",
            font=ctk.CTkFont(size=11), text_color=TEXT_MUTED, anchor="w",
        ).pack(anchor="w")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=26, fill="y")
        self.count_label = ctk.CTkLabel(
            right, text="0 skills selected", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=ACCENT,
        )
        self.count_label.pack(pady=27)

    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color=BG)
        body.pack(fill="both", expand=True, padx=24, pady=22)

        # --- Left: categorized skill chips ---
        left_panel = ctk.CTkFrame(body, fg_color=PANEL, corner_radius=18,
                                    border_width=1, border_color=CARD_BORDER)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 14))

        head_row = ctk.CTkFrame(left_panel, fg_color="transparent")
        head_row.pack(fill="x", padx=26, pady=(24, 6))
        ctk.CTkLabel(
            head_row, text="SELECT YOUR SKILLS", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=SECTION_LABEL, anchor="w",
        ).pack(side="left")
        ctk.CTkButton(
            head_row, text="Clear all", command=self.clear_all,
            fg_color="transparent", hover_color="#f1eef9", text_color=TEXT_MUTED,
            width=70, height=24, corner_radius=8, font=ctk.CTkFont(size=11),
        ).pack(side="right")

        chip_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
        chip_scroll.pack(fill="both", expand=True, padx=16, pady=(4, 18))

        for cat_idx, (category, items) in enumerate(SKILL_CATEGORIES):
            cat_color = CATEGORY_COLORS[cat_idx % len(CATEGORY_COLORS)]
            cat_label = ctk.CTkLabel(
                chip_scroll, text=category.upper(), font=ctk.CTkFont(size=10, weight="bold"),
                text_color=cat_color, anchor="w",
            )
            cat_label.pack(fill="x", padx=8, pady=(14, 6))

            row_frame = ctk.CTkFrame(chip_scroll, fg_color="transparent")
            row_frame.pack(fill="x", padx=4)

            cols = 4
            for i, (label, token) in enumerate(items):
                chip = SkillChip(row_frame, label, token, on_toggle=self.refresh)
                chip.grid(row=i // cols, column=i % cols, padx=5, pady=5, sticky="ew")
                self.chips.append(chip)
            for c in range(cols):
                row_frame.grid_columnconfigure(c, weight=1)

            sep = ctk.CTkFrame(chip_scroll, fg_color=CARD_BORDER, height=1)
            sep.pack(fill="x", padx=8, pady=(10, 0))

        # --- Right: recommendation cards ---
        right_panel = ctk.CTkFrame(body, fg_color=PANEL, corner_radius=18, width=340,
                                     border_width=1, border_color=CARD_BORDER)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        ctk.CTkLabel(
            right_panel, text="TOP MATCHES", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=SECTION_LABEL, anchor="w",
        ).pack(fill="x", padx=26, pady=(24, 12))

        self.empty_label = ctk.CTkLabel(
            right_panel, text="Select at least 3 skills\nto see your top career matches.",
            font=ctk.CTkFont(size=13), text_color=TEXT_MUTED, justify="center",
        )

        self.cards = []
        for _ in range(3):
            card = MatchCard(right_panel)
            self.cards.append(card)

    # -----------------------------------------------------
    def refresh(self):
        selected = [c.token for c in self.chips if c.selected]
        n = len(selected)
        self.count_label.configure(
            text=f"{n} skill{'s' if n != 1 else ''} selected"
        )

        for card in self.cards:
            card.pack_forget()
        self.empty_label.pack_forget()

        if n < 3:
            self.empty_label.pack(pady=70, padx=26)
            return

        ranked = recommend(selected)[:3]
        for i, (role, score) in enumerate(ranked):
            card = self.cards[i]
            card.update_data(
                rank=i + 1, role=role, score=score,
                blurb=JOB_ROLES[role]["blurb"], color=RANK_COLORS[i],
            )
            card.pack(fill="x", padx=26, pady=8)

    def clear_all(self):
        for chip in self.chips:
            if chip.selected:
                chip._toggle()


if __name__ == "__main__":
    app = VantageApp()
    app.mainloop()
