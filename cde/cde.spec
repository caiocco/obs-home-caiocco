#
# spec file for package cde
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
#
# Snapshot of the master branch of git://git.code.sf.net/p/cdesktopenv/code
# (the tarball is "git archive <commit>:cde", the repository keeps the
# sources in a cde/ subdirectory).  Started from the spec in
# home:AndnoVember:test/cde.
#
# Master can relocate the historical /usr/dt, /etc/dt and /var/dt trees.
# This package uses an FHS layout: programs in /usr/bin, libraries in
# %%{_libdir}, internal helpers in /usr/libexec/cde, read-only data in
# /usr/share/cde.  Admin configuration stays in /etc/dt and runtime
# state in /var/dt, as every CDE manual describes them.
#

%define cde_commit adb6cc69401692c127ae83d5a77a7f8df695b0d1
%define cde_short  adb6cc6
%define cde_date   20261106
%define cde_data   %{_datadir}/cde

Name:           cde
Version:        2.5.3+git%{cde_date}.%{cde_short}
Release:        0
Summary:        Common Desktop Environment, the classic UNIX desktop
License:        LGPL-2.1-or-later
Group:          System/GUI/Other
URL:            https://sourceforge.net/projects/cdesktopenv/
Source0:        %{name}-%{version}.tar.xz
Source1:        dtlogin.displaymanager
Source2:        dtlogin.pamd
Source3:        dtsession.pamd
Source99:       %{name}-rpmlintrc
# PATCH-FIX-UPSTREAM uninitialized ostringstream buffers broke the
# dtinfo book build under MALLOC_PERTURB_
Patch0:         cde-ostringstream-uninitialized-buffer.patch
Patch1:         cde-dtwm-sys-dtwmrc-data-dir.patch
Patch2:         cde-xsession-copyright-data-dir.patch
Patch3:         cde-fontaliases-iso10646.patch
Patch4:         cde-xsession-keep-x-connection.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bdftopcf
BuildRequires:  bison
BuildRequires:  byacc
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  glibc-locale-base
BuildRequires:  gzip
BuildRequires:  ksh
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  mkfontscale
BuildRequires:  motif
# X11/bitmaps/xm_* are in the motif package, not motif-devel
BuildRequires:  motif-devel
BuildRequires:  ncompress
BuildRequires:  ncurses-devel
BuildRequires:  opensp
BuildRequires:  pam-devel
BuildRequires:  perl
BuildRequires:  pkgconfig
BuildRequires:  rpcgen
BuildRequires:  sessreg
BuildRequires:  tcl-devel
BuildRequires:  xbitmaps-devel
BuildRequires:  xrdb
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libcrypt)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libtirpc)
BuildRequires:  pkgconfig(lmdb)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xau)
BuildRequires:  pkgconfig(xaw7)
BuildRequires:  pkgconfig(xdmcp)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xt)
Requires:       cpp
Requires:       ksh
Requires:       m4
# X11/bitmaps/xm_* cursors (dtinfo aborts without xm_noenter16)
Requires:       motif
Requires:       ncompress
Requires:       rpcbind
Requires:       sessreg
Requires:       xrdb
# Xsession holds an X connection with it until dtsession is up
Requires:       xprop
Requires:       xset
Requires:       xsetroot
Requires(post): update-alternatives
Requires(postun): update-alternatives
Recommends:     xinetd
Recommends:     xorg-x11-fonts
Provides:       cdesktopenv = %{version}

%description
The Common Desktop Environment, the classic UNIX desktop created by
Sun, HP, IBM, DEC, SCO, Fujitsu and Hitachi and used on commercial
UNIX systems such as Solaris, HP-UX and AIX.  It was released as open
source by The Open Group in 2012.

It includes the dtwm window manager with its front panel and
workspaces, the dtsession session manager, the dtlogin display
manager, dtfile, dtterm, dtpad, dtcalc, dtcm (calendar), dtmail,
dthelpview, dtinfo, the dtksh shell, the ToolTalk messaging service
and the App Builder.

