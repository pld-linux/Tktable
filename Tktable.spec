%define tkver	8.4
#
Summary:	TkTable is a table/matrix widget extension to tk/tcl
Name:		Tktable
Version:	2.9
Release:	1
License:	BSD
Group:		Development/Languages/Tcl
Source0:	http://dl.sourceforge.net/tktable/%{name}%{version}.tar.gz
# Source0-md5:	a91cac4270a0c46945723d8f5106e80b
Patch0:		%{name}-pkg_lib_file.patch
URL:		http://tktable.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	tk-devel >= %{tkver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	/usr/lib

%description
TkTable is a table/matrix widget extension to tk/tcl.
The basic features of the widget are:
 * multi-line cells
 * support for embedded windows (one per cell)
 * row & column spanning
 * variable width columns / height rows (interactively resizable)
 * row and column titles
 * multiple data sources ((Tcl array || Tcl command) &| internal caching)
 * supports standard Tk reliefs, fonts, colors, etc.
 * x/y scrollbar support
 * 'tag' styles per row, column or cell to change visual appearance
 * in-cell editing - returns value back to data source
 * support for disabled (read-only) tables or cells (via tags)
 * multiple selection modes, with "active" cell
 * multiple drawing modes to get optimal performance for larger tables
 * optional 'flashes' when things update
 * cell validation support
 * Works everywhere Tk does (including Windows and Mac!)
 * Unicode support (Tk8.1+)

%package devel
Summary:	TkTable - development files
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}
Requires:	tk-devel >= %{tkver}

%description devel
TkTable development files.

%package demo
Summary:	TkTable - demo programs
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}

%description demo
TkTable demo programs.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1

%build
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_mandir},%{_ulibdir}}

%{__make} install \
	 DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}%{version}/html
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}%{version}/*.txt

mv $RPM_BUILD_ROOT%{_libdir}/%{name}%{version}/lib%{name}%{version}.so $RPM_BUILD_ROOT%{_libdir}

%if "%{_libdir}" != "%{_ulibdir}"
mv $RPM_BUILD_ROOT%{_libdir}/%{name}%{version} $RPM_BUILD_ROOT%{_ulibdir}
ln -sf %{_libdir}/lib%{name}%{version}.so $RPM_BUILD_ROOT%{_ulibdir}/lib%{name}%{version}.so
%endif

ln -sf %{_libdir}/lib%{name}%{version}.so $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so

install -d $RPM_BUILD_ROOT%{_mandir}/mann
install doc/*.n $RPM_BUILD_ROOT%{_mandir}/mann

install generic/tkTable.h $RPM_BUILD_ROOT%{_includedir}

cp -a demos $RPM_BUILD_ROOT%{_ulibdir}/%{name}%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt README.blt TODO.txt UPGRADING.txt license.txt
%attr(755,root,root) %{_libdir}/lib%{name}%{version}.so
%dir %{_ulibdir}/%{name}%{version}
%{_ulibdir}/%{name}%{version}/*.tcl
%if "%{_libdir}" != "%{_ulibdir}"
%{_ulibdir}/lib*%{version}.so
%endif
%{_mandir}/mann/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib%{name}.so
%{_includedir}/*

%files demo
%defattr(644,root,root,755)
%{_ulibdir}/%{name}%{version}/demos
