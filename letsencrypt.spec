# TODO: finish, test
#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"

%define	snap	20151017
Summary:	Let's Encrypt client
Name:		letsencrypt
Version:	0.0.0
Release:	0.%{snap}.1
License:	APL 2.0
Group:		Libraries/Python
Source0:	https://github.com/letsencrypt/letsencrypt/archive/v%{version}.dev20151017.tar.gz
# Source0-md5:	1cac8a454e466136f70834c76977ef17
URL:		https://letsencrypt.org/
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pythondialog
BuildRequires:	python-zope.component
BuildRequires:	python-zope.interface
%endif
%if %{with doc}
BuildRequires:	python-repoze.sphinx.autointerfac
BuildRequires:	sphinx-pdg
%endif
Requires:	python-cryptography
Requires:	python-modules
Requires:	python-pyOpenSSL
Requires:	python-pytz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Let's Encrypt Client is a tool to automatically receive and
install X.509 certificates to enable TLS on servers. The client will
interoperate with the Let's Encrypt CA which will be issuing
browser-trusted certificates for free.

%prep
%setup -q -n %{name}-%{version}.dev%{snap}

%build
%{__python} setup.py build %{?with_tests:test}

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py \
	build \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {CHANGES,README}.rst CONTRIBUTING.md %{?with_doc:docs/_build/html/*}
%attr(755,root,root) %{_bindir}/letsencrypt
%attr(755,root,root) %{_bindir}/letsencrypt-renewer
%{py_sitescriptdir}/letsencrypt
%{py_sitescriptdir}/letsencrypt-*py*.egg-info
