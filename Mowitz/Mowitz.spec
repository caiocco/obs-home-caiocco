#
# spec file for package Mowitz
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define sover 0

Name:           Mowitz
Version:        0.3.1
Release:        0
Summary:        "More widgets" library for Siag Office
License:        GPL-2.0-or-later AND LGPL-2.0-or-later AND MIT
Group:          Development/Libraries/X11
URL:            https://siag.nu/mowitz/
Source0:        https://siag.nu/pub/mowitz/%{name}-%{version}.tar.gz
# PATCH-FIX-UPSTREAM mowitz-gcc15.patch -- missing includes (GCC 15)
Patch0:         mowitz-gcc15.patch
# PATCH-FIX-UPSTREAM mowitz-link-libs.patch -- link libMowitz against the X libraries it uses
Patch1:         mowitz-link-libs.patch
# PATCH-FIX-UPSTREAM mowitz-64bit-colors.patch -- int overflow in colour scaling turned bright colours dark on 64-bit
Patch2:         mowitz-64bit-colors.patch
# PATCH-FEATURE-OPENSUSE mowitz-urw-t1lib.patch -- render document fonts with t1lib using the URW base 35 Type 1 fonts (metric clones of the AFMs); fix T1_GetNoFonts name
Patch3:         mowitz-urw-t1lib.patch
# PATCH-FIX-UPSTREAM mowitz-xim-latin1.patch -- compose dead keys through XIM and return Latin-1 (UTF-8 locales lost accented letters)
Patch4:         mowitz-xim-latin1.patch
# PATCH-FIX-UPSTREAM mowitz-filesel-utf8.patch -- file selector shows Latin-1 but file names are UTF-8: convert at the boundary
Patch5:         mowitz-filesel-utf8.patch
# PATCH-FEATURE-UPSTREAM mowitz-cursor-resource.patch -- cursor resource for MwTable and MwRichtext
Patch6:         mowitz-cursor-resource.patch
# PATCH-FEATURE-OPENSUSE mowitz-xft-antialias.patch -- draw document glyphs antialiased with Xft from the same Type 1 files (MW_NO_XFT=1 restores t1lib bitmaps)
Patch7:         mowitz-xft-antialias.patch
# PATCH-FIX-UPSTREAM mowitz-selection-utf8.patch -- UTF-8/Latin-1 selection helpers; MwTextField pastes UTF8_STRING (UTF-8 STRING replies decoded too) and no longer hands Xt its own buffer to free
Patch8:         mowitz-selection-utf8.patch
# PATCH-FIX-UPSTREAM mowitz-center-on-parent.patch -- MwCenter places dialogs over the application window instead of the middle of the root window, which spans all monitors
Patch9:         mowitz-center-on-parent.patch
BuildRequires:  XawM-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  t1lib-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xt)

%description
Mowitz ("More widgets") is a collection of X Toolkit widgets used by
Siag Office: canvas, combo box, notebook, rich text, table, spinner,
tooltips, menus, list tree, file selector and more. This build is linked
against XawM, the Motif-like Athena widget set, and renders document
text with t1lib using the URW Type 1 fonts.

%package -n lib%{name}%{sover}
Summary:        "More widgets" library for Siag Office
Group:          System/Libraries
Requires:       %{name}-data = %{version}

%description -n lib%{name}%{sover}
Mowitz ("More widgets") is a collection of X Toolkit widgets used by
Siag Office, built on the XawM (Motif-like Athena) widget set.

%package data
Summary:        Font metrics, pixmaps and data files for Mowitz
Group:          System/Libraries
BuildArch:      noarch

# Type 1 fonts rendered through t1lib (FontDataBase/t1lib.config point here)
Requires:       ghostscript-fonts-std

%description data
Font metrics, Type 1 fonts, encodings, colour names and pixmaps used by
the Mowitz widget library.

%package devel
Summary:        Development files for the Mowitz widget library
Group:          Development/Libraries/X11
Requires:       XawM-devel
Requires:       lib%{name}%{sover} = %{version}
Requires:       pkgconfig(xpm)
Requires:       t1lib-devel

%description devel
Headers, the shared library link and the mowitz-config script for
the Mowitz widget library.

%prep
%autosetup -p1
# regenerate t1lib.config for the real data directory (shipped one says /usr/local)
touch Mowitz/mkt1cfg

%build
autoreconf -fi
%configure --disable-static --with-xaw3d=XawM --with-t1lib --with-xft \
  CPPFLAGS="-I%{_includedir}/XawM" \
  CFLAGS="%{optflags} -std=gnu17"
%make_build

%install
%make_install docdir=%{_docdir}/%{name}-devel
find %{buildroot} -type f -name '*.la' -delete -print
cp -p AUTHORS COPYING ChangeLog README %{buildroot}%{_docdir}/%{name}-devel/

%ldconfig_scriptlets -n lib%{name}%{sover}

%files -n lib%{name}%{sover}
%license COPYING
%{_libdir}/libMowitz.so.%{sover}{,.*}

%files data
%license COPYING
%{_datadir}/%{name}

%files devel
%{_bindir}/mowitz-config
%{_libdir}/libMowitz.so
%{_includedir}/%{name}
%{_docdir}/%{name}-devel

%changelog
