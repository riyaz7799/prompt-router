#!/usr/bin/env python3
# ============================================================
#  main.py  –  CLI Interface for the Prompt Router
# ============================================================

import sys
from router import handle_message

# ── ANSI color codes ─────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
GRAY   = "\033[90m"

INTENT_COLORS = {
    "code":    BLUE,
    "data":    GREEN,
    "writing": YELLOW,
    "career":  CYAN,
    "unclear": RED,
}

INTENT_ICONS = {
    "code":    "🧑‍💻",
    "data":    "📊",
    "writing": "✍️ ",
    "career":  "💼",
    "unclear": "🤔",
}

BANNER = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════╗
║       LLM-Powered Prompt Router          ║
║  Type your message and press Enter.      ║
║  Prefix with @code/@data/@writing/       ║
║  @career to override the classifier.     ║
║  Type 'quit' or 'exit' to stop.          ║
╚══════════════════════════════════════════╝{RESET}
"""


def print_result(result: dict):
    intent     = result["intent"]
    confidence = result["confidence"]
    response   = result["response"]

    color = INTENT_COLORS.get(intent, GRAY)
    icon  = INTENT_ICONS.get(intent, "❓")

    print(f"\n{color}{BOLD}╔═ Detected Intent ════════════════════════╗{RESET}")
    print(f"{color}{BOLD}  {icon}  Intent    : {intent.upper()}{RESET}")
    print(f"{color}{BOLD}  📈 Confidence: {confidence:.0%}{RESET}")
    print(f"{color}{BOLD}╚══════════════════════════════════════════╝{RESET}\n")
    print(f"{BOLD}Response:{RESET}")
    print(f"{response}")
    print(f"\n{GRAY}─────────────────────────────────────────────{RESET}\n")


def interactive_mode():
    print(BANNER)
    while True:
        try:
            user_input = input(f"{BOLD}You:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{CYAN}Goodbye!{RESET}")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print(f"{CYAN}Goodbye!{RESET}")
            break

        print(f"\n{GRAY}Classifying intent...{RESET}")
        result = handle_message(user_input)
        print_result(result)


def single_message_mode(message: str):
    """Run a single message (useful for scripting / testing)."""
    result = handle_message(message)
    print_result(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Allow passing a message directly: python main.py "fix this bug"
        msg = " ".join(sys.argv[1:])
        single_message_mode(msg)
    else:
        interactive_mode()