#
# Conditional build:
# _without_tests - do not perform "make test"
%include	/usr/lib/rpm/macros.perl
%define		pdir	DBD
%define		pnam	SQLite
Summary:	DBD::SQLite - DBI driver for SQLite database
Summary(pl):	DBD::SQLite - sterownik DBI dla bazy SQLite
Name:		perl-DBD-SQLite
Version:	0.25
Release:	0
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
BuildRequires:	perl >= 5.6
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sqlite-devel >= 2.6
%if %{?_without_tests:0}%{!?_without_tests:1}
BuildRequires:	perl-DBI
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SQLite is a public domain RDBMS database engine that you can find at
http://www.hwaci.com/sw/sqlite/. Rather than ask you to install SQLite
first, because SQLite is public domain, DBD::SQLite includes the
entire thing in the distribution. So in order to get a fast
transaction capable RDBMS working for your perl project you simply
have to install this module, and nothing else.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL
%{__make}
%{!?_without_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_sitearch}/DBD/SQLite.pm
%{perl_sitearch}/auto/DBD/SQLite/SQLite.so
%{perl_sitearch}/auto/DBD/SQLite/SQLite.bs
%{_mandir}/man3/DBD*
