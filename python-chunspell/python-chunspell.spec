#
# spec file for package python-chunspell
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# Cython wrapper around hunspell (fork of CyHunspell), needed by OutWiker.
# The sdist ships a prebuilt libhunspell and would download and build its
# own hunspell 1.7.2; the patch links the extension against the system
# hunspell instead.  The Cython-generated hunspell.cpp is used as shipped.
#

Name:           python-chunspell
Version:        2.0.5
Release:        0
Summary:        Cython wrapper around the hunspell spell checker
License:        MIT
Group:          Development/Languages/Python
URL:            https://github.com/cdhigh/chunspell
Source0:        https://files.pythonhosted.org/packages/source/c/chunspell/chunspell-%{version}.tar.gz
Patch0:         chunspell-system-hunspell.patch
BuildRequires:  %{python_module devel}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module wheel}
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  hunspell-devel
BuildRequires:  python-rpm-macros
# Same "hunspell" module name as CyHunspell
Conflicts:      python-cyhunspell
%python_subpackages

%description
A Cython wrapper around the hunspell spell checking library, forked from
CyHunspell.  It provides spell checking, suggestions, stemming and
morphological analysis from Python, with optional caching and bulk
operations.  The module is imported as "hunspell".

%prep
%autosetup -p1 -n chunspell-%{version}
# Prebuilt private copy of hunspell; the system library is used instead
rm hunspell/libhunspell-1.7.so.0

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
%pyproject_wheel

%install
%pyproject_install
%python_expand %fdupes %{buildroot}%{$python_sitearch}

%check
# Upstream tests are not in the sdist: check the module against the
# bundled en_US dictionary
%{python_expand export PYTHONPATH=%{buildroot}%{$python_sitearch}
cd /
$python -c "
import hunspell
h = hunspell.Hunspell('en_US')
assert h.spell('dictionary')
assert not h.spell('dictionnary')
assert 'dictionary' in h.suggest('dictionnary')
print('hunspell', hunspell.__version__, 'OK')
"
}
# Must not carry a private hunspell or an $ORIGIN rpath
! find %{buildroot} -name 'libhunspell*' | grep .
! objdump -p %{buildroot}%{python3_sitearch}/hunspell/hunspell.*.so | grep -E 'RUNPATH|RPATH'

%files %{python_files}
%license LICENSE
%doc README.md
%{python_sitearch}/hunspell
%{python_sitearch}/chunspell-%{version}.dist-info

%changelog
