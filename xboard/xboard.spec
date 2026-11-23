#
# spec file for package xboard
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


Name:           xboard
Version:        4.9.1
Release:        0
Summary:        X Window System Interface for playing chess
License:        GPL-3.0-or-later
Group:          Amusements/Games/Board/Chess
URL:            http://www.gnu.org/software/xboard/
Source:         http://ftp.gnu.org/pub/gnu/xboard/%{name}-%{version}.tar.gz
Source2:        http://ftp.gnu.org/pub/gnu/xboard/%{name}-%{version}.tar.gz.sig
# https://pgp.mit.edu
Source3:        xboard.keyring
# PATCH-FIX-OPENSUSE xboard-prefer-gnuchess.patch
Patch0:         xboard-prefer-gnuchess.patch
BuildRequires:  cairo-devel
BuildRequires:  gpg2
BuildRequires:  gtk2-devel >= 2.20.0
BuildRequires:  librsvg-devel
BuildRequires:  pango-devel
BuildRequires:  pkgconfig
BuildRequires:  texinfo
BuildRequires:  texlive-latex
BuildRequires:  update-desktop-files
BuildRequires:  xdg-utils
BuildRequires:  xorg-x11-libXt-devel
%if %{?suse_version} < 1330
BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info
%endif
Requires:       chess_backend
Requires(post): %{install_info_prereq}
Requires(preun): %{install_info_prereq}
Recommends:     gnuchess

%description
XBoard is a graphical user interface for chess in all its major forms, including international chess, xiangqi (Chinese chess), shogi Japanese chess) and Makruk, in addition to many minor variants such as Losers Chess, Crazyhouse, Chess960 and Capabanca Chess. It displays a chessboard on the screen, accepts moves made with the mouse, and loads and saves games in Portable Game Notation (PGN). It serves as a front-end for many different chess services, including:

    * Chess engines that will run on your machine and play a game against you or help you analyze, such as GNU Chess, Crafty, or many others.

    * Chess servers on the Internet, where you can connect to play chess with people from all over the world, watch other users play, or just hang out and chat.

    * Correspondence chess played by electronic mail. The CMail program automates the tasks of parsing email from your opponent, playing his moves out on your board, and mailing your reply move after you have chosen it.

%prep
# Check the upstream signature against the xboard keyring
export GNUPGHOME=$(mktemp -d)
gpg --batch --quiet --import %{SOURCE3}
gpg --batch --verify %{SOURCE2} %{SOURCE0}
%setup -q
%patch -P 0 -p1

%build
export CFLAGS="%{optflags} -fcommon"
%configure --disable-silent-rules --enable-zippy --disable-update-mimedb
make %{?_smp_mflags}

%install
%make_install
%find_lang %{name} %{name}.lang
mkdir -p  %{buildroot}/%{_datadir}/icons/hicolor/32x32/mimetypes
mkdir -p  %{buildroot}/%{_datadir}/icons/hicolor/48x48/mimetypes
mv %{buildroot}/%{_datadir}/games/xboard/pixmaps/textures/ini32.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/mimetypes/application-x-chess-opt.png
mv %{buildroot}/%{_datadir}/games/xboard/pixmaps/textures/ini48.png %{buildroot}/%{_datadir}/icons/hicolor/48x48/mimetypes/application-x-xboard-opt.png
mv %{buildroot}/%{_datadir}/games/xboard/pixmaps/textures/board32.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/mimetypes/application-x-chess-pgn.png
mv %{buildroot}/%{_datadir}/games/xboard/pixmaps/textures/cross32.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/mimetypes/application-x-xboard-trn.png
mv %{buildroot}/%{_datadir}/games/xboard/pixmaps/textures/board48.png %{buildroot}/%{_datadir}/icons/hicolor/48x48/mimetypes/application-x-chess-pgn.png
mv %{buildroot}/%{_datadir}/games/xboard/pixmaps/textures/cross48.png %{buildroot}/%{_datadir}/icons/hicolor/48x48/mimetypes/application-x-xboard-trn.png
%suse_update_desktop_file -i %{name} Game BoardGame
%suse_update_desktop_file -i -u %{name}-tourney Game BoardGame
%suse_update_desktop_file -i -u %{name}-pgn-viewer Game BoardGame
%suse_update_desktop_file -i -u %{name}-fen-viewer Game BoardGame

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz
%if %{?suse_version} < 1330
%mime_database_post
%desktop_database_post
%icon_theme_cache_post
%endif

%preun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%if %{?suse_version} < 1330
%postun
%mime_database_postun
%desktop_database_postun
%icon_theme_cache_postun
%endif

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog COPYRIGHT FAQ.html DIFFSTAT SHORTLOG NEWS README TODO engine-intf.html ics-parsing.txt readme.htm zippy.README
%{_bindir}/*
%{_mandir}/man6/*.*
%{_infodir}/xboard.info%{?ext_info}
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*.xml
%dir %{_datadir}/games/xboard
%dir %{_datadir}/games/xboard/sounds/
%dir %{_datadir}/games/xboard/themes
%dir %{_datadir}/games/xboard/themes/conf/
%dir %{_datadir}/games/xboard/themes/default/
%dir %{_datadir}/games/xboard/themes/shogi/
%dir %{_datadir}/games/xboard/themes/xiangqi/
%dir %{_datadir}/games/xboard/themes/textures/
%{_datadir}/games/xboard/sounds/*
%{_datadir}/games/xboard/themes/conf/*
%{_datadir}/games/xboard/themes/default/*svg
%{_datadir}/games/xboard/themes/shogi/*svg
%{_datadir}/games/xboard/themes/xiangqi/*svg
%{_datadir}/games/xboard/themes/textures/*png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/icons/hicolor/48x48/mimetypes/*png
%{_datadir}/icons/hicolor/32x32/mimetypes/*png
%config %{_sysconfdir}/%{name}.conf

%changelog
