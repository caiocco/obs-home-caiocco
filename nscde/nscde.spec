#
# spec file for package nscde
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# The last upstream release (2.3) dates from 2023; this is a snapshot of
# the master branch, which configure.ac already calls 2.4.
#
# NsCDE runs on top of FVWM 2 (>= 2.6.7) or FVWM 3 and picks whichever is
# in $PATH at session start.  Leap 16.0 ships fvwm2 2.7.0, which is what
# this package requires.
#

%define nscde_commit 2d26bbece7e9c0dbee31bfe23ebfc1e1c88792bd
%define nscde_short  2d26bbe
%define nscde_date   20261013

Name:           nscde
Version:        2.3+git%{nscde_date}.%{nscde_short}
Release:        0
Summary:        Not so Common Desktop Environment, a CDE look-alike built on FVWM
License:        GPL-3.0-only
Group:          System/GUI/Other
URL:            https://github.com/NsCDE/NsCDE
Source0:        https://github.com/NsCDE/NsCDE/archive/%{nscde_commit}.tar.gz#/NsCDE-%{nscde_commit}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  gettext-tools
BuildRequires:  ksh
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xpm)
Requires:       ImageMagick
Requires:       cpp
Requires:       fvwm
Requires:       gettext-runtime
Requires:       ksh
Requires:       python3
Requires:       python3-PyYAML
Requires:       python3-psutil
Requires:       python3-pyxdg
Requires:       python3-qt5
Requires:       sed
Requires:       xdg-utils
Requires:       xdotool
Requires:       xdpyinfo
Requires:       xprop
Requires:       xrandr
Requires:       xrdb
Requires:       xset
Requires:       xterm
Recommends:     dejavu-fonts
Recommends:     dex
Recommends:     dunst
Recommends:     groff-full
Recommends:     libqt5-qtstyleplugins-platformtheme-gtk2
Recommends:     qt5ct
Recommends:     stalonetray
Recommends:     xclip
Recommends:     xscreensaver
Recommends:     xsettingsd
Suggests:       gkrellm
Suggests:       picom
Suggests:       qt6ct
Suggests:       rofi
Provides:       NsCDE = %{version}

%description
NsCDE is a retro but powerful UNIX desktop environment which resembles
the CDE look (and partially feel), with a more powerful and flexible
framework beneath the surface, more suited to 21st century unix-like
and Linux systems than the original CDE.

It is a heavyweight FVWM configuration combined with FvwmScript
applications, Korn shell and Python helpers, a front panel, workspace
manager, style managers, and GTK 2/3 and Qt 5/6 theme integration.

%prep
%autosetup -n NsCDE-%{nscde_commit}
# use absolute interpreters
sed -i '1s|^#!/bin/ksh|#!%{_bindir}/ksh|' doc/examples/fvwm3-per-monitor/nitrowrapper

%build
autoreconf -fiv
%configure \
  --libexecdir=%{_libexecdir} \
  --docdir=%{_docdir}/%{name} \
  --with-python-shebang=%{_bindir}/python3
%make_build

%install
%make_install
# Python modules imported by the tools, not scripts
chmod 0644 %{buildroot}%{_libdir}/NsCDE/python/SpritesGtk2.py
# already shipped as %%license
rm %{buildroot}%{_docdir}/%{name}/LICENSE
%find_lang %{name} --all-name
%fdupes %{buildroot}%{_datadir}

%files -f %{name}.lang
%license COPYING
%doc %{_docdir}/%{name}
%{_bindir}/nscde
%{_bindir}/nscde_fvwmclnt
%{_libdir}/NsCDE/
%{_libexecdir}/NsCDE/
%{_datadir}/NsCDE/
%{_datadir}/applications/nscde-*.desktop
%dir %{_datadir}/desktop-directories
%{_datadir}/desktop-directories/nscde-*.directory
%{_datadir}/icons/NsCDE/
%{_datadir}/xsessions/nscde.desktop
%dir %{_sysconfdir}/xdg/menus
%config %{_sysconfdir}/xdg/menus/nscde-applications.menu

%changelog
