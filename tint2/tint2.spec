#
# spec file for package tint2
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           tint2
Version:        17.1.3
Release:        0
Summary:        A lightweight X11 desktop panel and task manager
License:        GPL-2.0-only
Group:          System/X11/Utilities
URL:            https://gitlab.com/nick87720z/tint2
Source0:        https://gitlab.com/nick87720z/%{name}/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# PATCH-FIX-UPSTREAM tint2-glib-list-copy.patch nick87720z/tint2#4 -- iterate over copies of lists the callbacks modify (segfault with glib >= 2.76; from X11:Utilities)
Patch0:         %{name}-glib-list-copy.patch
# PATCH-FIX-UPSTREAM tint2-cmake4.patch nick87720z/tint2#8 -- cmake_minimum_required ranges accepted by CMake 4 (Debian #1113576)
Patch1:         %{name}-cmake4.patch
# PATCH-FIX-UPSTREAM tint2conf-libm.patch -- tint2conf uses libm too (Debian #1082699)
Patch2:         tint2conf-libm.patch
# PATCH-FIX-UPSTREAM tint2-null-x-events.patch nick87720z/tint2#5 -- ignore pointer/key events for windows that are not a panel (crash with Conky; from Arch)
Patch3:         %{name}-null-x-events.patch
# PATCH-FIX-OPENSUSE tint2-expand-exec-overflow.patch -- build launcher Exec expansion in a GString (fixed buffer overflow and _FORTIFY_SOURCE=3 abort; based on Arch fix_fortify_source_crash.patch)
Patch4:         %{name}-expand-exec-overflow.patch
# PATCH-FIX-UPSTREAM tint2-systray-workarea-fixes.patch -- read tray _NET_WM_PID as format 32, free filtered icon names, validate _NET_WORKAREA (from Arch tint2.patch)
Patch5:         %{name}-systray-workarea-fixes.patch
# PATCH-FIX-UPSTREAM tint2-icon-cache-save.patch nick87720z/tint2#6 -- open the icon cache for writing (was never saved) and stop closing fds twice
Patch6:         %{name}-icon-cache-save.patch
# PATCH-FIX-UPSTREAM tint2-multi-desktop-switch.patch nick87720z/tint2#2 -- revert fd30b3ad: clicking a task on another desktop switches to it again
Patch7:         %{name}-multi-desktop-switch.patch
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
# project() declares no LANGUAGES, so CMake also looks for a C++ compiler
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-x11-3.0)
BuildRequires:  pkgconfig(imlib2)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)

%description
tint2 is a simple panel/taskbar made for modern X window managers. It was
specifically made for Openbox3 but should also work with other window
managers. It has a taskbar, system tray, clock, battery monitor, launcher
and executors, and comes with tint2conf, a GTK theme editor.

This is the continuation of tint2 maintained by nick87720z.

%lang_package

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%cmake \
  -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name}
%cmake_build

%install
%cmake_install

# tint2 itself is started from the session, not from the menu
desktop-file-install \
  --set-key=NoDisplay --set-value=true \
  --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/tint2.desktop

# man page written for Debian, shipped in the tarball
install -Dpm 0644 packaging/debian/tint2conf.1 %{buildroot}%{_mandir}/man1/tint2conf.1

%find_lang tint2conf

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/tint2.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/tint2conf.desktop

%files
%license COPYING
%doc %{_docdir}/%{name}/
%dir %{_sysconfdir}/xdg/tint2
%config(noreplace) %{_sysconfdir}/xdg/tint2/tint2rc
%{_bindir}/tint2
%{_bindir}/tint2-send
%{_bindir}/tint2conf
%{_datadir}/tint2/
%{_datadir}/applications/tint2.desktop
%{_datadir}/applications/tint2conf.desktop
%{_datadir}/icons/hicolor/scalable/apps/tint2.svg
%{_datadir}/icons/hicolor/scalable/apps/tint2conf.svg
%{_datadir}/mime/packages/tint2conf.xml
%{_mandir}/man1/tint2.1%{?ext_man}
%{_mandir}/man1/tint2conf.1%{?ext_man}

%files lang -f tint2conf.lang

%changelog
