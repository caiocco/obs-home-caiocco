#
# spec file for package tkdesk
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define tkdesk_lib %{_prefix}/lib/tkdesk

Name:           tkdesk
Version:        2.0
Release:        0
Summary:        Graphical file manager and desktop tool for X11 written in Tcl/Tk
License:        GPL-2.0-or-later AND TCL AND MIT
Group:          Productivity/File utilities
URL:            https://tkdesk.sourceforge.net/
Source0:        https://downloads.sourceforge.net/project/tkdesk/TkDesk/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
# PATCH-FIX-UPSTREAM tkdesk-2.0p1.patch -- official upstream patch 2.0p1 (via Debian)
Patch0:         tkdesk-2.0p1.patch
# PATCH-FIX-UPSTREAM tkdesk-2.0p2.patch -- official upstream patch 2.0p2 (via Debian)
Patch1:         tkdesk-2.0p2.patch
# PATCH-FIX-OPENSUSE tkdesk-debian-fixes.patch -- Debian's before_quilt.patch (Itcl 4, Tcl 8.6, safe /tmp), without its dpkg-specific configs
Patch2:         tkdesk-debian-fixes.patch
# PATCH-FIX-OPENSUSE tkdesk-debian-buildflags.patch -- honour CFLAGS/LDFLAGS (Debian)
Patch3:         tkdesk-debian-buildflags.patch
# PATCH-FIX-OPENSUSE tkdesk-debian-spelling.patch -- typo fixes (Debian)
Patch4:         tkdesk-debian-spelling.patch
# PATCH-FIX-OPENSUSE tkdesk-debian-reproducible.patch -- sorted tclIndex (Debian)
Patch5:         tkdesk-debian-reproducible.patch
# PATCH-FIX-OPENSUSE tkdesk-debian-parallel-build.patch -- parallel make race (Debian)
Patch6:         tkdesk-debian-parallel-build.patch
# PATCH-FIX-OPENSUSE tkdesk-debian-gcc-15.patch -- prototypes for GCC 15 (Debian)
Patch7:         tkdesk-debian-gcc-15.patch
# PATCH-FIX-OPENSUSE tkdesk-blt-tk86.patch -- bundled BLT subset on Tk 8.6/64-bit: tkInt.h, Tcl allocator, handle/pid sizes; Itcl via package require
Patch8:         tkdesk-blt-tk86.patch
# PATCH-FIX-OPENSUSE tkdesk-server-key.patch -- server: no /dev/kmem, random key from /dev/urandom, bind to 127.0.0.1
Patch9:         tkdesk-server-key.patch
# PATCH-FIX-OPENSUSE tkdesk-xdg-open.patch -- open URLs with xdg-open instead of netscape
Patch10:        tkdesk-xdg-open.patch
BuildRequires:  autoconf
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  tcl-devel >= 8.6
BuildRequires:  tk-devel >= 8.6
BuildRequires:  pkgconfig(x11)
# [incr Tcl] 4 ships inside the tcl package
Requires:       tcl >= 8.6
Requires:       tk >= 8.6
Recommends:     xdg-utils
Recommends:     xterm

%description
TkDesk is a graphical file manager and desktop tool for the X Window
System, written in Tcl/Tk with [incr Tcl].  It offers multi-pane file
browser and file list windows, drag and drop between them, an
application bar with clock, mail and trash displays, a built-in text
editor, find and disk usage tools, and menus, popups and file tags
that are configured through editable Tcl files in ~/.tkdesk.

This build carries the Debian patches plus fixes for Tcl/Tk 8.6 on
64-bit systems in TkDesk's bundled BLT subset.

%prep
%autosetup -p1
# tclConfig.sh's TCL_LD_SEARCH_FLAGS expands to an empty -rpath, which
# leaves an empty RUNPATH (= current directory) in tkdesksh
sed -i 's/@TCL_LD_SEARCH_FLAGS@//' Makefile.in
# the patches touch configure.in
autoconf

%build
export CFLAGS="%{optflags} -std=gnu17 -DUSE_INTERP_RESULT"
export LDFLAGS="%{?build_ldflags}"
export LIBS="-lX11 -lm"
%configure \
  --with-tcl=%{_libdir} \
  --with-tk=%{_libdir} \
  --with-itcl-lib=" " \
  --with-itcl-version=4
# CC_EXTRA_OPTS defaults to -O, which would override -O2 from optflags
%make_build CC_EXTRA_OPTS= TKDESK_LIBRARY=%{tkdesk_lib}

%install
export CFLAGS="%{optflags} -std=gnu17 -DUSE_INTERP_RESULT"
# "make install" runs the freshly installed tkdesksh to build tclIndex
make install \
  CC_EXTRA_OPTS= \
  INSTALL_ROOT=%{buildroot} \
  TKDESK_LIBRARY=%{tkdesk_lib}
install -Dm0644 tcldesk/images/desk2.xpm %{buildroot}%{_datadir}/pixmaps/%{name}.xpm
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license COPYING license.terms
%doc README CREDITS ChangeLog doc/guide.txt
%{_bindir}/tkdesk
%{_bindir}/tkdeskclient
%{_bindir}/cd-tkdesk
%{_bindir}/ed-tkdesk
%{_bindir}/od-tkdesk
%{_bindir}/op-tkdesk
%{_bindir}/pop-tkdesk
%{_bindir}/pauseme
%{tkdesk_lib}
%{_mandir}/man1/tkdesk.1%{?ext_man}
%{_mandir}/man1/cd-tkdesk.1%{?ext_man}
%{_mandir}/man1/ed-tkdesk.1%{?ext_man}
%{_mandir}/man1/od-tkdesk.1%{?ext_man}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.xpm

%changelog
