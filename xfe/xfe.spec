#
# spec file for package xfe
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           xfe
Version:        2.1.13
Release:        0
Summary:        X File Explorer, a lightweight file manager for X11
License:        GPL-2.0-or-later
Group:          Productivity/File utilities
URL:            https://sourceforge.net/projects/xfe/
Source0:        https://downloads.sourceforge.net/project/xfe/xfe/%{version}/%{name}-%{version}.tar.xz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  fox16-devel >= 1.6.50
BuildRequires:  gcc-c++
BuildRequires:  gettext-tools >= 0.21
BuildRequires:  hicolor-icon-theme
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libnotify) >= 0.7.7
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(udisks2) >= 2.7.6
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb) >= 1.6
BuildRequires:  pkgconfig(xcb-aux)
BuildRequires:  pkgconfig(xcb-event)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xrandr)
Requires:       bzip2
Requires:       file
Requires:       gzip
Requires:       tar
Recommends:     %{name}-lang
Recommends:     udisks2
Recommends:     unzip
Recommends:     xz
Recommends:     zip
Suggests:       7zip
Suggests:       xterm

%description
X File Explorer (Xfe) is a lightweight file manager for X11, written
using the FOX toolkit. It is desktop independent and can easily be
customized. It has Commander or Explorer styles and is very fast and
small.

Xfe is based on the popular, but discontinued, X Win Commander. It
comes with a text editor (Xfw), an archive viewer (Xfa), an image
viewer (Xfi), a package viewer (Xfp) and an automounter
(xfe-automount) for removable media.

%lang_package

%prep
%autosetup -p1
# PackageManager needs System as main category (desktop-file-validate)
sed -i 's|^Categories=Utility;PackageManager;|Categories=System;PackageManager;|' xfp.desktop.in.in

%build
autoreconf -fiv
# --enable-minimalflags keeps %%optflags (no -O3/-ffast-math)
%configure \
    --docdir=%{_docdir}/%{name} \
    --enable-minimalflags \
    --enable-sn \
    --with-xrandr
%make_build

%install
%make_install
# Norwegian Bokmål uses the "nb" locale directory on openSUSE
if [ -d %{buildroot}%{_datadir}/locale/no ]; then
    mv %{buildroot}%{_datadir}/locale/no %{buildroot}%{_datadir}/locale/nb
fi
rm -f %{buildroot}%{_datadir}/locale/locale.alias
# XPM icons are redundant with the PNG/SVG ones (and xfi.xpm is empty)
rm -f %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/*.xpm
for f in %{buildroot}%{_datadir}/applications/*.desktop; do
    desktop-file-validate "$f"
done
%find_lang %{name}
%fdupes -s %{buildroot}%{_datadir}

%files
%license COPYING
%doc AUTHORS BUGS ChangeLog README TODO
%{_bindir}/xfa
%{_bindir}/xfe
%{_bindir}/xfe-automount
%{_bindir}/xfi
%{_bindir}/xfp
%{_bindir}/xfw
%{_mandir}/man1/xf*.1%{?ext_man}
%{_datadir}/applications/xf*.desktop
%{_datadir}/icons/hicolor/48x48/apps/xf*.png
%{_datadir}/icons/hicolor/scalable/apps/xf*.svg
%dir %{_datadir}/xfe
%{_datadir}/xfe/icons
%{_datadir}/xfe/xferc

%files lang -f %{name}.lang

%changelog
