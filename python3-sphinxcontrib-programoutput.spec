#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Sphinx extension to include program output
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do załączania wyjścia programu
Name:		python3-sphinxcontrib-programoutput
Version:	0.20
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-programoutput/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-programoutput/sphinxcontrib_programoutput-%{version}.tar.gz
# Source0-md5:	ce0623eab95cf96f6bad0e9d0a972349
URL:		https://pypi.org/project/sphinxcontrib-programoutput/
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:61
%if %{with tests}
BuildRequires:	python3-Sphinx >= 5.0.0
BuildRequires:	python3-erbsland-sphinx-ansi >= 1.2.4
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	sphinx-pdg-3 >= 5.0.0
%endif
Requires:	python3-modules >= 1:3.10
Requires:	python3-sphinxcontrib
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples up
to date.

%description -l pl.UTF-8
Rozszerzenie Sphinksa do dokładnego wstawiania wyjścia dowolnych
poleceń do dokumentów. Pozwala utrzymywać aktualność przykładów
poleceń.

%package apidocs
Summary:	API documentation for Python sphinxcontrib-programoutput module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphinxcontrib-programoutput
Group:		Documentation

%description apidocs
API documentation for Python sphinxcontrib-programoutput module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphinxcontrib-programoutput.

%prep
%setup -q -n sphinxcontrib_programoutput-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest src
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinxcontrib/programoutput/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE README.rst
%{py3_sitescriptdir}/sphinxcontrib/programoutput
%{py3_sitescriptdir}/sphinxcontrib_programoutput-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
