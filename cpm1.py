import getpass
import re
import sys
import os
import requests
import json
import time
from rich.console import Console

c = Console()

# ═══════════════════════════════════════════════
#  ⚙️  CONFIG
# ═══════════════════════════════════════════════

API_KEY = "AIzaSyAe_aOVT1gSfmHKBrorFvX4fRwN5nODXVA"
SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
UPDATE_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={API_KEY}"

FIREBASE_URL = "https://kayzen-1ff37-default-rtdb.firebaseio.com/users"
CHANNEL = "ZentanShopChannel"
CHAT = "ZentanShopChat"

PRICES = {
    1: 10000,   # change email
    3: 5000,    # change password
}

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

def is_email(e):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", e) is not None

# ═══════════════════════════════════════════════
#  🖼️  GOODBYE BANNER  (defined at top level!)
# ═══════════════════════════════════════════════

def goodbye_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(color_text(f"""
╔══════════════════════════════════════════════════╗
║                                                  ║
║              ███████╗████████╗███████╗          ║
║              ╚══███╔╝╚══██╔══╝██╔════╝          ║
║                ███╔╝    ██║   ███████╗          ║
║               ███╔╝     ██║   ╚════██║          ║
║              ███████╗   ██║   ███████║          ║
║              ╚══════╝   ╚═╝   ╚══════╝          ║
║                                                  ║
║             ✦ THANK YOU FOR USING ZTS ✦         ║
║                                                  ║
║              🚗  CAR PARKING MULTIPLAYER  🚗     ║
║                       ⚡ CPM1 ⚡                  ║
║                                                  ║
║          📢 JOIN  @{CHANNEL}  |  @{CHAT}             ║
║                                                  ║
║              🔥 SEREKBOL BOSS 🔥                 ║
║                                                  ║
║                 ★ GOOD BYE ★                     ║
║                                                  ║
╚══════════════════════════════════════════════════╝
""", Colors.GREEN))

# ═══════════════════════════════════════════════
#  🔐 FIREBASE AUTH
# ═══════════════════════════════════════════════

def sign_in(email, password):
    try:
        r = requests.post(
            SIGN_IN_URL,
            json={"email": email, "password": password, "returnSecureToken": True},
            timeout=10,
        )
        data = r.json()
        if r.status_code == 200:
            return data.get("idToken"), data.get("email", email)
        c.print(f"[bold red]Error:[/bold red] {data.get('error', {}).get('message', 'Auth failed')}")
    except Exception as e:
        c.print(f"[bold red]Net error:[/bold red] {e}")
    return None, None

def update_email(token, new_email):
    try:
        r = requests.post(
            UPDATE_URL,
            json={"idToken": token, "email": new_email, "returnSecureToken": True},
            timeout=10,
        )
        data = r.json()
        if r.status_code == 200:
            c.print("[bold green]Email updated successfully![/bold green]")
            return True, data.get("idToken", token), data.get("email", new_email)
        error_msg = data.get('error', {}).get('message', 'Update failed')
        c.print(f"[bold red]Error:[/bold red] {error_msg}")
    except Exception as e:
        c.print(f"[bold red]Net error:[/bold red] {e}")
    return False, token, None

def update_password(token, new_password):
    try:
        r = requests.post(
            UPDATE_URL,
            json={"idToken": token, "password": new_password, "returnSecureToken": True},
            timeout=10,
        )
        data = r.json()
        if r.status_code == 200:
            c.print("[bold green]Password updated successfully![/bold green]")
            return True, data.get("idToken", token), None
        error_msg = data.get('error', {}).get('message', 'Update failed')
        c.print(f"[bold red]Error:[/bold red] {error_msg}")
    except Exception as e:
        c.print(f"[bold red]Net error:[/bold red] {e}")
    return False, token, None

# ═══════════════════════════════════════════════
#  🌐 LOCATION & FIREBASE
# ═══════════════════════════════════════════════

def get_location():
    try:
        response = requests.get("http://ip-api.com/json", timeout=10)
        return response.json()
    except:
        return None

def get_firebase_data():
    try:
        response = requests.get(f"{FIREBASE_URL}.json", timeout=10)
        return response.json() or {}
    except:
        return {}

def verify_access_key(access_key):
    db = get_firebase_data()
    for uid, user_data in db.items():
        if isinstance(user_data, dict):
            user_key = user_data.get('key')
            if user_key is not None and str(user_key) == str(access_key):
                if user_data.get('is_blocked') == True:
                    return None, None, None, None, True
                is_unlimited = user_data.get('is_unlimited', False)
                balance = 999999 if is_unlimited else user_data.get('balance', 0)
                if not isinstance(balance, (int, float)):
                    balance = 0
                tg_id = user_data.get('telegram_id', 'Unknown')
                if tg_id == 'Unknown' or tg_id is None:
                    tg_id = 'Not Linked'
                return uid, tg_id, balance, is_unlimited, False
    return None, None, None, None, False

