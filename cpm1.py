# zentan_tool.py
import getpass
import re
import sys
import os
import json
import time
import uuid
import requests
import subprocess
import platform
from rich.console import Console

c = Console()

# ═══════════════════════════════════════════════
# 🔑 CONFIG
# ═══════════════════════════════════════════════

API_KEY = os.getenv("CPM_FIREBASE_KEY", "AIzaSyAe_aOVT1gSfmHKBrorFvX4fRwN5nODXVA")

SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
SIGN_UP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
UPDATE_URL  = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={API_KEY}"

RANK_URL = os.getenv(
    "CPM_RANK_URL",
    "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating6",
)

FIREBASE_URL = os.getenv(
    "CPM_FIREBASE_URL",
    "https://zentanshopv2-default-rtdb.firebaseio.com/users",
)

CHANNEL = "ZentanShopChannel"
CHAT    = "ZentanShopChat"

# IMPORTANT: replace with the NEW token after rotating the exposed token.
ADMIN_BOT_TOKEN   = os.getenv("ZENTAN_ADMIN_BOT_TOKEN", "YOUR_NEW_BOT_TOKEN")
ADMIN_TELEGRAM_ID = os.getenv("ZENTAN_ADMIN_ID", "6822729424")

PRICES = {
    1: 10000,
    2: 5000,
    3: 9000,
    4: 2000,
}

GAME_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/json",
    "User-Agent": "UnityPlayer/2022.3.62f2 (UnityWebRequest/1.0, libcurl/8.10.1-DEV)",
    "X-Unity-Version": "2022.3.62f2",
}

# ═══════════════════════════════════════════════
# 🎨 COLORS
# ═══════════════════════════════════════════════

class Colors:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    RESET   = '\033[0m'
    BOLD    = '\033[1m'

def color_text(text, color):
    return f"{color}{text}{Colors.RESET}"

def horizontal_colors(text):
    result = ""
    colors = [Colors.RED, Colors.GREEN, Colors.YELLOW,
              Colors.BLUE, Colors.MAGENTA, Colors.CYAN]
    for i, char in enumerate(text):
        result += f"{colors[i % len(colors)]}{char}{Colors.RESET}"
    return result

def is_email(e):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", e) is not None

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')


def confirm_action(action_name):
    """Ask for confirmation before every paid/service action."""
    while True:
        ans = input(color_text(f"\n[?] {action_name} — Continue? (y/n/exit): ", Colors.CYAN)).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            c.print("[yellow][←] Cancelled.[/yellow]")
            return False
        if ans == "exit":
            farewell()
        c.print("[red][!] Please enter y, n, or exit.[/red]")

# ═══════════════════════════════════════════════
# 🔐 FIREBASE AUTH
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

def sign_up(email, password):
    try:
        r = requests.post(
            SIGN_UP_URL,
            json={"email": email, "password": password, "returnSecureToken": True},
            timeout=10,
        )
        data = r.json()
        if r.status_code == 200:
            c.print("[bold green][✓] Account created successfully![/bold green]")
            return data.get("idToken"), data.get("email", email), data.get("localId")
        err = data.get('error', {}).get('message', 'Signup failed')
        friendly = {
            "EMAIL_EXISTS": "This email is already registered.",
            "OPERATION_NOT_ALLOWED": "Email/password sign-up is disabled in Firebase Console.",
            "WEAK_PASSWORD": "Password is too weak (min 6 chars).",
            "INVALID_EMAIL": "Invalid email address.",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts. Try again later.",
        }.get(err, err)
        c.print(f"[bold red]Error:[/bold red] {friendly}")
    except Exception as e:
        c.print(f"[bold red]Net error:[/bold red] {e}")
    return None, None, None

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
        c.print(f"[bold red]Error:[/bold red] {data.get('error', {}).get('message', 'Update failed')}")
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
        c.print(f"[bold red]Error:[/bold red] {data.get('error', {}).get('message', 'Update failed')}")
    except Exception as e:
        c.print(f"[bold red]Net error:[/bold red] {e}")
    return False, token, None

# ═══════════════════════════════════════════════
# 📱 DEVICE + TELEGRAM ADMIN NOTIFICATION
# ═══════════════════════════════════════════════

def get_device_name():
    try:
        if os.name == "posix":
            result = subprocess.run(
                ["getprop", "ro.product.model"],
                capture_output=True,
                text=True,
                timeout=3,
            )
            model = result.stdout.strip()
            if model:
                return model
    except Exception:
        pass

    try:
        return platform.node() or platform.machine() or "Unknown Device"
    except Exception:
        return "Unknown Device"

