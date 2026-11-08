#
# spec file for package wine-mono
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           wine-mono
Version:        11.3.0
Release:        0
Summary:        A .NET replacement for use by Wine
License:        LGPL-2.1 and MIT and MS-PL
Group:          Development/Tools/Other
Url:            https://github.com/madewokherd/wine-mono
#Source:         https://downloads.sourceforge.net/project/wine/Wine%20Mono/%{version}/wine-mono-%{version}.tar.gz
#Source1:        http://dl.winehq.org/wine/wine-mono/%{version}/wine-mono-%{version}-x86.msi
Source2:        https://dl.winehq.org/wine/wine-mono/%{version}/wine-mono-%{version}-x86.tar.xz
# upstream patch to fix build
# https://github.com/mono/mono/commit/c79a76411a8ea0d66e98a4394e6906b2f27be746
#Patch0:         fix.patch
#BuildRequires:  autoconf
#BuildRequires:  p7zip
#BuildRequires:  automake
#BuildRequires:  gcc gcc-c++
#BuildRequires:  libtool
#BuildRequires:  libgdiplus-devel
#BuildRequires:  mingw32-gcc mingw32-cross-gcc mingw64-gcc mingw64-cross-gcc
#BuildRequires:  mono-complete mono-devel
#BuildRequires:  pkgconfig
#%ifnarch ia64 %arm
#BuildRequires:  valgrind-devel
#%endif
#BuildRequires:  wine wine-devel
#BuildRequires:  xorg-x11-libX11-devel
Requires:       wine
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
This package contains the prepackaged Windows Mono Runtime environment
for use by Wine.

%prep


%build
#export MAKEOPTS=%{?_smp_mflags}
# used by buildscript
#export TZ=UTC
#./build-winemono.sh

%install
mkdir -p %{buildroot}%{_datadir}/wine/mono
# we use the prebuilt binaries: wine-mono-VERSION-ARCH.msi
# MSI is not needed if we have the unpacked tree
#cp -a %{SOURCE1} %{buildroot}%{_datadir}/wine/mono/
# and the actual binaries unpacked
tar xf %{SOURCE2} -C %{buildroot}%{_datadir}/wine/mono/


%files
%defattr(-, root, root)
%dir %{_datadir}/wine
%dir %{_datadir}/wine/mono
%{_datadir}/wine/mono/*

%changelog
