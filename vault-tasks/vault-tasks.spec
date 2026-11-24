#
# spec file for package vault-tasks
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# vendor.tar.zst holds the crates from "cargo vendor" plus the matching
# .cargo/config.toml; regenerate it for every version bump.
#

Name:           vault-tasks
Version:        2.0.4
Release:        0
Summary:        TUI Markdown task manager
# LICENSE in the tree is MPL-2.0 (Cargo.toml still says MIT)
License:        MPL-2.0
URL:            https://github.com/louis-thevenet/vault-tasks
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        vendor.tar.zst
# The 2.0.4 tag bumped the crate versions but not Cargo.lock
Patch0:         vault-tasks-cargo-lock-version.patch
BuildRequires:  cargo-packaging
BuildRequires:  desktop-file-utils
# edition 2024
BuildRequires:  rust+cargo >= 1.85
BuildRequires:  zstd
ExclusiveArch:  %{rust_tier1_arches}

%description
vault-tasks is a terminal task manager for Markdown vaults (such as
Obsidian vaults or any directory of notes). It parses tasks written as
Markdown check lists, with due dates, priorities, tags and subtasks, and
shows them in an explorer view, a filter view, a calendar and a time
management (Pomodoro/flowtime) view. Tasks are edited in place, so the
notes remain the only data store.

%prep
%autosetup -p1 -a1
# "Productivity" is not a registered category; Version is the spec
# version, not the program's
sed -i -e 's/^Categories=.*/Categories=Utility;ConsoleOnly;/' \
       -e 's/^Version=.*/Version=1.5/' \
       -e '/^GenericName=/a Comment=Manage the tasks written in a Markdown vault' \
       desktop/vault-tasks-tui.desktop

%build
%{cargo_build}

%install
%cargo_install -p vault-tasks-tui
install -Dm0644 desktop/vault-tasks-tui.desktop \
  %{buildroot}%{_datadir}/applications/vault-tasks-tui.desktop
export HOME=$(mktemp -d)
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions \
         %{buildroot}%{_datadir}/zsh/site-functions \
         %{buildroot}%{_datadir}/fish/vendor_completions.d
%{buildroot}%{_bindir}/vault-tasks-tui generate-completions bash \
  > %{buildroot}%{_datadir}/bash-completion/completions/vault-tasks-tui
%{buildroot}%{_bindir}/vault-tasks-tui generate-completions zsh \
  > %{buildroot}%{_datadir}/zsh/site-functions/_vault-tasks-tui
%{buildroot}%{_bindir}/vault-tasks-tui generate-completions fish \
  > %{buildroot}%{_datadir}/fish/vendor_completions.d/vault-tasks-tui.fish

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/vault-tasks-tui.desktop
%{cargo_test}

%files
%license LICENSE
%doc README.md vault-tasks-tui/CHANGELOG.md
%doc vault-tasks-core/.config/core.toml vault-tasks-tui/.config/tui.toml
%{_bindir}/vault-tasks-tui
%{_datadir}/applications/vault-tasks-tui.desktop
%{_datadir}/bash-completion/completions/vault-tasks-tui
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_vault-tasks-tui
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/vault-tasks-tui.fish

%changelog