def update_balance(user_ref, new_balance):
    try:
        requests.patch(f"{FIREBASE_URL}/{user_ref}.json", json={"balance": new_balance}, timeout=10)
        return True
    except:
        return False

# ═══════════════════════════════════════════════
#  🖼️  BANNER & INFO
# ═══════════════════════════════════════════════

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')

    # ─── ZET LOGO ───
    print(color_text("███████╗████████╗███████╗", Colors.CYAN))
    print(color_text("╚══███╔╝╚══██╔══╝██╔════╝", Colors.CYAN))
    print(color_text("  ███╔╝    ██║   ███████╗", Colors.CYAN))
    print(color_text(" ███╔╝     ██║   ╚════██║", Colors.CYAN))
    print(color_text("███████╗   ██║   ███████║", Colors.CYAN))
    print(color_text("╚══════╝   ╚═╝   ╚══════╝", Colors.CYAN))
    print()

    # ─── CPM1 LOGO ───
    print(color_text(" ██████╗██████╗ ███╗   ███╗", Colors.MAGENTA))
    print(color_text("██╔════╝██╔══██╗████╗ ████║", Colors.MAGENTA))
    print(color_text("██║     ██████╔╝██╔████╔██║", Colors.MAGENTA))
    print(color_text("██║     ██╔═══╝ ██║╚██╔╝██║", Colors.MAGENTA))
    print(color_text("╚██████╗██║     ██║ ╚═╝ ██║", Colors.MAGENTA))
    print(color_text(" ╚═════╝╚═╝     ╚═╝     ╚═╝", Colors.MAGENTA))
    print()

    # ─── TITLE ───
    print(color_text("              🚗 CPM1 🚗", Colors.GREEN))
    print(color_text("        🔥 SEREKBOL BOSS 🔥", Colors.RED))
    print(horizontal_colors("=" * 60))

def show_info(email, access_key, tg_id, balance, is_unlimited, location):
    print(color_text("\n========[ PLAYER DETAILS ]========", Colors.CYAN))
    print(color_text(f">> Email      : {email}", Colors.GREEN))
    print(color_text(f">> Name       : Player", Colors.GREEN))
    print(color_text(f">> LocalID    : DEFAULT_ID", Colors.GREEN))
    print(color_text(f">> Moneys     : 50,000,000", Colors.GREEN))
    print(color_text(f">> Coins      : 500,000", Colors.GREEN))
    print(color_text(f">> Car Count  : 220", Colors.GREEN))

    print(color_text("\n========[ ACCESS KEY DETAILS ]========", Colors.CYAN))
    print(color_text(f">> Access Key  : {access_key}", Colors.YELLOW))
    print(color_text(f">> Telegram ID : {tg_id}", Colors.YELLOW))

    if is_unlimited:
        print(color_text(f">> Balance     : Unlimited", Colors.MAGENTA))
    else:
        print(color_text(f">> Balance     : {balance:,}", Colors.MAGENTA))

    if location:
        print(color_text("\n========[ LOCATION ]========", Colors.CYAN))
        print(color_text(f">> IP Address : {location.get('query', 'Unknown')}", Colors.BLUE))
        print(color_text(f">> Location   : {location.get('city', '')} {location.get('regionName', '')} {location.get('countryCode', '')}", Colors.BLUE))
        print(color_text(f">> Country    : {location.get('country', '')} {location.get('zip', '')}", Colors.BLUE))

    print(color_text("\n========[ MENU ]========", Colors.CYAN))
    print(color_text("(01): Change email       10K", Colors.GREEN))
    print(color_text("(03): Change password     5K", Colors.GREEN))
    print(color_text("(05): Back to Home", Colors.YELLOW))
    print(color_text("(0) : Exit From Tool", Colors.RED))
    print(horizontal_colors("\n========[ ZentanShop ]========"))

# ═══════════════════════════════════════════════
#  🎯 MAIN
# ═══════════════════════════════════════════════

