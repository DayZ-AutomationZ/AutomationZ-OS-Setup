#!/usr/bin/env bash
set -euo pipefail

# === CONFIG (edit these) ===
AUTOMATIONZ_GIT_URL="${AUTOMATIONZ_GIT_URL:-https://github.com/DayZ-AutomationZ/AutomationZ.git}"
AUTOMATIONZ_BRANCH="${AUTOMATIONZ_BRANCH:-main}"
INSTALL_DIR="${INSTALL_DIR:-/opt/automationz}"
# ===========================

if [[ $EUID -ne 0 ]]; then
  echo "Please run as root: sudo ./install.sh"
  exit 1
fi

echo "[1/8] Enabling RPM Fusion (needed for Steam on Fedora)..."
dnf -y install \
  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

echo "[2/8] Updating system metadata..."
dnf -y update --refresh

echo "[3/8] Installing base apps + tooling..."
dnf -y install \
  git curl wget unzip tar \
  python3 python3-pip python3-tkinter \
  filezilla \
  firefox \
  p7zip p7zip-plugins \
  htop nano \
  openssl \
  inotify-tools \
  steam \
  gamemode mangohud \
  jq

echo "[4/8] Installing VSCodium (VS Code alternative)..."
rpm --import https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg
cat >/etc/yum.repos.d/vscodium.repo <<'EOF'
[gitlab.com_paulcarroty_vscodium_repo]
name=download.vscodium.com
baseurl=https://download.vscodium.com/rpms/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg
metadata_expire=1h
EOF
dnf -y install codium || true

echo "[5/8] Installing AutomationZ into ${INSTALL_DIR}..."
mkdir -p "$(dirname "$INSTALL_DIR")"
if [[ -d "$INSTALL_DIR/.git" ]]; then
  echo " - Existing repo detected, pulling latest..."
  git -C "$INSTALL_DIR" fetch --all
  git -C "$INSTALL_DIR" checkout "$AUTOMATIONZ_BRANCH"
  git -C "$INSTALL_DIR" pull --ff-only
else
  rm -rf "$INSTALL_DIR"
  git clone --branch "$AUTOMATIONZ_BRANCH" "$AUTOMATIONZ_GIT_URL" "$INSTALL_DIR"
fi

echo "[6/8] Installing AutomationZ Hub launcher..."
install -d /opt/automationz-os/hub
install -m 0755 ./hub/automationz-hub.py /opt/automationz-os/hub/automationz-hub.py

install -d /usr/share/applications
install -m 0644 ./desktop/automationz-hub.desktop /usr/share/applications/automationz-hub.desktop

echo "[7/8] Installing auto-updater service + timer..."
install -d /opt/automationz-os/updater
install -m 0755 ./updater/automationz-update.sh /opt/automationz-os/updater/automationz-update.sh

install -d /etc/systemd/system
install -m 0644 ./systemd/automationz-updater.service /etc/systemd/system/automationz-updater.service
install -m 0644 ./systemd/automationz-updater.timer /etc/systemd/system/automationz-updater.timer

systemctl daemon-reload
systemctl enable --now automationz-updater.timer

echo "[8/8] Done."
echo "AutomationZ Hub is now in your KDE menu: Applications -> AutomationZ"
echo "Auto-updater timer enabled: systemctl status automationz-updater.timer"
