#
# spec file for package krunner_recoll
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
Name:           krunner_recoll
Version:        1.46.0
Release:        0
Summary:        KRunner for the Recoll full text search tool
License:        GPL-2.0-or-later
URL:            https://www.recoll.org
Source:         https://www.recoll.org/%{rname}-%{version}.tar.gz
BuildRequires:  recoll-devel = %{version}
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6Runner)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(xapian-core)
Requires:       recoll = %{version}
Supplements:    (plasma6-workspace and recoll)
ExclusiveArch:  %{x86_64} aarch64 riscv64

%description
Recoll is a personal full text search tool.
This package provides the krunner.

%prep
%autosetup -n %{rname}-%{version}

%build
pushd kde/krunner
mv -f CMakeLists-KF6.txt CMakeLists.txt
%cmake_kf6
%kf6_build
popd

%install
pushd kde/krunner
%kf6_install
popd

%files
%dir %{_kf6_plugindir}/kf6/krunner
%{_kf6_plugindir}/kf6/krunner/krunner_recoll.so

%changelog
