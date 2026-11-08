#
# spec file for package antiword
#
# Copyright (c) 2023 SUSE LLC
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


Name:           antiword
Version:        0.37
Release:        0
Summary:        A Free MS Word Reader for Linux and RISC OS
License:        GPL-2.0-or-later
URL:            http://www.winfield.demon.nl/
Source0:        antiword-%{version}.tar.bz2
# PATCH-FIX-UPSTREAM
Patch0:         10_fix_buffer_overflow_wordole_c.patch
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(x11)

%description
Antiword converts the files from Microsoft Word (TM) 6, 7, 97,
2000, and 2003 to plain text and PostScript (TM) format.

%prep
%autosetup -p1

%build
%make_build CFLAGS="%{optflags} -pedantic -DNDEBUG"

%install
chmod 644 Docs/* Resources/*.txt
install -d %{buildroot}/%{_bindir}
install -m 755 antiword %{buildroot}/%{_bindir}
install -m 755 kantiword %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_mandir}/man1
mv Docs/antiword.1 %{buildroot}/%{_mandir}/man1
mkdir -p %{buildroot}/%{_datadir}/antiword
install -m 644 Resources/*.txt %{buildroot}/%{_datadir}/antiword
install -m 644 Resources/fontnames %{buildroot}/%{_datadir}/antiword

%files
%doc Docs/*
%{_bindir}/kantiword
%{_bindir}/antiword
%{_datadir}/antiword
%{_mandir}/man1/antiword.1%{?ext_man}

%changelog
