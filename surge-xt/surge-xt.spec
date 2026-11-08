#
# spec file for package surge-xt
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Built from upstream's self-contained source release (surge-src), which
# already carries every git submodule: a JUCE 7 fork, the sst-* libraries,
# clap/clap-juce-extensions, LuaJIT, simde, PEGTL, fmt, etc. They are all
# linked statically into the plugins, as upstream does.
#
# LTO is off: Arch found the LTO build crashing at startup.
# LV2 is opt-in upstream ("crashes in our CI pipeline"); it is built here
# because LMMS only loads native LV2, and ships in its own subpackage.
#

Name:           surge-xt
Version:        1.3.4
Release:        0
Summary:        Hybrid synthesizer (standalone, VST3, CLAP and LV2)
License:        GPL-3.0-or-later
Group:          Productivity/Multimedia/Sound/Midi
URL:            https://surge-synthesizer.github.io/
Source0:        https://github.com/surge-synthesizer/releases-xt/releases/download/%{version}/surge-src-%{version}.tar.gz
BuildRequires:  cmake >= 3.21
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  memory-constraints
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xrandr)
Requires:       %{name}-data = %{version}
Provides:       bundled(JUCE) = 7.0.12
Provides:       bundled(luajit)
ExclusiveArch:  x86_64 aarch64

%description
Surge XT is a free and open-source hybrid synthesizer, originally sold
as Vember Audio Surge. It offers subtractive, wavetable, FM, physical
modelling and other oscillators, extensive modulation and a large set of
effects. Surge XT Effects exposes the effect section as a separate
plugin.

This package contains the standalone applications (with JACK and ALSA
support) and the surge-xt-cli command line player.

%package data
Summary:        Patches, wavetables and skins for Surge XT
Group:          Productivity/Multimedia/Sound/Midi
BuildArch:      noarch

%description data
Factory and third-party patches, wavetables, effect and modulator
presets, tuning files and skins used by all Surge XT variants.

%package vst3
Summary:        Surge XT synthesizer and effects as VST3 plugins
Group:          Productivity/Multimedia/Sound/Midi
Requires:       %{name}-data = %{version}

%description vst3
Surge XT and Surge XT Effects as VST3 plugins, for hosts such as Ardour.

%package clap
Summary:        Surge XT synthesizer and effects as CLAP plugins
Group:          Productivity/Multimedia/Sound/Midi
Requires:       %{name}-data = %{version}

%description clap
Surge XT and Surge XT Effects as CLAP plugins, for hosts such as
Bitwig Studio, Reaper or Qtractor.

%package lv2
Summary:        Surge XT synthesizer and effects as LV2 plugins
Group:          Productivity/Multimedia/Sound/Midi
Requires:       %{name}-data = %{version}

%description lv2
Surge XT and Surge XT Effects as LV2 plugins, for hosts such as LMMS
and Ardour. Upstream considers the JUCE LV2 wrapper less tested than
the VST3 and CLAP builds.

%prep
%autosetup -p1 -n surge

%build
%define _lto_cflags %{nil}
%limit_build -m 2500
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DSURGE_BUILD_TESTRUNNER=OFF \
  -DSURGE_BUILD_LV2=ON \
  -DSURGE_SKIP_WERROR=ON
%cmake_build

%install
%cmake_install

# Lower-case commands for the standalone apps
ln -s "Surge XT" %{buildroot}%{_bindir}/surge-xt
ln -s "Surge XT Effects" %{buildroot}%{_bindir}/surge-xt-effects

install -Dm0644 scripts/installer_linux/assets/applications/Surge-XT.desktop \
  %{buildroot}%{_datadir}/applications/surge-xt.desktop
install -Dm0644 scripts/installer_linux/assets/applications/Surge-XT-FX.desktop \
  %{buildroot}%{_datadir}/applications/surge-xt-fx.desktop
# Drop the empty Path= and deprecated TerminalOptions= keys
sed -i -e '/^MimeType=$/d;/^Path=$/d;/^TerminalOptions=/d' \
  %{buildroot}%{_datadir}/applications/surge-xt*.desktop
sed -i -e 's|^Exec=.*|Exec=surge-xt|' %{buildroot}%{_datadir}/applications/surge-xt.desktop
sed -i -e 's|^Exec=.*|Exec=surge-xt-effects|' \
  -e 's|^Comment=.*|Comment=Surge XT effect section as a standalone processor|' \
  %{buildroot}%{_datadir}/applications/surge-xt-fx.desktop
mkdir -p %{buildroot}%{_datadir}/icons
cp -r scripts/installer_linux/assets/icons/hicolor %{buildroot}%{_datadir}/icons/
cp -r scripts/installer_linux/assets/icons/scalable %{buildroot}%{_datadir}/icons/hicolor/

%fdupes %{buildroot}%{_datadir}/surge-xt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/surge-xt.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/surge-xt-fx.desktop

%files
%license LICENSE
%doc README.md AUTHORS
"%{_bindir}/Surge XT"
"%{_bindir}/Surge XT Effects"
%{_bindir}/surge-xt
%{_bindir}/surge-xt-effects
%{_bindir}/surge-xt-cli
%{_datadir}/applications/surge-xt.desktop
%{_datadir}/applications/surge-xt-fx.desktop
%{_datadir}/icons/hicolor/*/apps/surge-xt.*
%{_datadir}/icons/hicolor/*/apps/surge-xt-fx.*
%dir %{_datadir}/icons/hicolor/384x384
%dir %{_datadir}/icons/hicolor/384x384/apps

%files data
%license LICENSE
%{_datadir}/surge-xt

%files vst3
%license LICENSE
%dir %{_libdir}/vst3
"%{_libdir}/vst3/Surge XT.vst3"
"%{_libdir}/vst3/Surge XT Effects.vst3"

%files clap
%license LICENSE
%dir %{_libdir}/clap
"%{_libdir}/clap/Surge XT.clap"
"%{_libdir}/clap/Surge XT Effects.clap"

%files lv2
%license LICENSE
%dir %{_libdir}/lv2
"%{_libdir}/lv2/Surge XT.lv2"
"%{_libdir}/lv2/Surge XT Effects.lv2"

%changelog
