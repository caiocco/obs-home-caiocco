#
# spec file for package orbitiny-desktop
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

# Orbitiny resolves its resources relative to an install directory that
# must be called "orbitiny" (see common::get_install_dir()) and expects
# its programs in <appdir>/usr/bin. Data goes to /usr/share/orbitiny and
# the panel plugins to /usr/lib64/orbitiny, linked into that directory
%define appdir %{_libexecdir}/orbitiny
%define orbdatadir %{_datadir}/orbitiny
%define plugindir %{_libdir}/orbitiny/plugins
%define data_release pilotx5e
Name:           orbitiny-desktop
Version:        1.0~pilotx5e+git20261107.4d5ba1d
Release:        0
Summary:        Qt-based desktop environment with panel, desktop and file manager
License:        BSD-3-Clause AND GPL-2.0-or-later
Group:          System/GUI/Other
URL:            https://orbitiny.com
# git archive of https://gitea.com/sasko.usinov/orbitiny-desktop commit 4d5ba1d
# ("1.0 Pilot X (R5E) Source Code")
Source0:        %{name}-%{version}.tar.xz
# Default settings, themes, wallpapers and templates (data/, shared/ and
# desktop-files/) taken from the upstream binary release
# https://sourceforge.net/projects/orbitiny-desktop/files/orbitiny-bin-release.tar.gz
# with every binary removed; they are not part of the git repository
Source1:        orbitiny-data-%{data_release}.tar.xz
Source2:        orbitiny-session
Source3:        orbitiny.desktop
Source4:        qutiny.desktop
Source99:       %{name}-rpmlintrc
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  qt6-base-common-devel
BuildRequires:  cmake(Qt6Charts)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(dconf)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-mainloop-glib)
BuildRequires:  pkgconfig(sigc++-2.0)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-damage)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xtst)
Requires:       /usr/bin/pactl
Requires:       udisks2
Requires:       util-linux
Requires:       wmctrl
Requires:       xdotool
Requires:       xinput
Requires:       xprop
Requires:       xrandr
Requires:       xrdb
Requires:       xset
Recommends:     numlockx
Recommends:     xfwm4
Recommends:     xsettingsd
Provides:       orbitiny = %{version}
Provides:       qutiny = %{version}

%description
Orbitiny Desktop is a lightweight, portable desktop environment written
from scratch in Qt for X11. It provides a desktop with icons and
independent per-screen desktops, a panel with plugins (application
menu, quick launch, window list, system tray, desktop switcher, clock,
audio and battery applets), the Qutiny file manager, a search tool, a
device manager, a screenshot grabber, screen and brightness
configuration and a control center. It runs on top of an existing
window manager such as xfwm4, marco or openbox.

Use the "Orbitiny" session in the display manager, or run start-orbitiny
inside another session. Settings are kept in ~/.config/orbitiny.

This package is built from the 1.0 Pilot X (Release 5E) source code.

%prep
%autosetup -p1
mkdir orbitiny-data
tar -xf %{SOURCE1} -C orbitiny-data --strip-components=1

# Debian multiarch paths, and libexplain (only included, never called)
find . -name '*.pro' -exec sed -i \
  -e 's|/usr/lib/x86_64-linux-gnu|%{_libdir}|g' \
  -e '/-lexplain/d' {} +
grep -rl 'libexplain/read.h' . | xargs sed -i '/libexplain\/read.h/d'

