#!/bin/bash

read -p "What Arch To Use Like arm64 or x86_64: " arch
read -p "What Distro Base To Use: " distro
read -p "File Path To DTB (Optional): " dtb
read -p "File Path To Kernel (Optional): " kernel
read -p "Type PC or PHONE: " type

echo "Starting Build For Rootfs..."
sleep 2
python3 base-rootfs-builder.py --scripts-dir="Scripts" --outdir="out" --rootfs-dir="Rootfs" --arch=$arch --distro=$distro # Start Builder

mkdir -p Rootfs/boot/

if [ -n "$dtb" ]; then
    cp "$dtb" Rootfs/boot/
fi

if [ -n "$kernel" ]; then
    cp "$kernel" Rootfs/boot/
fi

mkdir -p "out/$arch"

# Repack rootfs
tar -cJf "out/$arch/$distro-$arch.tar.xz" -C Rootfs .

if [ "$type" = "PHONE" ]; then
    # Get Rootfs size in MB and add 512 MB free space
    rootfs_size=$(du -sm Rootfs | cut -f1)
    image_size=$((rootfs_size + 512))

    echo "Creating ${image_size}MB rootfs image..."

    truncate -s "${image_size}M" "out/$arch/$distro-$arch.img"
    mkfs.ext4 -F "out/$arch/$distro-$arch.img"

    mkdir -p /tmp/rootfs-mount
    sudo mount -o loop "out/$arch/$distro-$arch.img" /tmp/rootfs-mount
    sudo cp -a Rootfs/. /tmp/rootfs-mount/
    sudo umount /tmp/rootfs-mount
    rmdir /tmp/rootfs-mount

elif [ "$type" = "PC" ]; then
    echo "PC build: skipping rootfs image."

else
    echo "Unknown type: $type"
    exit 1
fi

rm -rf Rootfs

echo "=============================================="
echo "Built Rootfs: $distro-$arch"
echo "=============================================="
echo "Distro: $distro"
echo "Architecture: $arch"
echo "Type: $type"
echo "DTB: ${dtb:-None}"
echo "Kernel: ${kernel:-None}"
echo "=============================================="
