#
# spec file for package pgmodeler
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Community build of pgModeler (the paid "Plus" sources are not public).
# The helper programs (crash handler, schema editor) live with the private
# libraries, where their $ORIGIN RUNPATH finds them.
# Upstream ships no .desktop or MIME file, so they are provided here.
#

# Private, unversioned libraries (libcore.so, libutils.so, ...)
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude ^lib(canvas|cli|connector|core|gui|parsers|utils)\.so.*$

Name:           pgmodeler
Version:        2.0.0
Release:        0
Summary:        PostgreSQL Database Modeler
License:        GPL-3.0-only
Group:          Productivity/Databases/Tools
URL:            https://pgmodeler.io/
Source0:        https://github.com/nullptrlabs/pgmodeler/archive/refs/tags/v%{version}.tar.gz#/pgmodeler-%{version}.tar.gz
Source1:        pgmodeler.desktop
Source2:        pgmodeler-mime.xml
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
Requires:       shared-mime-info
Recommends:     %{name}-lang = %{version}

%description
pgModeler is an open source data modeling tool designed for PostgreSQL.
It brings together the concepts of entity-relationship diagrams and the
features that PostgreSQL implements as extensions of the SQL standard,
generates the SQL (DDL) code for a model, deploys it on a server, and can
import, compare and diff existing databases.

%package lang
Summary:        Translations for pgModeler
Group:          System/Localization
Requires:       %{name} = %{version}
BuildArch:      noarch

%description lang
User interface translations for pgModeler.

%prep
%autosetup -p1
# Upstream hard-codes clang on Linux; use the distribution compiler
sed -i '/set(CMAKE_C\(XX\)\?_COMPILER \/usr\/bin\/clang/d' BuildConfs.cmake

%build
%cmake \
  -DNO_UPDATE_CHECK=ON \
  -DPGM_PREFIX=%{_prefix} \
  -DPGM_BINDIR=%{_bindir} \
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
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm0644 %{SOURCE2} %{buildroot}%{_datadir}/mime/packages/%{name}.xml
install -Dm0644 assets/conf/pgmodeler_logo.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -Dm0644 assets/conf/pgmodeler_dbm.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/mimetypes/application-x-pgmodeler.png
install -Dm0644 pgmodeler.appdata.xml %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
%fdupes %{buildroot}%{_datadir}/%{name}

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
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/mimetypes/application-x-pgmodeler.png
%{_datadir}/metainfo/%{name}.appdata.xml

%files lang
%{_datadir}/%{name}/lang

%changelog
