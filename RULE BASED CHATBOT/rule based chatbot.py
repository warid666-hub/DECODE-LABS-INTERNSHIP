import customtkinter as ctk
from datetime import datetime
 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
 
# =========================================================
# RESPONSES  (Intent -> Reply)
# =========================================================
responses = {
    "hello": "Hi there! How can I help you today?",
    "hi": "Hello! What can I do for you?",
    "hey": "Hey! What's up?",
    "good morning": "Good morning! Hope you have a great day ahead.",
    "good evening": "Good evening! How can I assist you?",
    "how are you": "I'm just a program, but I'm doing great! How about you?",
    "what is your name": "I am Nova, your personal AI assistant.",
    "who made you": "I was built to help answer your questions quickly and clearly.",
    "what can you do": "I can respond to greetings and a few simple questions. Try 'help'.",
    "help": "Try saying: hello, how are you, what is your name, what can you do, or bye.",
    "thanks": "You're welcome!",
    "thank you": "You're welcome! Happy to help.",
    "bye": "Goodbye! Have a great day!",
    "exit": "Goodbye! Have a great day!",
    "quit": "Goodbye! Have a great day!",
}
 
EXIT_COMMANDS = {"bye", "exit", "quit"}
FALLBACK_RESPONSE = "I don't understand that yet. Type 'help' to see what I can do."
 
 
def get_response(user_input: str) -> str:
    """Look up a cleaned input and return a reply, with a fallback."""
    return responses.get(user_input, FALLBACK_RESPONSE)
 
 
# =========================================================
# COLOR PALETTE
# =========================================================
COL_BG = "#0f1117"
COL_SIDEBAR = "#151822"
COL_HEADER = "#151822"
COL_BUBBLE_BOT = "#1c2333"
COL_BUBBLE_USER = "#3b82f6"
COL_TEXT = "#e5e7eb"
COL_TEXT_MUTED = "#7c8394"
COL_ACCENT = "#3b82f6"
COL_ACCENT_HOVER = "#2563eb"
COL_ONLINE = "#22c55e"
COL_INPUT_BG = "#1a1e29"
 
 
class ChatBubble(ctk.CTkFrame):
    """A single chat message bubble, aligned left (bot) or right (user)."""
 
    def __init__(self, master, text, is_user=False, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
 
        timestamp = datetime.now().strftime("%H:%M")
        bubble_color = COL_BUBBLE_USER if is_user else COL_BUBBLE_BOT
        text_color = "#ffffff" if is_user else COL_TEXT
        anchor_side = "e" if is_user else "w"
 
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=16, pady=6)
 
        bubble = ctk.CTkFrame(
            container, fg_color=bubble_color, corner_radius=16,
        )
        bubble.pack(anchor=anchor_side)
 
        label = ctk.CTkLabel(
            bubble, text=text, text_color=text_color,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            wraplength=340, justify="left", anchor="w",
        )
        label.pack(padx=14, pady=(10, 2))
 
        time_label = ctk.CTkLabel(
            bubble, text=timestamp, text_color="#c7d2fe" if is_user else COL_TEXT_MUTED,
            font=ctk.CTkFont(family="Segoe UI", size=9),
        )
        time_label.pack(anchor=anchor_side, padx=14, pady=(0, 8))
 
 
