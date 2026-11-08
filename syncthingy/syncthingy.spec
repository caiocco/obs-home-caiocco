#
# spec file for package syncthingy
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Upstream targets Flatpak and Qt 5 only. syncthingy-qt6.patch builds it
# with Qt 6 (Leap 16.0 has no libportal-qt5) and drops libportal, which a
# native build does not need. syncthingy-native.patch replaces the portal
# calls: URIs are opened with QDesktopServices, autostart is an entry in
# ~/.config/autostart instead of the Background portal, the tray icons are
# looked up under the installed app ID, and the "service" dialog points to
# the syncthing.service user unit shipped by the syncthing package.
# SingleApplication (a git submodule upstream) is bundled.
#

%define appid           com.github.zocker_160.SyncThingy
%define singleapp_commit f1e15081dc57a9c03f7f4f165677f18802e1437a

Name:           syncthingy
Version:        1.0
Release:        0
Summary:        Syncthing with a simple tray indicator
License:        GPL-3.0-only AND MIT
Group:          Productivity/Networking/Other
URL:            https://github.com/zocker-160/SyncThingy
Source0:        https://github.com/zocker-160/SyncThingy/archive/refs/tags/%{version}.tar.gz#/SyncThingy-%{version}.tar.gz
Source1:        https://github.com/itay-grudev/SingleApplication/archive/%{singleapp_commit}.tar.gz#/SingleApplication-f1e1508.tar.gz
Patch0:         syncthingy-qt6.patch
Patch1:         syncthingy-native.patch
BuildRequires:  appstream-glib
BuildRequires:  cmake >= 3.16
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Widgets)
Requires:       syncthing
Provides:       bundled(SingleApplication)
Obsoletes:      qsyncthingtray < 0.5.9

%description
SyncThingy is a minimal tray indicator for Syncthing. It starts Syncthing
(or attaches to an instance already running, e.g. the syncthing.service
user unit), shows a tray icon and opens the Syncthing web UI.

%prep
%autosetup -p1 -n SyncThingy-%{version}
rmdir src/singleapplication 2>/dev/null || :
mkdir -p src/singleapplication
tar xzf %{SOURCE1} -C src/singleapplication --strip-components=1

%build
%cmake -DBUILD_SHARED_LIBS=OFF
%cmake_build

%install
%cmake_install
cp src/singleapplication/LICENSE LICENSE.SingleApplication

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{appid}.metainfo.xml

%files
%license LICENSE LICENSE.SingleApplication
%doc README.md
%{_bindir}/SyncThingy
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{appid}*.png
%{_datadir}/metainfo/%{appid}.metainfo.xml

%changelog
