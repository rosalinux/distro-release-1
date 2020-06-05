# Please update release notes:
# make -C SOURCES release-notes.{html,txt}
#

%define new_distribution OpenMandriva Lx
%define new_vendor OpenMandriva
%define new_product OpenMandriva Lx
# (tpg) use codename from here https://wiki.openmandriva.org/en/Codename
%define new_codename Argon
%define vendor_tag %(echo %{new_vendor} |tr A-Z a-z)
%define distribution_tag %(echo %{new_distribution} |tr A-Z a-z |sed -e 's,[ /!?],_,g')
%define product_tag %(echo %{new_product} |tr A-Z a-z |sed -e 's,[ /!?],_,g')
%define shorttag omv
%define new_disturl http://openmandriva.org/
%define new_bugurl http://issues.openmandriva.org/

%define am_i_cooker 1
%define am_i_rolling 0
%if %am_i_cooker
%define distrib Cooker
%else
%if %am_i_rolling
%define distrib Rolling
%else
%define distrib Official
%endif
%endif
%define _distribution %(echo %{new_distribution} | tr A-Z a-z |sed -e 's#[ /()!?]#_#g')
%define product_type Basic
%if %am_i_cooker
%define product_branch Devel
%else
%define product_branch Official
%endif
%define product_release 1
%define product_arch %{_target_cpu}

# The Distribution release, what is written on box
%define distro_release %{version}

# The distro branch: Cooker, Community or Official
%define distro_branch %{distrib}

# The distro arch, notice: using %_target_cpu is bad
# elsewhere because this depend of the config of the packager
# _target_cpu => package build for
# distro_arch => the distribution we are using
%define distro_arch %{_target_cpu}

%define major %(printf %u 0%(echo %{version}|cut -d. -f1))
%define minor %(printf %u 0%(echo %{version}|cut -d. -f2))
%define subminor %(printf %u 0%(echo %{version}|cut -d. -f3))
%define distro_tag %(echo $((%{major}*1000+%{minor})))
%define version_tag %(echo $((%{major}*1000000+%{minor}*1000+%{subminor})))
%define mdkver %{version_tag}

%ifarch %{x86_64}
%global secondary_distarch i686
%else
%ifarch %{aarch64}
%global secondary_distarch armv7hnl
%endif
%endif

Summary:	%{new_distribution} release file
Name:		distro-release
Version:	4.2
# (tpg) something needs to be done to make comparision 3.0 > 2015.0 came true
# 3001 = 3.1
# 3001 = 3.2 etc.
DistTag:	%{shorttag}%{distro_tag}
%if 0%am_i_cooker
Release:	0.4
%else
%if 0%am_i_rolling
Release:	0.2
%else
Release:	1
%endif
%endif
License:	GPLv2+
URL:		%{new_disturl}
Group:		System/Configuration/Other

%description
%{distribution} release file.

%package common
Summary:	%{new_distribution} release common files
Group:		System/Configuration/Other
%rename		rosa-release-common
%rename		mandriva-release-common
%rename		opemandriva-release-common
%rename		moondrake-release-common
%rename		mandriva-release
%rename		mandriva-release-Free
%rename		mandriva-release-One
%rename		mandriva-release-Powerpack
%rename		mandriva-release-Mini
# (tpg) older releases provides %{_sysconfdir}/os-release
Conflicts:	systemd < 37-5
Requires:	lsb-release
Requires:	setup
Requires:	filesystem
# cf mdvbz#32631
Provides:	arch(%{_target_cpu})
Provides:	%{arch_tagged distro-release-common}
# (tpg) remove after rpm5 to rpmv4 migration
%ifnarch x86_64
BuildRequires:	spec-helper
Requires:	spec-helper
%endif
# (tpg) get rid of it
%rename distro-release-Moondrake

%description common
Common files for %{new_distribution} release packages.

# build release flavour rpm
%package %{new_vendor}
Summary:	%{new_vendor} release file
Group:		System/Configuration/Other
Requires:	%{name}-common = %{EVRD}
Requires:	%{arch_tagged distro-release-common}
Requires:	%{name}-common >= %{version}
Provides:	mandriva-release = %{EVRD}
Provides:	distro-release = %{EVRD}
Provides:	system-release
Provides:	system-release(%{version})
Provides:	system-release(releasever) = %{version}

%description %{new_vendor}
%{new_distribution} release file for %{new_vendor} flavor.

%files %{new_vendor}
%{_rpmmacrodir}/macros.%{new_vendor}
%{_sysconfdir}/os-release.%{vendor_tag}
%{_sysconfdir}/%{vendor_tag}-release
%{_sysconfdir}/product.id.%{new_vendor}
%{_sysconfdir}/version.%{vendor_tag}
%{_sysconfdir}/os-release
%{_sysconfdir}/release
%{_sysconfdir}/product.id
%{_sysconfdir}/version

