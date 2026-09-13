import os
import sys
import time
import subprocess


# ═══════════════════════════════════════════════
#  🎨 COLORS
# ═══════════════════════════════════════════════

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def color_text(text, color):
    return f"{color}{text}{Colors.RESET}"


def horizontal_colors(text):
    colors = [
        Colors.RED,
        Colors.GREEN,
        Colors.YELLOW,
        Colors.BLUE,
        Colors.MAGENTA,
        Colors.CYAN
    ]

    return "".join(
        f"{colors[i % len(colors)]}{char}{Colors.RESET}"
        for i, char in enumerate(text)
    )


def clear():
    os.system("clear" if os.name == "posix" else "cls")


# ═══════════════════════════════════════════════
#  🖼️  BANNER
# ═══════════════════════════════════════════════

def banner():
    clear()

    print(horizontal_colors(
        "╔══════════════════════════════════════════════════╗"
    ))
    print(color_text(
        "║                                                  ║",
        Colors.CYAN
    ))
    print(color_text(
        "║           ⚡  Z E N T A N S H O P  ⚡           ║",
        Colors.CYAN + Colors.BOLD
    ))
    print(color_text(
        "║                  [ 1 · 2 ]                       ║",
        Colors.YELLOW + Colors.BOLD
    ))
    print(color_text(
        "║                                                  ║",
        Colors.CYAN
    ))
    print(horizontal_colors(
        "╚══════════════════════════════════════════════════╝"
    ))

    print()

    # ─── ZET ───
    print(color_text("███████╗████████╗███████╗", Colors.CYAN))
    print(color_text("╚══███╔╝╚══██╔══╝██╔════╝", Colors.CYAN))
    print(color_text("  ███╔╝    ██║   ███████╗", Colors.CYAN))
    print(color_text(" ███╔╝     ██║   ╚════██║", Colors.CYAN))
    print(color_text("███████╗   ██║   ███████║", Colors.CYAN))
    print(color_text("╚══════╝   ╚═╝   ╚══════╝", Colors.CYAN))

    print()

    # ─── FET ───
    print(color_text("███████╗████████╗███████╗", Colors.MAGENTA))
    print(color_text("██╔════╝╚══██╔══╝██╔════╝", Colors.MAGENTA))
    print(color_text("█████╗     ██║   ███████╗", Colors.MAGENTA))
    print(color_text("██╔══╝     ██║   ╚════██║", Colors.MAGENTA))
    print(color_text("███████╗   ██║   ███████║", Colors.MAGENTA))
    print(color_text("╚══════╝   ╚═╝   ╚══════╝", Colors.MAGENTA))

    print()

    # ─── Divider ───
    print(horizontal_colors(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ))
    print()

    # ─── MENU ───
    print(color_text(
        "   ╭──────────────────────────────────────────╮",
        Colors.YELLOW
    ))
    print(color_text(
        "   │              MAIN MENU                   │",
        Colors.YELLOW + Colors.BOLD
    ))
    print(color_text(
        "   ├──────────────────────────────────────────┤",
        Colors.YELLOW
    ))
    print(color_text(
        "   │   🚗   [1]   CPM 1 TOOL                  │",
        Colors.GREEN + Colors.BOLD
    ))
    print(color_text(
        "   │                                          │",
        Colors.YELLOW
    ))
    print(color_text(
        "   │   🚘   [2]   CPM 2 TOOL                  │",
        Colors.GREEN + Colors.BOLD
    ))
    print(color_text(
        "   │                                          │",
        Colors.YELLOW
    ))
    print(color_text(
        "   │   ❌   [0]   EXIT                        │",
        Colors.RED + Colors.BOLD
    ))
    print(color_text(
        "   ╰──────────────────────────────────────────╯",
        Colors.YELLOW
    ))

    print()

    # ─── FOOTER ───
    print(horizontal_colors(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ))
    print(color_text(
        "                 © ZENTANSHOP 2026",
        Colors.MAGENTA + Colors.BOLD
    ))
    print(color_text(
        "              🔥 SEREKBOL BOSS 🔥",
        Colors.RED + Colors.BOLD
    ))
    print(horizontal_colors(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ))


# ═══════════════════════════════════════════════
#  🚀 RUN TOOL
# ═══════════════════════════════════════════════

def run_tool(script):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, script)

    if not os.path.isfile(script_path):
        print()
        print(color_text(
            f"   [!] File not found: {script}",
            Colors.RED + Colors.BOLD
        ))
        time.sleep(2)
        return

    try:
        subprocess.run(
            [sys.executable, script_path],
            check=False
        )

    except KeyboardInterrupt:
        print(color_text(
            "\n   [!] Tool stopped.",
            Colors.YELLOW
        ))
        time.sleep(1)

    except Exception as e:
        print(color_text(
            f"\n   [!] Error: {e}",
            Colors.RED
        ))
        time.sleep(2)


# ═══════════════════════════════════════════════
#  👋 GOODBYE
# ═══════════════════════════════════════════════

def goodbye():
    clear()

    print(color_text("""
╔══════════════════════════════════════════════════╗
║                                                  ║
║              ███████╗████████╗███████╗          ║
║              ╚══███╔╝╚══██╔══╝██╔════╝          ║
║                ███╔╝    ██║   ███████╗          ║
║               ███╔╝     ██║   ╚════██║          ║
║              ███████╗   ██║   ███████║          ║
║              ╚══════╝   ╚═╝   ╚══════╝          ║
║                                                  ║
║             ✦  T H A N K  Y O U  ✦              ║
║                                                  ║
║          🚗  CAR PARKING MULTIPLAYER  🚗         ║
║                                                  ║
║                🔥 SEREKBOL BOSS 🔥              ║
║                                                  ║
║                 ★  GOOD BYE  ★                   ║
║                                                  ║
╚══════════════════════════════════════════════════╝
""", Colors.GREEN + Colors.BOLD))

    time.sleep(1)


# ═══════════════════════════════════════════════
#  🎯 MAIN
# ═══════════════════════════════════════════════

def main():
    while True:
        banner()

        try:
            choice = input(
                color_text(
                    "\n   [?] Select a Tool [0-2]: ",
                    Colors.CYAN + Colors.BOLD
                )
            ).strip()

        except (KeyboardInterrupt, EOFError):
            goodbye()
            sys.exit(0)

        if choice == "0":
            goodbye()
            sys.exit(0)

        elif choice == "1":
            run_tool("cpm1.py")

        elif choice == "2":
            run_tool("cpm2.py")

        else:
            print()
            print(color_text(
                "   [!] Invalid choice! Please select 0, 1 or 2.",
                Colors.RED + Colors.BOLD
            ))
            time.sleep(1)


# ═══════════════════════════════════════════════
#  🚀 ENTRY POINT
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        goodbye()
        sys.exit(0)
