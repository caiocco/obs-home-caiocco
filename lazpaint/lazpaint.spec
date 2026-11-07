#
# spec file for package lazpaint
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

# Submodule commits pinned by the v%%{version} tag
%define bgrabitmap_commit   6ada359c45fe2230b8af6e108bd6c660bf9202ec
%define bgracontrols_commit 20dbed8ca89620721dc3028c221c91609db53fe2

# libwebp is dlopen()ed, so its dependency is added by hand
%if "%{_lib}" == "lib64"
%define soarch ()(64bit)
%endif

Name:           lazpaint
Version:        7.3
Release:        0
Summary:        Raster and vector image editor
License:        GPL-3.0-only AND LGPL-3.0-or-later WITH LGPL-3.0-linking-exception
Group:          Productivity/Graphics/Bitmap Editors
URL:            https://lazpaint.github.io/
Source0:        https://github.com/bgrabitmap/lazpaint/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/bgrabitmap/bgrabitmap/archive/%{bgrabitmap_commit}.tar.gz#/bgrabitmap-6ada359.tar.gz
Source2:        https://github.com/bgrabitmap/bgracontrols/archive/%{bgracontrols_commit}.tar.gz#/bgracontrols-20dbed8.tar.gz
BuildRequires:  fdupes
BuildRequires:  fpc >= 3.2.0
BuildRequires:  fpc-src
BuildRequires:  hicolor-icon-theme
BuildRequires:  lazarus-ide >= 3.0
BuildRequires:  lazarus-lcl >= 3.0
BuildRequires:  lazarus-lcl-gtk2 >= 3.0
BuildRequires:  lazarus-lcl-nogui
BuildRequires:  lazarus-lcl-qt5 >= 3.0
BuildRequires:  lazarus-tools
BuildRequires:  libQt5Pas-devel
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(x11)
ExclusiveArch:  x86_64 aarch64 %{ix86}

%description
LazPaint is an image editor with raster and vector layers. It can read
layered files (lzp, ora, pdn, oXo, flat psd), multi-image files (gif,
ico, tiff), flat files (bmp, jpeg, pcx, png, tga, webp, xpm, xwd),
vector files (svg) and 3D objects (obj). It has drawing tools, vector
shapes, phong shading, curve adjustments, filters, texture rendering
and Python scripting.

%package gtk
Summary:        Raster and vector image editor (GTK 2)
Group:          Productivity/Graphics/Bitmap Editors
Requires:       libwebp.so.7%{?soarch}
Recommends:     python3-tk
Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-qt
RemovePathPostfixes: .gtk

%description gtk
LazPaint is an image editor with raster and vector layers. It can read
layered files (lzp, ora, pdn, oXo, flat psd), multi-image files (gif,
ico, tiff), flat files (bmp, jpeg, pcx, png, tga, webp, xpm, xwd),
vector files (svg) and 3D objects (obj). It has drawing tools, vector
shapes, phong shading, curve adjustments, filters, texture rendering
and Python scripting.

This package contains the GTK 2 build.

%package qt
Summary:        Raster and vector image editor (Qt 5)
Group:          Productivity/Graphics/Bitmap Editors
Requires:       libwebp.so.7%{?soarch}
Recommends:     python3-tk
Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-gtk
RemovePathPostfixes: .qt

%description qt
LazPaint is an image editor with raster and vector layers. It can read
layered files (lzp, ora, pdn, oXo, flat psd), multi-image files (gif,
ico, tiff), flat files (bmp, jpeg, pcx, png, tga, webp, xpm, xwd),
vector files (svg) and 3D objects (obj). It has drawing tools, vector
shapes, phong shading, curve adjustments, filters, texture rendering
and Python scripting.

This package contains the Qt 5 build.

%prep
%autosetup -p1
rmdir use/bgrabitmap use/bgracontrols
tar xf %{SOURCE1} && mv bgrabitmap-%{bgrabitmap_commit} use/bgrabitmap
tar xf %{SOURCE2} && mv bgracontrols-%{bgracontrols_commit} use/bgracontrols

# libwebp is loaded at runtime; openSUSE ships libwebp.so.7
sed -i "s/'libwebp\.so\.6'/'libwebp.so.7'/" use/bgrabitmap/bgrabitmap/libwebp.pas
grep -q "'libwebp.so.7'" use/bgrabitmap/bgrabitmap/libwebp.pas

# Build the two widgetsets in separate trees
cd ..
rm -rf %{name}-%{version}-qt
cp -a %{name}-%{version} %{name}-%{version}-qt

%build
# $1 = widgetset, $2 = build mode of lazpaint.lpi
build_lazpaint() {
  local conf=$(pwd)/../lazconf-$1
  mkdir -p $conf
  export HOME=$conf
  local opts="--pcp=$conf --ws=$1"
  lazbuild $opts use/bgrabitmap/bgrabitmap/bgrabitmappack.lpk
  lazbuild $opts use/bgracontrols/bgracontrols.lpk
  lazbuild $opts lazpaintcontrols/lazpaintcontrols.lpk
  lazbuild $opts --bm=$2 -B lazpaint/lazpaint.lpi
  test -x lazpaint/release/bin/lazpaint
}

build_lazpaint gtk2 Release

cd ../%{name}-%{version}-qt
build_lazpaint qt5 ReleaseQt5

%install
# Qt 5 tree first, keeping only the binary
pushd ../%{name}-%{version}-qt
./configure --prefix=%{_prefix}
%make_install
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.qt
popd

# GTK 2 tree
./configure --prefix=%{_prefix}
%make_install
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.gtk

chmod 0644 %{buildroot}%{_datadir}/applications/%{name}.desktop
# Same file as the 48x48 hicolor icon
rm %{buildroot}%{_datadir}/pixmaps/%{name}.png
%fdupes -s %{buildroot}%{_datadir}

%files gtk
%license COPYING.txt use/bgrabitmap/COPYING.*
%doc README.md
%{_bindir}/%{name}.gtk
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1%{?ext_man}

%files qt
%license COPYING.txt use/bgrabitmap/COPYING.*
%doc README.md
%{_bindir}/%{name}.qt
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1%{?ext_man}

%changelog