# desktop-common-data
%package desktop
Summary:	Desktop common files
Group:		System/Configuration/Other
Epoch:		2
BuildArch:	noarch
Requires:	distro-release
#XDG stuff
Requires:	libxdg-basedir
Requires:	xdg-compliance
Requires:	xdg-user-dirs
Requires:	xdg-utils
Requires:	run-parts
Requires(post):	hicolor-icon-theme
Requires:	hicolor-icon-theme
Conflicts:	kdelibs-common < 30000000:3.5.2
Conflicts:	kdebase-kdm-config-file < 1:3.2-62mdk
Requires(post):	etcskel
Requires(post):	run-parts
Requires:	shared-mime-info
Obsoletes:	menu-messages <= 2011.1
Obsoletes:	desktop-common-data < 1:4.2-4
%rename		mandrake_desk
%rename		menu
%rename		menu-xdg
%rename		faces-openmandriva
%rename		faces-icons
%rename		desktop-common-data

%description desktop
This package contains useful icons, menu structure and others goodies for the
%{distribution} desktop.

%package desktop-Plasma
Summary:	Plasma desktop configuration
Group:		Graphical desktop/KDE
BuildRequires:	cmake(ECM)
Requires:	%{name}-desktop >= %{version}
Requires:	%{name}-theme >= %{version}
Requires:	breeze
Requires:	breeze-gtk
Requires:	breeze-icons
Requires:	noto-sans-fonts
Provides:	kde4-config-file
Provides:	distro-kde4-config-OpenMandriva = 2015.0
Provides:	distro-kde4-config-OpenMandriva-common = 2015.0
Obsoletes:	distro-kde4-config-OpenMandriva < 2015.0
Obsoletes:	distro-kde4-config-OpenMandriva-common < 2015.0
Provides:	mandriva-kde4-config = 2014.0
Obsoletes:	mandriva-kde4-config < 2014.0
Provides:	distro-kde4-config-common = 2015.0
Obsoletes:	distro-kde4-config-common < 2015.0
%rename		distro-plasma-config
BuildArch:	noarch

%description desktop-Plasma
KDE Plasma desktop configuration.

#package desktop-Xfce
#description desktop-Xfce

%package theme
Summary:	Themes for %{distribution}
Group:		Graphics
Provides:	plymouth(system-theme)
Requires:	distro-theme-common
%ifnarch %{arm}
Requires:	plymouth-plugin-script
Requires:	grub2
%endif
%rename		grub2-OpenMandriva-theme
%rename		grub2-Moondrake-theme
%rename		distro-theme-common
%rename		distro-theme-extra
%rename		distro-theme-screensaver
%rename		distro-theme-OpenMandriva-screensaver
%rename		distro-theme-OpenMandriva-grub2
%rename		mandriva-theme-common
%rename		mandriva-theme-extra
%rename		mandriva-theme-Rosa-screensaver
%rename		mandriva-screensaver
%rename		mandriva-theme-screensave
%rename		mandriva-theme-Moondrake
%rename		mandriva-theme-OpenMandriva
BuildArch:	noarch

%description theme
This package provides default themes for %{distribution}'s components:
grub
screensaver
plymouth.

%package repos
Summary:	OpenMandriva package repositories
Group:		System/Base
License:	MIT
Provides:	openmandriva-repos(%{version})
Requires:	system-release(%{version})
Requires:	openmandriva-repos-pkgprefs = %{EVRD}
Requires:	openmandriva-repos-keys = %{EVRD}
Obsoletes:	openmandriva-repos-cooker < %{EVRD}

%description repos
OpenMandriva package repository files for DNF and PackageKit
with GPG public keys.

%package repos-keys
Summary:	OpenMandriva repository GPG keys
Group:		System/Base
# GPG keys are architecture independent
BuildArch:	noarch

%description repos-keys
OpenMandriva GPG keys for validating packages from OpenMandriva repositories by
DNF and PackageKit.

%package repos-pkgprefs
# (ngompa): See the following page on why this exists:
# https://fedoraproject.org/wiki/PackagingDrafts/ProvidesPreferences#Distribution_preference
Summary:	OpenMandriva repository package preferences
Group:		System/Base
# Preferences list is architecture independent
BuildArch:	noarch

## Base packages

# webfetch
Suggests:	curl

# webclient
Suggests:	lynx

# bootloader
Suggests:	grub2

# vim
Suggests:	vim-enhanced

# libEGL.so.1 (also provided by proprietary drivers)
Suggests:	libegl1
Suggests:	lib64egl1

# libGL.so.1 (also provided by proprietary drivers)
Suggests:	libgl1
Suggests:	lib64gl1

