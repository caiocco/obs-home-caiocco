#
# spec file for package treesheets
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# TreeSheets needs wxWidgets >= 3.3.4, which openSUSE does not ship (Leap
# 16.0 has 3.2), so wxWidgets is built here from the bundled release and
# linked statically, using the system image/compression/regex libraries.
# The other dependencies that upstream fetches at configure time (Lobster,
# wxPdfDocument, Monocypher and libunibreak) are bundled too; CMake is run
# fully disconnected and pointed at the unpacked sources.
#

%define wx_ver          3.3.4
%define lobster_ver     2026.8
%define wxpdfdoc_ver    1.4.0
%define monocypher_ver  4.0.3
%define unibreak_ver    8.0

Name:           treesheets
Version:        2.23.4
Release:        0
Summary:        Free-form hierarchical data organizer
License:        Zlib AND LGPL-2.0-or-later WITH WxWindows-exception-3.1 AND Apache-2.0 AND LGPL-2.1-or-later AND BSD-3-Clause AND MIT AND (BSD-2-Clause OR CC0-1.0)
Group:          Productivity/Office/Organizers
URL:            https://strlen.com/treesheets/
Source0:        https://github.com/aardappel/treesheets/archive/v%{version}.tar.gz#/treesheets-%{version}.tar.gz
Source1:        https://github.com/wxWidgets/wxWidgets/releases/download/v%{wx_ver}/wxWidgets-%{wx_ver}.tar.bz2
Source2:        https://github.com/aardappel/lobster/archive/refs/tags/v%{lobster_ver}.tar.gz#/lobster-%{lobster_ver}.tar.gz
Source3:        https://github.com/utelle/wxpdfdoc/archive/refs/tags/v%{wxpdfdoc_ver}.tar.gz#/wxpdfdoc-%{wxpdfdoc_ver}.tar.gz
Source4:        https://github.com/LoupVaillant/Monocypher/archive/refs/tags/%{monocypher_ver}.tar.gz#/Monocypher-%{monocypher_ver}.tar.gz
Source5:        https://github.com/adah1972/libunibreak/releases/download/libunibreak_8_0/libunibreak-%{unibreak_ver}.tar.gz

BuildRequires:  cmake >= 3.25
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  shared-mime-info
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpcre2-32)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(zlib)
Requires:       shared-mime-info
Provides:       bundled(libtcc)
Provides:       bundled(libunibreak) = %{unibreak_ver}
Provides:       bundled(lobster) = %{lobster_ver}
Provides:       bundled(monocypher) = %{monocypher_ver}
Provides:       bundled(wxPdfDocument) = %{wxpdfdoc_ver}
Provides:       bundled(wxWidgets) = %{wx_ver}

%description
TreeSheets is a "hierarchical spreadsheet" that can replace spreadsheets,
mind mappers, outliners, PIMs, text editors and small databases.

It is suitable for any kind of data organization, such as todo lists,
calendars, project management, brainstorming, organizing ideas, planning,
requirements gathering and presentation of information.  Cells can hold
text, images and nested grids, and can be scripted with Lobster.

%prep
%setup -q -a1 -a2 -a3 -a4 -a5
chmod -x ZLIB_LICENSE.txt

%build
%cmake \
    -DTREESHEETS_VERSION=%{version} \
    -DTREESHEETS_BUNDLE_WXWIDGETS=ON \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DFETCHCONTENT_SOURCE_DIR_WXWIDGETS=$PWD/../wxWidgets-%{wx_ver} \
    -DFETCHCONTENT_SOURCE_DIR_LOBSTER=$PWD/../lobster-%{lobster_ver} \
    -DFETCHCONTENT_SOURCE_DIR_WXPDFDOC=$PWD/../wxpdfdoc-%{wxpdfdoc_ver} \
    -DFETCHCONTENT_SOURCE_DIR_MONOCYPHER=$PWD/../Monocypher-%{monocypher_ver} \
    -DFETCHCONTENT_SOURCE_DIR_LIBUNIBREAK=$PWD/../libunibreak-%{unibreak_ver} \
    -DwxBUILD_TOOLKIT=gtk3 \
    -DwxUSE_REGEX=sys \
    -DwxUSE_ZLIB=sys \
    -DwxUSE_EXPAT=sys \
    -DwxUSE_LIBJPEG=sys \
    -DwxUSE_LIBPNG=sys \
    -DwxUSE_LIBTIFF=sys \
    -DwxUSE_LIBWEBP=sys \
    -DwxUSE_OPENGL=OFF \
    -DwxUSE_LIBSDL=OFF \
    -DwxUSE_LIBNOTIFY=OFF \
    -DwxUSE_LIBMSPACK=OFF \
    -DwxUSE_LIBGNOMEVFS=OFF \
    -DwxUSE_SECRETSTORE=OFF \
    -DwxUSE_SPELLCHECK=OFF
%cmake_build

%install
%cmake_install
# lower-case command name for convenience
ln -s TreeSheets %{buildroot}%{_bindir}/treesheets
%fdupes %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.strlen.TreeSheets.desktop || :

%files
%license ZLIB_LICENSE.txt
%{_bindir}/TreeSheets
%{_bindir}/treesheets
%{_docdir}/%{name}/
%{_datadir}/TreeSheets/
%{_datadir}/applications/com.strlen.TreeSheets.desktop
%{_datadir}/icons/hicolor/scalable/apps/com.strlen.TreeSheets.svg
%{_datadir}/metainfo/com.strlen.TreeSheets.metainfo.xml
%{_datadir}/mime/packages/com.strlen.TreeSheets.xml

%changelog
