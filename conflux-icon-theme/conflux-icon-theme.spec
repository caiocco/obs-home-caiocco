#To the extent possible under law, the person who associated CC0 with
#this spec file has waived all copyright and related or neighboring rights
#to this spec file.
#
#You should have received a copy of the CC0 legalcode along with this
#work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

%define commit  f3808414e66ac8d32847c9cdcc6a657b69c6c792
%define shortcommit %(c=%{commit}; echo ${c:0:7})
%define gitdate 20261114
%define _name   Conflux

Name:           conflux-icon-theme
Version:        0+git%{gitdate}.%{shortcommit}
Release:        0
Summary:        Modern, neutral icon theme that blends with unthemed icons
License:        GPL-3.0-only
Group:          System/GUI/Other
URL:            https://github.com/MoshiurRahmanAdib/Conflux-Icon-Theme
Source0:        %{url}/archive/%{commit}/Conflux-Icon-Theme-%{commit}.tar.gz
BuildRequires:  fdupes
BuildRequires:  hicolor-icon-theme
Recommends:     adwaita-icon-theme
BuildArch:      noarch

%description
Conflux is a modern, clean icon theme with a neutral visual language,
designed so that applications without a themed icon still fit in.
Many icons are adapted from WhiteSur, McMuse, Kora, MoreWaita, MacTahoe,
Papirus and other themes; the rest falls back to Adwaita and hicolor.

%prep
%autosetup -n Conflux-Icon-Theme-%{commit}

%build
# Nothing to build: the icons are pre-rendered SVGs.

%install
install -d %{buildroot}%{_datadir}/icons/%{_name}
# Workspace/ (Inkscape sources), images/ (README pictures) and update.sh
# (git pull helper) are not part of the theme.
cp -a index.theme apps apps@2x devices devices@2x emblems emblems@2x \
      mimes mimes@2x places places@2x preferences preferences@2x \
      status status@2x %{buildroot}%{_datadir}/icons/%{_name}/
pushd %{buildroot}%{_datadir}/icons/%{_name}
# Convenience links to Workspace/optimize.sh inside the icon dirs.
find . -name optimize.sh -type l -delete
# These two aliases lack the .svg suffix, so icon lookup never finds them.
mv apps/scalable/kcalc apps/scalable/kcalc.svg
mv apps/scalable/org.kde.kcalc apps/scalable/org.kde.kcalc.svg
popd
%icon_theme_cache_create_ghost %{_name}
%fdupes -s %{buildroot}%{_datadir}/icons/%{_name}

%files
%license LICENSE
%doc README.md CREDITS.md
%dir %{_datadir}/icons/%{_name}
%{_datadir}/icons/%{_name}/index.theme
%{_datadir}/icons/%{_name}/{apps,devices,emblems,mimes,places,preferences,status}
%{_datadir}/icons/%{_name}/{apps,devices,emblems,mimes,places,preferences,status}@2x
%ghost %{_datadir}/icons/%{_name}/icon-theme.cache

%changelog
