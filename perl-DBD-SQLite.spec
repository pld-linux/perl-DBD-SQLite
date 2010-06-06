#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	DBD
%define		pnam	SQLite
Summary:	DBD::SQLite - Self Contained RDBMS in a DBI Driver (sqlite 3.x)
Summary(pl.UTF-8):	DBD::SQLite - Kompletny RDBMS zawarty w sterowniku DBI (sqlite 3.x)
Name:		perl-DBD-SQLite
Version:	1.25
Release:	2
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/DBD/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	3bc9c8f141cb6c9256ea6dbcddbb9fe7
URL:		http://search.cpan.org/dist/DBD-SQLite/
BuildRequires:	perl-DBI
%{?with_tests:BuildRequires:	perl-Encode}
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DBD::SQLite is a DBI driver for SQLite database. SQLite is a public
domain RDBMS database engine that you can find at
<http://www.sqlite.org/>.

Rather than ask you to install SQLite first, DBD::SQLite includes the
entire thing in the distribution. So in order to get a fast
transaction capable RDBMS working for your perl project you simply
have to install this module, and nothing else.

To use databases created using older SQLite version (2.x) you should
use perl-DBD-SQLite2 package.

%description -l pl.UTF-8
DBD::SQLite to sterownik DBI do baz danych SQLite. SQLite to silnik
relacyjnych baz danych na licencji public domain. Można go znaleźć pod
adresem <http://www.sqlite.org/>.

DBD::SQLite zawiera w sobie cały silnik bazy danych. Dzięki temu aby
otrzymać działający RDBMS dostępny z poziomu Perla nie trzeba
instalować żadnych innych pakietów.

Aby używać baz danych stworzonych przy pomocy starszej wersji SQLite
(2.x) należy zainstalować pakiet perl-DBD-SQLite2.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
echo y | %{__perl} Makefile.PL \
	USE_LOCAL_SQLITE=1 \
	INSTALLDIRS=vendor

# dumps core with sqlite 3.5.4 sometimes (eg. t/06error.t)
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}" \
	OTHERLDFLAGS="%{rpmcflags} %{rpmldflags}"

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
