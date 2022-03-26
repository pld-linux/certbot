#
# Conditional build:
%bcond_with	doc		# build doc
%bcond_with	tests		# do perform tests (pulls extra dependencies from network)
%bcond_without	python3 	# build CPython 3.x ACME module

Summary:	Certbot -  EFF's tool to obtain certs from Let's Encrypt
Name:		certbot
Version:	0.40.1
Release:	7
License:	Apache v2.0
Group:		Applications/Networking
Source0:	https://github.com/certbot/certbot/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6b187c9b843c715b5486ac4b212316cd
URL:		https://certbot.eff.org/
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
%if %{with doc}
BuildRequires:	python-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg
%endif
%if %{with tests}
BuildRequires:	Zope-Interface
BuildRequires:	python-mock
BuildRequires:	python-six
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
Requires:	python3-zope.component >= 4.4.1
Requires:	python3-ndg-httpsclient
%else:
Requires:	python-zope.component >= 4.4.1
Requires:	python-ndg-httpsclient
%endif
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

%package -n python-acme
Summary:	Python library for the ACME protocol
Group:		Libraries/Python
Obsoletes:	python-acme-doc < 0.9.3

%description -n python-acme
Python 2 library for use of the Automatic Certificate Management
Environment protocol as defined by the IETF. It's used by the Let's
Encrypt project.

%package -n python3-acme
Summary:	Python library for the ACME protocol
Group:		Libraries/Python

%description -n python3-acme
Python 3 library for use of the Automatic Certificate Management
Environment protocol as defined by the IETF. It's used by the Let's
Encrypt project.

%prep
%setup -q

%build
%py_build %{?with_tests:test}

%if %{with doc}
cd docs
%{__make} -j1 html
rm -r _build/html/_sources
%endif

cd acme
%py_build %{?with_tests:test}

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/var/log,/var/lib}/letsencrypt

%if %{with python3}
%py3_install
%else
%py_install
%endif

cd acme

%py_install

%if %{with python3}
%py3_install
%endif
cd ..

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst CHANGELOG.md CONTRIBUTING.md docs/*.txt docs/*.rst
%if %{with doc}
%doc docs/_build/html/*
%else
%doc docs/*.rst docs/api docs/man
%endif
%dir %{_sysconfdir}/letsencrypt
%dir /var/log/letsencrypt
%dir /var/lib/letsencrypt
%attr(755,root,root) %{_bindir}/certbot
%if %{with python3}
%{py3_sitescriptdir}/certbot
%{py3_sitescriptdir}/certbot-%{version}*-py*.egg-info
%else
%{py_sitescriptdir}/certbot
%{py_sitescriptdir}/certbot-%{version}*-py*.egg-info
%endif

%files -n python-acme
%defattr(644,root,root,755)
%doc acme/README.rst
%if %{with doc}
%doc acme/docs/_build/html/*
%else
%doc acme/docs/*.rst acme/docs/api acme/docs/man
%endif
%{py_sitescriptdir}/acme
%{py_sitescriptdir}/acme-%{version}*-py*.egg-info

%files -n python3-acme
%defattr(644,root,root,755)
%doc acme/README.rst
%if %{with doc}
%doc acme/docs/_build/html/*
%else
%doc acme/docs/*.rst acme/docs/api acme/docs/man
%endif
%{py3_sitescriptdir}/acme
%{py3_sitescriptdir}/acme-%{version}*-py*.egg-info
