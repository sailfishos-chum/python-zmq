# TODO package pytest
%bcond_with run_tests
# TODO: upstream removal of unnecessary shebang
# suffix of python executable (not defined at OBS)
%global python3_pkgversion 3

# OBS doesn't accept macros defined with %%global in "Name:"
%define DISTNAME zmq
Name:           python-%{DISTNAME}
Summary:        Software library for fast, message-based applications
Version:        22.3.0
Release:        1%{?dist}
License:        LGPLv3+ and ASL 2.0 and BSD
URL:            https://github.com/zeromq/pyzmq
Source:         %{name}-%{version}.tar.bz2

BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-cython
BuildRequires: pkgconfig(libzmq)
BuildRequires: python3-wheel
BuildRequires: python3-pip
BuildRequires: pyproject-rpm-macros
BuildRequires: gcc
# fails to provide python3dist(DISTNAME):
BuildRequires: python3-toml
%if %{with run_tests}
BuildRequires: python%{python3_pkgversion}-pytest
BuildRequires: python%{python3_pkgversion}-tornado
%endif

%generate_buildrequires
# see pyproject.toml
%pyproject_buildrequires

%global common_description %{expand:
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.}

%description %{common_description}

%prep
%autosetup -n %{name}-%{version}/pyzmq

# remove bundled libraries
rm -rf bundled

# forcibly regenerate the Cython-generated .c files:
find zmq -name "*.c" -delete
%{__python3} setup.py cython

# remove excecutable bits
chmod -x examples/pubsub/topics_pub.py
chmod -x examples/pubsub/topics_sub.py

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files zmq

%if %{with run_tests}
%check
%pytest
%endif


%package -n     python%{python3_pkgversion}-%{DISTNAME}
Summary:        %{summary}
%description -n python%{python3_pkgversion}-%{DISTNAME} %{common_description}

This package contains the python bindings.
%if "%{?vendor}" == "chum"
PackagerName: takimata
Categories:
 - Development
 - Library
%endif

%files -n       python%{python3_pkgversion}-%{DISTNAME} -f %{pyproject_files}
%doc README.md


%changelog
* Tue May 10 2022 takimata <takimata@gmx.de> - 22.3.0-1
- Initial packaging for Chum
