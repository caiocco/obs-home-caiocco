#
# spec file for package xpad
#
# Copyright (c) 2026 Caio
# Based on the Fedora xpad spec (https://src.fedoraproject.org/rpms/xpad),
# MIT License.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           xpad
Version:        6.0.0
Release:        0
Summary:        Sticky notepad for GTK
License:        GPL-3.0-or-later
Group:          Productivity/Office/Other
URL:            https://launchpad.net/xpad
Source0:        https://launchpad.net/xpad/trunk/6.0/+download/%{name}-%{version}.tar.bz2
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext-tools
BuildRequires:  hicolor-icon-theme
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(atk) >= 2.8
BuildRequires:  pkgconfig(atk-bridge-2.0)
BuildRequires:  pkgconfig(ayatana-appindicator3-0.1)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.28
BuildRequires:  pkgconfig(gio-2.0) >= 2.56
BuildRequires:  pkgconfig(glib-2.0) >= 2.58
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.22
BuildRequires:  pkgconfig(gtksourceview-4) >= 4.0.3
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(pango) >= 1.32
BuildRequires:  pkgconfig(sm)

%description
Xpad is a sticky note application that strives to be simple,
fault-tolerant and customizable. It consists of independent pad
windows; each is basically a text box in which notes can be written.
Pads can be colored, made transparent, kept on top and hidden to the
system tray (via Ayatana AppIndicator).

%lang_package

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --enable-appindicator=yes
%make_build

%install
%make_install
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/%{name}.1%{?ext_man}

%files lang -f %{name}.lang

%changelog
