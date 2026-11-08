#
# spec file for package lmms
#
# Copyright (c) 2025 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
# Based on openSUSE:Factory/lmms, updated to the upstream 1.3.0-alpha.2 tag.
# The tarball is made by "osc service manualrun" (tar_scm with submodules),
# because GitHub's archive lacks the bundled plugins (ZynAddSubFx, CALF, Carla
# headers, ...).
#
# Carla: Leap 16.0 has no carla package, so LMMS builds its "weak Carla"
# dummy library; the Carla Rack/Patchbay plugins work at run time if a
# carla package is installed later.
# VST: Leap 16.0 has no 32-bit userland, so only the 64-bit Wine VST host is
# built (with_wine); 32-bit Windows VSTs are not supported.
#

%bcond_without  wine
Name:           lmms
Version:        1.3.0~alpha.2
Release:        0
Summary:        Linux MultiMedia Studio
License:        GPL-2.0-or-later
Group:          Productivity/Multimedia/Sound/Midi
URL:            https://lmms.io/
Source0:        %{name}-%{version}.tar.xz
Source1:        _service
%if %{with wine}
Source3:        lmms-warning
%endif
# PATCH-FIX-UPSTREAM Fix plugin library search path, testing an upstream proposal
Patch2:         lmms-1.2.0-libdir.patch
BuildRequires:  cmake >= 3.13
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  fltk-devel
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  libQt5Core-private-headers-devel
BuildRequires:  libQt5Gui-private-headers-devel
BuildRequires:  libQt5Widgets-private-headers-devel
BuildRequires:  libstk-devel
BuildRequires:  perl
BuildRequires:  perl-List-MoreUtils
BuildRequires:  perl-XML-Parser
BuildRequires:  pkgconfig
BuildRequires:  sndio-devel
BuildRequires:  cmake(Qt5Core) >= 5.15
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5Test)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  cmake(Qt5Xml)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fftw3f) >= 3.0.0
BuildRequires:  pkgconfig(fluidsynth) >= 1.1.7
BuildRequires:  pkgconfig(gig)
BuildRequires:  pkgconfig(jack) >= 0.77
BuildRequires:  pkgconfig(libmp3lame)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(lilv-0)
BuildRequires:  pkgconfig(lv2)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(samplerate) >= 0.1.8
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(shared-mime-info)
BuildRequires:  pkgconfig(sndfile) >= 1.0.11
BuildRequires:  pkgconfig(suil-0)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vorbisenc)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(zlib)
%if %{with wine}
BuildRequires:  wine
BuildRequires:  wine-devel
%endif
Recommends:     carla

%description
LMMS is a free cross-platform music studio which allows you to produce music
with your computer. This includes the creation of melodies and beats, the
synthesis and mixing of sounds, and arranging of samples.
%if %{with wine}
You need to install lmms-vst for VST plugins
%endif

%if %{with wine}
%package vst
Summary:        Wine dependent VST plugins
Group:          Productivity/Multimedia/Sound/Midi
Requires:       %{name} = %{version}
Requires:       wine

%description vst
LMMS is a free cross-platform music studio which allows you to produce music
with your computer. This includes the creation of melodies and beats, the
synthesis and mixing of sounds, and arranging of samples.
This package contains the wine dependent (64-bit) VST plugins
%endif

%package devel
Summary:        Headers to create LMMS plugins
Group:          Development/Libraries/C and C++

%description devel
Headers that provide access to the LMMS features. Install it if you plan to
create a LMMS plugin.

%prep
%autosetup -p1
# All submodules are in the tarball (doc/wiki excluded); without
# .gitmodules CMake skips its git-based submodule check/clone.
rm .gitmodules

%build
export CFLAGS="%{optflags} -fPIC -fno-omit-frame-pointer"
export CXXFLAGS="%{optflags} -fPIC -fno-omit-frame-pointer"
%cmake \
  -DWANT_QT6:BOOL=OFF \
  -DWANT_CARLA:BOOL=ON \
  -DWANT_VST_32:BOOL=OFF \
%if %{with wine}
  -DWANT_VST_64:BOOL=ON \
%else
  -DWANT_VST:BOOL=OFF \
%endif
  -DCMAKE_SHARED_LINKER_FLAGS="" \
  -DCMAKE_EXE_LINKER_FLAGS:STRING="$LDFLAGS -pie" \
  -Wno-dev
%cmake_build

%install
%cmake_install

# remove unneeded static helper library from install
rm -f %{buildroot}%{_libdir}/libqx11embedcontainer.a

if [ ! -e %{buildroot}%{_datadir}/bash-completion/completions/lmms ]; then
  install -Dm0644 doc/bash-completion/lmms %{buildroot}%{_datadir}/bash-completion/completions/lmms
fi

%fdupes -s %{buildroot}%{_datadir}

%if %{with wine}
install -Dm0644 %{SOURCE3} %{buildroot}%{_localstatedir}/adm/update-messages/%{name}-warning
%endif

%files
%doc doc/AUTHORS README.md
%license LICENSE.txt
%{_bindir}/lmms
%{_mandir}/man1/lmms.1%{?ext_man}
%{_libdir}/lmms/
%{_datadir}/lmms/
%{_datadir}/applications/lmms.desktop
%{_datadir}/icons/hicolor/*
%{_datadir}/mime/packages/lmms.xml
%{_datadir}/bash-completion/completions/lmms
%if %{with wine}
%exclude %{_libdir}/lmms/RemoteVstPlugin*
%exclude %{_libdir}/lmms/libvsteffect.so
%endif

%if %{with wine}
%files vst
%{_localstatedir}/adm/update-messages/%{name}-warning
%{_libdir}/lmms/RemoteVstPlugin*
%{_libdir}/lmms/libvsteffect.so
%endif

%files devel
%{_includedir}/lmms/

%changelog
