# spec file for package harvid
#
# Copyright (c) 2020 Fabio Pesari
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
# Please submit bugfixes or comments via http://bugs.opensuse.org/

Name:          harvid
Version:       0.9.1
Release:       0
Summary:       Decode still images from videos and serve them via HTTP
License:       GPL-2.0
Group:         Productivity/Multimedia/Video/Editors and Convertors
URL:           https://x42.github.io/harvid/
Source0:       %{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
BuildRequires: vim
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(jack)
BuildRequires: pkgconfig(libpng)
BuildRequires: ffmpeg-devel

%description
Harvid decodes still images from movie files and serves them
via HTTP.

Its intended use-case is to efficiently provide frame-accurate data
and act as second level cache for rendering the video-timeline in
Ardour.

%prep
%setup -q

%build
make PREFIX=%{_prefix} -j1

%install
%make_install PREFIX=%{_prefix}

%files
%doc README.md
%license COPYING
%{_bindir}/harvid
%{_mandir}/man1/harvid.1.gz

%changelog
