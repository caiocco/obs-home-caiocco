#
# spec file for package sarasa-gothic-fonts
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           sarasa-gothic-fonts
Version:        1.0.43
Release:        0
Summary:        Sarasa Gothic font
License:        OFL-1.1
Group:          System/X11/Fonts
URL:            https://github.com/be5invis/Sarasa-Gothic/
Source0:        https://github.com/be5invis/Sarasa-Gothic/releases/download/v%{version}/Sarasa-SuperTTC-%{version}.7z
Source1:        https://raw.githubusercontent.com/be5invis/Sarasa-Gothic/v%{version}/LICENSE
BuildRequires:  fontpackages-devel
# Needed for Leap 15.5 (the archive is sucessfully unzipped on TW with just p7zip though)
BuildRequires:  p7zip-full
Provides:       scalable-font-zh_CN
Provides:       scalable-font-zh_HK
Provides:       scalable-font-jp
Provides:       scalable-font-kr
Provides:       scalable-font-zh_TW
Obsoletes:      sarasa-gothic-fonts < %version-%release
Provides:       sarasa-gothic-fonts = %version-%release
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch


%description
This is SARASA GOTHIC, a CJK programming font based on Iosevka and Source Han Sans.

%prep
%setup -q -c
cp %{S:1} ./

%build

%install
install -d %{buildroot}%{_ttfontsdir}
# by default install command uses 755 umask
install -m 0644 *.ttc %{buildroot}%{_ttfontsdir}

%reconfigure_fonts_scriptlets -c

%files
%license LICENSE
%{_ttfontsdir}

%changelog
