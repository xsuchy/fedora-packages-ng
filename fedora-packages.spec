Name:           fedora-packages
Version:        5.0.1
Release:        1%{?dist}
Summary:        Fedora packages search engine

License:        AGPLv3
# temporary on github.com/xsuchy/fedora-packages-ng
URL:            https://github.com/fedora-infra/fedora-packages
# Source is created by:
# git clone %%url fedora-packages && cd fedora-packages
# tito build --tgz --tag %%name-%%version-%%release
Source0:        %name-%version.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
Requires:       js-html5shiv
Requires:       js-jquery1
Requires:       js-respond
Requires:       python3
Requires:       python3-bodhi-client
Requires:       python3-bugzilla
Requires:       python3-devel
Requires:       python3-flask-cache
Requires:       python3-paste
Requires:       python3-pdc-client
Requires:       python3-humanize
Requires:       python3-koji
Requires:       python3-requests
Requires:       python3-setuptools
Requires:       python3-markdown
Requires:       xstatic-bootstrap-scss-common
Requires:       xstatic-datatables-common
Requires:       xstatic-jquery-ui-common
Requires:       xstatic-patternfly-common
Recommends:     logrotate

Provides:       bundled(bootstrap-combobox) = 1.1.6
Provides:       bundled(bootstrap-select) = 1.5.4
Provides:       bundled(bootstrap-treeview) = 1.0.1
Provides:       bundled(c3) = 0.4.10
Provides:       bundled(d3) = 3.5.0
Provides:       bundled(datatables-colreorder) = 1.1.3
Provides:       bundled(datatables-colvis) = 1.1.2
Provides:       bundled(font-awesome) = 1.0.1
Provides:       bundled(google-code-prettify) = 4.3.0

%description
Fedora-packages is a web application that allow the user to search for
packages inside Fedora.

%prep
%autosetup


%build
#nothing to do

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a fedoracommunity manage.py %{buildroot}%{_datadir}/%{name}

install -d %{buildroot}%{_sysconfdir}/logrotate.d
cp -a logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}


%post
/bin/systemctl condrestart httpd.service || :

%postun
/bin/systemctl condrestart httpd.service || :

%files
%doc README.md setup-with-docker.md setup-without-docker.md
%license COPYING
%{_datadir}/%{name}


%changelog
* Wed Oct 30 2019 Miroslav Suchý <msuchy@redhat.com> 5.0.1-1
- migrated to python3 and Flask

* Tue Jan 15 2019 Clement Verna <cverna@tutanota.com> - 4.2.0-2
- Fix dependencies

* Wed Oct 31 2018 Clement Verna <cverna@tutanota.com> - 4.2.0-1
- New version

* Thu Apr 05 2018 Clement Verna <cverna@tutanota.com> - 4.0.1-1
- Display pending release in the Release overview
