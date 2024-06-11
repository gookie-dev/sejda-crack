import os
import sys
import json
import string
import struct
import random
import subprocess


class SejdaCrack:
    def __init__(self):
        self.platform = sys.platform
        self.emoji = None
        self.asar = None
        self.prefs = None
        self.versions = ["7.7.0"]
        self.cmd = None
        self.main()

    def main(self):
        self.print("🔥", "Sejda PDF Desktop crack by gookie")

        if self.platform == "darwin":
            self.print("🍎", "MacOS not supported (yet)")
            exit(1)
        elif self.platform == "win32":
            self.asar = r"C:\Program Files\Sejda PDF Desktop\resources\app.asar"
            self.prefs = os.path.join(os.getenv("APPDATA"), "sejda-desktop", "prefs.json")
            self.cmd = ["powershell", "-Command",
                        "Get-Process | Where-Object {$_.ProcessName -eq \"Sejda PDF Desktop\"}"]
            self.print("🪟", "Windows detected")
        elif self.platform == "linux":
            self.asar = "/opt/sejda-desktop/resources/app.asar"
            sudo_user = os.getenv("SUDO_USER")
            if sudo_user:
                home_dir = os.path.expanduser(f'~{sudo_user}')
            else:
                home_dir = os.getenv("HOME")
            self.prefs = os.path.join(home_dir, ".sejda")
            self.cmd = ["pgrep", "-x", "sejda-desktop"]
            self.print("🐧", "Linux detected")
        else:
            self.exit(f"Unsupported platform: {self.platform}")

        self.check_file(self.asar, "Sejda PDF Desktop ASAR")
        self.check_file(self.asar, "Sejda PDF Desktop preferences")
        self.check_version()
        self.check_process()
        self.patch_files()
        self.print("🎉", "Cracked successful")
        self.print("⭐", "Would appreciate a star https://github.com/gookie-dev/sejda-crack")

    def check_file(self, file: str, name: str):
        if not os.path.exists(file):
            self.print("❌", f"{name} not found in default location: {file}")
            self.asar = input(f"Enter path to {name}: ")
            self.check_files()
        self.print("📦", f"Found {name}")

        if not os.access(self.asar, os.R_OK):
            self.exit(
                f"{self.asar} is not readable.\nTry to run this script as administrator / root or change file permissions")

        if not os.access(self.asar, os.W_OK):
            self.exit(
                f"{self.asar} is not writable.\nTry to run this script as administrator / root or change file permissions")

    def check_version(self):
        asar_file = open(self.asar, 'rb')
        asar_file.seek(4)
        header_size = struct.unpack('I', asar_file.read(4))
        if len(header_size) <= 0:
            self.exit("Failed to read ASAR header size")
        header_size = header_size[0] - 8
        asar_file.seek(asar_file.tell() + 8)
        header = asar_file.read(header_size).decode('utf-8')
        files = json.loads(header.replace("\x00",""))
        offset = asar_file.seek(asar_file.tell())
        files = files["files"]
        for name, contents in files.items():
            if name == "package.json":
                if "offset" in contents:
                    asar_file.seek(int(contents["offset"]) + offset)
                    json_data = json.loads(asar_file.read(contents["size"]))
                    version = json_data["version"]
                    if version in self.versions:
                        self.print("⚙️", f"Found Sejda PDF Desktop version {version}")
                    else:
                        self.print("⚠️",
                                   f"Sejda PDF Desktop version {version} is not tested. Continue at your own risk")
                        input("Press Enter to continue")
                    return
        self.exit("Failed to find package.json in ASAR header")

    def check_process(self):
        try:
            result = subprocess.run(self.cmd, capture_output=True, text=True)
            if result.stdout != "":
                self.exit("Sejda PDF Desktop is running. Please close it first")
        except Exception as e:
            self.exit(f"Failed to check running process: {e}")

    def patch_files(self):
        try:
            with open(self.prefs, "r") as f:
                data = json.load(f)
            data["licenseExpires"] = 9999999999999
            data[
                "licenseToken"] = "nx/yFCVXn/g0++Hf5S7iaPmM/H2u0kJ14CtbxlI5m76MNQ0wcyNyvYadZJBf0UBlM23dk65MfYHH+sbBD2M2zgBGkhQd9gKMtrRzmZ6+2mQ="
            data["licenseKey"] = "cracked by gookie"
            data["startPage"] = ""
            with open(self.prefs, "w") as f:
                json.dump(data, f)
        except Exception as e:
            self.exit(f"Failed to patch {self.prefs}\n{e}")
        self.print("🩹", "Patched preferences")

        try:
            with open(self.asar, "rb") as f:
                data = f.read()
            endpoint = "/" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
            data = data.replace(b"/licenses/verify", endpoint.encode())
            with open(self.asar, 'wb') as f:
                f.write(data)
        except Exception as e:
            self.exit(f"Failed to patch {self.asar}\n{e}")
        self.print("🩹", "Patched ASAR")

    def exit(self, msg: str):
        self.print("❌", msg)
        exit(1)

    def print(self, emoji: str, msg: str):
        if self.emoji is None:
            try:
                print(f"{emoji} {msg}")
                self.emoji = True
            except UnicodeEncodeError:
                print(msg)
                self.emoji = False
        elif self.emoji:
            print(f"{emoji} {msg}")
        else:
            print(msg)


if __name__ == "__main__":
    SejdaCrack()