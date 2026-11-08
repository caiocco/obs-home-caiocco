#To the extent possible under law, the person who associated CC0 with
#this spec file has waived all copyright and related or neighboring rights
#to this spec file.
#
#You should have received a copy of the CC0 legalcode along with this
#work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

Name:           skeuos-gtk
Version:        20220629
Release:        0
Summary:        Skeuomorphic multi-toolkit GTK theme
License:        GPL-3.0-only
Group:          System/GUI/Other
URL:            https://github.com/daniruiz/skeuos-gtk
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make

%description
Skeuos GTK is a skeuomorphic theme for GTK 2, GTK 3, GTK 4, GNOME Shell,
Cinnamon, Metacity, and XFCE/XFWM4. It comes in 13 accent colors
(Black, Blue, Brown, Cyan, Green, Grey, Magenta, Orange, Red, Teal, Violet,
White, Yellow), each in Dark and Light variants. GNOME Shell variants are
provided for GNOME 36/38, 40/41, and 42, including optional full-panel
variants. HiDPI variants are included for the XFWM4 window manager.

%prep
%setup -q
# The Nautilus "Icon view" rules (src/sass/gtk-applications-css/nautilus)
# are pasted unscoped into every gtk.css, so "flowbox { padding: 18px }"
# hits every GtkFlowBox in every app (e.g. mtPaint's GTK3 toolbar box gets
# 18px of blank space around it). Scope them to Nautilus windows.
find themes src -name '*.css' -exec sed -i -E \
    's/^(flowbox|flowboxchild|flowboxchild:selected) \{$/.nautilus-window \1 {/' {} +
test "$(grep -rlE --include='*.css' '^flowbox \{$' themes | wc -l)" -eq 0

%build
# No compilation required; all assets are pre-built.

%install
make install DESTDIR=%{buildroot} PREFIX=/usr

%files
%license LICENSE
%doc README.md CHANGELOG
%{_datadir}/themes/Skeuos-*

%changelog
