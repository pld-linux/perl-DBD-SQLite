#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%include	/usr/lib/rpm/macros.perl
%define	pdir	DBD
%define	pnam	SQLite
Summary:	DBD::SQLite - DBI driver for SQLite database
Summary(pl):	DBD::SQLite - sterownik DBI dla bazy SQLite
Name:		perl-DBD-SQLite
Version:	0.31
Release:	0.1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	4aa99c39104b7cd39129aec548e7d3e4
BuildRequires:	perl-devel >= 1:5.8.0
%if %{with tests}
BuildRequires:	perl-DBI
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
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

# If SQLITE_PTR_SZ is not set in OPTIMIZE SQLite assumes 64-bit
# architecture and fails. 
%{__make} \
	OPTIMIZE="%{rpmcflags} -DSQLITE_PTR_SZ=`%{__perl} -MConfig -e 'print \"$Config{ptrsize}\";'`"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
