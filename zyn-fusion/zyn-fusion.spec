#
# spec file for package zyn-fusion
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Zyn-Fusion is ZynAddSubFX with the newer mruby-zest user interface.
# Upstream ships both halves in the zynaddsubfx/3.0.6 SourceForge folder:
# the synth core (zynaddsubfx-3.0.6) and the UI (zyn-fusion-ui-src-3.0.6,
# with a bundled mruby, pcre, nanovg and pugl).
#
# The core is built here again with -DGuiModule=zest. The classic NTK
# build comes from the zynaddsubfx package (a link to openSUSE:Factory),
# and both can be installed side by side:
#  - the zest-built core is /usr/bin/zyn-fusion (the classic one stays
#    /usr/bin/zynaddsubfx);
#  - the UI (zyn-fusion executable, libzest.so, fonts, schema) lives in
#    %%{_libdir}/zyn-fusion instead of upstream's hardcoded /opt/zyn-fusion;
#  - banks and examples come from zynaddsubfx-common.
# Only the LV2/VST plugins conflict, since they use the same URIs/IDs.
#

%define uiname zyn-fusion-ui-src
Name:           zyn-fusion
Version:        3.0.6
Release:        0
Summary:        ZynAddSubFX software synthesizer with the Zyn-Fusion interface
License:        GPL-2.0-or-later AND LGPL-2.1-only AND MIT AND Zlib AND ISC AND BSD-3-Clause
Group:          Productivity/Multimedia/Sound/Midi
URL:            https://zynaddsubfx.sourceforge.io/zyn-fusion.html
Source0:        https://downloads.sourceforge.net/project/zynaddsubfx/zynaddsubfx/%{version}/zynaddsubfx-%{version}.tar.bz2
Source1:        https://downloads.sourceforge.net/project/zynaddsubfx/zynaddsubfx/%{version}/%{uiname}-%{version}.tar.bz2
Source2:        zyn-fusion-jack.desktop
Source3:        zyn-fusion-alsa.desktop
Source4:        zyn-fusion.svg
# From openSUSE:Factory zynaddsubfx
Patch0:         zynaddsubfx-buildflags.patch
Patch1:         fix-missing-include.patch
Patch2:         0001-Bump-C-version-to-C-20.patch
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  ruby-devel
BuildRequires:  update-desktop-files
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(liblo)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(mxml)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
Requires:       zynaddsubfx-common = %{version}

%description
ZynAddSubFX is a real-time software synthesizer with additive,
subtractive and pad synthesis engines, polyphony, multi-timbral and
microtonal capabilities, and system and insertion effects.

Zyn-Fusion is ZynAddSubFX with the newer mruby-zest user interface.
Run it as "zyn-fusion"; the classic interface stays available as
"zynaddsubfx" from the zynaddsubfx package.

%package lv2
Summary:        Zyn-Fusion LV2 plugins
Group:          Productivity/Multimedia/Sound/Midi
Requires:       %{name} = %{version}-%{release}
Conflicts:      zynaddsubfx-lv2

%description lv2
ZynAddSubFX synthesizer and effect LV2 plugins with the Zyn-Fusion
interface. They replace the ones from zynaddsubfx-lv2 (same URIs).

%package vst
Summary:        Zyn-Fusion VST plugin
Group:          Productivity/Multimedia/Sound/Midi
Requires:       %{name} = %{version}-%{release}
Conflicts:      zynaddsubfx-vst

%description vst
ZynAddSubFX synthesizer VST plugin with the Zyn-Fusion interface. It
replaces the one from zynaddsubfx-vst.

%prep
%setup -q -n zynaddsubfx-%{version} -a 1
%autopatch -p1

# Look for the UI in %%{_libdir}/zyn-fusion, never in the current directory
# or PATH (/usr/bin/zyn-fusion is this core itself).
sed -i \
    -e '/exec_fusion("\.\/zyn-fusion");/d' \
    -e '/exec_fusion("zyn-fusion");/d' \
    -e 's|/opt/zyn-fusion/zyn-fusion|%{_libdir}/zyn-fusion/zyn-fusion|' \
    src/main.cpp
sed -i \
    -e 's|"\./libzest\.so"|"%{_libdir}/zyn-fusion/libzest.so"|' \
    -e 's|/opt/zyn-fusion/libzest\.so|%{_libdir}/zyn-fusion/libzest.so|' \
    src/Plugin/ZynAddSubFX/ZynAddSubFX-UI-Zest.cpp \
    %{uiname}-%{version}/test-libversion.c
grep -q '%{_libdir}/zyn-fusion/zyn-fusion' src/main.cpp
! grep -rq '/opt/zyn-fusion\|"\./libzest\.so' src/main.cpp \
    src/Plugin/ZynAddSubFX/ZynAddSubFX-UI-Zest.cpp \
    %{uiname}-%{version}/test-libversion.c

%build
# The UI
pushd %{uiname}-%{version}
make linux
make pack
popd

# The core, with the zest GUI
%cmake \
    -DGuiModule=zest \
    -DDefaultOutput=jack \
    -DNoNeonPlease:BOOL=ON \
    -DOssEnable:BOOL=OFF \
    -DDssiEnable:BOOL=OFF \
    -DCompileTests:BOOL=OFF \
%ifarch %{ix86} x86_64
    -DX86Build=ON \
%endif
    -DPluginLibDir:STRING=%{_lib}
%cmake_build

%install
%cmake_install

# Only the binary and the plugins are ours; the rest is zynaddsubfx-common's
# or the classic package's.
mv %{buildroot}%{_bindir}/zynaddsubfx %{buildroot}%{_bindir}/zyn-fusion
rm -rf %{buildroot}%{_datadir}

pushd %{uiname}-%{version}/package
install -Dm0755 zest %{buildroot}%{_libdir}/zyn-fusion/zyn-fusion
install -Dm0755 libzest.so %{buildroot}%{_libdir}/zyn-fusion/libzest.so
cp -a font schema %{buildroot}%{_libdir}/zyn-fusion/
# libzest only checks that qml/MainWindow.qml exists (the QML is built in)
mkdir -p %{buildroot}%{_libdir}/zyn-fusion/qml
echo "// Placeholder: the QML is compiled into libzest.so" > %{buildroot}%{_libdir}/zyn-fusion/qml/MainWindow.qml
popd

install -Dm0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/zyn-fusion-jack.desktop
install -Dm0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/zyn-fusion-alsa.desktop
install -Dm0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/zyn-fusion.svg

%files
%license COPYING
%license %{uiname}-%{version}/LICENSE
%doc AUTHORS.txt NEWS.txt README.adoc
%{_bindir}/zyn-fusion
%{_libdir}/zyn-fusion/
%{_datadir}/applications/zyn-fusion-*.desktop
%{_datadir}/icons/hicolor/scalable/apps/zyn-fusion.svg

%files lv2
%{_libdir}/lv2/

%files vst
%{_libdir}/vst/

%changelog
