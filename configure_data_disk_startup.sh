#!/usr/bin/env bash
set -euo pipefail

DEVICE="/dev/disk/by-id/google-data"
MOUNT_POINT="/workspace/data"

if [[ ! -e "$DEVICE" ]]; then
  exit 0
fi

if ! blkid "$DEVICE" >/dev/null 2>&1; then
  mkfs.ext4 -F "$DEVICE"
fi

mkdir -p "$MOUNT_POINT"
if ! mountpoint -q "$MOUNT_POINT"; then
  mount "$DEVICE" "$MOUNT_POINT"
fi

UUID="$(blkid -s UUID -o value "$DEVICE")"
if ! grep -q "$UUID" /etc/fstab; then
  echo "UUID=$UUID $MOUNT_POINT ext4 defaults,nofail 0 2" >> /etc/fstab
fi

chown -R "${SUDO_USER:-${USER}}:${SUDO_USER:-${USER}}" "$MOUNT_POINT" || true
