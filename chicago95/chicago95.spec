#To the extent possible under law, the person who associated CC0 with
#this spec file has waived all copyright and related or neighboring rights
#to this spec file.
#
#You should have received a copy of the CC0 legalcode along with this
#work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

# Source0 is NOT the upstream tarball: it is made by Source99
# (prune-microsoft-assets.sh) from a git checkout, and leaves out every
# file that reproduces Microsoft artwork (Windows 95 splash, wallpapers,
# sounds, Office/MSN/MS-DOS/IE icons, Windows-flag Start buttons). See
# README.SUSE. To update:
#   git clone https://github.com/grassmunk/Chicago95 && \
#   sh prune-microsoft-assets.sh Chicago95 .
%define commit  5da19b8
%define gitdate 20261001

Name:           chicago95
Version:        3.0.1+git%{gitdate}.%{commit}
Release:        0
Summary:        Windows 95 look for Xfce and GTK (metapackage)
License:        (GPL-3.0-or-later OR MIT) AND CC-BY-SA-4.0 AND Cronyx AND SUSE-Public-Domain
Group:          System/GUI/Other
URL:            https://github.com/grassmunk/Chicago95
Source0:        %{name}-%{version}.tar.xz
Source1:        README.SUSE
Source99:       prune-microsoft-assets.sh
BuildRequires:  fdupes
BuildRequires:  fontpackages-devel
BuildRequires:  hicolor-icon-theme
BuildArch:      noarch
Requires:       %{name}-cursor-theme = %{version}
Requires:       %{name}-gtk-theme = %{version}
Requires:       %{name}-icon-theme = %{version}
Recommends:     %{name}-fonts = %{version}

%description
Chicago95 makes Xfce look as close to Microsoft Windows 95 as possible:
GTK 2/3/4 and xfwm4 themes, icons, cursors and fonts.

This build leaves out the upstream files that reproduce Microsoft
artwork (boot splash, wallpapers, sounds, Office/MSN/MS-DOS icons and
Windows-flag Start buttons). The Tux variants stand in for them.

This metapackage installs the GTK, icon and cursor themes.

%package -n %{name}-gtk-theme
Summary:        Windows 95 GTK, xfwm4 and Metacity themes (Chicago95)
License:        GPL-3.0-or-later OR MIT
Group:          System/GUI/Other
Recommends:     %{name}-icon-theme = %{version}
Recommends:     %{name}-cursor-theme = %{version}
Suggests:       gtk2-engine-murrine

%description -n %{name}-gtk-theme
The Chicago95 theme for GTK 2, GTK 3, GTK 4/libadwaita, xfwm4 (normal
and HiDPI), Metacity, Openbox, Cinnamon, GNOME Shell and
xfce4-notifyd, plus an xfce4-terminal color scheme and an
xfce4-panel-profiles layout.

%package -n %{name}-icon-theme
Summary:        Windows 95 icon themes (Chicago95, -tux, -puffy)
License:        (GPL-3.0-or-later OR MIT) AND CC-BY-SA-4.0
Group:          System/GUI/Other

%description -n %{name}-icon-theme
Windows 95 style icon themes: Chicago95, Chicago95-tux (Tux Start
button) and Chicago95-puffy (OpenBSD Puffy Start button).

%package -n %{name}-cursor-theme
Summary:        Windows 95 cursor themes (Chicago95)
License:        GPL-3.0-or-later OR MIT
Group:          System/GUI/Other

%description -n %{name}-cursor-theme
Windows 95 style X cursor themes: black, white, Emerald, standard and
animated hourglass (also HiDPI).

%package -n %{name}-fonts
Summary:        DOS VGA and Cronyx bitmap fonts used by Chicago95
License:        Cronyx AND SUSE-Public-Domain
Group:          System/X11/Fonts
%reconfigure_fonts_prereq

%description -n %{name}-fonts
The "Less/More Perfect DOS VGA" TrueType fonts and the Cronyx Cyrillic
Helvetica/Courier/Times bitmap fonts (OTB) used by the Chicago95 theme.

%package -n plymouth-theme-%{name}-retrotux
Summary:        RetroTux Plymouth boot theme from Chicago95
License:        GPL-3.0-or-later OR MIT
Group:          System/Boot
Requires:       plymouth-plugin-script

%description -n plymouth-theme-%{name}-retrotux
RetroTux, a retro Tux boot splash from the Chicago95 project. Enable
it with: plymouth-set-default-theme -R RetroTux

%prep
%autosetup -p1
cp %{SOURCE1} .

%build
# Nothing to build.

