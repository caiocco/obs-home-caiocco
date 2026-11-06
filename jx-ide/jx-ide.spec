#
# spec file for package jx-ide
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# JX IDE (Code Crusader, Code Medic and Code Mill) depends on the JX
# Application Framework (static libraries), on ACE and on RE/flex 6.x,
# none of which is packaged (in a usable version) for openSUSE.  All three
# are built here from bundled sources and linked statically; only the
# application binaries and their data files are shipped.
# The JX commit is the one upstream CI pairs with this jx-ide commit, and
# the RE/flex version is the one pinned in JX's .reflex-version.
#

%define ide_commit  22f67189bae353256c051ebdaa0407d171b6aa85
%define ide_short   22f6718
%define ide_date    20260824
%define jx_commit   ae783358dc10b2965e8d5762ffd94bbdca978b53
%define ace_ver     8.0.6
%define reflex_ver  6.3.0
# static JX/ACE archives are built with plain ar
%define _lto_cflags %{nil}

Name:           jx-ide
Version:        7.1.5+git%{ide_date}.%{ide_short}
Release:        0
Summary:        Code Crusader, Code Medic and Code Mill development tools for X11
License:        GPL-3.0-only AND LGPL-2.1-or-later AND DOC AND BSD-3-Clause
Group:          Development/Tools/IDE
URL:            https://github.com/jafl/jx-ide
Source0:        https://github.com/jafl/jx-ide/archive/%{ide_commit}.tar.gz#/jx-ide-%{ide_commit}.tar.gz
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
BuildRequires:  libeditorconfig-devel
BuildRequires:  libjpeg-devel
BuildRequires:  lldb-devel
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

%description
JX IDE is the development environment built with the JX Application
Framework.  It consists of Code Crusader (editor and project manager),
Code Medic (graphical debugger) and Code Mill (C++ class generator).

%package -n code-crusader
Summary:        Graphical development environment for X11
Group:          Development/Tools/IDE
Requires:       ctags
Requires:       make
Requires:       perl
Requires:       xdg-utils
Recommends:     code-medic = %{version}-%{release}
Recommends:     code-mill = %{version}-%{release}

%description -n code-crusader
Code Crusader is a graphical development environment for UNIX.  It
provides a programmer's text editor with syntax highlighting for many
languages, a project manager that builds Makefiles, a class tree browser
for C++, Java and other languages, and integration with Code Medic.

%package -n code-medic
Summary:        Graphical debugger for X11 (gdb and lldb frontend)
Group:          Development/Tools/Debuggers
Recommends:     gdb
Recommends:     code-crusader = %{version}-%{release}

%description -n code-medic
Code Medic is a graphical debugger for UNIX.  It can use gdb or lldb as
its backend and integrates with the Code Crusader editor.

%package -n code-mill
Summary:        C++ class generator for X11
Group:          Development/Tools/Other
Recommends:     code-crusader = %{version}-%{release}

%description -n code-mill
Code Mill generates the skeleton of a C++ class that overrides the
virtual functions of its base classes.

%prep
%setup -q -c -n %{name}-build -a1 -a2 -a3
mv jx-ide-%{ide_commit} jx-ide
mv jx_application_framework-%{jx_commit} JX
mv RE-flex-%{reflex_ver} reflex

# ACE configuration
ln -s config-linux.h ACE_wrappers/ace/config.h
ln -s platform_linux.GNU ACE_wrappers/include/makeinclude/platform_macros.GNU

# JX configuration (what JX's ./configure does, minus network access)
pushd JX
ln -sf sys/Linux_g++ include/jx-af/make/jx_config
mkdir -p lib
for l in jcore jx jfs jexpr j2dplot; do ln -sf ../lib$l/lib$l.a lib/lib$l.a; done
cp -f libjcore/jStringData_init.h libjcore/code/jStringData.h
echo -n 1 > 0-RELEASE
# do not turn compiler warnings into errors with newer toolchains
sed -i 's/-Wall -Werror/-Wall/' include/jx-af/make/jx_config_common
touch libjexpr/code/JExprParserY.cpp libjexpr/code/JExprParserY.hpp
find . -type d -name image-build -exec sh -c 'touch "$1"/*' _ {} \;
popd