# Prefer openssh-askpass over openssh-askpass-gnome (for keychain)
Suggests:	openssh-askpass

# Python 3.x
Suggests:	python

# Initrd
Suggests:	dracut

## Multimedia

# festival-voice
Suggests:	festvox-kallpc16k

# gnome-speech-driver
Suggests:	gnome-speech-driver-espeak

# esound
Suggests:	pulseaudio-esound-compat

# gst-install-plugins-helper
Suggests:	packagekit-gstreamer-plugin

# libbaconvideowidget.so.0 (totem backend)
Suggests:	libbaconvideowidget-gstreamer0
Suggests:	lib64baconvideowidget-gstreamer0

# phonon-backend: prefer phonon-vlc over phonon-gstreamer
Suggests:	phonon-gstreamer

# phonon4qt5-backend: prefer phonon4qt5-vlc over phonon4qt5-gstreamer
Suggests:	phonon4qt5-gstreamer

# mate backends
Suggests:	mate-settings-daemon-pulse
Suggests:	mate-media-pulse

## Devel

# xemacs-extras provides ctags, prefer simple ctags
Suggests:	ctags

# prefer openssl-devel over libressl-devel
Suggests:	libopenssl-devel
Suggests:	lib64openssl-devel

# preferred compiler(s)
Suggests:	clang
Suggests:	libstdc++-devel

# prefer dnf-utils over urpmi-debuginfo-install
Suggests:	dnf-utils

## Servers

# sendmail-command and mail-server
Suggests:	postfix

# imap-server
Suggests:	dovecot

# webserver
Suggests:	apache

# nfs-server
Suggests:	nfs-utils

# ftpserver
Suggests:	proftpd

# postgresql
Suggests:	libpq5
Suggests:	lib64pq5

# syslog-daemon
Suggests:	systemd

# vnc
Suggests:	tigervnc

# x2goserver database backend
Suggests:	x2goserver-sqlite

## Various
# sane (also provided by saned)
Suggests:	sane-backends

# skanlite vs. xsane
Suggests:	skanlite

# virtual-notification-daemon
Suggests:	notification-daemon

# sgml-tools
# (the other choice is linuxdoc-tools which requires docbook-utils anyway)
Suggests:	docbook-utils

# input method
Suggests:	fcitx

# drupal database storage
Suggests:	drupal-mysql

# polkit-agent
Suggests:	polkit-kde-agent-1

# java
Suggests:	jre-current
Suggests:	jdk-current

# java-plugin
Suggests:	icedtea-web

Suggests:	lxsession-lite

# pinentry
Suggests:	pinentry-qt5

# %{_lib}qt5-output-driver
Suggests:	libqt5gui-x11
Suggests:	lib64qt5gui-x11

%description repos-pkgprefs
This package supplies DNF and PackageKit with global
preferences for packages in which multiple options are possible.

%if 0
%package rpm-setup
%description rpm-setup

%package rpm-setup-build
%description rpm-setup-build
%endif

%package installer
Summary:	Installer configuration for %{distribution}
Group:		Graphics
Conflicts:	calamares < 3.2.20-5
Requires:	%{name} = %{EVRD}

%description installer
Installer configuration files for %{distribution}.

%prep
cp -a %{_sourcedir}/doc/CREDITS CREDITS
cp -a %{_sourcedir}/doc/distro.txt distro.txt
cp -a %{_sourcedir}/doc/release-notes.txt release-notes.txt
cp -a %{_sourcedir}/doc/release-notes.html release-notes.html

# check that CREDITS file is in UTF-8, fail otherwise
if iconv -f utf-8 -t utf-8 < CREDITS > /dev/null
then
    true
else
    printf '%s\n' "The CREDITS file *MUST* be encoded in UTF-8"
    printf '%s\n' "Please fix it before continuing"
    false
fi

%install
mkdir -p %{buildroot}%{_sysconfdir}
ln -sf release %{buildroot}%{_sysconfdir}/mandriva-release
ln -sf release %{buildroot}%{_sysconfdir}/redhat-release
ln -sf release %{buildroot}%{_sysconfdir}/mandrake-release
ln -sf release %{buildroot}%{_sysconfdir}/mandrakelinux-release
ln -sf release %{buildroot}%{_sysconfdir}/rosa-release
ln -sf release %{buildroot}%{_sysconfdir}/system-release

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/10distro-release.csh << EOF
if ( -r %{_sysconfdir}/sysconfig/system ) then
    eval $(sed 's|^#.*||' %{_sysconfdir}/sysconfig/system | sed 's|\([^=]*\)=\([^=]*\)|set \1=\2|g' | sed 's|$|;|')
    setenv META_CLASS $META_CLASS