def save_device_and_check(user_ref):
    """Save current device and return unique devices for this user."""
    if not user_ref:
        return []

    device = get_device_name()
    safe_device = re.sub(r"[^a-zA-Z0-9._-]", "_", device)

    try:
        device_url = f"{FIREBASE_URL}/{user_ref}/devices/{safe_device}.json"
        requests.put(
            device_url,
            json={
                "name": device,
                "last_seen": int(time.time()),
            },
            timeout=10,
        )

        response = requests.get(
            f"{FIREBASE_URL}/{user_ref}/devices.json",
            timeout=10,
        )
        response.raise_for_status()
        data = response.json() or {}

        devices = set()
        if isinstance(data, dict):
            for item in data.values():
                if isinstance(item, dict) and item.get("name"):
                    devices.add(str(item["name"]))

        return sorted(devices)

    except Exception as e:
        c.print(f"[yellow][!] Device tracking error: {e}[/yellow]")
        return []

def send_admin_telegram(message):
    if not ADMIN_BOT_TOKEN or ADMIN_BOT_TOKEN == "YOUR_NEW_BOT_TOKEN":
        return False

    url = f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            data={
                "chat_id": ADMIN_TELEGRAM_ID,
                "text": message,
            },
            timeout=10,
        )
        return response.status_code == 200
    except requests.RequestException:
        return False

def notify_multi_device(tg_id, devices, email):
    if len(devices) < 2:
        return

    message = (
        "🚨 MULTI-DEVICE LOGIN\n\n"
        f"Telegram ID: {tg_id}\n"
        f"Email: {email}\n"
        f"Devices: {', '.join(devices)}\n"
        f"Device count: {len(devices)}"
    )

    if send_admin_telegram(message):
        c.print("[yellow][!] Multi-device login reported to admin.[/yellow]")

# ═══════════════════════════════════════════════
# 🏆 SET RANK
# ═══════════════════════════════════════════════

def set_rank(auth_token):
    rating_data = {
        "RatingData": {
            "time": int(1e22), "cars": int(1e16), "car_fix": int(1e13),
            "car_collided": int(1e12), "car_exchange": int(1e13),
            "car_trade": int(1e13), "car_wash": int(1e13),
            "slicer_cut": int(1e13), "drift_max": int(1e14),
            "drift": int(1e14), "cargo": int(1e5), "delivery": int(1e5),
            "race_win": int(3e20), "taxi": int(1e10),
            "levels": 10000990000, "gifts": int(1e9),
            "fuel": int(1e10), "offroad": int(1e10),
            "speed_banner": int(1e9), "reactions": int(1e17),
            "run": int(1e9), "real_estate": int(1e9),
            "t_distance": int(1e10), "treasure": int(1e10),
            "block_post": int(1e10), "push_ups": int(1e12),
            "burnt_tire": int(1e10), "passanger_distance": int(1e8),
        }
    }
    try:
        r = requests.post(
            RANK_URL,
            json={"data": json.dumps(rating_data)},
            headers={**GAME_HEADERS, "Authorization": f"Bearer {auth_token}"},
            timeout=15,
        )
        if r.status_code == 200:
            c.print("[bold green][✓] Rank set successfully![/bold green]")
            return True
        c.print(f"[bold red][!] Rank failed: HTTP {r.status_code} — {r.text[:120]}[/bold red]")
    except Exception as e:
        c.print(f"[bold red][!] Rank net error: {e}[/bold red]")
    return False

# ═══════════════════════════════════════════════
# 🌐 LOCATION & FIREBASE
# ═══════════════════════════════════════════════

def get_location():
    try:
        response = requests.get("http://ip-api.com/json", timeout=10)
        return response.json()
    except Exception:
        return None

def get_firebase_data():
    try:
        response = requests.get(f"{FIREBASE_URL}.json", timeout=10)
        return response.json() or {}
    except Exception:
        return {}

def verify_access_key(access_key):
    db = get_firebase_data()
    for uid, user_data in db.items():
        if isinstance(user_data, dict):
            user_key = user_data.get("key")
            if user_key is not None and str(user_key) == str(access_key):
                if user_data.get("is_blocked") is True:
                    return None, None, None, None, True
                is_unlimited = user_data.get("is_unlimited", False)
                balance = 999999 if is_unlimited else user_data.get("balance", 0)
                if not isinstance(balance, (int, float)):
                    balance = 0
                tg_id = user_data.get("telegram_id", "Unknown")
                if tg_id == "Unknown" or tg_id is None:
                    tg_id = "Not Linked"
                return uid, tg_id, balance, is_unlimited, False
    return None, None, None, None, False

