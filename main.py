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
    result = ""
    colors = [Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.MAGENTA, Colors.CYAN]
    for i, char in enumerate(text):
        result += f"{colors[i % len(colors)]}{char}{Colors.RESET}"
    return result

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

# ═══════════════════════════════════════════════
#  🖼️  BANNER
# ═══════════════════════════════════════════════

def banner():
    clear()

    # ─── Top box ───
    print(horizontal_colors("╔══════════════════════════════════════════════════╗"))
    print(color_text("║                                                  ║", Colors.CYAN))
    print(color_text("║           ⚡  Z E N T A N S H O P  ⚡           ║", Colors.CYAN + Colors.BOLD))
    print(color_text("║                  [ 1 · 2 ]                       ║", Colors.YELLOW))
    print(color_text("║                                                  ║", Colors.CYAN))
    print(horizontal_colors("╚══════════════════════════════════════════════════╝"))
    print()

    # ─── ZET logo ───
    print(color_text("███████╗████████╗███████╗", Colors.CYAN))
    print(color_text("╚══███╔╝╚══██╔══╝██╔════╝", Colors.CYAN))
    print(color_text("  ███╔╝    ██║   ███████╗", Colors.CYAN))
    print(color_text(" ███╔╝     ██║   ╚════██║", Colors.CYAN))
    print(color_text("███████╗   ██║   ███████║", Colors.CYAN))
    print(color_text("╚══════╝   ╚═╝   ╚══════╝", Colors.CYAN))
    print()

    # ─── FET logo ───
    print(color_text("███████╗████████╗███████╗", Colors.MAGENTA))
    print(color_text("██╔════╝╚══██╔══╝██╔════╝", Colors.MAGENTA))
    print(color_text("█████╗     ██║   ███████╗", Colors.MAGENTA))
    print(color_text("██╔══╝     ██║   ╚════██║", Colors.MAGENTA))
    print(color_text("███████╗   ██║   ███████║", Colors.MAGENTA))
    print(color_text("╚══════╝   ╚═╝   ╚══════╝", Colors.MAGENTA))
    print()

    # ─── Divider ───
    print(horizontal_colors("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
    print()

    # ─── Menu box ───
    print(color_text("   ╭──────────────────────────────────────────╮", Colors.YELLOW))
    print(color_text("   │                                          │", Colors.YELLOW))
    print(color_text("   │   🚗   [01]   CPM 1 TOOL                 │", Colors.GREEN))
    print(color_text("   │                                          │", Colors.YELLOW))
    print(color_text("   │   🚘   [02]   CPM 2 TOOL                 │", Colors.GREEN))
    print(color_text("   │                                          │", Colors.YELLOW))
    print(color_text("   │   ❌   [00]   EXIT                       │", Colors.RED))
    print(color_text("   │                                          │", Colors.YELLOW))
    print(color_text("   ╰──────────────────────────────────────────╯", Colors.YELLOW))
    print()

    # ─── Footer ───
    print(horizontal_colors("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
    print(color_text("                 © ZentanShop 2025", Colors.MAGENTA + Colors.BOLD))
    print(color_text("            🔥 SEREKBOL BOSS 🔥", Colors.RED))
    print(horizontal_colors("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))

# ═══════════════════════════════════════════════
#  🚀 RUN TOOL
# ═══════════════════════════════════════════════

def run_tool(script):
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
    if not os.path.exists(script_path):
        print(color_text(f"\n[!] File not found: {script_path}", Colors.RED))
        input(color_text("\nPress ENTER to return...", Colors.CYAN))
        return
    try:
        subprocess.run([sys.executable, script_path])
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(color_text(f"\n[!] Error launching {script}: {e}", Colors.RED))
        input(color_text("\nPress ENTER to return...", Colors.CYAN))

# ═══════════════════════════════════════════════
#  🎯 GOODBYE
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
║          ✦  T H A N K  Y O U  ✦                 ║
║                                                  ║
║              🚗  CAR PARKING MULTIPLAYER  🚗     ║
║                                                  ║
║                  🔥 SEREKBOL BOSS 🔥             ║
║                                                  ║
║                 ★  GOOD BYE  ★                   ║
║                                                  ║
╚══════════════════════════════════════════════════╝
""", Colors.GREEN))

# ═══════════════════════════════════════════════
#  🎯 MAIN
# ═══════════════════════════════════════════════

def main():
    while True:
        banner()
        try:
            choice = input(color_text("\n   [?] Select a Tool [0-2]: ", Colors.CYAN + Colors.BOLD)).strip()
        except (KeyboardInterrupt, EOFError):
            goodbye()
            sys.exit()

        if choice == "0":
            goodbye()
            sys.exit()
        elif choice == "1":
            run_tool("cpm1.py")
        elif choice == "2":
            run_tool("cpm2.py")
        else:
            print(color_text("   [!] Invalid choice!", Colors.RED))
            time.sleep(1)

# ═══════════════════════════════════════════════
#  🚀 ENTRY POINT
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        goodbye()
        sys.exit()
