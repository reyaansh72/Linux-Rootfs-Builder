# Linux Rootfs Builder

An extendable Linux rootfs builder for **PCs and Android devices with existing mainline Linux support**.

Currently supports **Debian** and **Kali Linux**.

> This project does **not** port Linux kernels or add mainline support to devices. It is designed for devices and systems that already have a working Linux/mainline kernel.

## Features

* 🐧 Debian rootfs support
* 🐉 Kali Linux rootfs support
* 🖥️ PC rootfs builds
* 📱 Android-phone rootfs/image builds
* 🌳 Optional DTB support
* 🐧 Optional kernel support
* 🛠️ U-Boot support
* 📦 `.tar.xz` rootfs output
* 💾 `.img` output for phone builds
* 📊 Download progress bar with percentage, speed, and ETA
* 🧩 Extendable distro/rootfs backend

---

# How It Works

The project is split into two main components:

```text
builder.sh
    │
    ├── Gets build options
    ├── Runs base-rootfs-builder.py
    ├── Adds optional DTB
    ├── Adds optional Kernel
    ├── Creates the rootfs archive
    └── Creates the phone image
             │
             ▼
base-rootfs-builder.py
    │
    ├── Downloads rootfs
    ├── Extracts rootfs
    ├── Performs rootfs setup
    └── Cleans downloaded files
```

### `builder.sh`

`builder.sh` is the main build script.

It handles:

* Architecture selection
* Distribution selection
* DTB selection
* Kernel selection
* PC/PHONE selection
* Adding boot files
* Repacking the rootfs
* Creating the `.img` for phone builds

### `base-rootfs-builder.py`

`base-rootfs-builder.py` handles the actual distro rootfs preparation.

It handles:

* Downloading the selected rootfs
* Showing download progress
* Extracting the rootfs
* Rootfs setup
* Cleaning up downloaded files

Keeping these components separate makes it easier to add support for more distributions.

---

# Requirements

You need:

* Linux
* Bash
* Python 3
* `tar`
* `xz`
* `mkfs.ext4`
* `sudo`

For example, on Debian/Ubuntu:

```bash
sudo apt install python3 tar xz-utils e2fsprogs
```

---

# Running the Builder

Run:

```bash
bash builder.sh
```

The builder will ask:

```text
What Arch To Use Like arm64 or x86_64:
What Distro Base To Use:
File Path To DTB (Optional):
File Path To Kernel (Optional):
Type PC or PHONE:
```

Example:

```text
What Arch To Use Like arm64 or x86_64: arm64
What Distro Base To Use: kali
File Path To DTB (Optional): /home/user/device.dtb
File Path To Kernel (Optional):
Type PC or PHONE: PHONE
```

---

# DTB and Kernel

The builder supports optional **DTB** and **Kernel** files.

Which files you need depends on the boot setup of the existing Linux port.

## Standard Mainline Android Kernel Port

For a standard mainline Linux kernel port on an Android device, **use the DTB in most cases**.

Example:

```text
File Path To DTB (Optional): /home/user/device.dtb
File Path To Kernel (Optional):
```

The DTB will be copied into:

```text
Rootfs/boot/
```

Result:

```text
Rootfs/
└── boot/
    └── device.dtb
```

The kernel can normally be left empty because the kernel is already supplied by the Android boot partition.

### Optional Kernel

Some setups may also require the kernel inside the rootfs.

In that case:

```text
File Path To DTB (Optional): /home/user/device.dtb
File Path To Kernel (Optional): /home/user/Image
```

Result:

```text
Rootfs/
└── boot/
    ├── device.dtb
    └── Image
```

---

# U-Boot

For **U-Boot**, in most cases you should provide **both the DTB and Kernel**.

Example:

```text
File Path To DTB (Optional): /home/user/device.dtb
File Path To Kernel (Optional): /home/user/Image
```

The builder will place them in:

```text
Rootfs/boot/
```

Result:

```text
Rootfs/
└── boot/
    ├── device.dtb
    └── Image
```

