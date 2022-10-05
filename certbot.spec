#
# Conditional build:
%bcond_without	doc		# build doc
%bcond_with	tests		# do perform tests (pulls extra dependencies from network)

Summary:	Certbot -  EFF's tool to obtain certs from Let's Encrypt
Name:		certbot
Version:	1.31.0
Release:	1
License:	Apache v2.0
Group:		Applications/Networking
Source0:	https://github.com/certbot/certbot/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8e1da9cfc9441eebc96224c0a0c43982
URL:		https://certbot.eff.org/
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg >= 4.5.0
%endif
%if %{with tests}
BuildRequires:	Zope-Interface
BuildRequires:	python3-mock
BuildRequires:	python3-six
%endif
BuildRequires:	python3-setuptools
Requires:	python3-acme >= %{version}
Requires:	python3-zope.component >= 4.4.1
Requires:	python3-ndg-httpsclient
Obsoletes:	letsencrypt
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Certbot is part of EFF's effort to encrypt the entire Internet. Secure
communication over the Web relies on HTTPS, which requires the use of
a digital certificate that lets browsers verify the identify of web
servers (e.g., is that really google.com?). Web servers obtain their
certificates from trusted third parties called certificate authorities
(CAs). Certbot is an easy-to-use client that fetches a certificate
from Let's Encrypt - an open certificate authority launched by the
EFF, Mozilla, and others - and deploys it to a web server.

%prep
%setup -q

%build
cd certbot
%py3_build %{?with_tests:test}

%if %{with doc}
%{__make} -C docs html
%{__rm} -r docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/var/log,/var/lib}/letsencrypt

cd certbot
%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst CHANGELOG.md CONTRIBUTING.md certbot/docs/*.txt
%if %{with doc}
%doc certbot/docs/_build/html/*
%else
%doc certbot/docs/*.rst certbot/docs/api certbot/docs/man
%endif
%dir %{_sysconfdir}/letsencrypt
%dir /var/log/letsencrypt
%dir /var/lib/letsencrypt
%attr(755,root,root) %{_bindir}/certbot
%{py3_sitescriptdir}/certbot
%{py3_sitescriptdir}/certbot-%{version}*-py*.egg-info
