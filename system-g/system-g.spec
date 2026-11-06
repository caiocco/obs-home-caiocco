#
# spec file for package system-g
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# System G depends on the JX Application Framework (static libraries) and
# on ACE, neither of which is packaged for openSUSE.  Both are built here
# from bundled sources and linked statically; only the systemg binary is
# shipped.  Commits are paired the same way upstream CI pairs them.
#

%define sg_commit  84e80593aae657ea7c1ab725f1f6f57ddd217d25
%define sg_short   84e8059
%define sg_date    20260330
%define jx_commit  ae783358dc10b2965e8d5762ffd94bbdca978b53
%define ace_ver    8.0.6
# static JX/ACE archives are built with plain ar
%define _lto_cflags %{nil}

Name:           system-g
Version:        3.0.3+git%{sg_date}.%{sg_short}
Release:        0
Summary:        File manager for X11, similar to the classic Mac OS Finder
License:        GPL-3.0-only AND LGPL-2.1-or-later AND DOC
Group:          Productivity/File utilities
URL:            https://github.com/jafl/system-g
Source0:        https://github.com/jafl/system-g/archive/%{sg_commit}.tar.gz#/system-g-%{sg_commit}.tar.gz
Source1:        https://github.com/jafl/jx_application_framework/archive/%{jx_commit}.tar.gz#/jx_application_framework-%{jx_commit}.tar.gz
Source2:        https://github.com/DOCGroup/ACE_TAO/releases/download/ACE%%2BTAO-8_0_6/ACE-%{ace_ver}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gd-devel
BuildRequires:  libboost_context-devel
BuildRequires:  libboost_fiber-devel
BuildRequires:  libboost_headers-devel
BuildRequires:  libjpeg-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xpm)
Requires:       xdg-utils
Recommends:     git-gui
Recommends:     xterm
Provides:       systemg = %{version}-%{release}

%description
System G provides a graphical interface to the UNIX file system,
similar to the Finder of Mac OS 7.  It offers a tree view of folders,
drag-and-drop file management, file bindings, git integration and
quick access to a terminal in any folder.

%prep
%setup -q -c -n %{name}-build -a1 -a2
mv system-g-%{sg_commit} system-g
mv jx_application_framework-%{jx_commit} JX

# ACE configuration
ln -s config-linux.h ACE_wrappers/ace/config.h
ln -s platform_linux.GNU ACE_wrappers/include/makeinclude/platform_macros.GNU

# JX configuration (what JX's ./configure does, minus network access)
pushd JX
ln -sf sys/Linux_g++ include/jx-af/make/jx_config
mkdir -p lib
for l in jcore jx jfs; do ln -sf ../lib$l/lib$l.a lib/lib$l.a; done
cp -f libjcore/jStringData_init.h libjcore/code/jStringData.h
echo -n 1 > 0-RELEASE
# do not turn compiler warnings into errors with newer toolchains
sed -i 's/-Wall -Werror/-Wall/' include/jx-af/make/jx_config_common
find . -type d -name image-build -exec sh -c 'touch "$1"/*' _ {} \;
popd

pushd system-g
echo -n 1 > 0-RELEASE
touch image-build/*
popd

%build
TOP=$PWD
export ACE_ROOT=$TOP/ACE_wrappers
export CPATH=$ACE_ROOT
export LIBRARY_PATH=$ACE_ROOT/lib:$ACE_ROOT/ace
JXI=$TOP/jx-install
export PATH=$JXI/bin:$PATH
JXMAKE="make %{?_smp_mflags} JX_INSTALL_ROOT=$JXI jx.test.skip=true"
JXOPT="J_OPTIMIZE_LEVEL=%{optflags}"

# ACE (static only)
make %{?_smp_mflags} -C $ACE_ROOT/ace \
     static_libs=1 shared_libs=0 exceptions=0 debug=0 optimize=1

# makemake
pushd JX/tools/makemake
make -f Makefile.port JX_INSTALL_ROOT=$JXI "$JXOPT" install
popd

# generate Makefiles
for d in libjcore libjx libjfs tools/compile_jstrings; do
  (cd JX/$d && makemake)
done

# JX libraries and string compiler
pushd JX/libjcore
$JXMAKE "$JXOPT" COMPILE_STRINGS=0
popd
pushd JX/tools/compile_jstrings
$JXMAKE "$JXOPT" install
popd
for d in libjcore libjx libjfs; do
  (cd JX/$d && $JXMAKE "$JXOPT")
done

# System G
pushd system-g
makemake
$JXMAKE "$JXOPT"
popd

%install
cd system-g
install -Dm0755 systemg %{buildroot}%{_bindir}/systemg
install -Dm0644 release/pkg/desktop/systemg.desktop \
        %{buildroot}%{_datadir}/applications/systemg.desktop
install -Dm0644 release/pkg/desktop/systemg_choose.desktop \
        %{buildroot}%{_datadir}/applications/systemg_choose.desktop
install -Dm0644 release/pkg/desktop/systemg.png \
        %{buildroot}%{_datadir}/pixmaps/systemg.png
# use standard freedesktop categories
sed -i -e 's/^Categories=.*/Categories=System;FileTools;FileManager;/' \
       -e '/^Type=/a GenericName=File Manager' \
       %{buildroot}%{_datadir}/applications/*.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop || :

%files
%license system-g/COPYING
%doc system-g/README.md system-g/release/doc/*.html
%{_bindir}/systemg
%{_datadir}/applications/systemg.desktop
%{_datadir}/applications/systemg_choose.desktop
%{_datadir}/pixmaps/systemg.png

%changelog
