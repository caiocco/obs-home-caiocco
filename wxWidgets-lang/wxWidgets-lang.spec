#
# spec file for package wxWidgets-lang
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define catalog wxstd-3.2
Name:           wxWidgets-lang
Version:        3.2.8
Release:        0
Summary:        Translations for the wxWidgets 3.2 library
License:        LGPL-2.1-or-later WITH WxWindows-exception-3.1
Group:          System/Localization
URL:            https://www.wxwidgets.org/
Source0:        https://github.com/wxWidgets/wxWidgets/releases/download/v%{version}/wxWidgets-%{version}.tar.bz2
BuildRequires:  gettext-tools
BuildArch:      noarch

%description
Translations of the standard wxWidgets 3.2 messages ("wxstd" catalog):
labels of stock buttons, common dialogs, error messages and so on.

openSUSE's wxWidgets-3_2 package drops these catalogs and only recommends
this package, which no longer exists in the distribution. Without them,
wxWidgets applications show stock dialogs in English, and some (e.g.
wxMaxima) warn at startup that no standard catalogs were found.

%prep
%autosetup -n wxWidgets-%{version}

%build
cd locale
for po in *.po; do
  msgfmt --check-format -o "${po%%.po}.mo" "$po"
done

%install
cd locale
for mo in *.mo; do
  lang=${mo%%.mo}
  install -Dpm 0644 "$mo" %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/%{catalog}.mo
done
cd ..
%find_lang %{catalog}

%files -f %{catalog}.lang
%license docs/licence.txt docs/lgpl.txt

%changelog
