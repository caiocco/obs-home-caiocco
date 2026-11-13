#
# spec file for package t1lib
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


Name:           t1lib
Version:        5.1.2
Release:        0
Summary:        Adobe Type 1 Font Rasterizing Library
License:        LGPL-2.0-only AND LGPL-2.1-only
Group:          System/Libraries
URL:            ftp://sunsite.unc.edu/pub/Linux/libs/graphics/
Source0:        ftp://sunsite.unc.edu/pub/Linux/libs/graphics/t1lib-5.1.2.tar.bz2
Patch0:         t1lib-auto.patch
Patch1:         https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/t1lib/files/t1lib-5.1.2-CVE-2010-2642_2011-0433_2011-5244.patch
Patch2:         https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/t1lib/files/t1lib-5.1.2-CVE-2011-0764.patch
Patch3:         https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/t1lib/files/t1lib-5.1.2-CVE-2011-1552_1553_1554.patch
Patch4:         https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/t1lib/files/t1lib-do-not-install-t1lib_doc-r1.patch
Patch5:         t1lib-5.1.2-format-security.patch
Patch6:         lib-cleanup.diff
Patch7:         no-config.diff
Patch8:         t1lib-5.1.2-segfault.patch
Patch9:         t1lib-5.1.2-aarch64.patch
Patch11:        t1lib-5.1.2-t1.patch
Patch13:        t1lib-c99.patch
Patch14:        t1lib-configure-c99.patch
# PATCH-FIX-OPENSUSE t1lib-5.1.2-searchpath-overflow.patch -- the segfault patch wrote past short search path strings (heap corruption with ~25+ font database entries)
Patch15:        t1lib-5.1.2-searchpath-overflow.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libXaw-devel
BuildRequires:  libtool

%description
T1lib is a library for generating character and string glyphs from
Adobe Type 1 fonts under UNIX. T1lib uses most of the code of the X
Window System rasterizer donated by IBM to the X Window System project.
Some disadvantages of the rasterizer included in the X Window System
have been eliminated.

%package      -n t1lib-devel
Summary:        Development Libraries for T1lib
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description  -n t1lib-devel

This package provides the t1lib development environment header files, and more.

%package      -n t1lib-static-devel
Summary:        Static Development Libraries for T1lib
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       glibc-devel
Requires:       xorg-x11-libICE-devel
Requires:       xorg-x11-libSM-devel
Requires:       xorg-x11-libX11-devel
Requires:       xorg-x11-libXext-devel
Requires:       xorg-x11-libXpm-devel

%description  -n t1lib-static-devel

This package provides the t1lib static libraries.

%prep
%autosetup -p1 -n t1lib-%{version}

%build
autoreconf -fi
%if 0%{?suse_version} >= 1600
export CFLAGS="%{optflags} -ffat-lto-objects -std=gnu17"
%else
export CFLAGS="%{optflags} -ffat-lto-objects"
%endif
%configure %{_target_cpu}-suse-linux-gnu
#%make_build without_doc
make without_doc

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc Changes LGPL README.t1*
%doc doc/t1lib_doc.pdf
%doc doc/t1_data.eps
%{_libdir}/libt1.so.*
%{_libdir}/libt1x.so.*
%{_bindir}/type1afm
%{_bindir}/xglyph

%files -n t1lib-devel
%{_libdir}/libt1.so
%{_libdir}/libt1x.so
%{_includedir}/t1lib.h
%{_includedir}/t1libx.h

%files -n t1lib-static-devel
%{_libdir}/libt1x.la
%{_libdir}/libt1x.a
%{_libdir}/libt1.la
%{_libdir}/libt1.a

%changelog
