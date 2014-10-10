Summary:	TextOCR scanner and image validator SpamAssassin plugin
Name:		perl-Mail-SpamAssassin-Plugin-ocrtext
Version:	3.2
Release:	4
License:	Apache License
Group:		Development/Perl
URL:		http://antispam.imp.ch/patches/
#Source0:	http://antispam.imp.ch/patches/patch-ocrtext
Source0:	http://antispam.imp.ch/patches/ocrtext-3.2.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  spamassassin-spamd >= 3.2.0
Requires:	spamassassin-spamd >= 3.2.0
Requires:	gocr
Requires:	netpbm
Requires:	perl-Image-ExifTool >= 6.12-3mdk
BuildRequires:	perl-doc
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
textocr.pm is a plugin for spamassassin 3.1+ to detect suspect pictures and
extract text from them with gocr. The OCR dictionary functionaliy has been
replaced with regexes. The plugin can also verify the validity of the pictures
and detects spoofing of the content type.

%prep

%setup -q -n ocrtext

# fix path
perl -pi -e "s|/usr/local/bin|%{_bindir}|g" ocrtext.cf

echo "loadplugin Mail::SpamAssassin::Plugin::ocrtext %{perl_vendorlib}/Mail/SpamAssassin/Plugin/ocrtext.pm" > ocrtext.pre

# bug since 1.7
perl -pi -e "s|^package ocrtext\;|package Mail::SpamAssassin::Plugin::ocrtext\;|g" ocrtext-sa32.pm

%build

perldoc ocrtext-sa32.pm > Mail::SpamAssassin::Plugin::ocrtext.3pm

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -d %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin
install -d %{buildroot}%{_mandir}/man3

install -m0644 ocrtext.cf %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 ocrtext.pre %{buildroot}%{_sysconfdir}/mail/spamassassin/ocrtext.pre
install -m0644 ocrtext-sa32.pm %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin/ocrtext.pm
install -m0644 Mail::SpamAssassin::Plugin::ocrtext.3pm %{buildroot}%{_mandir}/man3/

%post
if [ -f %{_var}/lock/subsys/spamd ]; then
    %{_initrddir}/spamd restart 1>&2;
fi
    
%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/spamd ]; then
        %{_initrddir}/spamd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/spamassassin/ocrtext.cf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/spamassassin/ocrtext.pre
%{perl_vendorlib}/Mail/SpamAssassin/Plugin/ocrtext.pm
%{_mandir}/man3/Mail::SpamAssassin::Plugin::ocrtext.3pm*


%changelog
* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 3.2-3mdv2010.0
+ Revision: 430489
- rebuild

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2-2mdv2009.0
+ Revision: 239113
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Jul 01 2007 Oden Eriksson <oeriksson@mandriva.com> 3.2-1mdv2008.0
+ Revision: 46388
- 3.2


* Sun Dec 17 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1-1mdv2007.0
+ Revision: 98300
- more small fixes
- fix a small issue
- 3.1
- fix a bug since 1.7 to make it actually work
- Import perl-Mail-SpamAssassin-Plugin-ocrtext

* Mon Oct 16 2006 Oden Eriksson <oeriksson@mandriva.com> 1.9-1mdv2007.1
- 1.9

* Sun Aug 13 2006 Oden Eriksson <oeriksson@mandriva.com> 1.7-1mdv2007.0
- 1.7

* Fri May 19 2006 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-1mdk
- initial Mandriva package

