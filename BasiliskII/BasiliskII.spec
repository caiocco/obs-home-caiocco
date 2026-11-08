#
# spec file for package BasiliskII
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Built from the kanjitalk755 fork of macemu, the maintained upstream
# (cebix/macemu has been dormant since 2021; Debian switched in 2023).
# The tarball is a "git archive" of the fork; SheepShaver uses the same one.
#

%define commit  f532be3d
%define gitdate 20261021
%define tarname macemu-%{gitdate}.%{commit}
# the 68k JIT does not like LTO
%define _lto_cflags %{nil}
Name:           BasiliskII
Version:        1.0+git%{gitdate}.%{commit}
Release:        0
Summary:        68k Macintosh emulator
License:        GPL-2.0-or-later
Group:          System/Emulators/Other
URL:            https://github.com/kanjitalk755/macemu
Source0:        %{tarname}.tar.xz
# Adapted from Debian (1001_use_system_tinyxml2.patch), extended to SheepShaver
Patch0:         macemu-system-tinyxml2.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  libvdeplug-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(tinyxml2)
BuildRequires:  pkgconfig(x11)
%ifnarch %{ix86} x86_64
BuildRequires:  mpfr-devel
%endif

%description
Basilisk II is an Open Source 68k Macintosh emulator. It runs 68k MacOS
software on your computer, but you still need a copy of MacOS and a
Macintosh ROM image to use it.

Some features of Basilisk II:
  - Emulates either a Mac Classic (MacOS 0.x thru 7.5) or a Mac II
    series machine (MacOS 7.x, 8.0 and 8.1), depending on the ROM used
  - Color video display and CD quality sound output (SDL2)
  - Floppy, HFS partition/hardfile and CD-ROM drivers (incl. BIN/CUE)
  - File exchange with the host through a "Host Directory Tree" icon
  - Ethernet (slirp, TUN/TAP, VDE) and serial drivers
  - GTK3 preferences editor
  - UAE 68k emulation with a JIT compiler on x86

%prep
%autosetup -p1 -n %{tarname}
# make sure the bundled tinyxml2 copy is not used
rm -f BasiliskII/src/Unix/tinyxml2.cpp BasiliskII/src/Unix/tinyxml2.h

%build
cd BasiliskII/src/Unix
NO_CONFIGURE=1 ./autogen.sh
%configure \
        --enable-sdl-video \
        --enable-sdl-audio \
        --with-gtk=gtk3 \
        --without-esd \
        --without-mon \
        --with-bincue \
        --with-vdeplug \
%ifarch %{ix86} x86_64
        --enable-jit-compiler
%else
        --disable-jit-compiler
%endif
%make_build

%install
cd BasiliskII/src/Unix
%make_install
chmod 0755 %{buildroot}%{_datadir}/BasiliskII/tunconfig

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.kanjitalk755.macemu.basilisk.desktop

%files
%license BasiliskII/COPYING
%doc BasiliskII/README BasiliskII/TECH BasiliskII/TODO README.md
%{_bindir}/BasiliskII
%{_mandir}/man1/BasiliskII.1%{?ext_man}
%{_datadir}/BasiliskII/
%{_datadir}/applications/io.github.kanjitalk755.macemu.basilisk.desktop
%{_datadir}/icons/hicolor/*/apps/io.github.kanjitalk755.macemu.basilisk.*
%{_datadir}/metainfo/io.github.kanjitalk755.macemu.basilisk.metainfo.xml

%changelog
