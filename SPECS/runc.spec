%define debug_package      %{nil}
%define __os_install_post  %{nil}

# Use major.minor.patch-rcX
%define RUNC_VERSION %{version}
%define RUNC_BRANCH  v%{RUNC_VERSION}
%define gopath_comp  github.com/opencontainers/runc

Name:           runc
Version:        1.3.6
Release:        1%{?dist}
Summary:        Run and manage containers
Summary(ru):    Запуск и управление контейнерами
License:        LGPL-2.1-only
URL:            https://runc.io

Source0:        https://github.com/opencontainers/runc/archive/refs/tags/v%{version}.tar.gz#%{name}-%{version}.tar.gz

Packager:       NICE SOFT GROUP LLC (ООО "НАЙС СОФТ ГРУПП") 5024245440 <niceos@ncsgp.ru>
Vendor:         NiceSOFT
Distribution:   NiceOS.Core
BugURL:         https://bugs.niceos.ru/
VCS:            https://specs.niceos.ru/rpms/%{name}

BuildRequires:  go >= 1.25
BuildRequires:  go-md2man
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  pkg-config
BuildRequires:  which

%description
runc is a lightweight command-line tool for running containers according to the
Open Container Initiative (OCI) specification. It creates and manages containers
with strong isolation and security primitives, and is commonly used by projects
such as Docker and Kubernetes.

%description -l ru
runc — легковесная утилита командной строки для запуска контейнеров в соответствии
со спецификацией Open Container Initiative (OCI). Она позволяет создавать и
управлять контейнерами, обеспечивая изоляцию и безопасность, и используется в
таких проектах, как Docker и Kubernetes.

%package        doc
Summary:        Documentation for runc, a lightweight container runtime
Summary(ru):    Документация для runc, легковесного контейнерного рантайма
Requires:       %{name} = %{version}-%{release}

%description -n %{name}-doc
This subpackage contains manual pages and other documentation for runc.

%description -l ru -n %{name}-doc
Подпакет содержит man-страницы и прочую документацию для runc.

%prep
%autosetup -p1 -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{RUNC_VERSION} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make %{?_smp_mflags} \
    GIT_BRANCH=%{RUNC_BRANCH} \
    BUILDTAGS='seccomp selinux apparmor' \
    EXTRA_LDFLAGS=-w \
    %{name} man

%install
cd src/%{gopath_comp}
# BINDIR is pointing to absolute path so DESTDIR is not required.
install -v -m 0644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
make %{?_smp_mflags} \
    DESTDIR="" \
    PREFIX=%{buildroot}%{_prefix} \
    BINDIR=%{buildroot}%{_bindir} \
    install install-bash install-man

%files
%defattr(-,root,root)
%license %{_datadir}/licenses/%{name}/LICENSE
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}

%files -n %{name}-doc
%defattr(-,root,root)
%doc %{_mandir}/man8/*

%changelog
* Tue Jul 07 2026 NiceOS Team <support@niceos.ru> - 1.3.6-1
- EN: Update to upstream version 1.3.6. Security references: CVE-2025-31133, CVE-2025-52565, CVE-2025-52881, CVE-2026-41579.
- RU: Обновление до upstream-версии 1.3.6. Упоминания безопасности: CVE-2025-31133, CVE-2025-52565, CVE-2025-52881, CVE-2026-41579.


* Sat May 02 2026 NiceOS Team <support@niceos.ru> - 1.3.5-1
- EN: - Update runc from 1.3.0 to 1.3.5.
- Apply upstream patch fixes for recursive atime-related mount flags and revert the runc create regression.
- Refresh source archive, checksums, and related packaging metadata.
- RU: - Обновить runc с версии 1.3.0 до 1.3.5.
- Подтянуть upstream-исправления для рекурсивных mount-флагов, связанных с atime, и откат регрессии в runc create.
- Обновить исходный архив, контрольные суммы и сопутствующие упаковочные метаданные.


* Sat Jan 10 2026 NiceOS Team <niceos@ncsgp.ru> - 1.3.0-1
- Initial build for NiceOS (Первая сборка для НАЙС.ОС)