def main():
    while True:
        banner()

        email = input(color_text("\n[?] Account Email: ", Colors.CYAN)).strip()
        password = getpass.getpass(color_text("[?] Account Password: ", Colors.CYAN))
        access_key = input(color_text("[?] Access key: ", Colors.CYAN)).strip()

        if not is_email(email):
            print(color_text("[!] Invalid email format!", Colors.RED))
            time.sleep(2)
            continue

        if len(password) < 6:
            print(color_text("[!] Password must be at least 6 characters!", Colors.RED))
            time.sleep(2)
            continue

        print(color_text("\n[*] Trying to Login...", Colors.YELLOW))
        time.sleep(1)

        user_ref, tg_id, balance, is_unlimited, is_blocked = verify_access_key(access_key)

        if is_blocked:
            print(color_text("[!] TRY AGAIN.", Colors.RED))
            print(color_text("[!] Note: This access key is blocked!", Colors.YELLOW))
            time.sleep(3)
            continue

        if user_ref is None:
            print(color_text("[!] TRY AGAIN.", Colors.RED))
            print(color_text("[!] Note: make sure you filled out the fields correctly!", Colors.YELLOW))
            time.sleep(3)
            continue

        token, cur_email = sign_in(email, password)

        if not token:
            print(color_text("[%] Trying to Login: TRY AGAIN. Note: make sure you filled out the fields correctly!", Colors.RED))
            time.sleep(2)
            continue

        print(color_text("[%] Trying to Login: SUCCESSFUL", Colors.GREEN))
        time.sleep(1)

        # ═══════════════════════════════════
        #  INNER MENU LOOP
        # ═══════════════════════════════════
        back_to_launcher = False

        while True:
            location = get_location()
            banner()

            if not is_unlimited and user_ref:
                db = get_firebase_data()
                balance = int(db.get(user_ref, {}).get('balance', 0))

            show_info(cur_email, access_key, tg_id, balance, is_unlimited, location)

            try:
                choice = int(input(color_text("\n[?] Select a Service [0-5]: ", Colors.CYAN)))
            except:
                choice = -1

            # ─── EXIT (0) ─────────────────────
            if choice == 0:
                answ = input(color_text("\n[?] DO YOU WANT TO EXIT? (y/n): ", Colors.CYAN)).lower()
                if answ == "y":
                    goodbye_banner()
                    sys.exit()
                else:
                    continue

            # ─── BACK TO HOME (5) ─────────────
            if choice == 5:
                print(color_text("\n[←] Returning to Main Menu...", Colors.YELLOW))
                time.sleep(1)
                back_to_launcher = True
                break

            # ─── VALIDATION ───────────────────
            if choice not in [1, 3]:
                print(color_text("INVALID CHOICE!", Colors.RED))
                time.sleep(1)
                continue

            cost = PRICES.get(choice, 0)

            # ─── PAID SERVICES ────────────────
            if is_unlimited or balance >= cost:
                if choice == 1:  # Change email
                    new_email = input(color_text("[?] New email: ", Colors.CYAN)).strip()
                    if not is_email(new_email):
                        print(color_text("[!] Invalid email format!", Colors.RED))
                        time.sleep(2)
                        continue

                    confirm_email = input(color_text("[?] Confirm email: ", Colors.CYAN)).strip()
                    if new_email != confirm_email:
                        print(color_text("[!] Emails don't match!", Colors.RED))
                        time.sleep(2)
                        continue

                    ok, token, updated_email = update_email(token, new_email)
                    if ok and updated_email:
                        cur_email = updated_email
                        if not is_unlimited:
                            balance -= cost
                            update_balance(user_ref, balance)
                        print(color_text("[✓] Email changed successfully!", Colors.GREEN))
                    time.sleep(2)

                elif choice == 3:  # Change password
                    new_password = getpass.getpass(color_text("[?] New password: ", Colors.CYAN))
                    if len(new_password) < 6:
                        print(color_text("[!] Password must be at least 6 characters!", Colors.RED))
                        time.sleep(2)
                        continue

                    confirm_password = getpass.getpass(color_text("[?] Confirm password: ", Colors.CYAN))
                    if new_password != confirm_password:
                        print(color_text("[!] Passwords don't match!", Colors.RED))
                        time.sleep(2)
                        continue

                    ok, token, _ = update_password(token, new_password)
                    if ok:
                        if not is_unlimited:
                            balance -= cost
                            update_balance(user_ref, balance)
                        print(color_text("[✓] Password changed successfully!", Colors.GREEN))
                    time.sleep(2)
            else:
                print(color_text(f"\nINSUFFICIENT BALANCE! Need {cost:,}", Colors.RED))
                print(color_text(f"Your balance: {balance:,}", Colors.YELLOW))
                time.sleep(2)

        # ─── Return to launcher ───
        if back_to_launcher:
            break


# ═══════════════════════════════════════════════
#  🚀 ENTRY POINT
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        goodbye_banner()
        sys.exit()

