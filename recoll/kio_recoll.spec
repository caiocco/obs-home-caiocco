#
# spec file for package kio_recoll
#
# Copyright (c) 2026 SUSE LLC and contributors
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

%define rname recoll
Name:           kio_recoll
Version:        1.44.2
Release:        0
Summary:        KIO worker for the Recoll full text search tool
License:        GPL-2.0-or-later
URL:            https://www.recoll.org
Source:         https://www.recoll.org/%{rname}-%{version}.tar.gz
BuildRequires:  recoll-devel = %{version}
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(xapian-core)
Requires:       recoll = %{version}
Supplements:    (dolphin and recoll)
ExclusiveArch:  %{x86_64} aarch64 riscv64

%description
Recoll is a personal full text search tool.
This package provides the kio worker.

%prep
%autosetup -n %{rname}-%{version}

%build
pushd kde/kioslave/kio_recoll
mv -f CMakeLists-KF6.txt CMakeLists.txt
%cmake_kf6
%kf6_build
popd

%install
pushd kde/kioslave/kio_recoll
%kf6_install
popd

%files
%{_kf6_plugindir}/kf6/kio/kio_recoll.so
%{_datadir}/kio_recoll/

%changelog