After installing, enable the services the desktop depends on (the
package does not enable them):

  systemctl enable --now rpcbind.socket
    ToolTalk needs it; without it the session stops with "The desktop
    messaging system could not be started".

  systemctl enable --now xinetd
    Starts the calendar server (rpc.cmsd, see
    %{_sysconfdir}/xinetd.d/cmsd) on demand for dtcm.

The calendar also needs the fully qualified host name to resolve, e.g.
an %{_sysconfdir}/hosts line such as "127.0.0.2 host.example.org host";
otherwise dtcm reports "Error opening Calendar file user@host".

%prep
%autosetup -p1
# the help volume and dtinfo book builds run in this locale
locale -a | grep -qi '^en_US\.utf-\?8$'

%build
# like Debian's packaging: no LTO for this code base
%define _lto_cflags %{nil}
export CFLAGS="%{optflags} -Wno-return-type"
export CXXFLAGS="%{optflags} -Wno-return-type"
NOCONFIGURE=1 ./autogen.sh
%configure \
    --disable-static \
    --with-cde-data-dir=%{cde_data} \
    --with-cde-config-dir=%{_sysconfdir}/dt \
    --with-cde-state-dir=%{_localstatedir}/dt \
    --with-cde-libexec-dir=%{_libexecdir}/%{name} \
    --with-pam-dir=%{_pamdir}
%make_build

%install
%make_install

# no development package
find %{buildroot}%{_libdir} \( -name '*.la' -o -name '*.so' -o -name '*.a' \) -print -delete
rm -rf %{buildroot}%{_includedir}

# top-level docs and the "man" compatibility link land in --prefix
# copyright is the dthello welcome text read by Xsession
mv %{buildroot}%{_prefix}/copyright %{buildroot}%{cde_data}/copyright
rm -fv %{buildroot}%{_prefix}/{CONTRIBUTORS,COPYING,HISTORY,README.md}
rm -fv %{buildroot}%{_prefix}/man
# SysV section 1m (admin commands) is section 8 on Linux, as in Debian
if [ -d %{buildroot}%{_mandir}/man1m ]; then
    install -d %{buildroot}%{_mandir}/man8
    for f in %{buildroot}%{_mandir}/man1m/*.1m; do
        sed -i -E '0,/^\.TH/s/^(\.TH[[:space:]]+("[^"]+"|[^[:space:]]+)[[:space:]]+)("[^"]+"|[^[:space:]]+)/\1"8"/I' "$f"
        mv "$f" %{buildroot}%{_mandir}/man8/$(basename "$f" .1m).8
    done
    rmdir %{buildroot}%{_mandir}/man1m
fi
# ncurses' terminfo already ships dtterm
rm -fv %{buildroot}%{_datadir}/terminfo/d/dtterm

# no setuid dtappgather: the per-session directories it creates live
# in sticky, world-writable directories instead (as Debian does)
chmod 0755 %{buildroot}%{_bindir}/dtappgather
# no setuid dtterm either: it gets its pty from posix_openpt(), root was
# only used for utmp entries
chmod 0755 %{buildroot}%{_bindir}/dtterm
install -d -m 1777 %{buildroot}%{_localstatedir}/dt/appconfig/appmanager
install -d -m 1777 %{buildroot}%{_localstatedir}/dt/tmp

# openSUSE PAM stacks (upstream's use pam_lastlog, gone from Linux-PAM)
rm -fv %{buildroot}%{_sysconfdir}/pam.d/dtsession %{buildroot}%{_pamdir}/dtsession
install -Dm 0644 %{SOURCE2} %{buildroot}%{_pamdir}/dtlogin
install -Dm 0644 %{SOURCE3} %{buildroot}%{_pamdir}/dtsession
rmdir %{buildroot}%{_sysconfdir}/pam.d 2>/dev/null || :

# session entry for other display managers
install -Dm 0644 contrib/desktopentry/cde.desktop %{buildroot}%{_datadir}/xsessions/cde.desktop
# xinetd services for the calendar and ToolTalk database servers
install -Dm 0644 contrib/xinetd/cmsd %{buildroot}%{_sysconfdir}/xinetd.d/cmsd
install -Dm 0644 contrib/xinetd/ttdbserver %{buildroot}%{_sysconfdir}/xinetd.d/ttdbserver

# dtlogin as a choice for display-manager.service
install -Dm 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/X11/displaymanagers/dtlogin
mkdir -p %{buildroot}%{_sysconfdir}/alternatives
touch %{buildroot}%{_sysconfdir}/alternatives/default-displaymanager
ln -s %{_sysconfdir}/alternatives/default-displaymanager \
    %{buildroot}%{_prefix}/lib/X11/displaymanagers/default-displaymanager

# interpreters from the historical layout
grep -rlI '^#![[:space:]]*/usr/dt/bin/dtksh' %{buildroot} | \
    xargs -r sed -i '1s|^#![[:space:]]*/usr/dt/bin/dtksh|#!%{_bindir}/dtksh|'

