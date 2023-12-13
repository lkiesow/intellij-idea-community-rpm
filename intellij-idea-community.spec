# don't strip bundled binaries because pycharm checks length (!!!) of binary fsnotif
# and if you strip debug stuff from it, it will complain
%global __strip /bin/true
# dont repack jars
%global __jar_repack %{nil}
# disable rpath checks
# needed as 'jbr/lib/libjceftesthelpers.so' fails with 'contains an invalid rpath'
%define __brp_check_rpaths %{nil}
%define debug_package %{nil}
# there are some python 2 and python 3 scripts so there is no way out to bytecompile them ^_^
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global build_vers 233.11799.300
%global idea_name idea-IC

Name:          intellij-idea-community
Version:       2023.3.1
Release:       3%{?dist}
Summary:       Intelligent Java IDE
License:       ASL 2.0
URL:           https://www.jetbrains.com/idea/

Source0:       https://download.jetbrains.com/idea/ideaIC-%{version}.tar.gz

Source101:     https://raw.githubusercontent.com/lkiesow/intellij-idea-community-rpm/master/intellij-idea.xml
Source102:     https://raw.githubusercontent.com/lkiesow/intellij-idea-community-rpm/master/intellij-idea-community.desktop
Source103:     https://raw.githubusercontent.com/lkiesow/intellij-idea-community-rpm/master/intellij-idea-community.appdata.xml

BuildRequires: desktop-file-utils
BuildRequires: /usr/bin/appstream-util
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem

%description
IntelliJ IDEA analyzes your code, looking for connections between symbols
across all project files and languages.  Using this information it provides
indepth coding assistance, quick navigation, clever error analysis, and, of
course, refactorings.

%package doc
Summary:       Documentation for intelligent Java IDE
BuildArch:     noarch

%description doc
This package contains documentation for Intelligent Java IDE.

%prep
%setup -q -n %{idea_name}-%{build_vers}

%build

