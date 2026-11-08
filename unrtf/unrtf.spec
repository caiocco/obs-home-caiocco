#
# spec file for package unrtf
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2017 Asterios Dramis <asterios.dramis@gmail.com>.
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


Name:           unrtf
Version:        0.21.13
Release:        0
Summary:        Rich Text Format (.rtf) Document Converter to Other Formats
License:        GPL-3.0-or-later
URL:            http://www.gnu.org/software/unrtf/
Source0:        http://ftp.gnu.org/gnu/unrtf/%{name}-%{version}.tar.gz
# PATCH-FIX-OPENSUSE unrtf-0.21.2-fix_dirs.patch lazy.kent@opensuse.org -- Fix hardcoded paths
Patch0:         unrtf-0.21.2-fix_dirs.patch
BuildRequires:  autoconf
BuildRequires:  automake

%description
UnRTF is a command-line program written in C which converts documents in Rich
Text Format (.rtf) to HTML, LaTeX, troff macros, and RTF itself.

%prep
%autosetup -p1

# Fix config dir
sed -i -e 's#CONFIG_DIR PKGDATADIR#CONFIG_DIR \"%{_sysconfdir}/unrtf\"#' src/main.h

%build
# Regenerate build system because of the following error:
# "configure: error: cannot find install-sh, install.sh, or shtool in config "."/config"
./bootstrap
%configure
make %{?_smp_mflags}

%install
%make_install

# Move config files to /etc/unrtf
mkdir -p %{buildroot}%{_sysconfdir}/unrtf/
mv %{buildroot}%{_datadir}/unrtf/*.{conf,charmap} %{buildroot}%{_sysconfdir}/unrtf/

%check
make %{?_smp_mflags} check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/unrtf/
%{_bindir}/unrtf
%{_mandir}/man1/unrtf.1%{ext_man}

%changelog
