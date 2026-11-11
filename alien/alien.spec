#
# spec file for package alien
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


Name:           alien
Version:        8.95.8
Release:        0
License:        GPL-2.0-or-later
Summary:        Perl Script to Convert Packages
URL:            https://sourceforge.net/projects/alien-pkg-convert/
Group:          System/Packages
Source0:        alien_%{version}.tar.xz
Patch0:         alien-strip-tilde-from-version.patch
BuildRequires:  deb
BuildRequires:  debhelper
Requires:       cpio
Requires:       deb
Requires:       make
Requires:       perl = %{perl_version}
Requires:       rpm
Requires:       rpm-build
BuildArch:      noarch

%description
Experimental Perl script to convert software packages. The following
formats are supported: deb (Debian), rpm (Red Hat), and tgz (Slackware).

%prep
%autosetup -p1 -n alien

%build
perl Makefile.PL
%make_build

%install
%perl_make_install
%make_install PREFIX=%{buildroot}%{_prefix} VARPREFIX=%{buildroot}
%perl_process_packlist

# rpmlint screams when we have something in sitelib (badness: 10000)
rm -r %buildroot/%perl_sitelib/

%files
%license GPL
%doc README TODO gendiff.txt debian/changelog
%doc %{_mandir}/man?/*
%{_bindir}/%{name}
%{perl_vendorlib}/Alien

%changelog
