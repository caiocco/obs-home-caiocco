#
# spec file for package classic-colors
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

Name:           classic-colors
Version:        1.1.1
Release:        0
Summary:        Paint program for X11 based on Motif
# Embedded fonts: Bitstream Vera Sans Mono (Bitstream-Vera), Vegur and Seshat (CC0-1.0)
License:        GPL-2.0-only AND Bitstream-Vera AND CC0-1.0
Group:          Productivity/Graphics/Bitmap Editors
URL:            https://github.com/justinmeiners/classic-colors
Source0:        https://github.com/justinmeiners/classic-colors/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
# PATCH-FIX-UPSTREAM classic-colors-gcc14.patch -- fix pointer types rejected by GCC 14+ (XmStringFree for an XmString, XmStringTable casts)
Patch0:         %{name}-gcc14.patch
# PATCH-FEATURE-OPENSUSE classic-colors-save-prompt.patch -- ask to save unsaved changes on File > Exit and window close
Patch1:         %{name}-save-prompt.patch
# PATCH-FIX-OPENSUSE classic-colors-text-box-click.patch -- a click no longer creates an invisible text box; boxes fit one line
Patch2:         %{name}-text-box-click.patch
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  hicolor-icon-theme
BuildRequires:  make
BuildRequires:  motif-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(xt)
# Help and the About "Website" button use xdg-open
Recommends:     xdg-utils
# Named colours in the Edit Colors dialog come from rgb.txt
Recommends:     rgb

%description
Classic Colors is a simple and efficient paint program for Unix
systems, inspired by MS Paint from Windows 95/98. It is built on the
Motif toolkit and offers pencil, brush, airbrush, eraser, fill, line,
curve, rectangle, ellipse, polygon, text, eye dropper, magnifier and
rectangle/free-form selection tools. It reads and writes PNG, JPEG,
BMP, GIF and TGA images.

%prep
%autosetup -p1
sed -i 's|file:///usr/local/share/classic-colors/|file://%{_datadir}/%{name}/|' ui_main.c
sed -i 's|Classic Colors v1\.0\.1|Classic Colors v%{version}|' ui_main.c
# Use the desktop file ID as the X class, so taskbars that look up
# <class>.desktop (libxfce4windowing) find our icon instead of guessing
sed -i 's|^\(            \)"Paint",$|\1"classic-colors",|' ui_main.c
# Use distribution optimisation flags instead of -O3
sed -i 's| -O3 | |' configure
grep -q 'file://%{_datadir}/%{name}/help' ui_main.c
grep -q 'v%{version}' ui_main.c
grep -q '"classic-colors",$' ui_main.c

%build
./configure
# The makefile appends to CFLAGS/LDFLAGS, so pass them through the environment
export CFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
%make_build

%install
%make_install PREFIX=%{buildroot}%{_prefix}
install -Dm0644 classic-colors.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -Dm0644 icons/icon_app.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_mandir}/man1/%{name}.1%{?ext_man}

%changelog
