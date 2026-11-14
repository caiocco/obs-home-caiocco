#
# spec file for package pgmodeler2
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# pgModeler 2.x Community edition, installable next to the pgmodeler
# package (1.2.x). Since 2.0 the database import, model diff, SQL tool,
# data grid and database explorer are exclusive to the paid Plus edition.
#
# Every executable lives in the private library directory, so the
# upstream $ORIGIN RUNPATH points at a library path, and /usr/bin only
# holds pgmodeler2 / pgmodeler2-cli symlinks. pgModeler starts its helper
# programs from BINDIR by their upstream names. The .dbm MIME type and its
# icon come from the pgmodeler package.
#

%define upname  pgmodeler

# Private, unversioned libraries (libcore.so, libutils.so, ...)
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude ^lib(canvas|cli|connector|core|gui|parsers|utils)\.so.*$

Name:           pgmodeler2
Version:        2.0.0
Release:        0
Summary:        PostgreSQL Database Modeler, 2.x Community edition
License:        GPL-3.0-only
Group:          Productivity/Databases/Tools
URL:            https://pgmodeler.io/
Source0:        https://github.com/nullptrlabs/pgmodeler/archive/refs/tags/v%{version}.tar.gz#/%{upname}-%{version}.tar.gz
Source1:        pgmodeler2.desktop
BuildRequires:  cmake >= 3.16
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  qt6-linguist-devel
BuildRequires:  cmake(Qt6Core) >= 6.6
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6PrintSupport)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(libpq)
BuildRequires:  pkgconfig(libxml-2.0)
Recommends:     %{name}-lang = %{version}

%description
pgModeler is an open source data modeling tool designed for PostgreSQL.
It brings together the concepts of entity-relationship diagrams and the
features that PostgreSQL implements as extensions of the SQL standard,
and generates the SQL (DDL) code for a model.

This is the 2.x Community edition, installed as pgmodeler2 so it can be
used next to pgModeler 1.2. It adds multi-scene models, a new interface and
initial PostgreSQL 18 support, but database import, model diff, the SQL
tool and the database explorer are only in the paid Plus edition.

%package lang
Summary:        Translations for pgModeler 2
Group:          System/Localization
Requires:       %{name} = %{version}
BuildArch:      noarch

%description lang
User interface translations for pgModeler 2.

%prep
%autosetup -p1 -n %{upname}-%{version}
# Upstream hard-codes clang on Linux; use the distribution compiler
sed -i '/set(CMAKE_C\(XX\)\?_COMPILER \/usr\/bin\/clang/d' BuildConfs.cmake

%build
%cmake \
  -DNO_UPDATE_CHECK=ON \
  -DPGM_PREFIX=%{_prefix} \
  -DPGM_BINDIR=%{_libdir}/%{name} \
  -DPGM_PRIVATEBINDIR=%{_libdir}/%{name} \
  -DPGM_PRIVATELIBDIR=%{_libdir}/%{name} \
  -DPGM_PLUGINSDIR=%{_libdir}/%{name}/plugins \
  -DPGM_SHAREDIR=%{_datadir}/%{name} \
  -DPGM_CONFDIR=%{_datadir}/%{name}/conf \
  -DPGM_DOCDIR=%{_docdir}/%{name} \
  -DPGM_LANGDIR=%{_datadir}/%{name}/lang \
  -DPGM_SAMPLESDIR=%{_datadir}/%{name}/samples \
  -DPGM_SCHEMASDIR=%{_datadir}/%{name}/schemas
%cmake_build

%install
%cmake_install
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/%{upname} %{buildroot}%{_bindir}/%{name}
ln -s %{_libdir}/%{name}/%{upname}-cli %{buildroot}%{_bindir}/%{name}-cli
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm0644 assets/conf/pgmodeler_logo.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
sed -e 's|<id type="desktop">pgmodeler.desktop</id>|<id type="desktop">%{name}.desktop</id>|' \
    -e 's|<name>pgmodeler</name>|<name>pgModeler 2</name>|' \
    pgmodeler.appdata.xml > appdata.xml
install -Dm0644 appdata.xml %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
%fdupes -s %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license %{_docdir}/%{name}/LICENSE
%doc CHANGELOG.md README.md RELEASENOTES.md
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/conf
%{_datadir}/%{name}/samples
%{_datadir}/%{name}/schemas
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/metainfo/%{name}.appdata.xml

%files lang
%{_datadir}/%{name}/lang

%changelog
