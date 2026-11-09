#
# spec file for package hardinfo2
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           hardinfo2
Version:        2.3.1
Release:        0
Summary:        System information and benchmark tool
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.1-only
Group:          System/Benchmark
URL:            https://github.com/hardinfo2/hardinfo2
# Made by prune-backgrounds.sh from the release-%%{version} tag: the window
# background pictures (pixmaps/bg*.jpg) are left out.
Source0:        %{name}-%{version}.tar.xz
Source1:        prune-backgrounds.sh
Source2:        %{name}.sysusers
# PATCH-FEATURE-OPENSUSE hardinfo2-no-background-themes.patch -- drop the Theme menu (its pictures are not shipped)
Patch0:         hardinfo2-no-background-themes.patch
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  glslang-devel
BuildRequires:  hicolor-icon-theme
BuildRequires:  libsensors4-devel
BuildRequires:  pkgconfig
BuildRequires:  sysuser-tools
BuildRequires:  systemd-rpm-macros
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5OpenGL)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gmodule-export-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libdecor-0)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(zlib)
Requires:       gawk
Recommends:     Mesa-demo-x
Recommends:     dmidecode
Recommends:     fwupd
Recommends:     iperf
Recommends:     lsscsi
Recommends:     sensors
Recommends:     sysbench
Recommends:     udisks2
Recommends:     vulkan-tools
Recommends:     xdg-utils
Recommends:     xrandr
Provides:       hardinfo = %{version}
Obsoletes:      hardinfo < 2
%sysusers_requires
%{?systemd_ordering}

%description
Hardinfo2 shows information about the hardware and basic software of
a Linux system, and benchmarks it. Results can be compared online with
other machines, and reports can be generated in HTML or plain text.

It is the continuation of HardInfo, whose last release was 0.5.1.

The optional hardinfo2 service collects data that only root can read
(DMI memory, I/O memory map, SPD). Enable it with
"systemctl enable --now hardinfo2" and add users to the hardinfo2 group.

%prep
%autosetup -p1

%build
%sysusers_generate_pre %{SOURCE2} %{name} %{name}.conf
%cmake \
  -DHARDINFO2_QT5=ON \
  -DHARDINFO2_QT6=OFF \
  -DHARDINFO2_VK=ON \
  -DHARDINFO2_LIBSOUP3=ON \
  -DHARDINFO2_SERVICE=ON \
  -DCMAKE_INSTALL_SERVICEDIR=%{_prefix}/lib
%cmake_build

%install
%cmake_install
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
mkdir -p %{buildroot}%{_sbindir}
ln -s service %{buildroot}%{_sbindir}/rc%{name}
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%pre -f %{name}.pre
%service_add_pre %{name}.service

%post
%service_add_post %{name}.service

%preun
%service_del_preun %{name}.service

%postun
%service_del_postun %{name}.service

%files -f %{name}.lang
%license LICENSE LICENSE.1 LICENSE.2
%doc README.md
%{_bindir}/%{name}
%{_bindir}/hwinfo2_fetch_sysdata
%{_sbindir}/rc%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/org.hardinfo2.hardinfo2.metainfo.xml
%{_mandir}/man1/%{name}.1%{?ext_man}
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf

%changelog
