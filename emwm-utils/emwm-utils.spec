#
# spec file for package emwm-utils
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           emwm-utils
Version:        2.0
Release:        0
Summary:        Session manager and application launcher for EMWM
License:        MIT
Group:          System/GUI/Other
URL:            https://fastestcode.org/emwm.html
Source0:        https://github.com/alx210/emwm-utils/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-session.desktop
Source2:        README.SUSE
# PATCH-FEATURE-OPENSUSE emwm-utils-lock-command.patch -- lockCommand resource to use an external screen locker
Patch0:         %{name}-lock-command.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  pkgconfig(libxcrypt)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xt)
Requires:       emwm
Requires:       xlockmore
Requires:       xrdb
Suggests:       xscreensaver

%description
Utilities for the Enhanced Motif Window Manager (EMWM):

xmsm is a simple session manager that provides session configuration
and screen locking, and launches the window manager and the toolbox.
xmsession is the X session script that sets up the environment and
starts xmsm.

xmtoolbox is an application launcher/menu configured with a simple
text file. It also talks to the session manager to provide lock,
log out and shutdown commands.

%prep
%autosetup -p1
ln -s ../mf/Makefile.Linux src/Makefile
sed -i \
  -e 's|^CFLAGS = .*|CFLAGS = %{optflags} -Wall -DUNPRIVILEGED_SHUTDOWN|' \
  -e 's|^INCDIRS = .*|INCDIRS =|' \
  -e 's|^LIBDIRS = .*|LIBDIRS =|' \
  mf/Makefile.Linux
# No setuid root: let logind/polkit authorize power management
sed -i \
  -e 's|"/sbin/poweroff"|"%{_bindir}/systemctl poweroff"|' \
  -e 's|"/sbin/reboot"|"%{_bindir}/systemctl reboot"|' \
  -e 's|"/usr/sbin/pm-suspend"|"%{_bindir}/systemctl suspend"|' \
  src/smconf.h
sed -i 's|install -m4755 xmsm|install -m755 xmsm|' src/common.mf
# Lock the screen with xlock (PAM) instead of the setuid built-in locker
echo '*lockCommand: %{_bindir}/xlock -mode blank' >> src/XmSm.ad.src
cp %{SOURCE2} .

%build
%make_build -C src \
  RCDIR=%{_sysconfdir}/X11 \
  LDFLAGS="%{optflags} %{?build_ldflags}"

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_sysconfdir}/X11
%make_install -C src \
  PREFIX=%{buildroot}%{_prefix} \
  MANDIR=%{buildroot}%{_mandir} \
  RCDIR=%{buildroot}%{_sysconfdir}/X11 \
  APPLRESDIR=%{buildroot}%{_datadir}/X11/app-defaults
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/xsessions/%{name}-session.desktop

%files
%license COPYING
%doc README README.SUSE src/toolboxrc
%{_bindir}/xmsession
%{_bindir}/xmtoolbox
%verify(not mode) %{_bindir}/xmsm
%config(noreplace) %{_sysconfdir}/X11/toolboxrc
%dir %{_datadir}/X11/app-defaults
%{_datadir}/X11/app-defaults/XmSm
%{_datadir}/X11/app-defaults/XmToolbox
%{_datadir}/xsessions/%{name}-session.desktop
%{_mandir}/man1/xmsm.1%{?ext_man}
%{_mandir}/man1/xmtoolbox.1%{?ext_man}

%changelog
