import sys
import os
import time
import urllib.request
import tarfile

def arg_reader(name):
    for arg in sys.argv:
        if arg.startswith(name + "="):
            return arg.split("=", 1)[1].strip('"')
    return None

def extract_tar_xz(filename, path):
    os.makedirs(path, exist_ok=True)

    with tarfile.open(filename, "r:xz") as tar:
        tar.extractall(path, filter="fully_trusted")
    
    print("Extracted Rootfs")
    return path

def download(url):
    filename = url.split("/")[-1].split("?")[0] or "download"

    req = urllib.request.urlopen(url)
    total = req.headers.get("Content-Length")
    total = int(total) if total else None

    downloaded = 0
    start = time.time()

    with open(filename, "wb") as f:
        while True:
            chunk = req.read(1024 * 64)

            if not chunk:
                break

            f.write(chunk)
            downloaded += len(chunk)

            elapsed = time.time() - start
            speed = downloaded / elapsed if elapsed > 0 else 0

            if total:
                percent = downloaded / total * 100
                bar_size = 30
                filled = int(bar_size * downloaded / total)
                bar = "█" * filled + "░" * (bar_size - filled)

                eta = (total - downloaded) / speed if speed > 0 else 0

                print(
                    f"\r[{bar}] {percent:6.2f}% "
                    f"{downloaded / 1024 / 1024:.2f} MB/"
                    f"{total / 1024 / 1024:.2f} MB "
                    f"{speed / 1024 / 1024:.2f} MB/s "
                    f"ETA {eta:.0f}s",
                    end="",
                    flush=True
                )
            else:
                print(
                    f"\rDownloaded: {downloaded / 1024 / 1024:.2f} MB "
                    f"@ {speed / 1024 / 1024:.2f} MB/s",
                    end="",
                    flush=True
                )

    print(f"\nDownloaded File: {filename}")
    return filename

scripts_dir = arg_reader(name="--scripts-dir")
out_dir = arg_reader(name="--outdir")
rootfs_dir = arg_reader(name="--rootfs-dir")
arch = arg_reader(name="--arch")
distro = arg_reader(name="--distro")

print(f"[INFO]: Output Dir -- {out_dir}")
print(f"[INFO]: Scripts Dir -- {scripts_dir}")
print(f"[INFO]: Rootfs Dir -- {rootfs_dir}")
print(f"[INFO]: Arch -- {arch}")
print(f"[INFO]: Distro -- {distro}")

print("================================")
print(f"Building {arch} Rootfs")
print("================================")

print(f"Downloading {distro} Rootfs...")

if arch == "arm64" and distro == "debian":
   rootfs = download("https://github.com/EXALAB/Anlinux-Resources/raw/refs/heads/master/Rootfs/Debian/arm64/debian-rootfs-arm64.tar.xz")
elif arch == "arm64" and distro == "kali":
     rootfs = download("https://github.com/EXALAB/Anlinux-Resources/raw/refs/heads/master/Rootfs/Kali/arm64/kali-rootfs-arm64.tar.xz")
elif arch == "x86_64" and distro == "debian":
     rootfs = download("https://github.com/EXALAB/Anlinux-Resources/raw/refs/heads/master/Rootfs/Debian/amd64/debian-rootfs-amd64.tar.xz")
elif arch == "x86_64" and distro == "kali":
     rootfs = download("https://github.com/EXALAB/Anlinux-Resources/raw/refs/heads/master/Rootfs/Kali/amd64/kali-rootfs-amd64.tar.xz")

print(f"Extracting Rootfs...")
extract_tar_xz(filename=rootfs, path="Rootfs")

print("Cleaning UP Downloaded Files...")
os.remove(rootfs) # Since The Rootfs Already Exists
print("Cleanup Complete")
time.sleep(2)
print("Built Base Rootfs!")
exit(1)
