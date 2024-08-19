import os
import sys
import json
import string
import struct
import random
import subprocess

VERSION = "1.1"


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
        self.print("🔥", f"Sejda PDF Desktop crack v{VERSION} by gookie")

        if self.platform == "linux":
            self.asar = "/opt/sejda-desktop/resources/app.asar"
            self.prefs = os.path.join(self.home_dir(), ".sejda")
            self.cmd = ["pgrep", "-x", "sejda-desktop"]
            self.print("🐧", "Linux detected")
        elif self.platform == "win32":
            self.asar = r"C:\Program Files\Sejda PDF Desktop\resources\app.asar"
            self.prefs = os.path.join(os.getenv("APPDATA"), "sejda-desktop", "prefs.json")
            self.cmd = ["powershell", "-Command", "Get-Process | Where-Object {$_.ProcessName -eq \"Sejda PDF Desktop\"}"]
            self.print("🪟", "Windows detected")
        elif self.platform == "darwin":
            self.asar = "/Applications/Sejda PDF Desktop.app/Contents/Resources/app.asar"
            self.prefs = os.path.join(self.home_dir(), ".sejda")
            self.cmd = ["pgrep", "-x", "\"Sejda PDF Desktop\""]
            self.print("🍎", "MacOS detected")
        else:
            self.exit(f"Unsupported platform: {self.platform}")

        self.asar = self.check_file(self.asar, "Sejda PDF Desktop ASAR")
        self.prefs = self.check_file(self.prefs, "Sejda PDF Desktop preferences")
        self.check_version()
        self.check_process()
        self.patch_files()
        self.print("🎉", "Cracked successful")
        self.print("⭐", "Would appreciate a star https://github.com/gookie-dev/sejda-crack")

    @staticmethod
    def home_dir():
        sudo_user = os.getenv("SUDO_USER")
        if sudo_user:
            return os.path.expanduser(f'~{sudo_user}')
        else:
            return os.getenv("HOME")

    def check_file(self, file: str, name: str) -> str:
        if not os.path.exists(file):
            self.print("❌", f"{name} not found in default location: {file}")
            file = input(f"Enter path to {name}: ").strip('"')
            self.check_file(file, name)
        self.print("📦", f"Found {name}")

        try:
            with open(file, "a"):
                pass
        except PermissionError:
            self.exit(f"{file} no read/write permissions.\nTry to run this script as administrator / root or change file permissions")

        return file

    def check_version(self):
        asar_file = open(self.asar, 'rb')
        asar_file.seek(4)
        header_size = struct.unpack('I', asar_file.read(4))
        if len(header_size) <= 0:
            self.exit("Failed to read ASAR header size")
        header_size = header_size[0] - 8
        asar_file.seek(asar_file.tell() + 8)
        header = asar_file.read(header_size).decode('utf-8')
        files = json.loads(header.replace("\x00", ""))
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
                        self.print("⚠️", f"Sejda PDF Desktop version {version} is not tested. Continue at your own risk")
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
            data["licenseToken"] = "nx/yFCVXn/g0++Hf5S7iaPmM/H2u0kJ14CtbxlI5m76MNQ0wcyNyvYadZJBf0UBlM23dk65MfYHH+sbBD2M2zgBGkhQd9gKMtrRzmZ6+2mQ="
            data["licenseKey"] = "AEZT43N8-97LZ-R67Y-44LE-0BB0RSBK5ODR"
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
            data = data.replace(bytes.fromhex("2250524F2061637469766520E2809420222B6C"), bytes.fromhex("22637261636B656420627920676F6F6B696522"))
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