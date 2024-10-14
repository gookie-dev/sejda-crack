import os
import sys
import json
import string
import struct
import random
import subprocess

VERSION = "1.3"


class SejdaCrack:
    def __init__(self):
        self.platform = sys.platform
        self.emoji = None
        self.asar = None
        self.prefs = None
        self.versions = ["7.7.0", "7.7.2", "7.7.4"]
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
            data["licenseToken"] = b"\x6e\x78\x2f\x79\x46\x43\x56\x58\x6e\x2f\x67\x30\x2b\x2b\x48\x66\x35\x53\x37\x69\x61\x50\x6d\x4d\x2f\x48\x32\x75\x30\x6b\x4a\x31\x34\x43\x74\x62\x78\x6c\x49\x35\x6d\x37\x36\x4d\x4e\x51\x30\x77\x63\x79\x4e\x79\x76\x59\x61\x64\x5a\x4a\x42\x66\x30\x55\x42\x6c\x4d\x32\x33\x64\x6b\x36\x35\x4d\x66\x59\x48\x48\x2b\x73\x62\x42\x44\x32\x4d\x32\x7a\x67\x42\x47\x6b\x68\x51\x64\x39\x67\x4b\x4d\x74\x72\x52\x7a\x6d\x5a\x36\x2b\x32\x6d\x51\x3d".decode('utf-8')
            data["licenseKey"] = b"\x41\x45\x5a\x54\x34\x33\x4e\x38\x2d\x39\x37\x4c\x5a\x2d\x52\x36\x37\x59\x2d\x34\x34\x4c\x45\x2d\x30\x42\x42\x30\x52\x53\x42\x4b\x35\x4f\x44\x52".decode('utf-8')
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
            data = data.replace(b"\x2f\x6c\x69\x63\x65\x6e\x73\x65\x73\x2f\x76\x65\x72\x69\x66\x79", endpoint.encode())
            data = data.replace(b"\x22\x50\x52\x4f\x20\x61\x63\x74\x69\x76\x65\x20\xe2\x80\x94\x20\x22\x2b\x6c", b"\x22\x63\x72\x61\x63\x6b\x65\x64\x20\x62\x79\x20\x67\x6f\x6f\x6b\x69\x65\x22")
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