%install
# GTK and window manager themes
install -d %{buildroot}%{_datadir}/themes
cp -a Theme/Chicago95 %{buildroot}%{_datadir}/themes/
rm -rf %{buildroot}%{_datadir}/themes/Chicago95/gnome-shell/assets-render
find %{buildroot}%{_datadir}/themes/Chicago95 -name '*.scss' -delete
install -Dpm 0644 Extras/Chicago95.theme \
  %{buildroot}%{_datadir}/xfce4/terminal/colorschemes/Chicago95.theme
install -Dpm 0644 Extras/Chicago95_Panel_Preferences.tar.bz2 \
  %{buildroot}%{_datadir}/xfce4-panel-profiles/layouts/Chicago95_Panel_Preferences.tar.bz2

# Icons
install -d %{buildroot}%{_datadir}/icons
cp -a Icons/Chicago95 Icons/Chicago95-tux Icons/Chicago95-puffy %{buildroot}%{_datadir}/icons/
rm -f %{buildroot}%{_datadir}/icons/*/icon-theme.cache
# Nameless ".png"/".svg" stray files and upstream helper scripts
find %{buildroot}%{_datadir}/icons -name '.*' -delete
find %{buildroot}%{_datadir}/icons -name '*.sh' -delete
chmod -R u+w,go-w %{buildroot}%{_datadir}/icons
find %{buildroot}%{_datadir}/icons -type f -exec chmod 0644 {} +
# All three icon themes are in one package: dedupe across them, before
# the cursors (another package) land in the same directory.
%fdupes -s %{buildroot}%{_datadir}/icons

# Cursors (src/ and build/ are only the sources of the compiled cursors)
for c in Cursors/*; do
  n=${c##*/}
  install -d %{buildroot}%{_datadir}/icons/$n
  cp -a $c/cursors $c/index.theme %{buildroot}%{_datadir}/icons/$n/
done

# Fonts
install -d %{buildroot}%{_ttfontsdir} %{buildroot}%{_miscfontsdir}
install -pm 0644 Fonts/vga_font/*.ttf %{buildroot}%{_ttfontsdir}/
install -pm 0644 Fonts/bitmap/cronyx-cyrillic/*.otb %{buildroot}%{_miscfontsdir}/

# Plymouth
install -d %{buildroot}%{_datadir}/plymouth/themes/RetroTux
install -pm 0644 Plymouth/RetroTux/*.png Plymouth/RetroTux/RetroTux.plymouth \
  Plymouth/RetroTux/RetroTux.script %{buildroot}%{_datadir}/plymouth/themes/RetroTux/
rm -f %{buildroot}%{_datadir}/plymouth/themes/RetroTux/test.png

find %{buildroot}%{_datadir} -type f -exec chmod 0644 {} +
for d in %{buildroot}%{_datadir}/icons/Chicago95_* %{buildroot}%{_datadir}/themes/Chicago95; do
  %fdupes -s $d
done

%reconfigure_fonts_scriptlets -n %{name}-fonts

%post -n %{name}-icon-theme
%icon_theme_cache_post Chicago95
%icon_theme_cache_post Chicago95-tux
%icon_theme_cache_post Chicago95-puffy

%files
%doc README.md README.SUSE CREDITS

%files -n %{name}-gtk-theme
%doc README.SUSE
%{_datadir}/themes/Chicago95
%dir %{_datadir}/xfce4
%dir %{_datadir}/xfce4/terminal
%dir %{_datadir}/xfce4/terminal/colorschemes
%{_datadir}/xfce4/terminal/colorschemes/Chicago95.theme
%dir %{_datadir}/xfce4-panel-profiles
%dir %{_datadir}/xfce4-panel-profiles/layouts
%{_datadir}/xfce4-panel-profiles/layouts/Chicago95_Panel_Preferences.tar.bz2

%files -n %{name}-icon-theme
%doc README.SUSE
%license Icons/Chicago95-puffy/LICENSE.md
%{_datadir}/icons/Chicago95
%{_datadir}/icons/Chicago95-tux
%{_datadir}/icons/Chicago95-puffy
%ghost %{_datadir}/icons/Chicago95/icon-theme.cache
%ghost %{_datadir}/icons/Chicago95-tux/icon-theme.cache
%ghost %{_datadir}/icons/Chicago95-puffy/icon-theme.cache

%files -n %{name}-cursor-theme
%{_datadir}/icons/Chicago95_*

%files -n %{name}-fonts
%doc README.SUSE
%dir %{_ttfontsdir}
%dir %{_miscfontsdir}
%{_ttfontsdir}/LessPerfectDOSVGA.ttf
%{_ttfontsdir}/MorePerfectDOSVGA.ttf
%{_miscfontsdir}/crox*.otb
%{_miscfontsdir}/koi*.otb

%files -n plymouth-theme-%{name}-retrotux
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%{_datadir}/plymouth/themes/RetroTux

%changelog
