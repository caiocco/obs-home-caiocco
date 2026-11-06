#
# spec file for package leibnitz
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Leibnitz depends on the JX Application Framework (static libraries), on
# ACE and on RE/flex 6.x, none of which is packaged (in a usable version)
# for openSUSE.  All three are built here from bundled sources and linked
# statically; only the leibnitz binary and its data files are shipped.
# The RE/flex version is the one pinned in JX's .reflex-version.
#

%define lb_commit   4aade11d6145f1796d9ac0f83a0390c2348bd87d
%define lb_short    4aade11
%define lb_date     20260331
%define jx_commit   ae783358dc10b2965e8d5762ffd94bbdca978b53
%define ace_ver     8.0.6
%define reflex_ver  6.3.0
# static JX/ACE archives are built with plain ar
%define _lto_cflags %{nil}

Name:           leibnitz
Version:        3.0.4+git%{lb_date}.%{lb_short}
Release:        0
Summary:        Graphing calculator for X11
License:        GPL-3.0-only AND LGPL-2.1-or-later AND DOC AND BSD-3-Clause
Group:          Productivity/Scientific/Math
URL:            https://github.com/jafl/leibnitz
Source0:        https://github.com/jafl/leibnitz/archive/%{lb_commit}.tar.gz#/leibnitz-%{lb_commit}.tar.gz
Source1:        https://github.com/jafl/jx_application_framework/archive/%{jx_commit}.tar.gz#/jx_application_framework-%{jx_commit}.tar.gz
Source2:        https://github.com/DOCGroup/ACE_TAO/releases/download/ACE%%2BTAO-8_0_6/ACE-%{ace_ver}.tar.gz
Source3:        https://github.com/Genivia/RE-flex/archive/v%{reflex_ver}.tar.gz#/RE-flex-%{reflex_ver}.tar.gz

BuildRequires:  bison
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

%description
Leibnitz provides electronic paper for calculations and graphs.  It
evaluates mathematical expressions (including complex numbers) with a
tape of past results, user-defined constants and functions, conversion
between number bases, and 2D plots of functions.

%prep
%setup -q -c -n %{name}-build -a1 -a2 -a3
mv leibnitz-%{lb_commit} leibnitz
mv jx_application_framework-%{jx_commit} JX
mv RE-flex-%{reflex_ver} reflex

# ACE configuration
ln -s config-linux.h ACE_wrappers/ace/config.h
ln -s platform_linux.GNU ACE_wrappers/include/makeinclude/platform_macros.GNU

# JX configuration (what JX's ./configure does, minus network access)
pushd JX
ln -sf sys/Linux_g++ include/jx-af/make/jx_config
mkdir -p lib
for l in jcore jx jexpr j2dplot; do ln -sf ../lib$l/lib$l.a lib/lib$l.a; done
cp -f libjcore/jStringData_init.h libjcore/code/jStringData.h
echo -n 1 > 0-RELEASE
# do not turn compiler warnings into errors with newer toolchains
sed -i 's/-Wall -Werror/-Wall/' include/jx-af/make/jx_config_common
touch libjexpr/code/JExprParserY.cpp libjexpr/code/JExprParserY.hpp
find . -type d -name image-build -exec sh -c 'touch "$1"/*' _ {} \;
popd

# Leibnitz configuration (what its ./configure does)
pushd leibnitz
echo -n 1 > 0-RELEASE
touch image-build/*
# standard freedesktop categories
sed -i 's/X-Red-Hat-Base;//' release/pkg/desktop/leibnitz.desktop
popd

%build
TOP=$PWD
export ACE_ROOT=$TOP/ACE_wrappers
RFI=$TOP/reflex-install
JXI=$TOP/jx-install
export CPATH=$ACE_ROOT:$RFI/include
export LIBRARY_PATH=$ACE_ROOT/lib:$ACE_ROOT/ace:$RFI/lib
export PATH=$JXI/bin:$RFI/bin:$PATH
JXMAKE="make %{?_smp_mflags} JX_INSTALL_ROOT=$JXI jx.test.skip=true"
JXOPT="J_OPTIMIZE_LEVEL=%{optflags}"

# RE/flex (static library + reflex tool); SIMD level fixed for
# reproducible and portable builds
pushd reflex
./configure --prefix=$RFI --disable-avx2 \
            CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
make %{?_smp_mflags}
make install
popd

# ACE (static only)
make %{?_smp_mflags} -C $ACE_ROOT/ace \
     static_libs=1 shared_libs=0 exceptions=0 debug=0 optimize=1

# makemake
pushd JX/tools/makemake
make -f Makefile.port JX_INSTALL_ROOT=$JXI "$JXOPT" install
popd

# generate Makefiles
for d in libjcore libjx libjexpr libj2dplot tools/compile_jstrings; do
  (cd JX/$d && makemake)
done

# JX libraries and string compiler
pushd JX/libjcore
$JXMAKE "$JXOPT" COMPILE_STRINGS=0
popd
pushd JX/tools/compile_jstrings
$JXMAKE "$JXOPT" install
popd
for d in libjcore libjx libjexpr libj2dplot; do
  (cd JX/$d && $JXMAKE "$JXOPT")
done

# Leibnitz
pushd leibnitz
makemake
$JXMAKE "$JXOPT"
popd

%install
cd leibnitz
install -Dm0755 leibnitz %{buildroot}%{_bindir}/leibnitz
install -Dm0644 release/pkg/desktop/leibnitz.desktop \
        %{buildroot}%{_datadir}/applications/leibnitz.desktop
install -Dm0644 release/pkg/desktop/leibnitz.png \
        %{buildroot}%{_datadir}/pixmaps/leibnitz.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop || :

%files
%license leibnitz/COPYING
%doc leibnitz/README.md leibnitz/release/doc/*.html
%{_bindir}/leibnitz
%{_datadir}/applications/leibnitz.desktop
%{_datadir}/pixmaps/leibnitz.png

%changelog
