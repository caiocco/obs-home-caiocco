#
# spec file for package doublecmd
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define commit  225ec86

Name:           doublecmd
Version:        1.2.11
Release:        0
Summary:        Twin-panel (commander-style) file manager
License:        GPL-2.0-or-later AND LGPL-2.0-or-later WITH Classpath-exception-2.0
Group:          Productivity/File utilities
URL:            https://doublecmd.sourceforge.io/
Source0:        https://github.com/doublecmd/doublecmd/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# PATCH-FIX-UPSTREAM TCustomGrid.TrySmoothScrollBy only exists in Lazarus 4
Patch0:         doublecmd-lazarus3-thumbview-scroll.patch
BuildRequires:  fdupes
BuildRequires:  fpc >= 3.2.0
BuildRequires:  fpc-src
BuildRequires:  lazarus-ide
BuildRequires:  lazarus-lcl-gtk2 >= 3.0
BuildRequires:  lazarus-lcl-nogui
BuildRequires:  lazarus-lcl-qt6 >= 3.0
BuildRequires:  lazarus-tools
BuildRequires:  libQt6Pas-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
ExclusiveArch:  x86_64 aarch64 %{ix86}

%description
Double Commander is a cross platform open source file manager with two
panels side by side. It is inspired by Total Commander and features
some new ideas.

%package gtk
Summary:        Twin-panel (commander-style) file manager (GTK 2)
Group:          Productivity/File utilities
Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-qt
RemovePathPostfixes: .gtk

%description gtk
Double Commander is a cross platform open source file manager with two
panels side by side. It is inspired by Total Commander and features
some new ideas.

This package contains the GTK 2 build.

%package qt
Summary:        Twin-panel (commander-style) file manager (Qt 6)
Group:          Productivity/File utilities
Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-gtk
RemovePathPostfixes: .qt

%description qt
Double Commander is a cross platform open source file manager with two
panels side by side. It is inspired by Total Commander and features
some new ideas.

This package contains the Qt 6 build.

%prep
%autosetup -p1

# Version information shown in the About dialog
cat > units/dcrevision.inc <<EOF
// Created by Git2RevisionInc
const dcRevision = 'Unknown';
const dcCommit = '%{commit}';
EOF

# Build the two widgetsets in separate trees
cd ..
rm -rf %{name}-%{version}-qt
cp -a %{name}-%{version} %{name}-%{version}-qt

%build
mkdir -p ../lazhome-gtk ../lazhome-qt
export HOME=$(pwd)/../lazhome-gtk
./build.sh release gtk2

cd ../%{name}-%{version}-qt
export HOME=$(pwd)/../lazhome-qt
./build.sh release qt6

%install
# GTK 2 tree
install/linux/install.sh --install-prefix=%{buildroot}

# Qt 6 tree in a scratch root, keeping only the widgetset dependent files
qtroot=$(pwd)/../qtroot
rm -rf $qtroot
pushd ../%{name}-%{version}-qt
install/linux/install.sh --install-prefix=$qtroot
popd
for f in doublecmd doublecmd.zdli plugins/wlx/wlxmplayer/wlxmplayer.wlx; do
  mv %{buildroot}%{_libdir}/%{name}/$f %{buildroot}%{_libdir}/%{name}/$f.gtk
  cp -p $qtroot%{_libdir}/%{name}/$f %{buildroot}%{_libdir}/%{name}/$f.qt
done
rm -rf $qtroot

# The binary only gets its final name at packaging time
# (RemovePathPostfixes), so use a wrapper instead of a symlink
rm %{buildroot}%{_bindir}/%{name}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
exec %{_libdir}/%{name}/%{name} "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Privileged operations fall back to the generic pkexec action
rm -rf %{buildroot}%{_datadir}/polkit-1

# Licenses are packaged with %%license
rm -f %{buildroot}%{_datadir}/%{name}/doc/COPYING*.txt

%fdupes -s %{buildroot}%{_datadir}

%files gtk
%license doc/COPYING*.txt
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{name}.gtk
%{_libdir}/%{name}/%{name}.zdli.gtk
%{_libdir}/%{name}/%{name}.help
%{_libdir}/%{name}/pinyin.tbl
%{_libdir}/%{name}/default
%{_libdir}/%{name}/doc
%{_libdir}/%{name}/highlighters
%{_libdir}/%{name}/language
%{_libdir}/%{name}/pixmaps
%{_libdir}/%{name}/scripts
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/dsx
%{_libdir}/%{name}/plugins/wcx
%{_libdir}/%{name}/plugins/wdx
%{_libdir}/%{name}/plugins/wfx
%dir %{_libdir}/%{name}/plugins/wlx
%dir %{_libdir}/%{name}/plugins/wlx/wlxmplayer
%{_libdir}/%{name}/plugins/wlx/wlxmplayer/wlxmplayer.wlx.gtk
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}.1%{?ext_man}

%files qt
%license doc/COPYING*.txt
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{name}.qt
%{_libdir}/%{name}/%{name}.zdli.qt
%{_libdir}/%{name}/%{name}.help
%{_libdir}/%{name}/pinyin.tbl
%{_libdir}/%{name}/default
%{_libdir}/%{name}/doc
%{_libdir}/%{name}/highlighters
%{_libdir}/%{name}/language
%{_libdir}/%{name}/pixmaps
%{_libdir}/%{name}/scripts
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/dsx
%{_libdir}/%{name}/plugins/wcx
%{_libdir}/%{name}/plugins/wdx
%{_libdir}/%{name}/plugins/wfx
%dir %{_libdir}/%{name}/plugins/wlx
%dir %{_libdir}/%{name}/plugins/wlx/wlxmplayer
%{_libdir}/%{name}/plugins/wlx/wlxmplayer/wlxmplayer.wlx.qt
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}.1%{?ext_man}

%changelog
