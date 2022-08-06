#!/usr/bin/env python

# (c) 2022 Rick Elrod
# MIT

# Yubikeys do not have built in clocks, and thus cannot generate TOTP 2fa codes
# on their own. Using applications like ykman, however, they are able to when
# requested. This script uses ykman to automate the process a bit:
# You can run the script, touch your yubikey, and then the script will type the
# resulting code into the application running at the time (useful if you keybind
# this script in your DE/WM).

# For Fedora Infrastructure, this means:
# - Go to accounts.fedoraproject.org, sign in, settings -> OTP, add a token.
# - In the otpauth:// line it gives you, copy the 'secret' key part.
# - Run: `ykman oath accounts add --touch fedora THAT_SECRET_FROM_ABOVE`
# - Call this script with: `/path/to/yubikey-fill-totp.py fedora` and touch your
#   yubikey.
# - Bind that command to a keybind of your choice, and when you need to auth to
#   Fedora, strike that keybind and touch your yubikey.
# - Win.

import pyautogui
import subprocess
import sys

def get_code(account):
    res = subprocess.run(
        ["ykman", "oath", "accounts", "code", account, "-s"],
        capture_output=True,
    )

    stdout = res.stdout.decode().strip()
    if not stdout.isnumeric():
        raise RuntimeError("Got bad response from ykman: {res}")
    return stdout

def main():
    account = sys.argv[1]
    code = get_code(account)
    pyautogui.typewrite(code)

if __name__ == "__main__":
    main()
