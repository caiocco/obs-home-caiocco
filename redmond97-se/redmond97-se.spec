#To the extent possible under law, the person who associated CC0 with
#this spec file has waived all copyright and related or neighboring rights
#to this spec file.
#
#You should have received a copy of the CC0 legalcode along with this
#work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

# The themes are generated in %%build from builder/presets/*.conf with
# upstream's builder/gen_theme.sh (ImageMagick), not taken from the
# prebuilt themes/themes-*.tar.xz in the tarball.

%define icons_version 2.08

Name:           redmond97-se
Version:        2.13
Release:        0
Summary:        Windows 95C style themes for GTK 2/3/4, Xfwm4 and Wine (metapackage)
License:        GPL-3.0-only
Group:          System/GUI/Other
URL:            https://codeberg.org/Sliver_X/Redmond97-SE
Source0:        %{url}/releases/download/v%{version}/Redmond97-SE_v%{version}.tar.xz
Source1:        README.SUSE
BuildRequires:  ImageMagick
BuildRequires:  bc
BuildRequires:  dejavu-fonts
BuildRequires:  fdupes
BuildRequires:  fontconfig
BuildRequires:  hicolor-icon-theme
BuildArch:      noarch
Requires:       %{name}-gtk-theme = %{version}
Requires:       obsidian-pure-icon-theme = %{version}

%description
Redmond97 SE recreates the Windows 95C (OSR 2.5) controls for GTK 2,
GTK 3, GTK 4/libadwaita, Xfce4/Xfwm4 and Wine, in 42 color schemes
(the Windows 95/98 Plus! schemes and new ones). It is a fork of
Redmond97 aimed at Xfce 4.20, with Deskbar panel support.

This metapackage installs the themes and the Obsidian Pure icon theme.

%package -n %{name}-gtk-theme
Summary:        Redmond97 SE GTK 2/3/4, Xfwm4 and Wine themes
License:        GPL-3.0-only
Group:          System/GUI/Other
Recommends:     obsidian-pure-icon-theme = %{version}
Suggests:       %{name}-gtk-theme-hidpi = %{version}
Suggests:       gtk2-engine-murrine
Suggests:       xfce4-panel-profiles

%description -n %{name}-gtk-theme
The 42 Redmond97 SE themes ("Redmond97 SE <scheme>") for GTK 2, GTK 3,
GTK 4/libadwaita and Xfwm4. Each theme directory also has a wine/*.reg
color scheme to import into a Wine prefix with regedit.

Also includes xfce4-panel-profiles layouts (Win9x, WinNT6, Deskbar,
Nanobar, Nanopanel, BoxStyle).

%package -n %{name}-gtk-theme-hidpi
Summary:        Redmond97 SE themes with 2x scaled assets (HiDPI)
License:        GPL-3.0-only
Group:          System/GUI/Other
Requires:       %{name}-gtk-theme = %{version}

%description -n %{name}-gtk-theme-hidpi
The "-HiDPI" variants of the Redmond97 SE themes, with 2x scaled Xfwm4,
GTK 2, GTK 3 and GTK 4 assets, for use with Xfce's 2x window scaling on
2K/4K displays.

%package -n obsidian-pure-icon-theme
Summary:        Obsidian Pure icon themes (Faenza/Obsidian fork) from Redmond97 SE
License:        GPL-3.0-only
Group:          System/GUI/Other

%description -n obsidian-pure-icon-theme
Obsidian Pure (upstream version %{icons_version}), a variant of
madmaxms' Obsidian icon theme (based on Faenza) adjusted for the
Redmond97 SE HiDPI themes, in 11 folder colors: Amber, Aqua, Gray,
Green, Indigo, Mint, Purple, Red, Sand, Silver and Teal.

%prep
%setup -q -c
cp %{SOURCE1} .
# Lucida Sans (the Whisker menu side-bar font upstream used) is not
# free; render that text with DejaVu Sans Bold. advpng (advancecomp)
# isn't available, so don't ask for PNG optimization.
sed -i -e 's/^menu_side_font=.*/menu_side_font="DejaVu-Sans-Bold"/' \
       -e 's/^optimize_pngs=.*/optimize_pngs=0/' builder/presets/*.conf

%build
export HOME=$PWD/_home
cd builder
# gen_theme.sh exits non-zero even on success (its final cleanup rm
# hits missing files), and 0 when it fails; check the output instead.
for c in presets/*.conf; do
  bash ./gen_theme.sh "$c" || :
done
cd ..
n=$(ls _home/.themes | wc -l)
test "$n" -eq 84 || { echo "expected 84 themes, got $n" >&2; exit 1; }
for t in _home/.themes/*; do
  for f in index.theme gtk-2.0/gtkrc gtk-3.0/gtk.css gtk-4.0/gtk.css xfwm4/themerc; do
    test -s "$t/$f" || { echo "missing $t/$f" >&2; exit 1; }
  done
done

%install
# Themes. The HiDPI ones go to their own package, so they are deduped
# in a sibling directory (fdupes makes relative links) and moved after.
install -d %{buildroot}%{_datadir}/themes %{buildroot}%{_datadir}/_hidpi
cp -a _home/.themes/*-HiDPI %{buildroot}%{_datadir}/_hidpi/
rm -rf _home/.themes/*-HiDPI
cp -a _home/.themes/* %{buildroot}%{_datadir}/themes/
find %{buildroot}%{_datadir}/themes %{buildroot}%{_datadir}/_hidpi -name .gitkeep -delete

# xfce4-panel-profiles layouts
install -d %{buildroot}%{_datadir}/xfce4-panel-profiles/layouts
install -pm 0644 extras/xfce4-panel-profiles/*.tar.bz2 \
  %{buildroot}%{_datadir}/xfce4-panel-profiles/layouts/

# Icons
install -d %{buildroot}%{_datadir}/icons
tar xJf icons/Obsidian_Pure_v%{icons_version}.tar.xz -C %{buildroot}%{_datadir}/icons
find %{buildroot}%{_datadir}/icons -xtype l -print -delete
find %{buildroot}%{_datadir}/icons -name icon-theme.cache -delete
# Stray zero-length temp files in the upstream icon tarball
find %{buildroot}%{_datadir}/icons -name "*.tmp[0-9]*" -print -delete

find %{buildroot}%{_datadir} -type d -exec chmod 0755 {} +
find %{buildroot}%{_datadir} -type f -exec chmod 0644 {} +

# Dedupe per package
%fdupes -s %{buildroot}%{_datadir}/icons
%fdupes -s %{buildroot}%{_datadir}/themes
%fdupes -s %{buildroot}%{_datadir}/_hidpi
mv %{buildroot}%{_datadir}/_hidpi/* %{buildroot}%{_datadir}/themes/
rmdir %{buildroot}%{_datadir}/_hidpi

%files
%doc README.md README.SUSE CHANGES

%files -n %{name}-gtk-theme
%license builder/src/LICENSE
%doc README.md README.SUSE CHANGES extras/r97se-fixes.sh
%{_datadir}/themes/Redmond97?SE*
%exclude %{_datadir}/themes/Redmond97?SE*-HiDPI
%dir %{_datadir}/xfce4-panel-profiles
%dir %{_datadir}/xfce4-panel-profiles/layouts
%{_datadir}/xfce4-panel-profiles/layouts/Redmond97-SE_*.tar.bz2

%files -n %{name}-gtk-theme-hidpi
%license builder/src/LICENSE
%{_datadir}/themes/Redmond97?SE*-HiDPI

%files -n obsidian-pure-icon-theme
%license builder/src/LICENSE
%{_datadir}/icons/Obsidian-Pure*

%changelog