%install
mkdir -p %{buildroot}%{_javadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/appdata
mkdir -p %{buildroot}%{_bindir}

# Remove files for different architectures
rm -rf lib/pty4j-native/linux/{aarch64,arm,mips64el,ppc64le,x86}
rm -rf plugins/cwm-plugin/quiche-native/linux-aarch64
rm -rf plugins/maven/lib/maven3/lib/jansi-native/{freebsd32,freebsd64,linux32,osx,windows32,windows64}
rm -rf plugins/Kotlin/bin/{macos,windows}
rm -rf plugins/webp/lib/libwebp/linux/libwebp_jni.so
rm -rf plugins/webp/lib/libwebp/{mac,win}
rm -rf plugins/cwm-plugin/quiche-native/{darwin,win}*
cp -arf ./{lib,bin,plugins,jbr} %{buildroot}%{_javadir}/%{name}/

cp -af ./bin/idea.png %{buildroot}%{_datadir}/pixmaps/idea.png
cp -af %{SOURCE101} %{buildroot}%{_datadir}/mime/packages/%{name}.xml
cp -af %{SOURCE102} %{buildroot}%{_datadir}/%{name}.desktop
cp -a %{SOURCE103} %{buildroot}%{_datadir}/appdata
ln -s %{_javadir}/%{name}/bin/idea.sh %{buildroot}%{_bindir}/idea
desktop-file-install \
  --add-category="Development" \
  --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/intellij-idea-community.desktop

%check
appstream-util validate-relax \
  --nonet %{buildroot}%{_datadir}/appdata/intellij-idea-community.appdata.xml

%files
%{_datadir}/applications/intellij-idea-community.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/idea.png
%{_datadir}/appdata/intellij-idea-community.appdata.xml
%{_javadir}/%{name}
%{_bindir}/idea

%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files doc
%doc *.txt
%license license/

%changelog
* Wed Dec 13 2023 Lars Kiesow <lkiesow@uos.de> - 2023.3.1
- Update to 2023.3.1 (233.11799.300)

* Thu Dec 07 2023 Lars Kiesow <lkiesow@uos.de> - 2023.3
- Update to 2023.3 (233.11799.241)

* Fri Nov 10 2023 Lars Kiesow <lkiesow@uos.de> - 2023.2.5
- Update to 2023.2.5 (232.10227.8)

* Thu Oct 26 2023 Lars Kiesow <lkiesow@uos.de> - 2023.2.4
- Update to 2023.2.4 (232.10203.10)

* Thu Oct 12 2023 Lars Kiesow <lkiesow@uos.de> - 2023.2.3
- Update to 2023.2.3 (232.10072.27)

* Thu Sep 14 2023 Lars Kiesow <lkiesow@uos.de> - 2023.2.2
- Update to 2023.2.2 (232.9921.47)

* Thu Aug 24 2023 Lars Kiesow <lkiesow@uos.de> - 2023.2.1
- Update to 2023.2.1 (232.9559.62)

* Thu Jul 27 2023 Lars Kiesow <lkiesow@uos.de> - 2023.2
- Update to 2023.2 (232.8660.185)

* Wed Jul 26 2023 Lars Kiesow <lkiesow@uos.de> - 2023.1.5
- Update to 2023.1.5 (231.9392.1)

* Thu Jul 13 2023 Lars Kiesow <lkiesow@uos.de> - 2023.1.4
- Update to 2023.1.4 (231.9225.16)

* Tue Jul 11 2023 Lars Kiesow <lkiesow@uos.de> - 2023.1.3-3
- New includes JDK
- Fixes Python 3 issue

* Wed Jun 21 2023 Lars Kiesow <lkiesow@uos.de> - 2023.1.3
- Update to 2023.1.3 (231.9161.38)

* Wed May 17 2023 Lars Kiesow <lkiesow@uos.de> - 2023.1.2
- Update to 2023.1.2 (231.9011.34)

* Sat Apr 29 2023 Lars Kiesow <lkiesow@uos.de> - 2023.1.1
- Update to 2023.1.1 (231.8770.65)

* Wed Mar 29 2023 Lars Kiesow <lkiesow@uos.de> - 2023.1
- Update to 2023.1 (231.8109.175)

* Sat Mar 11 2023 Lars Kiesow <lkiesow@uos.de> - 2022.3.3
- Update to 2022.3.3 (223.8836.41)

* Thu Mar 09 2023 Lars Kiesow <lkiesow@uos.de> - 2022.3.3
- Update to 2022.3.3 (223.8836.35)

* Fri Jan 27 2023 Lars Kiesow <lkiesow@uos.de> - 2022.3.2
- Update to 2022.3.2 (223.8617.56)

* Wed Dec 21 2022 Lars Kiesow <lkiesow@uos.de> - 2022.3.1
- Update to 2022.3.1 (223.8214.52)

* Thu Dec 01 2022 Lars Kiesow <lkiesow@uos.de> - 2022.3
- Update to 2022.3 (223.7571.182)

* Thu Nov 24 2022 Lars Kiesow <lkiesow@uos.de> - 2022.2.4
- Update to 2022.2.4 (222.4459.24)

* Thu Oct 06 2022 Lars Kiesow <lkiesow@uos.de> - 2022.2.3
- Update to 2022.2.3 (222.4345.14)

* Thu Sep 15 2022 Lars Kiesow <lkiesow@uos.de> - 2022.2.2
- Update to 2022.2.2 (222.4167.29)

* Thu Aug 18 2022 Lars Kiesow <lkiesow@uos.de> - 2022.2.1
- Update to 2022.2.1 (222.3739.54)

* Sat Aug 13 2022 Lars Kiesow <lkiesow@uos.de> - 2022.2-2
- Remove files for unsupported architectures

* Wed Jul 27 2022 Lars Kiesow <lkiesow@uos.de> - 2022.2
- Update to 2022.2 (222.3345.118)

* Tue Jul 19 2022 Lars Kiesow <lkiesow@uos.de> - 2022.1.4
- Update to 2022.1.4 (221.6008.13)

* Wed Jun 22 2022 Lars Kiesow <lkiesow@uos.de> - 2022.1.3
- Update to 2022.1.3 (221.5921.22)

* Thu Jun 02 2022 Lars Kiesow <lkiesow@uos.de> - 2022.1.2
- Update to 2022.1.2 (221.5787.30)

* Thu May 12 2022 Lars Kiesow <lkiesow@uos.de> - 2022.1.1
- Update to 2022.1.1 (221.5591.52)

* Wed Apr 13 2022 Lars Kiesow <lkiesow@uos.de> - 2022.1
- Update to 2022.1 (221.5080.210)

* Fri Mar 18 2022 Lars Kiesow <lkiesow@uos.de> - 2021.3.3
- Update to 2021.3.3 (213.7172.25)

* Sat Jan 29 2022 Lars Kiesow <lkiesow@uos.de> - 2021.3.2
- Update to 2021.3.2 (213.6777.52)

* Tue Jan 04 2022 Lars Kiesow <lkiesow@uos.de> - 2021.3.1
- Update to 2021.3.1 (213.6461.79)

* Thu Dec 16 2021 Lars Kiesow <lkiesow@uos.de> - 2021.3
- Update to 2021.3 (213.5744.223)

* Thu Dec 16 2021 Lars Kiesow <lkiesow@uos.de> - 2021.2.3-3
- Fix dependencies (Remove Mac/Win binaries)

* Fri Nov  5 2021 Lars Kiesow <lkiesow@uos.de> - 2021.2.3-2
- Fix architecture dependencies in Fedora 35

* Fri Nov 05 2021 Lars Kiesow <lkiesow@uos.de> - 2021.2.3-1
- Update to 2021.2.3 (212.5457.46)

* Sun Oct 17 2021 Lars Kiesow <lkiesow@uos.de> - 2021.2.2-3
- Fix Fedora 35/Rawhide builds

* Wed Oct 13 2021 Lars Kiesow <lkiesow@uos.de> - 2021.2.2-2
- Update to 2021.2.2 (212.5284.40)

* Thu Jul 29 2021 Lars Kiesow <lkiesow@uos.de> - 2021.2-2
- Include native file system watcher for Linux

* Wed Jul 28 2021 Lars Kiesow <lkiesow@uos.de> - 2021.2
- Update to 2021.2 (212.4746.92)

* Thu Jul 01 2021 Lars Kiesow <lkiesow@uos.de> - 2021.1.3
- Update to 2021.1.3 (211.7628.21)

* Wed Jun 09 2021 Lars Kiesow <lkiesow@uos.de> - 2021.1.2
- Update to 2021.1.2 (211.7442.40)

* Tue May 04 2021 Lars Kiesow <lkiesow@uos.de> - 2021.1.1
- Update to 2021.1.1 (211.7142.45)

* Thu Apr 08 2021 Lars Kiesow <lkiesow@uos.de> - 2021.1
- Update to 2021.1 (211.6693.111)

* Tue Mar 16 2021 Lars Kiesow <lkiesow@uos.de> - 2020.3.3
- Update to 2020.3.3 (203.7717.56)

* Wed Jan 27 2021 Lars Kiesow <lkiesow@uos.de> - 2020.3.2
- Update to 2020.3.2 (203.7148.57)

* Fri Jan 01 2021 Lars Kiesow <lkiesow@uos.de> - 2020.3.1
- Update to 2020.3.1 (203.6682.168)

* Wed Dec 02 2020 Lars Kiesow <lkiesow@uos.de> - 2020.3
- Update to 2020.3 (203.5981.155)

* Thu Nov 26 2020 Lars Kiesow <lkiesow@uos.de> - 2020.2.4
- Update to 2020.2.4 (202.8194.7)

* Wed Oct 07 2020 Lars Kiesow <lkiesow@uos.de> - 2020.2.3
- Update to 2020.2.3 (202.7660.26)

* Tue Sep 22 2020 Lars Kiesow <lkiesow@uos.de> - 2020.2.2
- Update to 2020.2.2 (202.7319.50)

* Tue Aug 25 2020 Lars Kiesow <lkiesow@uos.de> - 2020.2.1
- Update to 2020.2.1 (202.6948.69)

* Thu Jul 30 2020 Lars Kiesow <lkiesow@uos.de> - 2020.2
- Update to 2020.2 (202.6397.94)

* Fri Jul 24 2020 Lars Kiesow <lkiesow@uos.de> - 2020.1.4
- Update to 2020.1.4 (201.8743.12)

* Thu Jul 09 2020 Lars Kiesow <lkiesow@uos.de> - 2020.1.3-1
- Update to 2020.1.3

* Wed Jun 03 2020 Lars Kiesow <lkiesow@uos.de> - 2020.1.2-1
- Update to 2020.1.2

* Fri Apr 10 2020 Lars Kiesow <lkiesow@uos.de> - 2020.1-1
- Update to 2020.1

* Wed Jan 22 2020 Lars Kiesow <lkiesow@uos.de> - 2019.3.2-1
- Update to 2019.3.2

* Fri Dec 20 2019 Lars Kiesow <lkiesow@uos.de> - 2019.3.1-1
- Update to 2019.3.1

* Sat Nov 30 2019 Lars Kiesow <lkiesow@uos.de> - 2019.3-1
- Update to 2019.3

* Thu Oct 31 2019 Lars Kiesow <lkiesow@uos.de> - 2019.2.4-1
- Update to 2019.2.4

* Sun Sep 08 2019 Lars Kiesow <lkiesow@uos.de> - 2019.2.2-1
- Update to 2019.2.2

* Wed Aug 21 2019 Lars Kiesow <lkiesow@uos.de> - 2019.2.1-1
- Update to 2019.2.1

* Thu Jul 25 2019 Lars Kiesow <lkiesow@uos.de> - 2019.2-1
- Update to 2019.2

* Thu May 30 2019 Lars Kiesow <lkiesow@uos.de> - 2019.1.3-1
- Update to 2019.1.3

* Thu May 09 2019 Lars Kiesow <lkiesow@uos.de> - 2019.1.2-1
- Update to 2019.1.2

* Thu Apr 18 2019 Lars Kiesow <lkiesow@uos.de> - 2019.1.1-1
- Update to 2019.1.1

* Thu Mar 28 2019 Lars Kiesow <lkiesow@uos.de> - 2019.1-1
- Update to 2019.1

* Wed Mar 27 2019 Lars Kiesow <lkiesow@uos.de> - 2018.3.6-1
- Update to 2018.3.6

* Wed Feb 27 2019 Lars Kiesow <lkiesow@uos.de> - 2018.3.5-1
- Update to 2018.3.5

* Thu Jan 31 2019 Lars Kiesow <lkiesow@uos.de> - 2018.3.4-1
- Update to 2018.3.4

* Fri Jan 11 2019 Lars Kiesow <lkiesow@uos.de> - 2018.3.3-1
- Update to 2018.3.3

* Wed Dec 19 2018 Lars Kiesow <lkiesow@uos.de> - 2018.3.2-1
- Update to 2018.3.2

* Sat Dec 08 2018 Lars Kiesow <lkiesow@uos.de> - 2018.3.1-1
- Update to 2018.3.1

* Wed Nov 28 2018 Lars Kiesow <lkiesow@uos.de> - 2018.2.7-1
- Update to 2018.2.7

* Wed Nov 14 2018 Lars Kiesow <lkiesow@uos.de> - 2018.2.6-1
- Update to 2018.2.6

* Tue Oct 23 2018 Lars Kiesow <lkiesow@uos.de> - 2018.2.5-2
- Update to 2018.2.5

* Mon Jul 30 2018 Lars Kiesow <lkiesow@uos.de> - 2018.1.6-1
- Update to 2018.1.6

* Tue May 22 2018 Lars Kiesow <lkiesow@uos.de> - 2018.1.4-1
- Update to 2018.1.4

* Wed May 16 2018 Lars Kiesow <lkiesow@uos.de> - 2018.1.3-1
- Update to 2018.1.3

* Tue Dec 05 2017 Petr Hracek <phracek@redhat.com> - 2017.3-1
- Initial package
