# Nova — Rule-Based AI Chatbot

A desktop chatbot built entirely on rule-based logic — no machine learning, no external AI model. Just clean control flow, dictionary-based intent matching, and a polished GUI.

This project is the foundation of a broader internship track: understanding *why* deterministic, rule-based systems still matter even in the age of large language models (traceability, safety, zero hallucination risk, and compliance).

## Preview

*(Add a screenshot or short GIF of the app here once you run it — drag the image into this section on GitHub and it'll render automatically.)*

## Features

- 🖥️ **Modern desktop GUI** — dark theme, chat bubbles, timestamps, built with CustomTkinter
- 🖱️ **Fullscreen mode** — toggle with `F11`, exit with `Esc`
- 🔤 **Input sanitization** — case-insensitive and whitespace-tolerant matching
- 📚 **Dictionary-based knowledge base** — O(1) lookup instead of a long if-elif chain
- 🔁 **Continuous conversation loop** with a clean exit command
- 💬 **"Typing..." indicator** for a more natural feel
- 🧹 **Clear chat** button to reset the conversation

## How It Works

1. User input is captured and normalized (`.lower().strip()`)
2. The cleaned input is checked against a Python dictionary of known intents
3. If a match is found, the mapped response is returned
4. If no match is found, a fallback response is shown
5. Typing an exit command (`bye`, `exit`, `quit`) ends the session

```python
responses = {
    "hello": "Hi there! How can I help you today?",
    "how are you": "I'm just a program, but I'm doing great!",
    # ...
}

reply = responses.get(user_input, "I don't understand that yet.")
```

## Tech Stack

- **Python 3**
- **CustomTkinter** — for the modern GUI
- Standard library only otherwise (`datetime`, `tkinter`)

## Installation & Usage

```bash
# Clone the repo
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# Install the one dependency
pip install customtkinter

# Run the app
python rule_based_chatbot_pro.py
```

## Controls

| Action | Key |
|---|---|
| Send message | `Enter` |
| Toggle fullscreen | `F11` |
| Exit fullscreen | `Esc` |

## What This Project Demonstrates

- Control flow and conditional logic fundamentals
- Clean input handling and data normalization
- Efficient lookup design (dictionary vs. if-elif ladder)
- Building an actual usable GUI application in Python, not just a script

## Roadmap

- [ ] Keyword-based matching (instead of exact match) for more flexible input handling
- [ ] Expanded intent list (40+ responses)
- [ ] Hybrid mode — fall back to an LLM API when no rule matches
- [ ] Persistent chat history

## License

This project is open for learning purposes. Feel free to fork and build on it.

