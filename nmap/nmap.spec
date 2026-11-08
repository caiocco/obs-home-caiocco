#
# spec file for package nmap
#
# Copyright (c) 2023 SUSE LLC
# Copyright (c) 2024 Andreas Stieger <Andreas.Stieger@gmx.de>
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


%define _buildshell /bin/bash
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
# Something in Lua from openSUSE is broken
%if 0%{?suse_version}
%define with_system_lua 0
%else
%define with_system_lua 1
%endif
%define pythons python3
Name:           nmap
Version:        7.98
Release:        0
Summary:        Network exploration tool and security scanner
# nmap 7.94 is licensed under Nmap Public Source License Version 0.95
# https://nmap.org/npsl/
# https://bugzilla.opensuse.org/show_bug.cgi?id=1211571
License:        NonFree
Group:          Productivity/Networking/Diagnostic
URL:            https://nmap.org/
Source:         https://nmap.org/dist/nmap-%{version}.tar.bz2
Source1:        https://svn.nmap.org/nmap/docs/nmap_gpgkeys.txt#/%{name}.keyring
Source2:        http://nmap.org/dist/sigs/%{name}-%{version}.tar.bz2.asc
Patch1:         nmap-7.40-desktop_files.patch
Patch2:         nmap-4.75-nostrip.patch
Patch3:         su-to-zenmap.patch
Patch4:         nmap-ncat-skip-network-tests.patch
Patch6:         ndiff_build.patch
Patch7:         ndiff_install.patch
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  gobject-introspection
BuildRequires:  libopenssl-3-devel
BuildRequires:  libpcap-devel
BuildRequires:  libssh2-devel
BuildRequires:  pcre2-devel
BuildRequires:  python3-base
BuildRequires:  update-desktop-files
BuildRequires:  zlib-devel
%if %{with_system_lua}
BuildRequires:  pkgconfig(lua) >= 5.4.4
%endif
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module setuptools-gettext}
BuildRequires:  %{python_module build}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module wheel}

%description
Nmap ("Network Mapper") is a utility for network exploration or
security auditing. It may as well be used for tasks such as network
inventory, managing service upgrade schedules, and monitoring host or
service uptime. Nmap uses raw IP packets to determine what hosts are
available on the network, what services (application name and
version) those hosts are offering, what operating systems (and OS
versions) they are running, what type of packet filters/firewalls are
in use, and dozens of other characteristics. It scans large networks,
and works fine against single hosts.

%package -n zenmap
Summary:        A graphical front-end for Nmap
Group:          Productivity/Networking/Diagnostic
Requires:       %{name} = %{version}
Requires:       python3-gobject-Gdk
Obsoletes:      %{name}-gtk < %{version}
Provides:       %{name}-gtk = %{version}-%{release}

%description -n zenmap
zenmap is a graphical front-end for the nmap network scanner

%package -n ndiff
Summary:        Compare results of Nmap scans
Group:          Productivity/Networking/Diagnostic

%description -n ndiff
Ndiff is a tool to aid in the comparison of Nmap scans. It takes two Nmap XML
output files and prints the differences between them: hosts coming up and down,
ports becoming open or closed, etc.

%package -n ncat
Summary:        Network tool to concatenate and redirect sockets
Group:          Productivity/Networking/Diagnostic

%description -n ncat
Ncat is a networking utility which will read and write data across a
network from the command line. It uses both TCP and UDP for
communication and provides network connectivity to other applications
and users.

%package -n nping
Summary:        Packet generator
Group:          Productivity/Networking/Diagnostic

%description -n nping
Nping is a tool for network packet generation, response
analysis and response time measurement. Nping allows to generate network
packets of a wide range of protocols, letting users to tune virtually
any field of the protocol headers. While Nping can be used as a simple
ping utility to detect active hosts, it can also be used as a raw packet
generator for network stack stress tests, ARP poisoning, Denial of
Service attacks, route tracing, etc.

%prep
%autosetup -p1

# use system provided libraries
rm -rf libpcap libpcre macosx mswin32

#fix pt_PT/pt zh/zh_CN locale
sed -i '/ALL_LINGUAS =/s/pt_PT/pt/' Makefile.in
sed -i '/ALL_LINGUAS =/s/zh/zh_CN/' Makefile.in
mv docs/man-xlate/nmap-pt_PT.1 docs/man-xlate/nmap-pt.1
mv docs/man-xlate/nmap-zh.1 docs/man-xlate/nmap-zh_CN.1

%build
export CFLAGS="%{optflags} -DOPENSSL_LOAD_CONF"
export CXXFLAGS="%{optflags} -DOPENSSL_LOAD_CONF"

%configure --with-libpcap=%{_prefix}  \
           --with-libdnet=included    \
%if %{with_system_lua}
           --with-liblua=%{_prefix}   \
%else
           --with-liblua=included     \
%endif
           --with-libpcre=%{_prefix}  \
           --without-zenmap           \
           STRIP=/bin/true
           

