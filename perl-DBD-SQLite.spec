#
# Conditional build:
# _without_tests - do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	DBD
%define		pnam	SQLite
Summary:	DBD::SQLite - DBI driver for SQLite database
Summary(pl):	DBD::SQLite - sterownik DBI dla bazy SQLite
Name:		perl-DBD-SQLite
Version:	0.25
Release:	0.1
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
BuildRequires:	perl-devel >= 5.6
%if %{?_without_tests:0}%{!?_without_tests:1}
BuildRequires:	perl-DBI
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sqlite-devel >= 2.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DBD::SQLite is a DBI driver for SQLite database. SQLite is a public
domain RDBMS database engine that you can find at
http://www.hwaci.com/sw/sqlite/.

%description -l pl
DBD::SQLite to sterownik DBI do baz danych SQLite. SQLite to silnik
relacyjnych baz danych na licencji public domain. Mo¿na go znale¼æ pod
http://www.hwaci.com/sw/sqlite/.
 
%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} OPTIMIZE="%{rpmcflags}"

%{!?_without_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/DBD/SQLite.pm
%dir %{perl_vendorarch}/auto/DBD/SQLite
%{perl_vendorarch}/auto/DBD/SQLite/SQLite.bs
%attr(755,root,root) %{perl_vendorarch}/auto/DBD/SQLite/SQLite.so
%{_mandir}/man3/DBD*
