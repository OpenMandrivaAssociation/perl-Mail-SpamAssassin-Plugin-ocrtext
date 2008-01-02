Summary:	TextOCR scanner and image validator SpamAssassin plugin
Name:		perl-Mail-SpamAssassin-Plugin-ocrtext
Version:	3.2
Release:	%mkrel 1
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
Buildroot:	%{_tmppath}/%{name}-%{version}-root

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
