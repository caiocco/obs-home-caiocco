#
# spec file for package dosbox-x
#
# Copyright (c) 2023 Javier S. Pedro <dev.rpm@javispedro.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Based on the dosbox-x spec by Javier S. Pedro (home:javispedro:portpkgs).
#

Name:           dosbox-x
Version:        2026.10.01
Release:        0
Summary:        DOS emulator derived from DOSBox
License:        GPL-2.0-or-later
URL:            https://dosbox-x.com/
Source0:        https://github.com/joncampbell123/dosbox-x/archive/refs/tags/%{name}-v%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  libpcap-devel
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(SDL2_net)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(slirp)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
Recommends:     fluid-soundfont-gm
# file dialogs (tinyfiledialogs) need zenity, kdialog or similar
Recommends:     zenity

%description
DOSBox-X is a DOS emulator derived from DOSBox, designed to support
many kinds of DOS software and systems, including serious DOS
applications (printing, SHARE) and East Asian systems (DOS/V, PC-98).

It focuses on accurate emulation of hardware behavior, offers many
ways to configure the DOS virtual machine, and aims to be a good
platform for DOS-based Windows (3.x, 9x/Me) and for developing new
DOS software.

%prep
%autosetup -p1 -n %{name}-%{name}-v%{version}
sed -i 's/\r$//' CHANGELOG
autoreconf -fi

%build
%configure --enable-sdl2 --enable-debug
%make_build

%install
%make_install

%files
%license COPYING
%doc CHANGELOG README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/com.dosbox_x.DOSBox-X.desktop
%{_datadir}/icons/hicolor/scalable/apps/dosbox-x.svg
%{_datadir}/metainfo/com.dosbox_x.DOSBox-X.metainfo.xml
%{_mandir}/man1/dosbox-x.1%{?ext_man}
%{_datadir}/bash-completion/completions/dosbox-x

%changelog