# ═══════════════════════════════════════════════
# 🔐 ONE ACCESS KEY = ONE ACTIVE SESSION
# ═══════════════════════════════════════════════

SESSION_ID = str(uuid.uuid4())
DEVICE_ID_FILE = os.path.join(os.path.expanduser("~"), ".zentanshop_device_id")

def get_persistent_device_id():
    try:
        if os.path.exists(DEVICE_ID_FILE):
            value = open(DEVICE_ID_FILE, "r", encoding="utf-8").read().strip()
            if value:
                return value

        value = str(uuid.uuid4())
        with open(DEVICE_ID_FILE, "w", encoding="utf-8") as f:
            f.write(value)
        return value
    except Exception:
        return str(uuid.uuid4())

DEVICE_ID = get_persistent_device_id()
SESSION_TIMEOUT = 90


def claim_access_key(user_ref):
    """Allow only one active session for this access-key account."""
    if not user_ref:
        return False

    url = f"{FIREBASE_URL}/{user_ref}.json"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        user = r.json() or {}

        if user.get("is_blocked") is True:
            return False

        active = user.get("active_session")
        now = int(time.time())

        if isinstance(active, dict):
            old_session = str(active.get("session_id", ""))
            old_device = str(active.get("device_id", ""))
            last_seen = int(active.get("last_seen", 0) or 0)

            # Same running session: refresh its heartbeat.
            if old_session == SESSION_ID and old_device == DEVICE_ID:
                requests.patch(
                    url,
                    json={
                        "active_session": {
                            "session_id": SESSION_ID,
                            "device_id": DEVICE_ID,
                            "last_seen": now
                        }
                    },
                    timeout=10,
                )
                return True

            # Another session is still active.
            if last_seen and now - last_seen < SESSION_TIMEOUT:
                return False

        # No active session, or previous session expired.
        response = requests.patch(
            url,
            json={
                "active_session": {
                    "session_id": SESSION_ID,
                    "device_id": DEVICE_ID,
                    "last_seen": now
                }
            },
            timeout=10,
        )
        return response.status_code == 200

    except Exception as e:
        c.print(f"[yellow][!] Session check error: {e}[/yellow]")
        return False


def validate_active_session(user_ref):
    """Re-check block status and ensure this process owns the active session."""
    if not user_ref:
        return False

    try:
        r = requests.get(f"{FIREBASE_URL}/{user_ref}.json", timeout=10)
        r.raise_for_status()
        user = r.json() or {}

        if user.get("is_blocked") is True:
            return False

        active = user.get("active_session") or {}
        return (
            str(active.get("session_id", "")) == SESSION_ID
            and str(active.get("device_id", "")) == DEVICE_ID
        )
    except Exception:
        return False


def heartbeat(user_ref):
    """Refresh the current session heartbeat."""
    if not user_ref:
        return False

    try:
        if not validate_active_session(user_ref):
            return False

        r = requests.patch(
            f"{FIREBASE_URL}/{user_ref}/active_session.json",
            json={
                "session_id": SESSION_ID,
                "device_id": DEVICE_ID,
                "last_seen": int(time.time())
            },
            timeout=10,
        )
        return r.status_code == 200
    except Exception:
        return False


def release_access_key(user_ref):
    """Release only our own session on exit."""
    if not user_ref:
        return

    try:
        r = requests.get(f"{FIREBASE_URL}/{user_ref}/active_session.json", timeout=10)
        active = r.json() or {}

        if (
            str(active.get("session_id", "")) == SESSION_ID
            and str(active.get("device_id", "")) == DEVICE_ID
        ):
            requests.delete(
                f"{FIREBASE_URL}/{user_ref}/active_session.json",
                timeout=10,
            )
    except Exception:
        pass


def update_balance(user_ref, new_balance):
    try:
        r = requests.patch(
            f"{FIREBASE_URL}/{user_ref}.json",
            json={"balance": int(new_balance)},
            timeout=10,
        )
        return r.status_code == 200
    except Exception:
        return False

# ═══════════════════════════════════════════════
# 🖼️ BANNER & INFO
# ═══════════════════════════════════════════════

