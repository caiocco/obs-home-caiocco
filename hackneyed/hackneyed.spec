#To the extent possible under law, the person who associated CC0 with
#this spec file has waived all copyright and related or neighboring rights
#to this spec file.
#
#You should have received a copy of the CC0 legalcode along with this
#work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

Name:           hackneyed
Version:        0.9.3
Release:        0
Summary:        Windows 3.x-inspired X11 cursor theme
License:        BSD-2-Clause
Group:          System/GUI/Other
URL:            https://gitlab.com/Augmented-Development/hackneyed-x11-cursors
Source0:        Hackneyed-%{version}-right-handed.tar
Source1:        Hackneyed-Dark-%{version}-right-handed.tar

BuildArch:      noarch

%description
Hackneyed is a cursor theme inspired by the classic Windows 3.x arrow cursor.
It includes both bitmap cursors (for fixed sizes) and scalable SVG sources.
This package provides two variants: Hackneyed (light) and Hackneyed-Dark.

%prep
%setup -q -c -T
tar -xf %{SOURCE0}
tar -xf %{SOURCE1}

%build
# No compilation required; all assets are pre-built.

%install
install -dm 755 %{buildroot}%{_datadir}/icons
cp -a Hackneyed      %{buildroot}%{_datadir}/icons/
cp -a Hackneyed-Dark %{buildroot}%{_datadir}/icons/

%files
%{_datadir}/icons/Hackneyed/
%{_datadir}/icons/Hackneyed-Dark/

%changelog
