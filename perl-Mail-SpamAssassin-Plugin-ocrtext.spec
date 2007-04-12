Summary:	TextOCR scanner and image validator SpamAssassin plugin
Name:		perl-Mail-SpamAssassin-Plugin-ocrtext
Version:	3.1
Release:	%mkrel 1
License:	Apache License
Group:		Development/Perl
URL:		http://antispam.imp.ch/patches/
Source0:	http://antispam.imp.ch/patches/patch-ocrtext
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  spamassassin-spamd >= 3.1.1
Requires:	spamassassin-spamd >= 3.1.1
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

%setup -q -T -c -n %{name}-%{version}

cp %{SOURCE0} patch-ocrtext
patch -p0 < patch-ocrtext

perl -pi -e "s|/usr/local/bin|%{_bindir}|g" ocrtext.cf

cat > ocrtext.cf.top << EOF

# Mail::SpamAssassin::Plugin::ocrtext - Check for specific keywords in gif/jpg/png attachments, using gocr.

loadplugin Mail::SpamAssassin::Plugin::ocrtext %{perl_vendorlib}/Mail/SpamAssassin/Plugin/ocrtext.pm

# Max pics to scan
ocrtext_maxscans 3

# Scan timout per pic
ocrtext_timeout 8

# Maximum score to still do OCR
#ocrtext_dscore 10

# Min pixel per kb to to checks
ocrtext_minpixratio_suspect 10000

# Min pixel per kb to do OCR
ocrtext_minpixratio_ocr 2000

# Min pixels to do OCR
ocrtext_minpixels_ocr 20000

# Max size of pic in kb to do OCR
ocrtext_maxsize_ocr 100

# Min size of pic in kb to do OCR
ocrtext_minsize_ocr 4

# Min size of pic in kb to do anything at all
ocrtext_minsize 1

# Limit 1 of chars an OCR scan can have to match
ocrtext_alpha1 32

# Limit 2 of chars an OCR scan can have to match
ocrtext_alpha2 100

# Limit 3 of chars an OCR scan can have to match
ocrtext_alpha3 400

EOF

cat ocrtext.cf >> ocrtext.cf.top
mv ocrtext.cf.top ocrtext.cf

# bug since 1.7
perl -pi -e "s|^package ocrtext\;|package Mail::SpamAssassin::Plugin::ocrtext\;|g" ocrtext.pm

%build

grep "^#" patch-ocrtext > README
perldoc ocrtext.pm > Mail::SpamAssassin::Plugin::ocrtext.3pm

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -d %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin
install -d %{buildroot}%{_mandir}/man3

install -m0644 ocrtext.cf %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 ocrtext.pm %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin/
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
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/spamassassin/ocrtext.cf
%{perl_vendorlib}/Mail/SpamAssassin/Plugin/ocrtext.pm
%{_mandir}/man3/Mail::SpamAssassin::Plugin::ocrtext.3pm*