def banner():
    clear()
    print(horizontal_colors("=" * 60))
    print(horizontal_colors("Car Parking Multiplayer 1 Tool".center(60)))
    print(horizontal_colors("=" * 60))
    print(color_text("\n          PLEASE LOGOUT FROM CPM BEFORE USING THIS TOOL", Colors.YELLOW))
    print(color_text("    SHARING THE ACCESS KEY IS NOT ALLOWED AND WILL BE BLOCKED", Colors.RED))
    print(color_text(f"           Telegram: @{CHANNEL} or @{CHAT}", Colors.CYAN))
    print(horizontal_colors("=" * 60))

def show_info(email, access_key, tg_id, balance, is_unlimited, location):
    print(color_text("\n========[ PLAYER DETAILS ]========", Colors.CYAN))
    print(color_text(f">> Email        : {email}", Colors.GREEN))
    print(color_text(">> Name         : Player", Colors.GREEN))
    print(color_text(">> LocalID      : DEFAULT_ID", Colors.GREEN))
    print(color_text(">> Moneys       : 50,000,000", Colors.GREEN))
    print(color_text(">> Coins        : 500,000", Colors.GREEN))
    print(color_text(">> Car Count    : 250", Colors.GREEN))
    print(color_text(">> Friend count : 20", Colors.GREEN))

    print(color_text("\n========[ ACCESS KEY DETAILS ]========", Colors.CYAN))
    print(color_text(f">> Access Key  : {access_key}", Colors.YELLOW))
    print(color_text(f">> Telegram ID : {tg_id}", Colors.YELLOW))

    if is_unlimited:
        print(color_text(">> Balance     : Unlimited", Colors.MAGENTA))
    else:
        print(color_text(f">> Balance     : {balance:,}", Colors.MAGENTA))

    if location:
        print(color_text("\n========[ LOCATION ]========", Colors.CYAN))
        print(color_text(f">> IP Address : {location.get('query', 'Unknown')}", Colors.BLUE))
        print(color_text(f">> Location   : {location.get('city','')} {location.get('regionName','')} {location.get('countryCode','')}", Colors.BLUE))
        print(color_text(f">> Country    : {location.get('country','')} {location.get('zip','')}", Colors.BLUE))

    print(color_text("\n========[ MENU ]========", Colors.CYAN))
    print(color_text("(1): Change email                10K", Colors.GREEN))
    print(color_text("(2): Change password              5K", Colors.GREEN))
    print(color_text("(3): Set rank                     9K", Colors.GREEN))
    print(color_text("(4): Register from new account    2K", Colors.GREEN))
    print(color_text("(5): Back to home", Colors.YELLOW))
    print(color_text("(0): Exit out from tool", Colors.RED))
    print(horizontal_colors("\n========[ ZentanShop ]========"))