else
    setenv META_CLASS unknown
endif
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/10distro-release.sh << EOF
if [ -r %{_sysconfdir}/sysconfig/system ]; then
    . %{_sysconfdir}/sysconfig/system
    export META_CLASS
else
    export META_CLASS=unknown
fi
EOF

echo %{buildroot}%{_sysconfdir}/product.id.%{new_vendor}
cat >%{buildroot}%{_sysconfdir}/product.id.%{new_vendor} <<EOF
vendor=%{new_vendor},distribution=%{new_distribution},type=%{product_type},version=%{version},branch=%{product_branch},release=%{product_release},arch=%{product_arch},product=%{new_distribution}
EOF

mkdir -p %{buildroot}%{_rpmmacrodir}
cat >%{buildroot}%{_rpmmacrodir}/macros.%{new_vendor} <<EOF
%%distro_release	%{version}
%%distro_branch		%distro_branch
%%distro_class		%%(. %{_sysconfdir}/sysconfig/system; echo \\\$META_CLASS)
# (tpg) legacy stuff should be removed after all packages do not use macros begining with %%mandriva\
%%mandriva_release	%{version}
%%mandriva_branch	%mandriva_branch
%%mdkver		%mdkver
%%mdvver		%%mdkver
%%omvver		%%mdkver
# productid variable
%%product_id vendor=%{vendor_tag},distribution=%{new_distribution},type=%{product_type},version=%{version},branch=%{product_branch},release=%{product_release},arch=%{product_arch},product=%{new_distribution}
%%product_vendor	%{vendor_tag}
%%product_distribution	%{new_distribution}
%%product_type		%{product_type}
%%product_version	%{version}
%%product_branch	%{product_branch}
%%product_release	%{product_release}
%%product_arch		%{product_arch}
%%product_product	%{new_product}
%%distribution		%{new_distribution}
%%_distribution		%{distribution_tag}
%%disturl		%{new_disturl}
%%bugurl		%{new_bugurl}
%%vendor		%{new_vendor}
%%_vendor		%{vendor_tag}
%%distsuffix		%{shorttag}
%%distrelease		%{distro_tag}
EOF

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/system <<EOF
SECURITY=3
CLASS=beginner
LIBSAFE=no
META_CLASS=download
EOF

cat >%{buildroot}%{_sysconfdir}/%{vendor_tag}-release <<EOF
%{new_distribution} release %{version} (%{new_codename}) for %{_target_cpu}
EOF
cat >%{buildroot}%{_sysconfdir}/version.%{vendor_tag} <<EOF
%{version} %{release} (%{new_codename})
EOF

# (tpg) follow standard specifications http://www.freedesktop.org/software/systemd/man/os-release.html
cat >%{buildroot}%{_sysconfdir}/os-release.%{vendor_tag} <<EOF
NAME="%{new_distribution}"
VERSION="%{version} (%{new_codename})"
ID="%{vendor_tag}"
VERSION_ID="%{version}"
BUILD_ID="%(echo %(date +"%Y%m%d.%H"))"
PRETTY_NAME="%{new_distribution} %{version} (%{new_codename})"
VERSION_CODENAME="(%{new_codename})"
ANSI_COLOR="1;43"
CPE_NAME="cpe:/o:%{vendor_tag}:%{distribution_tag}:%{version}"
HOME_URL="%{new_disturl}"
BUG_REPORT_URL="%{new_bugurl}"
SUPPORT_URL="https://forum.openmandriva.org"
PRIVACY_POLICY_URL="https://www.openmandriva.org/tos"
EOF

ln -s os-release.%{vendor_tag} %{buildroot}%{_sysconfdir}/os-release
ln -s %{vendor_tag}-release %{buildroot}%{_sysconfdir}/release
ln -s product.id.%{new_vendor} %{buildroot}%{_sysconfdir}/product.id
ln -s version.%{vendor_tag} %{buildroot}%{_sysconfdir}/version

### DESKTOP ###

## Install backgrounds
# User & root's backgrounds
install -d -m 0755 %{buildroot}%{_datadir}/mdk/backgrounds/

# for easy access for users looking for wallpapers at expected location
install -d %{buildroot}%{_datadir}/wallpapers
ln -sr %{buildroot}%{_datadir}/mdk/backgrounds %{buildroot}%{_datadir}/wallpapers/mdk

## Install scripts
install -d -m 0755 %{buildroot}/%{_bindir}/
install -m 0755 %{_sourcedir}/desktops/bin/editor %{buildroot}/%{_bindir}/
install -m 0755 %{_sourcedir}/desktops/bin/www-browser %{buildroot}/%{_bindir}/
install -m 0755 %{_sourcedir}/desktops/bin/xvt %{buildroot}/%{_bindir}/

