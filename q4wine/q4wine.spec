#
# spec file for package q4wine
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           q4wine
Version:        1.4.2
Release:        0
Summary:        Qt GUI for Wine
License:        GPL-3.0-only AND MIT
Group:          System/Emulators/PC
URL:            https://github.com/brezerk/q4wine
Source0:        https://github.com/brezerk/q4wine/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake >= 3.28
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  fuseiso
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  icoutils
BuildRequires:  pkgconfig
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6DBus)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Network)
BuildRequires:  pkgconfig(Qt6Sql)
BuildRequires:  pkgconfig(Qt6Svg)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(Qt6Xml)
Requires:       fuseiso
Requires:       icoutils
Requires:       qt6-sql-sqlite
Requires:       sudo
Requires:       wine
Recommends:     %{name}-lang
# src/third-party/SingleApplication-3.5.2 is MIT licensed
Provides:       bundled(SingleApplication) = 3.5.2

%description
Q4Wine is a Qt GUI for Wine that helps manage Wine prefixes and
installed applications.

Features:
- Work with several Wine versions at the same time
- Create, delete and manage prefixes (WINEPREFIX)
- Control Wine processes
- Mount CD/DVD images (via fuseiso)
- Extract icons from PE files (.exe, .dll)
- Back up and restore managed prefixes
- Export the Qt colour theme into Wine colour settings
- Winetricks support and a logging subsystem

%lang_package

%prep
%autosetup -p1

%build
%cmake \
  -DLIBS_ENTRY_PATH=%{_libdir} \
  -DCMAKE_NO_BUILTIN_CHRPATH=ON \
  -DCMAKE_SHARED_LINKER_FLAGS=""
%cmake_build

%install
%cmake_install
# icons for Ubuntu's Unity panel
rm -rf %{buildroot}%{_datadir}/icons/ubuntu-mono-dark
%find_lang %{name} --with-qt
%fdupes %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/q4wine.desktop || :

%files
%license COPYING
%doc AUTHORS.md Changelog.md README.md
%{_bindir}/q4wine
%{_bindir}/q4wine-cli
%{_bindir}/q4wine-helper
%{_libdir}/libq4wine-core.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%exclude %{_datadir}/%{name}/l10n
%{_datadir}/applications/q4wine.desktop
%{_datadir}/metainfo/ua.org.brezblock.q4wine.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/q4wine*.svg
%{_mandir}/man1/q4wine*%{?ext_man}

%files lang -f %{name}.lang
%dir %{_datadir}/%{name}/l10n

%changelog
