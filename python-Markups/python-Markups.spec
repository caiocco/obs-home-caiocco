#
# spec file for package python-Markups
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Not available for Leap 16.0; needed by ReText.  The Markdown and
# reStructuredText backends are required, the others are optional.
#

Name:           python-Markups
Version:        4.1.1
Release:        0
Summary:        A wrapper around various text markups
License:        BSD-3-Clause
Group:          Development/Languages/Python
URL:            https://github.com/retext-project/pymarkups
Source0:        https://files.pythonhosted.org/packages/source/m/markups/markups-%{version}.tar.gz
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools >= 77.0}
BuildRequires:  %{python_module wheel}
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
# SECTION test requirements
BuildRequires:  %{python_module Markdown >= 3}
BuildRequires:  %{python_module PyYAML}
BuildRequires:  %{python_module Pygments}
BuildRequires:  %{python_module docutils}
BuildRequires:  %{python_module python-markdown-math}
BuildRequires:  %{python_module textile}
# /SECTION
Requires:       python-Markdown >= 3
Requires:       python-PyYAML
Requires:       python-docutils
Requires:       python-python-markdown-math
Recommends:     python-Pygments
Suggests:       python-textile
BuildArch:      noarch
%python_subpackages

%description
This module provides a wrapper around various text markup languages.

Available by default are Markdown, reStructuredText and Textile, but
other markups can be added as well.

%prep
%autosetup -n markups-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%check
%pyunittest discover -v

%files %{python_files}
%license LICENSE
%doc README.rst changelog
%{python_sitelib}/markups/
%{python_sitelib}/[Mm]arkups-%{version}.dist-info

%changelog
