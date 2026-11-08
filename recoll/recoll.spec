#
# spec file for package recoll
#
# Copyright (c) 2026 SUSE LLC and contributors
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

Name:           recoll
Version:        1.44.2
Release:        0
Summary:        Personal full text search tool
License:        GPL-2.0-or-later
URL:            https://www.recoll.org
Source0:        https://www.recoll.org/%{name}-%{version}.tar.gz
Source1:        https://www.recoll.org/%{name}-%{version}.tar.gz.asc
Source2:        https://www.lesbonscomptes.com/pages/lesbonscomptes.gpg#/%{name}.keyring
Patch0:         stop-recoll-truncating-metadata-to-150.patch
# PATCH-FIX-OPENSUSE recoll-respect-platform-font.patch -- use the platform (qt5ct/qt6ct) font size instead of a fixed 12pt
Patch1:         recoll-respect-platform-font.patch
BuildRequires:  aspell-devel
BuildRequires:  bison
BuildRequires:  chmlib-devel
BuildRequires:  file-devel
BuildRequires:  hicolor-icon-theme
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  qt6-tools-linguist
BuildRequires:  cmake(Qt6WebEngineWidgets)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  pkgconfig(jsoncpp) >= 1.9.0
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(xapian-core)
Requires:       awk
Requires:       python3
Requires:       sed
# Recommends for the helpers
Recommends:     antiword
Recommends:     aspell
Recommends:     djvulibre
Recommends:     exiftool
Recommends:     libwpd-tools
Recommends:     perl-Image-ExifTool
Recommends:     poppler-tools
Recommends:     python3-base
Recommends:     python3-icalendar
Recommends:     python3-libxml2
Recommends:     python3-mutagen
Recommends:     python3-pylzma
Recommends:     python3-rarfile
Recommends:     python3-zipp
Recommends:     unrar
Recommends:     unrtf
Recommends:     unzip
Recommends:     wv
Recommends:     xdg-utils
ExclusiveArch:  %{x86_64} aarch64 riscv64

%description
Recoll is a personal full text search tool based on Xapian.

Features:
  * Qt-based GUI.
  * Supports the following document types (and their compressed versions)
   - Natively: text, html, OpenOffice files,  excel, ppt, maildir and
     mailbox (Mozilla and IceDove mail) with attachments, pidgin log files
   - With external helpers:  pdf (pdftotext), postscript (ghostscript), msword
     (antiword), rtf (unrtf). And others...
  * Query facilities, with boolean searches, phrases, filter on file
    types and directory tree.
  * Support for multiple charsets, Internal processing and storage uses Unicode
    UTF-8.
  * Stemming performed at query time (can switch stemming language after
    indexing).
  * Easy installation. No database daemon, web server or exotic language
    necessary.
  * The indexer can run either continuously or in batch.

%package devel
Summary:        Development files for recoll
Requires:       recoll = %{version}

%description devel
Recoll is a personal full text search tool based on Xapian.

This package provides development files.

%prep
%autosetup -p1

%build
export QMAKE=qmake6
%meson \
  -Dpython-aspell=false \
  -Dwebengine=true \
  -Drecollq=true

%meson_build

%install
%meson_install

# rpmlint
# E: env-script-interpreter
sed -i 's|#!%{_bindir}/env perl|#!%{_bindir}/perl|' %{buildroot}%{_datadir}/recoll/filters/rclimg
sed -i 's|#!%{_bindir}/env python3|#!%{_bindir}/python3|' %{buildroot}%{_datadir}/recoll/filters/*.py
sed -i 's|#!%{_bindir}/env python3|#!%{_bindir}/python3|' %{buildroot}%{_datadir}/recoll/filters/rcl*
sed -i 's|#!%{_bindir}/env python3|#!%{_bindir}/python3|' %{buildroot}%{python3_sitearch}/recoll/rclconfig.py

# E:script-without-shebang
chmod -x %{buildroot}/%{_datadir}/recoll/filters/*.xsl

%ldconfig_scriptlets

%files
%license COPYING
%doc README
%{_bindir}/recoll
%{_bindir}/recollq
%{_bindir}/recollindex
%{_datadir}/applications/recoll-searchgui.desktop
%{_datadir}/icons/hicolor/48x48/apps/recoll.png
%{_datadir}/icons/hicolor/scalable/apps/recoll.svg
%{_datadir}/metainfo/org.recoll.recoll.appdata.xml
%{_datadir}/pixmaps/recoll.png
%{_datadir}/recoll/
%{_libdir}/librecoll.so.*
%{_mandir}/man1/recollq.1%{?ext_man}
%{_mandir}/man1/recoll.1%{?ext_man}
%{_mandir}/man1/recollindex.1%{?ext_man}
%{_mandir}/man5/recoll.conf.5%{?ext_man}
%{_unitdir}/recollindex@.service
%{_userunitdir}/recollindex.service
%{python3_sitearch}/recoll/
%{python3_sitearch}/recollchm/

%files devel
%{_includedir}/recoll/
%{_libdir}/librecoll.so

%changelog
