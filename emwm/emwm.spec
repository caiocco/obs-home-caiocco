#
# spec file for package emwm
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           emwm
Version:        2.1
Release:        0
Summary:        Enhanced Motif Window Manager
License:        LGPL-2.0-or-later AND MIT
Group:          System/GUI/Other
URL:            https://fastestcode.org/emwm.html
Source0:        https://github.com/alx210/emwm/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xt)

%description
EMWM is a fork of the Motif Window Manager with fixes and enhancements.
It provides compatibility with current X11 desktop environments and
applications: Extended Window Manager Hints (EWMH), Xinerama and XRandR
multi-head support, UTF-8 and Xft (anti-aliased) fonts in window titles,
workspaces, and a session-manager-independent configuration.

%prep
%autosetup
ln -s ../mf/Makefile.Linux src/Makefile
sed -i \
  -e 's|^CFLAGS = .*|CFLAGS = %{optflags}|' \
  -e 's|^INCDIRS = .*|INCDIRS =|' \
  -e 's|^LIBDIRS = .*|LIBDIRS =|' \
  mf/Makefile.Linux
# openSUSE keeps app-defaults in /usr/share/X11
sed -i 's|/etc/X11/app-defaults|%{_datadir}/X11/app-defaults|g' \
  src/emwm.1 src/emwmrc.4

%build
%make_build -C src emwm \
  RCDIR=%{_sysconfdir}/X11 \
  LDFLAGS="%{optflags} %{?build_ldflags}"

%install
install -d %{buildroot}%{_bindir}
%make_install -C src \
  PREFIX=%{buildroot}%{_prefix} \
  MANDIR=%{buildroot}%{_mandir} \
  RCDIR=%{buildroot}%{_sysconfdir}/X11 \
  APPLRESDIR=%{buildroot}%{_datadir}/X11/app-defaults
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/xsessions/%{name}.desktop

%files
%license COPYING
%doc README
%{_bindir}/emwm
%config(noreplace) %{_sysconfdir}/X11/system.emwmrc
%dir %{_datadir}/X11/app-defaults
%{_datadir}/X11/app-defaults/Emwm
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man1/emwm.1%{?ext_man}
%{_mandir}/man4/emwmrc.4%{?ext_man}

%changelog