# tradcpp does not expand macros inside quoted strings, so the
# sh -c '...' EXEC_STRINGs of the action files (Help Manager, dtwmrc
# editing, Reload Actions, ...) kept the literal CDE_*_TOP placeholders
grep -rlIE 'CDE_(INSTALLATION|CONFIGURATION|DATA|LOGFILES)_TOP' %{buildroot} | \
    xargs -r sed -i \
        -e 's|CDE_INSTALLATION_TOP|%{_prefix}|g' \
        -e 's|CDE_CONFIGURATION_TOP|%{_sysconfdir}/dt|g' \
        -e 's|CDE_DATA_TOP|%{cde_data}|g' \
        -e 's|CDE_LOGFILES_TOP|%{_localstatedir}/dt|g'

# Application Manager entries are identical placeholder files whose name
# is the action; dtfile types a symlink by its target, so linking them
# made every launcher resolve to one action (xpdf). Keep them real files.
for d in %{buildroot}%{cde_data}/* %{buildroot}%{cde_data}/appconfig/*; do
    case "$d" in
    */appconfig|*/appconfig/appmanager) continue ;;
    esac
    [ -d "$d" ] && %fdupes -s "$d"
done

%check
# report (do not fail on) /usr/dt, /etc/dt, /var/dt literals that did
# not follow the configured layout
sh util/check-fhs.sh %{buildroot} || :

%post
/sbin/ldconfig
%{_sbindir}/update-alternatives --install %{_prefix}/lib/X11/displaymanagers/default-displaymanager \
    default-displaymanager %{_prefix}/lib/X11/displaymanagers/dtlogin 12

%postun
/sbin/ldconfig
if [ ! -f %{_prefix}/lib/X11/displaymanagers/dtlogin ]; then
    %{_sbindir}/update-alternatives --remove default-displaymanager \
        %{_prefix}/lib/X11/displaymanagers/dtlogin
fi

%files
%license COPYING
%doc CONTRIBUTORS HISTORY README.md
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/%{name}/
%{_libexecdir}/%{name}/
%{cde_data}/
%{_mandir}/man*/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/fontaliases
%config(noreplace) %{_sysconfdir}/%{name}/fontaliases/fonts.alias
%{_pamdir}/dtlogin
%{_pamdir}/dtsession
%dir %{_sysconfdir}/xinetd.d
%config(noreplace) %{_sysconfdir}/xinetd.d/cmsd
%config(noreplace) %{_sysconfdir}/xinetd.d/ttdbserver
%{_datadir}/xsessions/cde.desktop
%dir %{_prefix}/lib/X11/displaymanagers
%{_prefix}/lib/X11/displaymanagers/dtlogin
%ghost %{_prefix}/lib/X11/displaymanagers/default-displaymanager
%ghost %{_sysconfdir}/alternatives/default-displaymanager
%dir %{_localstatedir}/dt
%dir %{_localstatedir}/dt/appconfig
%dir %{_localstatedir}/dt/appconfig/appmanager
%dir %{_localstatedir}/dt/tmp

%changelog
