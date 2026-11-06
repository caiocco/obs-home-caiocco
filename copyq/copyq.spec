#
# spec file for package copyq
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Built with Qt 6 and KDE Frameworks 6: native notifications and tray via
# KStatusNotifierItem, Wayland clipboard access through KGuiAddons.  Audio
# playback is disabled because miniaudio is not packaged for Leap 16.0.
#

Name:           copyq
Version:        17.0.0
Release:        0
Summary:        Clipboard manager with advanced features
License:        GPL-3.0-or-later
Group:          Productivity/Text/Utilities
URL:            https://hluk.github.io/CopyQ/
Source0:        https://github.com/hluk/CopyQ/releases/download/v%{version}/CopyQ-%{version}.tar.gz
BuildRequires:  cmake >= 3.16
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  kf6-extra-cmake-modules
BuildRequires:  pkgconfig
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6StatusNotifierItem)
BuildRequires:  cmake(Qca-qt6)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Keychain)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xtst)
# encrypted tabs need the OpenSSL backend of QCA at runtime
Requires:       qca-qt6-plugins

%description
CopyQ is an advanced clipboard manager with editing and scripting
features.  It monitors the system clipboard and saves its content in
customizable tabs.  Saved clipboard items can later be copied and pasted
directly into any application.

Features include support for text, HTML, images and other formats,
searching and filtering, a Vim-like editor, tab encryption, global
shortcuts and a command line interface with a JavaScript-like scripting
language.

%package -n gnome-shell-extension-copyq-clipboard
Summary:        GNOME Shell extension for CopyQ clipboard monitoring
Group:          System/GUI/GNOME
Requires:       %{name} = %{version}-%{release}
Requires:       gnome-shell
Supplements:    (%{name} and gnome-shell)
BuildArch:      noarch

%description -n gnome-shell-extension-copyq-clipboard
GNOME Shell extension that forwards clipboard changes to CopyQ.  It is
required for clipboard monitoring on GNOME Wayland sessions.

%prep
%autosetup -n CopyQ-%{version}

%build
%cmake \
    -DWITH_TESTS=OFF \
    -DWITH_AUDIO=OFF \
    -DPLUGIN_INSTALL_PREFIX=%{_libdir}/copyq/plugins
%cmake_build

%install
%cmake_install
%fdupes %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.github.hluk.copyq.desktop

%files
%license LICENSE
%doc AUTHORS CHANGES.md README.md
%{_bindir}/copyq
%{_libdir}/copyq/
%{_datadir}/copyq/
%{_datadir}/applications/com.github.hluk.copyq.desktop
%{_datadir}/metainfo/com.github.hluk.copyq.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/copyq*.png
%{_datadir}/icons/hicolor/scalable/apps/copyq*.svg
%{_datadir}/bash-completion/completions/copyq
%{_mandir}/man1/copyq.1%{?ext_man}

%files -n gnome-shell-extension-copyq-clipboard
%dir %{_datadir}/gnome-shell
%dir %{_datadir}/gnome-shell/extensions
%{_datadir}/gnome-shell/extensions/copyq-clipboard@hluk.github.com/

%changelog