def farewell():
    print(color_text("\n\n✨ THANK YOU FOR USING ZENTANSHOP ✨", Colors.GREEN))
    print(color_text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━", Colors.CYAN))
    print(color_text(f"📢 Join us: @{CHANNEL}", Colors.CYAN))
    print(color_text(f"💬 Community: @{CHAT}", Colors.CYAN))
    print(color_text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━", Colors.CYAN))
    print(color_text("🚀 Keep growing. Keep creating.", Colors.YELLOW))
    print(color_text("👋 See you next time, Boss!", Colors.GREEN))
    time.sleep(2)
    sys.exit(0)

# ═══════════════════════════════════════════════
# 🆕 REGISTER NEW ACCOUNT
# ═══════════════════════════════════════════════

def register_flow():
    """Create a new Firebase account. Returns (token, email) or (None, None)."""
    print(color_text("\n========[ REGISTER NEW ACCOUNT ]========", Colors.CYAN))

    email = input(color_text("\n[?] New Email: ", Colors.CYAN)).strip()
    if not is_email(email):
        print(color_text("[!] Invalid email format!", Colors.RED))
        time.sleep(2)
        return None, None

    password = getpass.getpass(color_text("[?] New Password (min 6 chars): ", Colors.CYAN))
    if len(password) < 6:
        print(color_text("[!] Password must be at least 6 characters!", Colors.RED))
        time.sleep(2)
        return None, None

    confirm = getpass.getpass(color_text("[?] Confirm Password: ", Colors.CYAN))
    if password != confirm:
        print(color_text("[!] Passwords don't match!", Colors.RED))
        time.sleep(2)
        return None, None

    print(color_text("\n[*] Creating account...", Colors.YELLOW))
    token, new_email, uid = sign_up(email, password)
    if not token:
        time.sleep(2)
        return None, None

    print(color_text(f"\n[✓] Account ready: {new_email}", Colors.GREEN))
    print(color_text(f"[i] Firebase UID: {uid}", Colors.CYAN))
    time.sleep(2)
    return token, new_email

# ═══════════════════════════════════════════════
# 🎯 MAIN
# ═══════════════════════════════════════════════

def main():
    # Startup warning for admin bot
    if ADMIN_BOT_TOKEN == "YOUR_NEW_BOT_TOKEN":
        c.print("[yellow][!] Admin bot token not configured — multi-device alerts DISABLED.[/yellow]")
        time.sleep(1)

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

        # One access key can have only one active user/session.
        if not claim_access_key(user_ref):
            print(color_text("[!] TRY AGAIN.", Colors.RED))
            print(color_text("[!] Note: make sure you filled out the fields correctly!", Colors.YELLOW))
            time.sleep(3)
            continue

        token, cur_email = sign_in(email, password)
        if not token:
            release_access_key(user_ref)
            print(color_text("[%] Trying to Login: TRY AGAIN. Note: make sure you filled out the fields correctly!", Colors.RED))
            time.sleep(2)
            continue

        print(color_text("[%] Trying to Login: SUCCESSFUL", Colors.GREEN))

        # Save device and report 2+ different devices to admin Telegram.
        devices = save_device_and_check(user_ref)
        if len(devices) >= 2:
            notify_multi_device(tg_id, devices, cur_email)

        time.sleep(1)
        back_to_launcher = False

        while True:
            location = get_location()
            banner()

            if not is_unlimited and user_ref:
                db = get_firebase_data()
                node = db.get(user_ref, {}) if isinstance(db, dict) else {}
                try:
                    balance = int(node.get("balance", balance))
                except Exception:
                    pass

            show_info(cur_email, access_key, tg_id, balance, is_unlimited, location)

            # Re-check the key/session before every action or refresh.
            if not validate_active_session(user_ref):
                print(color_text("\n[!] TRY AGAIN.", Colors.RED))
                print(color_text("[!] Note: make sure you filled out the fields correctly!", Colors.YELLOW))
                release_access_key(user_ref)
                time.sleep(2)
                back_to_launcher = True
                break

            heartbeat(user_ref)

            try:
                choice = int(input(color_text("\n[?] Select a Service [0-5]: ", Colors.CYAN)))
            except Exception:
                choice = -1

            if choice == 0:
                answ = input(color_text("\n[?] DO YOU WANT TO EXIT? (y/n): ", Colors.CYAN)).lower()
                if answ == "y":
                    release_access_key(user_ref)
                    farewell()
                else:
                    continue

            if choice == 5:
                print(color_text("\n[←] Returning to Main Menu...", Colors.YELLOW))
                time.sleep(1)
                back_to_launcher = True
                break

            if choice not in (1, 2, 3, 4):
                print(color_text("INVALID CHOICE!", Colors.RED))
                time.sleep(1)
                continue

            cost = PRICES.get(choice, 0)

            if not is_unlimited and balance < cost:
                print(color_text(f"\nINSUFFICIENT BALANCE! Need {cost:,}", Colors.RED))
                print(color_text(f"Your balance: {balance:,}", Colors.YELLOW))
                time.sleep(2)
                continue

            action_names = {
                1: "Change email",
                2: "Change password",
                3: "Set rank",
                4: "Register new account",
            }
            if not confirm_action(action_names[choice]):
                continue

            # ── (1) Change email ────────────────────────────────
            if choice == 1:
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

            # ── (2) Change password ─────────────────────────────
            elif choice == 2:
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

            # ── (3) Set rank ────────────────────────────────────
            elif choice == 3:
                print(color_text("[*] Applying max rank...", Colors.YELLOW))
                ok = set_rank(token)
                if ok:
                    if not is_unlimited:
                        balance -= cost
                        update_balance(user_ref, balance)
                    print(color_text(f"[✓] {cost:,} credit deducted. Balance: {balance:,}", Colors.GREEN))
                time.sleep(2)

            # ── (4) Register new account ────────────────────────
            elif choice == 4:
                new_token, new_email = register_flow()
                if new_token and new_email:
                    # Swap active session to the freshly created account
                    token = new_token
                    cur_email = new_email

                    if not is_unlimited:
                        balance -= cost
                        update_balance(user_ref, balance)

                    print(color_text(
                        f"[✓] {cost:,} credit deducted. Balance: {balance:,}",
                        Colors.GREEN,
                    ))
                    print(color_text(
                        f"[i] Now logged in as: {cur_email}",
                        Colors.CYAN,
                    ))
                time.sleep(2)

        if back_to_launcher:
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        farewell()