class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
 
        self.title("Nova — AI Chatbot")
        self.geometry("1000x680")
        self.minsize(760, 540)
        self.configure(fg_color=COL_BG)
 
        self.is_fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
 
        self._build_sidebar()
        self._build_main_area()
 
        self.after(400, lambda: self._add_bot_message(
            "Hi! I'm Nova, your AI assistant. Ask me something, or type 'help' to get started."
        ))
 
    # -----------------------------------------------------
    # LAYOUT
    # -----------------------------------------------------
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=230, fg_color=COL_SIDEBAR, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
 
        # Avatar + name
        avatar_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        avatar_frame.pack(pady=(36, 10))
 
        avatar = ctk.CTkLabel(
            avatar_frame, text="🤖", font=ctk.CTkFont(size=42),
            width=84, height=84, fg_color=COL_ACCENT, corner_radius=42,
        )
        avatar.pack()
 
        ctk.CTkLabel(
            sidebar, text="Nova", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=COL_TEXT,
        ).pack(pady=(14, 2))
 
        status_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        status_frame.pack(pady=(0, 30))
        ctk.CTkLabel(
            status_frame, text="●", text_color=COL_ONLINE, font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 4))
        ctk.CTkLabel(
            status_frame, text="Online",
            text_color=COL_TEXT_MUTED, font=ctk.CTkFont(size=11),
        ).pack(side="left")
 
        divider = ctk.CTkFrame(sidebar, height=1, fg_color="#242938")
        divider.pack(fill="x", padx=20, pady=(0, 20))
 
        # Spacer
        ctk.CTkLabel(sidebar, text="", fg_color="transparent").pack(expand=True, fill="both")
 
        # Buttons
        self.fullscreen_btn = ctk.CTkButton(
            sidebar, text="⛶  Fullscreen (F11)", command=self.toggle_fullscreen,
            fg_color=COL_INPUT_BG, hover_color="#242938", text_color=COL_TEXT,
            corner_radius=10, height=38, anchor="w",
        )
        self.fullscreen_btn.pack(fill="x", padx=20, pady=(0, 10))
 
        clear_btn = ctk.CTkButton(
            sidebar, text="🗑  Clear Chat", command=self.clear_chat,
            fg_color=COL_INPUT_BG, hover_color="#242938", text_color=COL_TEXT,
            corner_radius=10, height=38, anchor="w",
        )
        clear_btn.pack(fill="x", padx=20, pady=(0, 24))
 
    def _build_main_area(self):
        main = ctk.CTkFrame(self, fg_color=COL_BG, corner_radius=0)
        main.pack(side="left", fill="both", expand=True)
 
        # Header
        header = ctk.CTkFrame(main, fg_color=COL_HEADER, height=64, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
 
        ctk.CTkLabel(
            header, text="Nova",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=COL_TEXT,
        ).pack(side="left", padx=24)
 
        self.clock_label = ctk.CTkLabel(
            header, text="", font=ctk.CTkFont(size=12), text_color=COL_TEXT_MUTED,
        )
        self.clock_label.pack(side="right", padx=24)
        self._update_clock()
 
        # Scrollable chat area
        self.chat_scroll = ctk.CTkScrollableFrame(main, fg_color=COL_BG)
        self.chat_scroll.pack(fill="both", expand=True, padx=8, pady=8)
 
        # Typing indicator (hidden until used)
        self.typing_label = ctk.CTkLabel(
            main, text="", font=ctk.CTkFont(size=11, slant="italic"),
            text_color=COL_TEXT_MUTED,
        )
        self.typing_label.pack(anchor="w", padx=28)
 
        # Input bar
        input_bar = ctk.CTkFrame(main, fg_color=COL_BG, height=76)
        input_bar.pack(fill="x", side="bottom", padx=20, pady=16)
 
        self.entry = ctk.CTkEntry(
            input_bar, placeholder_text="Type a message...",
            fg_color=COL_INPUT_BG, border_color="#242938", border_width=1,
            text_color=COL_TEXT, corner_radius=20, height=46,
            font=ctk.CTkFont(size=13),
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.send_message())
 
        send_btn = ctk.CTkButton(
            input_bar, text="Send  ➤", command=self.send_message,
            fg_color=COL_ACCENT, hover_color=COL_ACCENT_HOVER,
            corner_radius=20, height=46, width=100,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        send_btn.pack(side="right")
 
        self.entry.focus()
 
    # -----------------------------------------------------
    # BEHAVIOR
    # -----------------------------------------------------
    def _update_clock(self):
        self.clock_label.configure(text=datetime.now().strftime("%A, %H:%M"))
        self.after(1000 * 30, self._update_clock)
 
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        self.fullscreen_btn.configure(
            text="⛶  Exit Fullscreen (Esc)" if self.is_fullscreen else "⛶  Fullscreen (F11)"
        )
 
    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.attributes("-fullscreen", False)
            self.fullscreen_btn.configure(text="⛶  Fullscreen (F11)")
 
    def clear_chat(self):
        for widget in self.chat_scroll.winfo_children():
            widget.destroy()
        self._add_bot_message("Chat cleared. How can I help you now?")
 
    def _add_bot_message(self, text):
        bubble = ChatBubble(self.chat_scroll, text, is_user=False)
        bubble.pack(fill="x")
        self.after(50, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))
 
    def _add_user_message(self, text):
        bubble = ChatBubble(self.chat_scroll, text, is_user=True)
        bubble.pack(fill="x")
        self.after(50, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))
 
    def send_message(self):
        raw_text = self.entry.get()
        if raw_text.strip() == "":
            return
 
        self.entry.delete(0, "end")
        self._add_user_message(raw_text)
 
        # --- Sanitization ---
        clean_input = raw_text.lower().strip()
 
        # --- Exit command ---
        if clean_input in EXIT_COMMANDS:
            self._show_typing_then_reply("Goodbye! Have a great day!", exit_after=True)
            return
 
        # --- Dictionary lookup + fallback ---
        reply = get_response(clean_input)
        self._show_typing_then_reply(reply)
 
    def _show_typing_then_reply(self, reply, exit_after=False):
        """Small delay + 'typing...' indicator for a natural feel."""
        self.typing_label.configure(text="Nova is typing...")
 
        def deliver():
            self.typing_label.configure(text="")
            self._add_bot_message(reply)
            if exit_after:
                self.after(1200, self.destroy)
 
        self.after(600, deliver)
 
 
if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
 