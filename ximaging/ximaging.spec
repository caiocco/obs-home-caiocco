#
# spec file for package ximaging
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define xi_commit   45d292f6bf54d199d1b8173a96d277095b811745
%define xi_short    45d292f
%define xi_date     20261018

Name:           ximaging
Version:        1.9.3+git%{xi_date}.%{xi_short}
Release:        0
Summary:        Image browser and viewer for X11 based on Motif
License:        MIT
Group:          Productivity/Graphics/Viewers
URL:            https://fastestcode.org/ximaging.html
Source0:        https://github.com/alx210/ximaging/archive/%{xi_commit}.tar.gz#/%{name}-%{xi_commit}.tar.gz
Source1:        %{name}.desktop
# PATCH-FIX-UPSTREAM ximaging-bmp-prototype.patch -- match the BMP loader definition to its prototype (LTO type mismatch)
Patch0:         %{name}-bmp-prototype.patch
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xt)

%description
XImaging is a raster image browser and viewer for Unix/X11 built with
the Motif toolkit. The browser window shows thumbnails of the images in
a directory and offers basic file management; the viewer displays
single images with zoom, rotation and slideshow functions.

Supported formats are JPEG, PNG, TIFF, TGA, SGI, Sun Raster, PCX,
Windows BMP, XPM, XBM and Netpbm; further formats can be read through
external conversion filters.

%prep
%autosetup -p1 -n %{name}-%{xi_commit}
ln -s ../mf/Makefile.Linux src/Makefile
sed -i \
  -e 's|^CFLAGS = .*|CFLAGS = %{optflags} -Wall $(INCDIRS)|' \
  -e 's|^LDFLAGS = .*|LDFLAGS = %{optflags} -pthread %{?build_ldflags}|' \
  -e 's|^APPLRESDIR = .*|APPLRESDIR = %{_datadir}/X11/app-defaults|' \
  mf/Makefile.Linux
# Unprivileged install
sed -i 's|install \(.*\)-o0 -g0 |install \1|' src/common.mf

%build
%make_build -C src

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_datadir}/X11/app-defaults
%make_install -C src \
  PREFIX=%{buildroot}%{_prefix} \
  MANDIR=%{buildroot}%{_mandir} \
  APPLRESDIR=%{buildroot}%{_datadir}/X11/app-defaults
install -Dm0644 share/viewer.xpm %{buildroot}%{_datadir}/pixmaps/%{name}.xpm
install -Dm0644 share/browser.xpm %{buildroot}%{_datadir}/pixmaps/%{name}-browser.xpm
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE
%doc README
%{_bindir}/ximaging
%dir %{_datadir}/X11/app-defaults
%{_datadir}/X11/app-defaults/XImaging
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/pixmaps/%{name}-browser.xpm
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/ximaging.1%{?ext_man}

%changelog
