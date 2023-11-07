Name:           espeak-ng
Version:        1.50
Release:        9%{?dist}
Summary:        eSpeak NG Text-to-Speech

License:        GPLv3+
URL:            https://github.com/espeak-ng/espeak-ng
Source0:        %{url}/archive/%{version}.tar.gz

BuildRequires:  gcc make autoconf automake libtool pkgconfig
BuildRequires:  rubygem-ronn rubygem-kramdown
BuildRequires:  pcaudiolib-devel

Patch0:         0001-fix-699-avoid-samplerate-clashing-with-LTO-in-gcc-10.patch

%description
The eSpeak NG (Next Generation) Text-to-Speech program is an open source speech
synthesizer that supports over 70 languages. It is based on the eSpeak engine
created by Jonathan Duddington. It uses spectral formant synthesis by default
which sounds robotic, but can be configured to use Klatt formant synthesis
or MBROLA to give it a more natural sound.

%package devel
Summary: Development files for espeak-ng
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for eSpeak NG, a software speech synthesizer.

%package vim
Summary: Vim syntax highlighting for espeak-ng data files
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description vim
%{summary}.

%package doc
Summary: Documentation for espeak-ng
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for eSpeak NG, a software speech synthesizer.

%prep
%autosetup -p1
# Remove unused files to make sure we've got the License tag right
rm -rf src/include/compat/endian.h src/compat/getopt.c android/

%build
./autogen.sh
%configure
%make_build src/espeak-ng src/speak-ng
make
# Force utf8 for docs building
LC_ALL=C.UTF-8 make docs

%install
%make_install
rm -vf %{buildroot}%{_libdir}/libespeak-ng-test.so*
rm -vf %{buildroot}%{_libdir}/*.{a,la}
# Remove files conflicting with espeak
rm -vf %{buildroot}%{_bindir}/{speak,espeak}
rm -vrf %{buildroot}%{_includedir}/espeak
# Move Vim files
mv %{buildroot}%{_datadir}/vim/addons %{buildroot}%{_datadir}/vim/vimfiles
rm -vrf %{buildroot}%{_datadir}/vim/registry

%check
ESPEAK_DATA_PATH=`pwd` LD_LIBRARY_PATH=src:${LD_LIBRARY_PATH} src/espeak-ng ...

%ldconfig_scriptlets

%files
%license COPYING
%license COPYING.IEEE
%doc README.md
%doc CHANGELOG.md
%{_bindir}/speak-ng
%{_bindir}/espeak-ng
%{_libdir}/libespeak-ng.so.1
%{_libdir}/libespeak-ng.so.1.*
%{_datadir}/espeak-ng-data
%{_mandir}/man1/speak-ng.1.gz
%{_mandir}/man1/espeak-ng.1.gz

%files devel
%{_libdir}/pkgconfig/espeak-ng.pc
%{_libdir}/libespeak-ng.so
%{_includedir}/espeak-ng

%files vim
%{_datadir}/vim/vimfiles/ftdetect/espeakfiletype.vim
%{_datadir}/vim/vimfiles/syntax/espeaklist.vim
%{_datadir}/vim/vimfiles/syntax/espeakrules.vim

%files doc
%doc docs/*.html

%changelog
* Tue Jun 20 2023 Tomas Korbar <tkorbar@redhat.com> - 1.50-9
- Fix gating.yaml
- Related: rhbz#2190221

* Tue Jun 20 2023 Tomas Korbar <tkorbar@redhat.com> - 1.50-8
- Rebuild for rhbz#2190221
- Resolves: rhbz#2190221

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.50-7
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 1.50-6
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.50-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Ondřej Lysoněk <olysonek@redhat.com> - 1.50-1
- New version
- Resolves: rhbz#1778315

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.49.2-5
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Thu Jul 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 1.49.2-4
- Remove some unsed files in %%prep

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 03 2017 Ondřej Lysoněk <olysonek@redhat.com> - 1.49.2-1
- New version

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Ondřej Lysoněk <olysonek@redhat.com> 1.49.1-2
- Corrected use of the ISA macro
- Included the COPYING.IEEE file

* Tue Jan 24 2017 Ondřej Lysoněk <olysonek@redhat.com> 1.49.1-1
- New version

* Fri Sep 16 2016 Ondřej Lysoněk <olysonek@redhat.com> 1.49.0-1
- Initial package
