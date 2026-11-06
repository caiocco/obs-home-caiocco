#
# spec file for package fvwm-crystal
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# The last upstream tag (3.7.6) is old; this is a snapshot of the master
# branch, which the About dialog reports as 3.7.7-git.
#
# Upstream's makesudoers.sh is not used: it grants the fvwm-crystal group
# password-less sudo for mount, umount, systemctl and loginctl with any
# arguments.  A restricted sudoers file (Source2) is shipped instead.
#

%define fc_commit   0ac6f2121c14489c154312b0033fd654ca3af5e3
%define fc_short    0ac6f21
%define fc_date     20260923

Name:           fvwm-crystal
Version:        3.7.6+git%{fc_date}.%{fc_short}
Release:        0
Summary:        Transparent, eye-candy desktop environment based on FVWM
License:        GPL-3.0-or-later
Group:          System/GUI/Other
URL:            https://github.com/fvwm-crystal/fvwm-crystal
Source0:        https://github.com/fvwm-crystal/fvwm-crystal/archive/%{fc_commit}.tar.gz#/%{name}-%{fc_commit}.tar.gz
Source1:        %{name}.sysusers
Source2:        %{name}.sudoers
# PATCH-FIX-UPSTREAM fix shell syntax error in the Trailblazer launcher
Patch0:         %{name}-trailblazer-quote.patch
BuildRequires:  fdupes
BuildRequires:  make
BuildRequires:  sudo
BuildRequires:  sysuser-tools
Requires:       bash
Requires:       fvwm
Requires:       nano
Requires:       python3
Recommends:     ImageMagick
Recommends:     bc
Recommends:     hsetroot
Recommends:     sudo
Recommends:     xdg-user-dirs
Recommends:     xterm
Suggests:       feh
Suggests:       mpc
Suggests:       mpd
Suggests:       python3-python-mpd2
Suggests:       rxvt-unicode
Suggests:       stalonetray
Suggests:       wget
Suggests:       xscreensaver
BuildArch:      noarch
%sysusers_requires

%description
FVWM-Crystal is a desktop environment built on top of the FVWM window
manager.  It provides transparent, themable panels and menus ("recipes"
and colorsets), a desktop menu generated from an application database,
virtual desktops, music player integration (MPD, mplayer, cmus, mocp,
XMMS2, ...), wallpaper management and a preferences editor.

It works with FVWM 2.6.9 or later, including FVWM3.

To use the reboot / shut down / suspend entries of the Exit menu, a user
must be a member of the fvwm-crystal group:

  usermod -a -G fvwm-crystal <user>

A system tray (stalonetray or trayer) is needed for the tray icons.

%prep
%autosetup -p1 -n %{name}-%{fc_commit}
# use absolute interpreters instead of /usr/bin/env
grep -rlZ '^#!/usr/bin/env ' bin fvwm addons | xargs -0 sed -i \
  -e '1s|^#!/usr/bin/env bash|#!/bin/bash|' \
  -e '1s|^#!/usr/bin/env python3|#!/usr/bin/python3|' \
  -e '1s|^#!/usr/bin/env sh|#!/bin/sh|'

%build
%sysusers_generate_pre %{SOURCE1} %{name} %{name}.conf

%install
%make_install \
  prefix=%{_prefix} \
  mandir=%{_mandir} \
  docdir=%{_docdir}/%{name} \
  nano=%{_bindir}/nano

# Gentoo-only session directory
rm -rf %{buildroot}%{_sysconfdir}/X11/Sessions
# restricted sudoers instead of the generated one
install -Dm0440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/%{name}
install -Dm0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
# upstream installs the addon scripts without the executable bit
for f in %{buildroot}%{_datadir}/%{name}/addons/*; do
  head -c2 "$f" | grep -q '^#!' && chmod 0755 "$f"
done
# license is shipped via %%license
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE

%fdupes -s %{buildroot}%{_datadir}

%pre -f %{name}.pre

%files
%license LICENSE
%doc %{_docdir}/%{name}
%{_bindir}/fvwm-crystal
%{_bindir}/fvwm-crystal.*
%{_datadir}/%{name}
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man1/*.1%{?ext_man}
%{_sysusersdir}/%{name}.conf
%config(noreplace) %attr(0440,root,root) %{_sysconfdir}/sudoers.d/%{name}

%changelog
