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
# pgModeler 1.2.x is kept on purpose: it is the last series whose open
# source build has database import, model diff, the SQL tool and the
# database explorer (2.0 moved them to the paid Plus edition). The 2.x
# Community edition is packaged separately as pgmodeler2.
#
# Every executable lives in the private library directory, so the
# upstream $ORIGIN RUNPATH points at a library path, and /usr/bin only
# holds symlinks. Upstream ships no .desktop or MIME file, so they are
# provided here.
#

# Private, unversioned libraries (libcore.so, libutils.so, ...)
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude ^lib(canvas|cli|connector|core|gui|parsers|utils)\.so.*$

Name:           pgmodeler
Version:        1.2.3
Release:        0
Summary:        PostgreSQL Database Modeler
License:        GPL-3.0-only
Group:          Productivity/Databases/Tools
URL:            https://pgmodeler.io/
Source0:        https://github.com/nullptrlabs/pgmodeler/archive/refs/tags/v%{version}.tar.gz#/pgmodeler-%{version}.tar.gz
Source1:        pgmodeler.desktop
Source2:        pgmodeler-mime.xml
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  qt6-macros
BuildRequires:  cmake(Qt6Core) >= 6.4
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6PrintSupport)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(libpq)
BuildRequires:  pkgconfig(libxml-2.0)
Requires:       shared-mime-info

%description
pgModeler is an open source data modeling tool designed for PostgreSQL.
It brings together the concepts of entity-relationship diagrams and the
features that PostgreSQL implements as extensions of the SQL standard,
generates the SQL (DDL) code for a model, deploys it on a server, and can
import, compare and diff existing databases.

%prep
%autosetup -p1

%build
%qmake6 pgmodeler.pro \
  NO_UPDATE_CHECK=true \
  PREFIX=%{_prefix} \
  BINDIR=%{_libdir}/%{name} \
  PRIVATEBINDIR=%{_libdir}/%{name} \
  PRIVATELIBDIR=%{_libdir}/%{name} \
  PLUGINSDIR=%{_libdir}/%{name}/plugins \
  SHAREDIR=%{_datadir}/%{name} \
  CONFDIR=%{_datadir}/%{name}/conf \
  DOCDIR=%{_docdir}/%{name} \
  LANGDIR=%{_datadir}/%{name}/lang \
  SAMPLESDIR=%{_datadir}/%{name}/samples \
  SCHEMASDIR=%{_datadir}/%{name}/schemas
%make_build

%install
make INSTALL_ROOT=%{buildroot} install
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}
ln -s %{_libdir}/%{name}/%{name}-cli %{buildroot}%{_bindir}/%{name}-cli
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm0644 %{SOURCE2} %{buildroot}%{_datadir}/mime/packages/%{name}.xml
install -Dm0644 assets/conf/pgmodeler_logo.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -Dm0644 assets/conf/pgmodeler_dbm.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/mimetypes/application-x-pgmodeler.png
install -Dm0644 pgmodeler.appdata.xml %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
%fdupes -s %{buildroot}%{_datadir}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/CHANGELOG.md
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/RELEASENOTES.md
%dir %{_docdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/mimetypes/application-x-pgmodeler.png
%{_datadir}/metainfo/%{name}.appdata.xml

%changelog
