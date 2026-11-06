#
# spec file for package nedit
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define ne_commit   dd408440cb392db2258edfef753c57e134cfbbd8
%define ne_short    dd40844
%define ne_date     20260411

Name:           nedit
Version:        5.7+git%{ne_date}.%{ne_short}
Release:        0
Summary:        Multi-purpose text editor for X11 based on Motif
License:        GPL-2.0-or-later AND LGPL-2.0-or-later AND (MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later)
Group:          Productivity/Text/Editors
URL:            https://github.com/alx210/nedit-classic
Source0:        https://github.com/alx210/nedit-classic/archive/%{ne_commit}.tar.gz#/%{name}-%{ne_commit}.tar.gz
Source1:        %{name}.desktop
BuildRequires:  bison
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  perl
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xt)

%description
NEdit is a multi-purpose text editor for the X Window System, which
combines a standard, easy to use, graphical user interface with the
functionality required by programmers: syntax highlighting for many
languages, smart indent, rectangular selections, regular expression
search and replace, a macro language, tags, tabbed editing and
shell command integration.

This is NEdit Classic, a maintained fork of NEdit 5.7 that adds
anti-aliased (Xft) font rendering and workspace support for MWM/EMWM.
The client program, which opens files in a running NEdit server, is
installed as ncl.

%prep
%autosetup -n %{name}-classic-%{ne_commit}
sed -i \
  -e 's|^CFLAGS=.*|CFLAGS=%{optflags} $(shell pkg-config --cflags xft) -DUSE_XRENDER -DUSE_DIRENT -DUSE_LPR_PRINT_CMD -ansi -U__STRICT_ANSI__|' \
  -e 's|^LIBS=.*|LIBS=%{?build_ldflags} $(shell pkg-config --libs xft fontconfig freetype2 xrender) -lXm -lXt -lX11 -lm|' \
  makefiles/Makefile.linux-xft
for d in util Xlt source; do
  ln -s ../makefiles/Makefile.linux-xft $d/
done
ln -s ../../makefiles/Makefile.linux-xft Microline/XmL/
# The client is installed as ncl (nc is netcat)
sed -i \
  -e 's|^nc - |ncl - |' \
  -e 's|^nc \[|ncl [|' \
  -e 's|B<nc>|B<ncl>|g' \
  -e 's|L<nc(1)>|L<ncl(1)>|g' \
  -e 's|^  nc |  ncl |' \
  doc/nc.pod

%build
%make_build -C util -f Makefile.linux-xft libNUtil.a
%make_build -C Xlt -f Makefile.linux-xft libXlt.a
%make_build -C Microline/XmL -f Makefile.linux-xft libXmL.a
%make_build -C source -f Makefile.linux-xft nedit nc
for m in nedit:nedit nc:ncl; do
  pod2man --release="NEdit %{version}" --center="NEdit documentation" \
    --name="${m#*:}" --section=1 doc/${m%%:*}.pod > ${m#*:}.1
done

%install
install -Dm0755 source/nedit %{buildroot}%{_bindir}/nedit
install -Dm0755 source/nc %{buildroot}%{_bindir}/ncl
install -Dm0644 -t %{buildroot}%{_mandir}/man1 nedit.1 ncl.1
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license COPYRIGHT
%doc README ReleaseNotes doc/faq.txt doc/NEdit.ad
%{_bindir}/nedit
%{_bindir}/ncl
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/nedit.1%{?ext_man}
%{_mandir}/man1/ncl.1%{?ext_man}

%changelog