## Install faces
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/faces/
install -d -m 0755 %{buildroot}/%{_datadir}/faces/
cp -a %{_sourcedir}/desktops/faces/*.png %{buildroot}/%{_datadir}/mdk/faces/

# David - 9.0-5mdk - For KDE
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/default.png

# David - 9.0-5mdk - For GDM
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/user-default-mdk.png

# (tpg) default desktop files (do not place them in /etc/skel/Desktop !)
install -d -m 0755 %{buildroot}%{_datadir}/applications
install -m 0644 %{_sourcedir}/desktops/applications/*.desktop %{buildroot}%{_datadir}/applications

# icons
install -d -m 0755 %{buildroot}%{_iconsdir}/hicolor/scalable/apps
cp -a %{_sourcedir}/theme/icons/*.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/

#install theme for GDM/KDM
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/dm
for i in %{_sourcedir}/desktops/dm/*.png %{_sourcedir}/desktops/dm/*.desktop %{_sourcedir}/desktops/dm/*.xml ; do
  install -m 0644 $i %{buildroot}/%{_datadir}/mdk/dm/
done

# install bookmarks
install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
for i in %{_sourcedir}/desktops/bookmarks/konqueror/*.html ; do
  install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
done

install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
for i in %{_sourcedir}/desktops/bookmarks/mozilla/*.html ; do
    install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
done

mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/applications.menu
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/kde-applications.menu
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/gnome-applications.menu
### DESKTOP END ###

### DESKTOP PLASMA ###

mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg
mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg/KDE
mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg/QtProject
mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg/plasma-workspace/env
mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg/plasma-workspace/shutdown
mkdir -p %{buildroot}%{_kde5_datadir}/kservices5
mkdir -p %{buildroot}%{_kde5_datadir}/plasma/shells/org.kde.plasma.desktop/contents
mkdir -p %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/contents
mkdir -p %{buildroot}%{_datadir}/konsole

for i in kcmdisplayrc kcmfonts kcminputrc kdeglobals kscreenlockerrc ksplashrc kwinrc plasmarc startupconfig startupconfigfiles kcm-about-distrorc ksmserverrc kiorc dolphinrc konsolerc klaunchrc discoverabstractnotifier.notifyrc plasma_workspace.notifyrc powermanagementprofilesrc; do
    install -m 0644 %{_sourcedir}/desktops/Plasma/$i %{buildroot}%{_kde5_sysconfdir}/xdg/$i
done

install -m 0644 %{_sourcedir}/desktops/Plasma/metadata.desktop %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/metadata.desktop
install -m 0644 %{_sourcedir}/desktops/Plasma/metadata.desktop %{buildroot}%{_kde5_datadir}/kservices5/plasma-layout-template-org.openmandriva.plasma.desktop.defaultPanel.desktop
install -m 0644 %{_sourcedir}/desktops/Plasma/org.kde.plasma.desktop-layout.js %{buildroot}%{_kde5_datadir}/plasma/shells/org.kde.plasma.desktop/contents/layout.js
install -m 0644 %{_sourcedir}/desktops/Plasma/org.openmandriva.plasma.desktop.defaultPanel-layout.js %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/contents/layout.js
install -m 0644 %{_sourcedir}/desktops/Plasma/plasma-firstsetup.sh %{buildroot}%{_kde5_sysconfdir}/xdg/plasma-workspace/env/plasma-firstsetup.sh
install -m 0644 %{_sourcedir}/desktops/Plasma/Sonnet.conf %{buildroot}%{_kde5_sysconfdir}/xdg/KDE/Sonnet.conf
install -m 0644 %{_sourcedir}/desktops/Plasma/kdeglobals.sh %{buildroot}%{_kde5_sysconfdir}/xdg/plasma-workspace/env/kdeglobals.sh
install -m 0644 %{_sourcedir}/desktops/Plasma/qtlogging.ini %{buildroot}%{_kde5_sysconfdir}/xdg/QtProject/qtlogging.ini
install -m 0644 %{_sourcedir}/desktops/Plasma/OMV.profile %{buildroot}%{_datadir}/konsole/OMV.profile
mkdir -p %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/contents
install -m 0644 %{_sourcedir}/desktops/Plasma/org.openmandriva.plasma.desktop.globalMenuPanel-layout.js %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/contents/layout.js
install -m 0644 %{_sourcedir}/desktops/Plasma/metadata-globalMenu.desktop %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/metadata.desktop
mkdir -p %{buildroot}%{_datadir}/plasma/look-and-feel
cp -a %{_sourcedir}/desktops/Plasma/org.openmandriva4.desktop %{buildroot}%{_datadir}/plasma/look-and-feel/org.openmandriva4.desktop

### DESKTOP PLASMA END ###

### THEME ###

# Make sure the logo can be found where modern applications expect it
mkdir -p %{buildroot}%{_iconsdir}/hicolor/scalable/apps
cp %{_sourcedir}/theme/icons/openmandriva.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
for i in 16 22 24 32 36 48 64 72 96 128 192 256 512; do
    mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
    convert -background none %{_sourcedir}/theme/icons/openmandriva.svg %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/openmandriva.png
done

# Default wallpaper should be available without browsing file system
mkdir -p %{buildroot}%{_datadir}/wallpapers
cp -a %{_sourcedir}/theme/backgrounds/*.*g %{buildroot}%{_datadir}/mdk/backgrounds
cp -a %{_sourcedir}/theme/extra-backgrounds/*.*g %{buildroot}%{_datadir}/mdk/backgrounds
# (tpg) add falvour name on the wallapaer
convert -fill white -pointsize 20 -gravity center -draw "text 565,560 '%{distrib}'" %{buildroot}%{_datadir}/mdk/backgrounds/%{vendor}-16x10.png %{buildroot}%{_datadir}/mdk/backgrounds/%{vendor}-16x10.png
convert -fill white -pointsize 20 -gravity center -draw "text 300,410 '%{distrib}'" %{buildroot}%{_datadir}/mdk/backgrounds/%{vendor}-16x9.png %{buildroot}%{_datadir}/mdk/backgrounds/%{vendor}-16x9.png
convert -fill white -pointsize 20 -gravity center -draw "text 700,500 '%{distrib}'" %{buildroot}%{_datadir}/mdk/backgrounds/%{vendor}-4x3.png %{buildroot}%{_datadir}/mdk/backgrounds/%{vendor}-4x3.png
convert -fill white -pointsize 20 -gravity center -draw "text 500,370 '%{distrib}'" %{buildroot}%{_datadir}/mdk/backgrounds/%{vendor}-5x4.png %{buildroot}%{_datadir}/mdk/backgrounds/%{vendor}-5x4.png
ln -sf /usr/share/mdk/backgrounds/OpenMandriva-16x9.png %{buildroot}%{_datadir}/mdk/backgrounds/default.png
ln -sf /usr/share/mdk/backgrounds/default.png %{buildroot}%{_datadir}/wallpapers/default.png
ln -sf /usr/share/mdk/backgrounds/default.png %{buildroot}%{_datadir}/wallpapers/default.jpg

mkdir -p %{buildroot}%{_datadir}/mdk/screensaver
cp -a %{_sourcedir}/theme/screensaver/*.jpg %{buildroot}%{_datadir}/mdk/screensaver

mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -a %{_sourcedir}/theme/pixmaps/*.*g %{buildroot}%{_datadir}/pixmaps

mkdir -p %{buildroot}%{_datadir}/plymouth/themes
cp -a %{_sourcedir}/theme/plymouth/%{vendor} %{buildroot}%{_datadir}/plymouth/themes/

# (tpg) arm does not uses grub, but aarch64 does
%ifnarch %{arm}
mkdir -p %{buildroot}/boot/grub2/themes/%{vendor}
cp -a %{_sourcedir}/theme/grub/%{vendor}/* %{buildroot}/boot/grub2/themes/%{vendor}
rm -rf %{buildroot}/boot/grub2/themes/%{vendor}/05_theme
mkdir -p %{buildroot}%{_sysconfdir}/grub.d
install -m755 %{_sourcedir}/theme/grub/%{vendor}/05_theme %{buildroot}%{_sysconfdir}/grub.d/05_theme
mkdir -p %{buildroot}%{_sysconfdir}/default/
cat > %{buildroot}%{_sysconfdir}/default/grub.%{vendor} << EOF
GRUB_THEME=/boot/grub2/themes/%{vendor}/theme.txt
GRUB_BACKGROUND=/boot/grub2/themes/%{vendor}/terminal_background.png
GRUB_DISTRIBUTOR="%{distribution}"
EOF
%endif

### THEME END ###

### REPOS ###
ARCH=%{_target_cpu}
echo $ARCH |grep -q arm && ARCH=armv7hnl
[ "$ARCH" = "i386" ] && ARCH=i686
[ "$ARCH" = "i586" ] && ARCH=i686

# Install the GPG key
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install %{_sourcedir}/rpm/RPM-GPG-KEY-%{vendor} -pm 0644 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

# Install the repositories
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d

%if %{defined secondary_distarch}
SECONDARY_ARCH=%{secondary_distarch}
%else
SECONDARY_ARCH=""
%endif

for arch in ${ARCH} ${SECONDARY_ARCH}; do
    for release in release rock rolling cooker; do
	for repo in main unsupported restricted non-free; do
	    case "$repo" in
			main)
				REPO=""
				REPONAME=""
                                ;;
			*)
				REPO="-$repo"
				REPONAME=" - $(echo $repo |cut -b1 |tr a-z A-Z)$(echo $repo |cut -b2-)"
				;;
			esac

			vertag=$release
			case "$release" in
			release)
				NAME='OpenMandriva $releasever'"$REPONAME - $arch"
				HAS_UPDATES=true
				vertag='$releasever'
				;;
			rock)
				NAME="OpenMandriva Rock$REPONAME - $arch"
				HAS_UPDATES=true
				;;
			rolling)
				NAME="OpenMandriva Rolling$REPONAME - $arch"
				HAS_UPDATES=false
				;;
			cooker)
				NAME="OpenMandriva Cooker$REPONAME - $arch"
				HAS_UPDATES=false
				;;
                        esac
                        cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-$arch$REPO]
name="$NAME"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/${repo}/release/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=release
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
type=rpm-md
enabled=0

EOF

if $HAS_UPDATES; then
    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-updates-$arch$REPO]
name="$NAME - Updates"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/${repo}/updates/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=updates
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF
fi

    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-testing-$arch$REPO]
name="$NAME - Testing"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/${repo}/testing/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=testing
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF

    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-$arch$REPO-debuginfo]
name="$NAME - Debug"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/debug_${repo}/release/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=release
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF

if $HAS_UPDATES; then
    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-updates-$arch$REPO-debuginfo]
name="$NAME - Updates - Debug"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/debug_${repo}/updates/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=updates
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF
fi

cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-testing-$arch$REPO-debuginfo]
name="$NAME - Testing - Debug"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/${arch}/debug_${repo}/testing/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=testing
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF

cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-$arch$REPO-source]
name="$NAME - Source"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/SRPMS/${repo}/release/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=release
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF

if $HAS_UPDATES; then
    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-updates-$arch$REPO-source]
name="$NAME - Updates - Source"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/SRPMS/${repo}/updates/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=updates
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF
fi

cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-testing-$arch$REPO-source]
name="$NAME - Testing - Source"
# Master repository:
# baseurl=http://abf-downloads.openmandriva.org/$vertag/repository/SRPMS/${repo}/testing/
mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=testing
fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF
                done
        done
done
sed -i '$ d' %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo

## And enable the one we're installing from
%if %am_i_cooker
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-cooker-${ARCH}.repo
%else
%if %am_i_rolling
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rolling-${ARCH}.repo
%else
# Second occurence in $RELEASE and Rock is updates/
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rock-${ARCH}.repo
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rock-${ARCH}.repo
%endif
%endif

chmod 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo

### REPOS END ###

### INSTALLER ###
mkdir -p %{buildroot}%{_sysconfdir}/calamares/modules
install -m644 %{_sourcedir}/installer/settings.conf %{buildroot}%{_sysconfdir}/calamares/settings.conf
for i in bootloader.conf displaymanager.conf finished.conf fstab.conf grubcfg.conf keyboard.conf locale.conf machineid.conf mount.conf packages.conf partition.conf removeuser.conf services-systemd.conf shellprocess.conf umout.conf unpackfs.conf users.conf webview.conf welcome.conf ; do
    install -m644 %{_sourcedir}/installer/$i %{buildroot}%{_sysconfdir}/calamares/modules/$i
done

mkdir -p %{buildroot}%{_sysconfdir}/calamares/branding/auto
for i in 2015-ads_01.png 2015-ads_02.png 2015-ads_03.png 2015-ads_04.png 2015-ads_05.png 2015-ads_06.png 2015-ads_07.png adverts.qml ; do
    install -m644 %{_sourcedir}/installer/$i %{buildroot}%{_sysconfdir}/calamares/branding/auto/$i
done

cat > %{buildroot}%{_sysconfdir}/calamares/branding/auto/branding.desc <<EOF
---
componentName:  auto

strings:
    productName:         "%{new_distribution}"
    shortProductName:    "%{new_distribution}"
    version:             "%{version} (%{new_codename})"
    shortVersion:        "%{version} (%{new_codename})"
    versionedName:       "%{new_distribution} %{version} (%{new_codename})"
    shortVersionedName:  "%{new_distribution} %{version} (%{new_codename})"
    bootloaderEntryName: "openmandriva"
    productUrl:          "%{new_disturl}"
    supportUrl:          "%{new_bugurl}"
    knownIssuesUrl:      "https://wiki.openmandriva.org/en/%{version}/Errata"
    releaseNotesUrl:     "https://wiki.openmandriva.org/en/%{version}/Release_Notes"

images:
    productLogo:         "%{_iconsdir}/openmandriva.svg"
    productIcon:         "%{_iconsdir}/openmandriva.svg"
# (tpg) need to decide what show here
#    productWelcome:      "languages.png"

slideshow:               "adverts.qml"

style:
   sidebarBackground:    "#263039"
   sidebarText:          "#FFFFFF"
   sidebarTextSelect:    "#292F34"
EOF

### INSTALLER END ###

%check
%if %{am_i_cooker}
case %{release} in
0.*)
    ;;
*)
    printf '%s\n' "Cooker distro should have this package with release < %{mkrel 1}"
    exit 1
    ;;
esac
%endif

%post theme
%ifnarch %{arm}
%{_sbindir}/plymouth-set-default-theme %{vendor}

if test -f %{_sysconfdir}/default/grub ; then
    . %{_sysconfdir}/default/grub
    if [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "x" ] || [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "xfalse" ]; then
	sed -e '/GRUB_DISTRIBUTOR/d' -e '/GRUB_THEME/d' -e '/GRUB_BACKGROUND/d' -i %{_sysconfdir}/default/grub
	if [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "x" ]; then
	    echo -e "\n" >> %{_sysconfdir}/default/grub
	    echo "GRUB_DISABLE_VENDOR_CONF=false" >> %{_sysconfdir}/default/grub
	fi
    fi
fi

update-alternatives --install %{_sysconfdir}/default/grub.vendor grub.vendor %{_sysconfdir}/default/grub.%{vendor} 10
%endif

%postun theme
%ifnarch %{arm}
if [ "$1" = "0" ]; then
    update-alternatives --remove grub.vendor %{_sysconfdir}/default/grub.%{vendor}
fi
%endif

%files common
%doc CREDITS distro.txt release-notes.*
%{_sysconfdir}/redhat-release
%{_sysconfdir}/mandrake-release
%{_sysconfdir}/mandriva-release
%{_sysconfdir}/mandrakelinux-release
%{_sysconfdir}/rosa-release
%{_sysconfdir}/system-release
%{_sysconfdir}/profile.d/10distro-release.sh
%{_sysconfdir}/profile.d/10distro-release.csh
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/system

%files desktop
%{_bindir}/*
%dir %{_sysconfdir}/xdg
%dir %{_sysconfdir}/xdg/menus
%config(noreplace) %{_sysconfdir}/xdg/menus/*.menu
%dir %{_datadir}/faces/
%{_datadir}/faces/default.png
%{_datadir}/faces/user-default-mdk.png
%dir %{_datadir}/mdk/
%dir %{_datadir}/mdk/faces/
%{_datadir}/mdk/faces/*.png
%{_datadir}/applications/*.desktop
%dir %{_datadir}/mdk/backgrounds
%{_datadir}/wallpapers/mdk
%dir %{_datadir}/mdk/bookmarks
%dir %{_datadir}/mdk/bookmarks/konqueror
%{_datadir}/mdk/bookmarks/konqueror/*.html
%dir %{_datadir}/mdk/bookmarks/mozilla
%{_datadir}/mdk/bookmarks/mozilla/*.html
%{_datadir}/mdk/dm
%{_iconsdir}/hicolor/scalable/apps/*.svg

%files desktop-Plasma
%{_kde5_sysconfdir}/xdg/*
%{_datadir}/konsole/OMV.profile
%{_kde5_datadir}/kservices5/plasma-layout-template-org.openmandriva.plasma.desktop.defaultPanel.desktop
%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel
%{_kde5_datadir}/plasma/shells/org.kde.plasma.desktop/contents/layout.js
%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel
%{_datadir}/plasma/look-and-feel/org.openmandriva4.desktop

%files theme
%{_datadir}/mdk/backgrounds/*.*g
%{_datadir}/wallpapers/default.*g
%{_iconsdir}/hicolor/scalable/apps/openmandriva.svg
%{_iconsdir}/hicolor/*/apps/openmandriva.png
%dir %{_datadir}/mdk/screensaver
%{_datadir}/mdk/screensaver/*.jpg
%{_datadir}/plymouth/themes/%{vendor}
%optional %{_datadir}/pixmaps/system-logo-white.png

%ifnarch %{arm}
%{_sysconfdir}/grub.d/05_theme
%{_sysconfdir}/default/grub.%{vendor}
%dir /boot/grub2/themes/%{vendor}
/boot/grub2/themes/%{vendor}/*
%{_sysconfdir}/grub.d/*
%endif

%files repos
%dir %{_sysconfdir}/yum.repos.d
%config(noreplace) %{_sysconfdir}/yum.repos.d/openmandriva*.repo

%files repos-keys
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva

%files repos-pkgprefs

%files installer
%{_sysconfdir}/calamares/*.conf
%{_sysconfdir}/calamares/modules/*.conf
%{_sysconfdir}/calamares/branding/auto/*
