#
# spec file for package free42
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           free42
Version:        3.5.4
Release:        0
Summary:        HP-42S calculator simulator
License:        GPL-2.0-only AND BSD-3-Clause
Group:          Productivity/Scientific/Math
URL:            https://thomasokken.com/free42/
Source0:        https://thomasokken.com/free42/upstream/%{name}-nologo-%{version}.tgz
Source1:        com.thomasokken.free42.desktop
Source2:        com.thomasokken.free42bin.desktop
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  hicolor-icon-theme
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gtk+-3.0)

%description
Free42 is a complete re-implementation of the HP-42S scientific
programmable RPN calculator and the HP 82240 printer. It was written
from scratch, without using any HP code.

Two executables are provided: free42dec uses decimal floating point
(Intel Decimal Floating-Point Math Library, 34 digits) and behaves like
the real calculator; free42bin uses the machine's binary floating point,
which is faster but shows binary rounding artifacts.

%prep
%autosetup -n %{name}-nologo-%{version}

%build
cd gtk
# CFLAGS must come from the environment: the Makefile appends to it
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
# Binary build first, then decimal; "clean" keeps the Intel library
%make_build AUDIO_ALSA=1
make clean
%make_build AUDIO_ALSA=1 BCD_MATH=1

%install
install -Dpm 0755 gtk/free42dec %{buildroot}%{_bindir}/free42dec
install -Dpm 0755 gtk/free42bin %{buildroot}%{_bindir}/free42bin
install -Dpm 0644 gtk/icon-48x48.png \
  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -Dpm 0644 gtk/icon-128x128.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/com.thomasokken.free42.desktop
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/com.thomasokken.free42bin.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
# Directory searched for system-wide skins ($XDG_DATA_DIRS/free42/skins)
install -d %{buildroot}%{_datadir}/%{name}/skins

%files
%license COPYING
%doc CREDITS HISTORY README gtk/README.txt
%{_bindir}/free42dec
%{_bindir}/free42bin
%{_datadir}/applications/com.thomasokken.free42.desktop
%{_datadir}/applications/com.thomasokken.free42bin.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}

%changelog
