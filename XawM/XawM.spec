#
# spec file for package XawM
#
# To the extent possible under law, the person who associated CC0 with
# this spec file has waived all copyright and related or neighboring rights
# to this spec file.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#

%define sover 1

Name:           XawM
Version:        1.5u
Release:        0
Summary:        Modern-look (Motif-like) Athena widget set
License:        MIT
Group:          Development/Libraries/X11
URL:            https://siag.nu/
Source0:        https://siag.nu/pub/widgets/%{name}-%{version}.tar.gz
# PATCH-FIX-UPSTREAM xawm-gcc15.patch -- missing prototypes/includes and implicit int (GCC 15)
Patch0:         xawm-gcc15.patch
# PATCH-FIX-UPSTREAM xawm-link-libs.patch -- link libXawM against the X libraries it uses
Patch1:         xawm-link-libs.patch
# PATCH-FIX-UPSTREAM xawm-xim-latin1.patch -- 8-bit Text composes dead keys through XIM (shared input context with Mowitz)
Patch2:         xawm-xim-latin1.patch
# PATCH-FIX-UPSTREAM xawm-delete-key.patch -- Delete/KP_Delete deleted backwards like BackSpace
Patch3:         xawm-delete-key.patch
# PATCH-FIX-UPSTREAM xawm-focus-explicit.patch -- default focus policy explicit: LeaveWindow no longer resets the X focus to PointerRoot
Patch4:         xawm-focus-explicit.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xt)

%description
XawM ("M" for Modern) is Edward A. Falk's variant of the Three-D Athena
widget set (Xaw3d 1.5), changed to follow the look and feel of Motif and
similar toolkits, as adapted by Ulric Eriksson for Siag Office.

%package -n lib%{name}%{sover}
Summary:        Modern-look (Motif-like) Athena widget library
Group:          System/Libraries

%description -n lib%{name}%{sover}
XawM ("M" for Modern) is Edward A. Falk's variant of the Three-D Athena
widget set (Xaw3d 1.5), changed to follow the look and feel of Motif and
similar toolkits.

%package devel
Summary:        Development files for the XawM widget set
Group:          Development/Libraries/X11
Requires:       lib%{name}%{sover} = %{version}
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xext)
Requires:       pkgconfig(xmu)
Requires:       pkgconfig(xt)

%description devel
Headers and the shared library link for XawM.

The headers live in %{_includedir}/X11/XawM. Programs written for
<X11/Xaw/...> can be built against XawM by adding
-I%{_includedir}/XawM to CPPFLAGS: that directory holds an X11/Xaw
symlink to the XawM headers, so the widget structures match the library.

%prep
%autosetup -p1
# keep the pregenerated parser and lexer (both patched)
touch X11/XawM/laygram.c X11/XawM/laylex.c

%build
autoreconf -fi
%configure --disable-static CFLAGS="%{optflags} -std=gnu17"
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.la' -delete -print
mkdir -p %{buildroot}%{_includedir}/%{name}/X11
ln -s ../../X11/XawM %{buildroot}%{_includedir}/%{name}/X11/Xaw

%ldconfig_scriptlets -n lib%{name}%{sover}

%files -n lib%{name}%{sover}
%doc README README.XAW3D README.XawM
%{_libdir}/libXawM.so.%{sover}{,.*}

%files devel
%doc ChangeLog README.Linux
%{_libdir}/libXawM.so
%{_includedir}/X11/XawM
%{_includedir}/%{name}

%changelog