## Quick Guide

| Boot setup                      | DTB              | Kernel           |
| ------------------------------- | ---------------- | ---------------- |
| Standard Android mainline port  | Usually required | Optional         |
| U-Boot                          | Usually required | Usually required |
| Setup that does not require DTB | Optional         | Optional         |

The builder **does not generate the DTB or kernel**.

You must provide working files from an existing Linux/mainline port when the target setup requires them.

---

# PC Builds

For a PC build, select:

```text
Type PC or PHONE: PC
```

The builder creates a `.tar.xz` rootfs archive.

Example:

```text
out/
└── x86_64/
    └── debian-x86_64.tar.xz
```

For ARM64:

```text
out/
└── arm64/
    └── debian-arm64.tar.xz
```

No `.img` is created for PC builds.

---

# Phone Builds

For a phone build, select:

```text
Type PC or PHONE: PHONE
```

The builder creates both:

```text
out/
└── arm64/
    ├── debian-arm64.tar.xz
    └── debian-arm64.img
```

The `.img` is an ext4 filesystem image.

Its size is calculated from the extracted rootfs and additional free space is added.

For example:

```text
Rootfs size: 447 MB
Image size: 959 MB
```

This leaves space for additional files and changes after installation.

---

# Example: Standard Mainline Phone

Suppose you have a phone with an already-working mainline kernel and its DTB is:

```text
/home/user/kernel/device.dtb
```

Run:

```text
What Arch To Use Like arm64 or x86_64: arm64
What Distro Base To Use: debian
File Path To DTB (Optional): /home/user/kernel/device.dtb
File Path To Kernel (Optional):
Type PC or PHONE: PHONE
```

The builder will:

1. Download the Debian ARM64 rootfs.
2. Extract it.
3. Set up the rootfs.
4. Add the DTB to `/boot/`.
5. Repack the rootfs.
6. Create the phone `.img`.

---

# Example: U-Boot Device

For a U-Boot setup where you have:

```text
/home/user/kernel/Image
/home/user/kernel/device.dtb
```

Use:

```text
What Arch To Use Like arm64 or x86_64: arm64
What Distro Base To Use: kali
File Path To DTB (Optional): /home/user/kernel/device.dtb
File Path To Kernel (Optional): /home/user/kernel/Image
Type PC or PHONE: PHONE
```

The resulting `/boot/` will contain:

```text
boot/
├── Image
└── device.dtb
```

---

# Supported Distributions

Currently:

| Distribution | PC | Phone |
| ------------ | -: | ----: |
| Debian       |  ✅ |     ✅ |
| Kali Linux   |  ✅ |     ✅ |

The project is designed so more distributions can be added later.

---

# Extending the Builder

The distro/rootfs logic is contained in:

```text
base-rootfs-builder.py
```

This means additional distributions can be added without having to completely redesign `builder.sh`.

The general workflow is:

```text
Select distro
      ↓
base-rootfs-builder.py
      ↓
Download distro rootfs
      ↓
Extract
      ↓
Rootfs setup
      ↓
Return to builder.sh
      ↓
Add DTB / Kernel
      ↓
Repack
```

---

# Output

Builds are stored under:

```text
out/<architecture>/
```

For PC:

```text
out/
└── arm64/
    └── debian-arm64.tar.xz
```

For PHONE:

```text
out/
└── arm64/
    ├── debian-arm64.tar.xz
    └── debian-arm64.img
```

---

# Project Scope

Linux Rootfs Builder is intended for:

* Normal Linux rootfs builds
* PC Linux rootfs packages
* Android-phone Linux rootfs builds
* Devices with existing mainline Linux support
* U-Boot-based Linux setups
* Reusing the same distro userspace with different device DTBs

It is **not** intended to:

* Port a Linux kernel to a device
* Generate a kernel
* Generate a DTB
* Add hardware support to a kernel
* Unlock Android bootloaders
* Replace the device's bootloader

The target device should already have the necessary working Linux/mainline support.

---
