#
# Conditional build:
%bcond_without	tests		# unit tests
%bcond_without	system_sqlite3	# system sqlite3
#
%define		pdir	DBD
%define		pnam	SQLite
Summary:	DBD::SQLite - Self Contained RDBMS in a DBI Driver (sqlite 3.x)
Summary(pl.UTF-8):	DBD::SQLite - Kompletny RDBMS zawarty w sterowniku DBI (sqlite 3.x)
Name:		perl-DBD-SQLite
Version:	1.74
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	https://www.cpan.org/modules/by-module/DBD/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	9481bd8b644a2ef56ab01aead403649c
Patch0:		data_type.patch
URL:		https://metacpan.org/dist/DBD-SQLite
BuildRequires:	perl-DBI >= 1.57
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%{?with_system_sqlite3:BuildRequires:	sqlite3-devel >= 3.6.0}
%if %{with tests}
BuildRequires:	perl-Encode
BuildRequires:	perl-Test-Simple >= 0.86
# needs ENABLE_FTS3_PARENTHESIS
%{?with_system_sqlite3:BuildRequires:	sqlite3 >= 3.8.11.1-2}
%endif
%{?with_system_sqlite3:Requires:	sqlite3 >= 3.6.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# virtual module provided by VirtualTable.pm
%define		_noautoreq_perl	DBD::SQLite::VirtualTable::Cursor

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
%patch -P0 -p1

# honour USE_LOCAL_SQLITE instead of using bundled sqlite3 (see comments inside)
%{__perl} -pi -e 's/if \( 0 \)/if ( 1 )/' Makefile.PL

%build
echo y | %{__perl} Makefile.PL \
	%{!?with_system_sqlite3:USE_LOCAL_SQLITE=1} \
	INSTALLDIRS=vendor

%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}" \
	OTHERLDFLAGS="%{rpmcflags} %{rpmldflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/DBD/SQLite/{Cookbook,Fulltext_search}.pod
# "sqlite3 amalgamation" sources
%{__rm} -r $RPM_BUILD_ROOT%{perl_vendorarch}/auto/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/DBD/SQLite.pm
%{perl_vendorarch}/DBD/SQLite
%dir %{perl_vendorarch}/auto/DBD/SQLite
%attr(755,root,root) %{perl_vendorarch}/auto/DBD/SQLite/SQLite.so
%{_mandir}/man3/DBD::SQLite*.3pm*
