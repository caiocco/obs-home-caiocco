#To the extent possible under law, the person who associated CC0 with
#this spec file has waived all copyright and related or neighboring rights
#to this spec file.
#
#You should have received a copy of the CC0 legalcode along with this
#work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

Name:           flat-remix
Version:        20261116
Release:        0
Summary:        Flat Remix icon theme
License:        GPL-3.0-only AND CC-BY-SA-4.0
Group:          System/GUI/Other
URL:            https://drasite.com/flat-remix
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Flat Remix is a pretty simple icon theme inspired by Material Design.
It is mostly flat using a colorful palette with some shadows, highlights
and gradients for some depth. It comes in 12 color variants (Black, Blue,
Brown, Cyan, Green, Grey, Magenta, Orange, Red, Teal, Violet, Yellow),
each available in Dark, Light, and Light-darkPanel variants.

%prep
%setup -q

%build
# No compilation required; all assets are pre-built.

%install
make install DESTDIR=%{buildroot} PREFIX=/usr
# 20261116 ships dangling links in the Dark variants (kali-server-mcp.svg
# -> missing server-mcp.svg, self-referencing xplico.svg); drop them
find %{buildroot}%{_datadir}/icons -xtype l -print -delete

%files
%license LICENSE
%doc README.md AUTHORS CHANGELOG
%{_datadir}/icons/Flat-Remix-*

%changelog
