#
# spec file for package xpdf
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# The command line tools have the same names as the ones in poppler-tools,
# so they go in a separate xpdf-tools package that conflicts with it; the
# viewer itself can be installed alongside poppler.
#

Name:           xpdf
Version:        4.06
Release:        0
Summary:        PDF viewer
License:        GPL-2.0-only OR GPL-3.0-only
Group:          Productivity/Publishing/PDF
URL:            https://www.xpdfreader.com/
Source0:        https://dl.xpdfreader.com/%{name}-%{version}.tar.gz
Source1:        xpdf.desktop
BuildRequires:  cmake >= 3.5
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  libpaper-devel
BuildRequires:  pkgconfig
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6PrintSupport)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(zlib)
Requires:       %{name}-common = %{version}
Recommends:     urw-base35-fonts

%description
Xpdf is a small and fast viewer for Portable Document Format (PDF)
files, built with the Qt toolkit.  It supports tabs, a sidebar with
the document outline, layers and attachments, full-text search,
printing and extensive configuration through the xpdfrc file.

%package common
Summary:        Configuration file for Xpdf and the Xpdf tools
Group:          Productivity/Publishing/PDF
BuildArch:      noarch

%description common
This package contains the system-wide xpdfrc configuration file and its
manual page, shared by the Xpdf viewer and the Xpdf command line tools.

%package tools
Summary:        Command line tools for PDF files from Xpdf
Group:          Productivity/Publishing/PDF
Requires:       %{name}-common = %{version}
Recommends:     urw-base35-fonts
Conflicts:      poppler-tools

%description tools
The Xpdf toolkit includes several command line tools that work on PDF
files:
  - pdftotext: convert PDF to text
  - pdftops: convert PDF to PostScript
  - pdftoppm: convert PDF pages to PPM/PGM/PBM images
  - pdftopng: convert PDF pages to PNG images
  - pdftohtml: convert PDF to HTML
  - pdfinfo: show PDF metadata
  - pdfimages: extract images from PDF files
  - pdffonts: list the fonts used in PDF files
  - pdfdetach: extract attached files from PDF files

These tools have the same names as the ones in poppler-tools, so the two
packages cannot be installed at the same time.

%prep
%autosetup -p1

%build
%cmake \
    -DBUILD_SHARED_LIBS=OFF \
    -DSYSTEM_XPDFRC=%{_sysconfdir}/xpdfrc \
    -DXPDFRC_DATADIR=%{_datadir}/%{name} \
    -DA4_PAPER=ON \
    -DUSE_XDG=ON \
    -DXPDFWIDGET_PRINTING=ON \
    -DCMAKE_DISABLE_FIND_PACKAGE_Qt5Widgets=ON
%cmake_build

%install
%cmake_install
install -Dpm 0644 doc/sample-xpdfrc %{buildroot}%{_sysconfdir}/xpdfrc
install -Dpm 0644 xpdf-qt/xpdf-icon.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
install -dm 0755 %{buildroot}%{_datadir}/%{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license COPYING COPYING3
%doc ANNOUNCE CHANGES README
%{_bindir}/xpdf
%{_mandir}/man1/xpdf.1%{?ext_man}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files common
%license COPYING COPYING3
%config(noreplace) %{_sysconfdir}/xpdfrc
%dir %{_datadir}/%{name}
%{_mandir}/man5/xpdfrc.5%{?ext_man}

%files tools
%license COPYING COPYING3
%{_bindir}/pdfdetach
%{_bindir}/pdffonts
%{_bindir}/pdfimages
%{_bindir}/pdfinfo
%{_bindir}/pdftohtml
%{_bindir}/pdftoppm
%{_bindir}/pdftopng
%{_bindir}/pdftops
%{_bindir}/pdftotext
%{_mandir}/man1/pdfdetach.1%{?ext_man}
%{_mandir}/man1/pdffonts.1%{?ext_man}
%{_mandir}/man1/pdfimages.1%{?ext_man}
%{_mandir}/man1/pdfinfo.1%{?ext_man}
%{_mandir}/man1/pdftohtml.1%{?ext_man}
%{_mandir}/man1/pdftoppm.1%{?ext_man}
%{_mandir}/man1/pdftopng.1%{?ext_man}
%{_mandir}/man1/pdftops.1%{?ext_man}
%{_mandir}/man1/pdftotext.1%{?ext_man}

%changelog
