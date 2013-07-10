%define url_ver    %(echo %{version}|cut -d. -f1,2)
%define oname      mate-character-map
%define name       mucharmap
%define major      7
%define libname    %mklibname %{name} %{major}
%define develname  %mklibname -d %{name}
%define gi_major   2.0
%define girname    %mklibname %{name}-gir %{gi_major}

Name:              %{name}
Version:           1.6.0
Release:           1
License:           GPLv2+ and LGPLv2+
Summary:           Unicode character map and font viewer for MATE
Url:               http://mate-desktop.org
Group:             Publishing
Source0:           http://pub.mate-desktop.org/releases/%{url_ver}/%{oname}-%{version}.tar.xz
 
BuildRequires:  libxml2-python
BuildRequires:  mate-common
BuildRequires:  which
BuildRequires:  xml2po
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(mate-doc-utils)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(pygtk-2.0)

Provides:       %oname = %version-%release

%description
Mucharmap is a Unicode/ISO 10646 character map and font viewer. It
supports anti-aliased, scalable truetype fonts in X, using Xft, and
works on Unix and Windows platforms.

%package -n %{libname}
Summary:        MATE Desktop mucharmap system libraries
Group:          System/Libraries
Provides:       %mklibname %{oname} %{major} = %{version}-%{release}

%description -n %{libname}
Mucharmap is a Unicode/ISO 10646 character map and font viewer. It
supports anti-aliased, scalable truetype fonts in X, using Xft, and
works on Unix and Windows platforms.

This package contains libraries used by Mucharmap.

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Requires:       %{libname} = %{version}

%description -n %{girname}
GObject Introspection interface description for %{name}

%package -n %{develname}
Summary:        Libraries and include files for developing %{name} components
Group:          Development/Other
Requires:       %{libname} = %{version}
Provides:       %{name}-devel = %{version}
Provides:       %mklibname -d %{oname} = %{version}
Provides:       %{oname}-devel = %{version}-%{release}

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop %{name} components.

%prep
%setup -q -n %oname-%version

%build
NOCONFIGURE=1 ./autogen.sh
%configure2_5x \
   --disable-static \
   --enable-python-bindings  \
   --enable-introspection    \
   --with-gtk=2.0

%make

%install
%makeinstall_std

find %{buildroot}%{_libdir} -type f -name '*.la' -delete -print

%find_lang %{name} --all-name --with-gnome

cat %name.lang >> Mucharmap.lang

%files -f Mucharmap.lang
%doc AUTHORS COPYING README
%{_bindir}/mate-character-map
%{_bindir}/mucharmap
%{_datadir}/applications/mucharmap.desktop
%{_datadir}/glib-2.0/schemas/*.xml
%{python_sitearch}/gtk-2.0/mucharmap.so
%{_datadir}/pygtk/2.0/defs/mucharmap.defs

%files -n %{libname}
%{_libdir}/libmucharmap.so.%{major}*

%files -n %{girname}
%defattr(-,root,root,-)
%{_libdir}/girepository-1.0/Mucharmap-%{gi_major}.typelib

%files -n %{develname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
# {_datadir}/gtk-doc/html/mucharmap/
%{_datadir}/gir-1.0/Mucharmap-%{gi_major}.gir