# Launch scripts: use the system Qt instead of bundled libraries, point
# the helper variables (as set by the binary release) to the system
# tools and don't try to delete files inside the read-only install
# directory
sed -i \
  -e '/LD_LIBRARY_PATH/d' \
  -e '/QT_PLUGIN_PATH/d' \
  -e '/QT_QPA_PLATFORM_PLUGIN_PATH/d' \
  -e '/QT_DEBUG_PLUGINS/d' \
  -e 's|^rm \$HOME/|rm -f $HOME/|' \
  -e '/^rm \$DIR\//d' \
  -e 's|^export ORBITINY_RELEASE_STATUS=1$|&\
export ORBITINY_XINPUT=${ORBITINY_XINPUT:-%{_bindir}/xinput}\
export ORBITINY_XSETTINGSD=${ORBITINY_XSETTINGSD:-%{_bindir}/xsettingsd}\
export ORBITINY_NUMLOCKX=${ORBITINY_NUMLOCKX:-%{_bindir}/numlockx}\
export ORBITINY_XRDB=${ORBITINY_XRDB:-%{_bindir}/xrdb}\
export ORBITINY_XSET=${ORBITINY_XSET:-%{_bindir}/xset}|' \
  scripts/*

# Load the panel plugins from the installed directory instead of a copy
# in ~/.config/orbitiny, which would go stale on every update
sed -i 's|\(get_local_app_plugins_dir *() *{return \).*;}|\1std::string("%{plugindir}");}|' \
  libui/common_data.h
grep -q 'get_local_app_plugins_dir.*"%{plugindir}"' libui/common_data.h

# Desktop and panel create ~/.config/orbitiny/data at the same time on
# first run; an existing directory must not abort the recursive mkdir
sed -i -e 's|if (mkdir(dir_path.c_str(), 0755) == 0)|if (mkdir(dir_path.c_str(), 0755) == 0 \|\| errno == EEXIST)|' \
  -e '0,/^#include <sys\/stat.h>/s//&\n#include <cerrno>/' \
  lib/libsources/fs.cpp
grep -q 'errno == EEXIST)' lib/libsources/fs.cpp

# Only scripts are executable; the themes ship CSS files with +x
find orbitiny-data -type f -exec sh -c \
  'for f; do if [ "$(head -c2 "$f")" = "#!" ]; then chmod 0755 "$f"; else chmod 0644 "$f"; fi; done' sh {} +

%build
# Programs in <appdir>/usr/bin
apps="orbitiny-dm orbitiny-panel orbitiny-desktop qutiny orbitiny-search
      orbitiny-brightness orbitiny-file-copier orbitiny-file-properties
      orbitiny-screen-config orbitiny-screenshot-grabber
      orbitiny-task-switcher process-sentinel mimetype/mimetype
      control-panel/control_panel_view"
# Programs in <appdir>/usr/bin/orbitiny-control-panel.d
cpanel="appearance autostart context_menus cursor_themes empty_area_clicks
        general_config gtk_icons gtk_styles keyboard_config
        keyboard_shortcuts left_button_gestures marco_themes middle_clicks
        pointer_config preferred_apps right_button_gestures
        supported_archives wallpaper_config xfwm4_themes"
# Panel plugins (dlopen()ed, so no -Wl,--no-undefined)
plugins="app_menu audiocontrol battery_monitor blockdev cpu_load
         desktop_switcher dirbrowser drawer launcher output_monitor places
         quicklaunch run_button screenres separator spacer systray_area
         timedate window_list"

build_pro() {
  local pro=$1 extra=$2 dir=build/$(echo $1 | tr / _)
  mkdir -p $dir
  pushd $dir
  %{_qt6_bindir}/qmake ../../$pro.pro \
    QMAKE_CFLAGS="%{optflags}" \
    QMAKE_CXXFLAGS="%{optflags}" \
    QMAKE_LFLAGS="%{?build_ldflags} -Wl,--as-needed $extra"
  %make_build
  popd
}

for p in $apps orbitiny-pavucontrol; do build_pro $p; done
for p in $cpanel; do build_pro control-panel/$p; done
# The plugins reference symbols that are never defined anywhere (declared
# but unimplemented slots, run::run_shell_script, combo_box, ...) on code
# paths that are never reached; upstream relies on lazy binding. With the
# distribution's -z now, dlopen() fails and the panel comes up empty.
for p in $plugins; do build_pro orbitiny-panel-plugins/$p "-Wl,-z,lazy"; done

%install
install -d %{buildroot}%{appdir}/usr/bin/orbitiny-control-panel.d \
           %{buildroot}%{plugindir} %{buildroot}%{orbdatadir}

# Binaries
for d in build/*; do
  case $d in
    build/orbitiny-panel-plugins_*)
      install -m0755 $d/lib*.so.1.0.0 %{buildroot}%{plugindir}/ ;;
    build/control-panel_control_panel_view)
      install -m0755 $d/orbitiny-control-panel %{buildroot}%{appdir}/usr/bin/ ;;
    build/control-panel_*|build/orbitiny-pavucontrol)
      find $d -maxdepth 1 -type f -perm -u+x -name 'orbitiny-*' \
        -exec install -m0755 {} %{buildroot}%{appdir}/usr/bin/orbitiny-control-panel.d/ \; ;;
    *)
      find $d -maxdepth 1 -type f -perm -u+x \( -name 'orbitiny-*' -o -name qutiny -o -name mimetype \) \
        -exec install -m0755 {} %{buildroot}%{appdir}/usr/bin/ \; ;;
  esac
done

# Launch scripts
for s in scripts/*; do
  [ "$(basename $s)" = install-orbitiny ] && continue
  install -m0755 $s %{buildroot}%{appdir}/
done

# Default configuration copied to ~/.config/orbitiny on first run
cp -a orbitiny-data/{data,shared,desktop-files} %{buildroot}%{orbdatadir}/
for d in data shared desktop-files; do
  ln -s %{orbdatadir}/$d %{buildroot}%{appdir}/$d
done
# The panel loads its plugins from %%{plugindir} (see %%prep)
rmdir %{buildroot}%{orbdatadir}/data/orbitiny-panel.d/plugins.d

# Commands in the PATH
install -d %{buildroot}%{_bindir}
for c in start-orbitiny qutiny orbitiny-control-panel orbitiny-search \
         orbitiny-screenshot-grabber; do
  printf '#!/bin/sh\nexec %{appdir}/%s "$@"\n' $c > %{buildroot}%{_bindir}/$c
  chmod 0755 %{buildroot}%{_bindir}/$c
done
sed -e 's|@APPDIR@|%{appdir}|g' %{SOURCE2} > %{buildroot}%{_bindir}/orbitiny-session
chmod 0755 %{buildroot}%{_bindir}/orbitiny-session

install -Dm0644 %{SOURCE3} %{buildroot}%{_datadir}/xsessions/orbitiny.desktop
install -Dm0644 %{SOURCE4} %{buildroot}%{_datadir}/applications/qutiny.desktop

%fdupes -s %{buildroot}%{orbdatadir}

%files
%license LICENSE
%doc README.md orbitiny-data/release_notes.txt
%{_bindir}/orbitiny-control-panel
%{_bindir}/orbitiny-screenshot-grabber
%{_bindir}/orbitiny-search
%{_bindir}/orbitiny-session
%{_bindir}/qutiny
%{_bindir}/start-orbitiny
%{appdir}
%dir %{_libdir}/orbitiny
%{plugindir}
%{orbdatadir}
%dir %{_datadir}/xsessions
%{_datadir}/xsessions/orbitiny.desktop
%{_datadir}/applications/qutiny.desktop

%changelog