%make_build
pushd zenmap
%if 0%{?suse_version} && 0%{?suse_version} <= 1600
# Leap 16.0 setuptools-gettext 0.1.14 ignores build_dir, so no .mo ends up
# in zenmapCore/data/locale; compile them by hand to match package-data
for po in zenmapCore/data/locale/*.po; do
  l=$(basename $po .po)
  mkdir -p zenmapCore/data/locale/$l/LC_MESSAGES
  msgfmt -o zenmapCore/data/locale/$l/LC_MESSAGES/zenmap.mo $po
done
%endif
%pyproject_wheel
popd

%install
make DESTDIR=%{buildroot} deskdir="%{_datadir}/gnome/apps/Utilities/" install
install -d "%{buildroot}%{_datadir}/pixmaps/"
install -d "%{buildroot}%{_datadir}/applications/"

pushd zenmap
%pyproject_install
install -m 644 ../docs/zenmap.1 %{buildroot}%{_mandir}/man1/
install -m 644 install_scripts/unix/*.desktop %{buildroot}%{_datadir}/applications/
install -m 755 install_scripts/unix/su-to-zenmap.sh %{buildroot}%{_bindir}/su-to-zenmap.sh
ln -s %{python_sitelib}/zenmapCore/data/pixmaps/zenmap.png %{buildroot}%{_datadir}/pixmaps/zenmap.png
ln -sf zenmap %{buildroot}%{_bindir}/nmapfe
ln -sf zenmap %{buildroot}%{_bindir}/xnmap
popd
# TODO: only temporary fix and might need cleanup later on:
#   7.98 build does not produce the correct dist-info folder yet, likely due to new ndiff/zenmap build process
mv %{buildroot}%{python_sitelib}/ndiff-7.96.dist-info/ %{buildroot}%{python_sitelib}/ndiff-%{version}.dist-info
mv %{buildroot}%{python_sitelib}/zenmap-7.97.dist-info/ %{buildroot}%{python_sitelib}/zenmap-%{version}.dist-info

find %{buildroot}/%{python_sitelib}/zenmapCore/data/locale -type f -name "*.po*" -print -delete
%find_lang zenmap

%suse_update_desktop_file zenmap System Network
%suse_update_desktop_file zenmap-root System Network
touch -r %{buildroot}/%{python_sitelib}/zenmapCore/Paths.py %{buildroot}/%{python_sitelib}/zenmapCore/Paths.pyc
dos2unix %{buildroot}%{_datadir}/%{name}/nselib/data/oracle-sids

%fdupes -s %{buildroot}

%check

pushd ncat
%make_build check
popd

pushd libdnet-stripped
%make_build check
popd

# retrieve list of compiled in modules
compiled_with=$("%{buildroot}%{_bindir}/nmap" -V | grep "Compiled with:" )
# for the following tests, the leading space is relevant
# check features built with system libraries
[[ $compiled_with == *\ libpcre2-* ]]
[[ $compiled_with == *\ libpcap-* ]]
[[ $compiled_with == *\ openssl-* ]]
# check features built with included sources
[[ $compiled_with == *\ nmap-libdnet-* ]]
# check for lua
%if %{with_system_lua}
[[ $compiled_with == *\ liblua-5.3* ]]
%else
# lua in nmap tarball identifies itself as "liblua-5.4.4"
[[ $compiled_with == *\ nmap-liblua-5.4.* ]]
%endif
#

%files
%license LICENSE
%doc CHANGELOG HACKING
%doc docs/README
%doc docs/nmap.usage.txt
%dir %{_mandir}/??
%dir %{_mandir}/??/man1
%dir %{_mandir}/??_??
%dir %{_mandir}/??_??/man1
%{_mandir}/man1/nmap.1%{?ext_man}
%{_mandir}/*/man1/*
%{_bindir}/nmap
%{_datadir}/nmap

%files -n zenmap -f zenmap.lang
%{_bindir}/xnmap
%{_bindir}/zenmap
%{_bindir}/nmapfe
%{_bindir}/su-to-zenmap.sh
%dir %{python_sitelib}/zenmapCore
%{python_sitelib}/zenmapCore/*.py{c,}
%{python_sitelib}/zenmapCore/__pycache__
%dir %{python_sitelib}/zenmapCore/data
%{python_sitelib}/zenmapCore/data/{config,docs,misc,pixmaps}
%dir %{python_sitelib}/zenmapCore/data/locale
%dir %{python_sitelib}/zenmapCore/data/locale/*
%if 0%{?suse_version} && 0%{?suse_version} <= 1600
%dir %{python_sitelib}/zenmapCore/data/locale/*/LC_MESSAGES
%endif
%{python_sitelib}/zenmapCore/data/locale/xgettext-profile_editor.py
%{python_sitelib}/zenmapCore/data/locale/__pycache__/*
%{python_sitelib}/zenmapGUI
%{python_sitelib}/radialnet
%{_datadir}/applications/zenmap-root.desktop
%{_datadir}/applications/zenmap.desktop
%{python_sitelib}/zenmap-%{version}.dist-info
%{_datadir}/pixmaps/zenmap.png
%{_mandir}/man1/zenmap.1%{?ext_man}

%files -n ndiff
%{_bindir}/ndiff
%{_mandir}/man1/ndiff.1%{?ext_man}
%{python_sitelib}/ndiff.*
%{python_sitelib}/ndiff-%{version}.dist-info
%pycache_only %{python_sitelib}/__pycache__/ndiff.*

%files -n ncat
%{_bindir}/ncat
%{_mandir}/man1/ncat.1%{?ext_man}
%dir %{_datadir}/ncat
%config(noreplace) %{_datadir}/ncat/ca-bundle.crt

%files -n nping
%{_bindir}/nping
%{_mandir}/man1/nping.1%{?ext_man}

%changelog
