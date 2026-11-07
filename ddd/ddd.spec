#
# spec file for package ddd
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Based on the work of Boian Berberov in home:bberberov:develop:Multi/ddd.
#

%define gitdate 20261102
%define gitcommit 12f6459

Name:           ddd
Version:        3.4.1+git%{gitdate}.%{gitcommit}
Release:        0
Summary:        Data Display Debugger, a graphical front end for GDB
License:        GPL-3.0-or-later AND LGPL-3.0-or-later
Group:          Development/Tools/Debuggers
URL:            https://www.gnu.org/software/ddd/
# git archive of https://github.com/eickeler/DDD.git, commit %%{gitcommit}
Source0:        %{name}-%{version}.tar.xz
# Install shared data in /usr/share/ddd instead of /usr/share/ddd-VERSION,
# and the docs in %%{_docdir}/ddd (from home:bberberov:develop:Multi)
Patch0:         ddd-paths.patch
BuildRequires:  autoconf >= 2.71
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  motif-devel >= 2.3.4
BuildRequires:  ncurses-devel
BuildRequires:  perl
BuildRequires:  readline-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(xpm)
# For the documentation
BuildRequires:  ghostscript
BuildRequires:  info
BuildRequires:  rgb
BuildRequires:  texinfo
BuildRequires:  transfig
Requires:       gdb
Recommends:     gnuplot
Recommends:     xfontsel
Suggests:       %{name}-doc = %{version}

%description
GNU DDD (Data Display Debugger) is a graphical front end for the
command-line debuggers GDB and CUDA-GDB.

* Interactive graphical data display (visualizing data structures as
  graphs)
* Source-level debugging with breakpoints, watchpoints and call stacks
* Support for multiple debuggers, with active development focused on
  GDB and CUDA-GDB

%package doc
Summary:        Manual of the Data Display Debugger in HTML, PDF and PostScript
Group:          Documentation/Other
BuildArch:      noarch

%description doc
This package contains the DDD manual and the DDD themes manual in HTML,
PDF and PostScript formats.

%prep
%autosetup -p1 -n %{name}-%{version}
# config.texi is generated, make sure the docs wait for it
sed -i \
	-e 's@$(srcdir)/ddd.texi $(srcdir)/ddd-themes.texi@$(srcdir)/ddd.texi $(srcdir)/ddd-themes.texi $(srcdir)/config.texi@' \
	ddd/Makefile.am

%build
autoreconf -fiv
%configure \
	--docdir=%{_docdir}/%{name} \
	--htmldir=%{_docdir}/%{name}/html \
	--pdfdir=%{_docdir}/%{name}/pdf \
	--with-termlib=ncurses \
	--with-readline \
	--with-x \
	--with-motif
# The HTML manual needs PICS/dddlogo.jpg, which is not shipped
test -e ddd/PICS/dddlogo.jpg || cp ddd/PICS/dddlogo35.jpg ddd/PICS/dddlogo.jpg
# Generated sources are not parallel safe
%make_build -C ddd -j1 progstuff
%make_build
%make_build -j1 html
%make_build pdf

%install
%make_install
install -D -m 0644 icons/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
cp -a doc/html doc/*.pdf doc/*.ps %{buildroot}%{_docdir}/%{name}/
rm -f %{buildroot}%{_docdir}/%{name}/html/Makefile*
rm -f %{buildroot}%{_infodir}/dir
%fdupes %{buildroot}%{_datadir}

%files
%license doc/COPYING doc/COPYING.LESSER
%doc doc/NEWS doc/CREDITS
%{_docdir}/%{name}/ddd.info.txt
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_infodir}/ddd*
%{_mandir}/man1/ddd.1%{?ext_man}

%files doc
%{_docdir}/%{name}/html
%{_docdir}/%{name}/*.pdf
%{_docdir}/%{name}/*.ps

%changelog
