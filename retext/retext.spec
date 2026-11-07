#
# spec file for package retext
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Snapshot of the master branch: the last release (8.1.0) is from January
# 2025.  Built with Qt 6 (PyQt6); the Qt translations are compiled with
# lrelease from qt6-tools-linguist.
#

%define rt_commit   746281ba92269561a26abed15fe7c14478ab15b1
%define rt_short    746281b
%define rt_date     20261016
%define pythons     python3

Name:           retext
Version:        8.1.0+git%{rt_date}.%{rt_short}
Release:        0
Summary:        Simple editor for Markdown and reStructuredText
License:        GPL-2.0-or-later
Group:          Productivity/Text/Editors
URL:            https://github.com/retext-project/retext
Source0:        https://github.com/retext-project/retext/archive/%{rt_commit}.tar.gz#/retext-%{rt_commit}.tar.gz
BuildRequires:  %{python_module Markups >= 4.0}
BuildRequires:  %{python_module PyQt6}
BuildRequires:  %{python_module Pygments}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools >= 62.4}
BuildRequires:  %{python_module wheel}
BuildRequires:  desktop-file-utils
# QTextDocument::toMarkdown() detects bold text through the resolved font,
# so test_pasteHtmlConvertedToMarkdown needs a real font with a bold face
BuildRequires:  dejavu-fonts
BuildRequires:  fdupes
BuildRequires:  hicolor-icon-theme
BuildRequires:  python-rpm-macros
BuildRequires:  qt6-macros
BuildRequires:  qt6-tools-linguist
Requires:       python3-Markups >= 4.0
Requires:       python3-PyQt6
Requires:       python3-Pygments
# WebEngine-based preview (optional, selected in the preferences)
Recommends:     python3-PyQt6-WebEngine
# automatic encoding detection
Recommends:     python3-chardet
# spell checking
Recommends:     python3-pyenchant
Provides:       ReText = %{version}
BuildArch:      noarch

%description
ReText is a simple but powerful editor for Markdown and reStructuredText
markup languages, written in Python using the PyQt libraries.

Features include a live preview (side by side or in a separate tab), tabs,
export to HTML, ODT and PDF, spell checking, table editing mode, syntax
highlighting, MathJax formulas and custom CSS styles.

%prep
%autosetup -n retext-%{rt_commit}
sed -i '1{/^#!/d}' ReText/__main__.py

%build
# setup.py looks for "lrelease" in PATH (via qmake6, not installed here)
export PATH=%{_qt6_bindir}:$PATH
%pyproject_wheel

%install
%pyproject_install
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/me.mitya57.ReText.desktop
# make sure the translations were compiled
ls %{buildroot}%{python3_sitelib}/ReText/locale/retext_pt_BR.qm
export QT_QPA_PLATFORM=offscreen
%pyunittest discover -v tests

%files
%license LICENSE_GPL
%doc README.md changelog.md configuration.md
%{_bindir}/retext
%{python3_sitelib}/ReText/
%{python3_sitelib}/[Rr]e[Tt]ext-*.dist-info
%{_datadir}/applications/me.mitya57.ReText.desktop
%{_datadir}/icons/hicolor/scalable/apps/retext.svg
%{_datadir}/metainfo/me.mitya57.ReText.metainfo.xml

%changelog
