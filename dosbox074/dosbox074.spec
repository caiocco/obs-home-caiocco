#
# spec file for package dosbox074
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Classic DOSBox 0.74-3.  openSUSE's "dosbox" package is DOSBox Staging and
# owns /usr/bin/dosbox, so this one installs as dosbox74.  The program still
# reads ~/.dosbox/dosbox-0.74-3.conf, since the file name comes from VERSION.
# Patches come from nixpkgs (C++17 fix) and Debian (the rest).
#

Name:           dosbox074
Version:        0.74.3
Release:        0
Summary:        Classic DOSBox 0.74-3 x86/DOS emulator
License:        GPL-2.0-or-later
URL:            https://www.dosbox.com/
Source0:        https://downloads.sourceforge.net/project/dosbox/dosbox/0.74-3/dosbox-0.74-3.tar.gz
Source1:        dosbox74.desktop
# from dosbox-x commit 006d572 (as used by nixpkgs): C++17 removed "register"
Patch0:         dosbox074-cxx17-register.patch
# Debian: SDL 1.2 sends spurious focus/key-up events in fullscreen
Patch1:         dosbox074-sdl-focus-events.patch
# Debian: missing format strings (debugger)
Patch2:         dosbox074-format-strings.patch
# Debian: ncurses 6.5 made WINDOW opaque (debugger)
Patch3:         dosbox074-ncurses-getbegy.patch
# Debian: man page and message spelling fixes
Patch4:         dosbox074-manpage-errors.patch
Patch5:         dosbox074-spelling-fixes.patch
BuildRequires:  GraphicsMagick
BuildRequires:  autoconf
BuildRequires:  desktop-file-utils
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  SDL_net-devel
BuildRequires:  SDL_sound-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl)

%description
DOSBox is an emulator that recreates an MS-DOS compatible environment,
with sound, input, graphics and basic networking, complete enough to run
many classic DOS games unmodified.

This is the classic 0.74-3 release, installed as "dosbox74" so it can
coexist with DOSBox Staging (package "dosbox").

%prep
%autosetup -p1 -n dosbox-0.74-3
iconv -f latin1 -t utf-8 THANKS > THANKS.utf8 && mv THANKS.utf8 THANKS
autoreconf -fi

%build
%configure
%make_build

%install
%make_install
mv %{buildroot}%{_bindir}/dosbox %{buildroot}%{_bindir}/dosbox74
mv %{buildroot}%{_mandir}/man1/dosbox.1 %{buildroot}%{_mandir}/man1/dosbox74.1
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/dosbox74.desktop
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
gm convert 'src/dosbox.ico[0]' %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/dosbox74.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dosbox74.desktop

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS
%{_bindir}/dosbox74
%{_mandir}/man1/dosbox74.1%{?ext_man}
%{_datadir}/applications/dosbox74.desktop
%{_datadir}/icons/hicolor/256x256/apps/dosbox74.png

%changelog