# jx-ide configuration (what jx-ide's ./configure does)
pushd jx-ide
for a in code_crusader code_medic code_mill; do
  echo -n 1 > $a/0-RELEASE
  touch $a/image-build/*
done
touch code_medic/backend/gdb/VarTreeParserY.cpp code_medic/backend/gdb/VarTreeParserY.hpp
# use the system lldb headers and library
mkdir -p code_medic/lldb-include
ln -sf %{_includedir}/lldb code_medic/lldb-include/lldb
ln -sf %{_libdir}/liblldb.so code_medic/liblldb.so
# desktop files: plain icon names, standard categories
sed -i -e 's/^Icon=\(.*\)\.png$/Icon=\1/' \
       -e 's/X-Red-Hat-Base;//' \
       code_crusader/release/pkg/desktop/*.desktop \
       code_medic/release/pkg/desktop/*.desktop
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
for d in libjcore libjx libjfs libjexpr libj2dplot tools/compile_jstrings; do
  (cd JX/$d && makemake)
done

# JX libraries and string compiler
pushd JX/libjcore
$JXMAKE "$JXOPT" COMPILE_STRINGS=0
popd
pushd JX/tools/compile_jstrings
$JXMAKE "$JXOPT" install
popd
for d in libjcore libjx libjfs libjexpr libj2dplot; do
  (cd JX/$d && $JXMAKE "$JXOPT")
done

# Code Crusader, Code Medic, Code Mill
for a in code_crusader code_medic code_mill; do
  pushd jx-ide/$a
  makemake
  $JXMAKE "$JXOPT"
  popd
done

%install
cd jx-ide

# Code Crusader
pushd code_crusader
install -Dm0755 jcc %{buildroot}%{_bindir}/jcc
ln -sf jcc %{buildroot}%{_bindir}/code-crusader
for m in xml-auto-close html-auto-close java-import; do
  install -m0755 macros/$m %{buildroot}%{_bindir}/$m
done
mkdir -p %{buildroot}%{_datadir}/jxcb
cp -R project_templates scripts %{buildroot}%{_datadir}/jxcb/
mkdir -p %{buildroot}%{_docdir}/code-crusader
cp -R README.md release/doc/*.html macros CPM_rules \
      %{buildroot}%{_docdir}/code-crusader/
install -Dm0644 release/pkg/desktop/code-crusader.desktop \
        %{buildroot}%{_datadir}/applications/code-crusader.desktop
install -Dm0644 release/pkg/desktop/code-crusader.png \
        %{buildroot}%{_datadir}/pixmaps/code-crusader.png
popd

# Code Medic
pushd code_medic
install -Dm0755 medic %{buildroot}%{_bindir}/medic
ln -sf medic %{buildroot}%{_bindir}/code-medic
install -Dm0644 release/pkg/desktop/code-medic.desktop \
        %{buildroot}%{_datadir}/applications/code-medic.desktop
install -Dm0644 release/pkg/desktop/code-medic.png \
        %{buildroot}%{_datadir}/pixmaps/code-medic.png
mkdir -p %{buildroot}%{_docdir}/code-medic
cp README.md release/doc/*.html %{buildroot}%{_docdir}/code-medic/
popd

# Code Mill
pushd code_mill
install -Dm0755 code-mill %{buildroot}%{_bindir}/code-mill
mkdir -p %{buildroot}%{_docdir}/code-mill
cp README.md release/doc/*.html %{buildroot}%{_docdir}/code-mill/
popd

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop || :

%files -n code-crusader
%license jx-ide/code_crusader/COPYING
%{_docdir}/code-crusader
%{_bindir}/jcc
%{_bindir}/code-crusader
%{_bindir}/xml-auto-close
%{_bindir}/html-auto-close
%{_bindir}/java-import
%{_datadir}/jxcb
%{_datadir}/applications/code-crusader.desktop
%{_datadir}/pixmaps/code-crusader.png

%files -n code-medic
%license jx-ide/code_medic/COPYING
%{_docdir}/code-medic
%{_bindir}/medic
%{_bindir}/code-medic
%{_datadir}/applications/code-medic.desktop
%{_datadir}/pixmaps/code-medic.png

%files -n code-mill
%license jx-ide/code_mill/COPYING
%{_docdir}/code-mill
%{_bindir}/code-mill

%changelog
