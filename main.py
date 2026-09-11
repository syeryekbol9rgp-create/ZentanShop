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

███████╗███████╗██████╗ ███████╗██╗  ██╗██████╗  ██████╗ ██╗     
██╔════╝██╔════╝██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗██║     
███████╗█████╗  ██████╔╝█████╗  ███████║██████╔╝██║   ██║██║     
╚════██║██╔══╝  ██╔══██╗██╔══╝  ██╔═██╗ ██╔══██╗██║   ██║██║     
███████║███████╗██║  ██║███████╗██║  ██╗██████╔╝╚██████╔╝███████╗
╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝

██████╗  ██████╗ ███████╗███████╗
██╔══██╗██╔═══██╗██╔════╝██╔════╝
██████╔╝██║   ██║███████╗███████╗
██╔══██╗██║   ██║╚════██║╚════██║
██████╔╝╚██████╔╝███████║███████║
╚═════╝  ╚═════╝ ╚══════╝╚══════╝
    print()
    print(color_text("        🚗  [01]  CPM 1 TOOL", Colors.GREEN))
    print()
    print(color_text("        🚘  [02]  CPM 2 TOOL", Colors.GREEN))
    print()
    print(color_text("        ❌  [0]  EXIT", Colors.RED))
    print()
    print(horizontal_colors("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
    print(color_text("             © ZentanShop", Colors.MAGENTA))
    print(horizontal_colors("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))

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
#  🎯 MAIN
# ═══════════════════════════════════════════════

def main():
    while True:
        banner()
        try:
            choice = input(color_text("\n[?] Select a Tool [0-2]: ", Colors.CYAN)).strip()
        except (KeyboardInterrupt, EOFError):
            print(color_text("\n\nBye bye 👋", Colors.YELLOW))
            sys.exit()

        if choice == "0":
            print(color_text("\nBye bye 👋", Colors.YELLOW))
            time.sleep(1)
            sys.exit()
        elif choice == "1":
            run_tool("cpm1.py")
        elif choice == "2":
            run_tool("cpm2.py")
        else:
            print(color_text("[!] Invalid choice!", Colors.RED))
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color_text("\n\nBye bye 👋", Colors.YELLOW))
        sys.exit()
