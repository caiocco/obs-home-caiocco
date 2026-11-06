#
# spec file for package python-python-markdown-math
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Not available for Leap 16.0; needed by python-Markups, whose Markdown
# backend refuses to load without the mdx_math module (used by ReText).
#

Name:           python-python-markdown-math
Version:        0.9
Release:        0
Summary:        Math extension for Python-Markdown
License:        BSD-3-Clause
Group:          Development/Languages/Python
URL:            https://github.com/mitya57/python-markdown-math
Source0:        https://files.pythonhosted.org/packages/source/p/python_markdown_math/python_markdown_math-%{version}.tar.gz
BuildRequires:  %{python_module Markdown >= 3}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools >= 77.0}
BuildRequires:  %{python_module wheel}
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
Requires:       python-Markdown >= 3
Provides:       python-markdown-math = %{version}-%{release}
BuildArch:      noarch
%python_subpackages

%description
This extension adds math formulas support to Python-Markdown.  Formulas
are output as <script type="math/tex"> elements, to be rendered by
MathJax.

%prep
%autosetup -n python_markdown_math-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%check
%pyunittest -v test.py

%files %{python_files}
%license LICENSE
%doc README.md changelog
%{python_sitelib}/mdx_math.py
%pycache_only %{python_sitelib}/__pycache__/mdx_math*.pyc
%{python_sitelib}/python_markdown_math-%{version}.dist-info

%changelog
