%define debug_package %{nil}

Name:         ipmitool
Summary:      ipmitool - Utility for IPMI control
Version:      1.8.18.244.gd7be5d0
Release:      1%{?_distro:.%{_distro}}
License:      BSD
Group:        Utilities
#Packager:    PackagerName <packager@example.com>
Distribution: GitHub Build
Source:       %{name}-%{version}.tar.gz
Buildroot:    /var/tmp/ipmitool-root

%description
This package contains a utility for interfacing with devices that support
the Intelligent Platform Management Interface specification.  IPMI is
an open standard for machine health, inventory, and remote power control.

This utility can communicate with IPMI-enabled devices through either a
kernel driver such as OpenIPMI or over the RMCP LAN protocol defined in
the IPMI specification.  IPMIv2 adds support for encrypted LAN
communications and remote Serial-over-LAN functionality.

It provides commands for reading the Sensor Data Repository (SDR) and
displaying sensor values, displaying the contents of the System Event
Log (SEL), printing Field Replaceable Unit (FRU) information, reading and
setting LAN configuration, and chassis power control.

%prep
if [ "$RPM_BUILD_ROOT" ] && [ "$RPM_BUILD_ROOT" != "/" ]; then
    rm -rf $RPM_BUILD_ROOT
fi

%setup

%build
./configure \
	--with-rpm-distro= \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--datadir=%{_datadir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--sysconfdir=%{_sysconfdir}
make

%install
make DESTDIR=$RPM_BUILD_ROOT install-strip

%clean
if [ "$RPM_BUILD_ROOT" ] && [ "$RPM_BUILD_ROOT" != "/" ]; then
    rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(755,root,root)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/ipmitool/*
%{_datadir}/misc/*
%{_mandir}/man*/*
%doc %{_datadir}/doc/ipmitool


%changelog
* Sat Oct 8 2016 <gilles.buloz@kontron.com>  1.8.18-1
- Add mac2str() and str2mac() to print/parse MAC address
- Change formatting, remove commented-out code in
  src/plugins/imb/imbapi.c
- Export find_lan_channel() as global
- Expose _ipmi_get_channel_info()
- Extend buf2str to allow separator
- Fix indentation of #define in src/plugins/imb/imbapi.c
- Fix missing `goto out_free;` when ipmi_parse_hex() returns (-1)
- Fix warning for buf2str argument
- ID 408 - fix sel list last X listing
- ID: 38 - Protocol violating SOL retries when talking to
  SIMSO-HTC
- ID: 459 - Fix reading FRU on Artesyn (Emerson) shelf manager,
  MF105.
- ID: 464 - ipmievd crash fix in log_event
- ID:230 - check return value of malloc() in lib/ipmi_ekanalyzer.c
- ID:261 - Fix err. output consistency for % ipmitool chassis
  INV_PARAM;
- ID:287 - Fix print-out of DDR3 SDRAM Serial Number
- ID:287 - Remove trailing white-spaces from dimm_spd.c
- ID:289 - bmx-snmp-proxy: PEF alerting does not work for
  multiple destinations
- ID:312 - BREAKING CHANGE - Re-design of PEF user interface
- ID:312 - Fix bitmask in _ipmi_set_pef_policy_entry()
- ID:335 - Check return value of fseek(), prevent segfault
- ID:335 - Check return value of fseek(), prevent segfault
- ID:355 - Comment out statement without effect in lib/ipmi_sel.c
- ID:355 - Fix 'missing initializer' in struct lan_param
- ID:355 - Fix ``warning: ISO C forbids zero-size array 'data'''
- ID:355 - Fix different pointer type in lib/ipmi_picmg.c
- ID:355 - Fix missing struct initializers in lib/ipmi_firewall.c
- ID:355 - Fix printf format in lib/ipmi_sunoem.c
- ID:355 - Fix printf() related warnings in lib/ipmi_delloem.c
- ID:355 - Fix signedness warnings in lib/ipmi_sdr.c
- ID:355 - Fix statements without effect in lib/ipmi_ekanalyzer.c
- ID:355 - Move section_id from ipmi_fru. to ipmi_fru.c
- ID:355 - Replace DEBUG() macro with lprintf(LOG_DEBUG, ...)
- ID:375 - Add lan6 subcommand to handle IPv6 LAN parameters
- ID:400 - Add support for VITA-specific sensor types and events.
- ID:441 - Add support for HMAC_MD5 and HMAC_SHA256
- ID:443 - Disable USB driver by default on non-Linux systems
- ID:444 - Cleanup of defaults in configure.ac
- ID:445 - Fix of compilation on FreeBSD
- ID:446 - Fix broken firewall reset iterator
- ID:447 - Fix access beyond array limits in serial_terminal
- ID:449 - ipmitool close console session for sol deactivate
  command
- ID:451 - Modify the memory ecc error display of SEL for new
  supermicro motherboards.
- ID:452 - Add PICMG extension 5.x for PICMG extension check
- ID:454 - Add support for PICMG 3.1 R2.0 Link Types and Link
  Classes.
- ID:456 - Unable to disable the VLAN ID using ipmitool
- ID:457 - Display User ID enable/disable status
- ID:463 - Removal of Nokia Siemens Networks
- ID:465 - Supermicro memory ecc Modify the memory ecc error
  display of SEL for new supermicro boards.
- Moved ipmi_parse_hex() to helper.c
- Re-work ipmi_mc_get_guid() and turn it into reusable code
- Revert "ID:335 - Check return value of fseek(), prevent segfault"
- Rewrite code with the notion that Kg is binary data, not string

* Sun May 1 2016 <gilles.buloz@kontron.com>  1.8.17-1
- Add INSTALL and NEWS, mandated by autoconf
- Added missing ipmi_sel_supermicro.h to template Makefile.am
- Check rsp->data_len in ipmi_sel_get_info()
- Fix "redirecting incorrect #include <sys/poll.h> to <poll.h>"
  warning with musl libc
- Fix automake compatibility warnings
- Fix implicit declaration of function
  'get_nic_selection_mode_12g' in lib/ipmi_delloem.c
- Fix implicit declaration of function 'ipmi_get_oem' in
  src/plugins/imb/imb.c
- Fix implicit declaration of function 'ipmi_get_oem' in
  src/plugins/lanplus/lanplus.c
- Fix implicit declaration of function 'ipmi_get_oem' in
  src/plugins/open/open.c
- Fix implicit declarations of functions 'HpmfwupgPreUpgradeCheck'
  and 'ipmi_intf_get_max_request_data_size' in lib/ipmi_hpmfwupg.c
- Fix implicit declarations of functions
  'ipmi_intf_set_max_request_data_size' and
  'ipmi_intf_set_max_response_data_size' in lib/hpm2.c
- Fix implicit function declaration of
  ipmi_intf_get_max_response_data_size in lib/ipmi_sdr.c
- Fix several implicit declarations of functions in
  lib/ipmi_main.c
- Fix several implicit function declarations in lib/ipmi_fru.c
- Fix warning: suggest parentheses around '+' inside '<<'
  in lib/ipmi_main.c
- Fix warning: suggest parentheses around arithmetic in operand of
  '|' in include/ipmitool/hpm2
- Get rid of old INCLUDES macro, use AM_CPPFLAGS instead.
- ID 440 - Fix 'unknown type name fd_set error.
- ID 440 - remove obsolete headers from lib/ipmi_sunoem.c
- ID:322 - let 'ekanalyzer frushow' run without a working
  IPMI target
- ID:355 - Add #include <strings.h> to lib/ipmi_sel.c
- ID:355 - Add macros and #include and reduce number of warnings
- ID:355 - Change CFLAG -std=c99 to -std=gnu99
- ID:355 - Move Super Micro stuff into dedicated header file
- ID:355 - Remove declared, but not used variables
- ID:404 - Edit FRU information update problem
- ID:405 - Use meaningful Generator ID for "ipmitool sel add"
- ID:407 - Avoid assert on mismatched session ID
- ID:409 - Fix IPv6 socket creation on Windows/Cygwin.
- ID:410 - Disable USB interface for Windows/Cygwin by default.
- ID:410 - Enable/disable USB interface by "auto"
- ID:411 - Fix HPM.2 revision check for R1.1 and subsequent
  specification revisions.
- ID:412 - Check errors when setting a user password.
- ID:413 - Print new line chne character when setting user
  privilege.
- ID:414 - ekanalyzer frushow fails to show 'Product Info'
  correctly
- ID:417 - Fix some typos
- ID:418 - Fix Compiling under Mac OS X
- ID:419 - List dummy.h in Makefile.am, so it gets included in
  a release tarball
- ID:421 - Fix memleak for sol output
- ID:423 - Don't assume internal use area is present in ekanalyzer
- ID:424 - Update dimm_spd.c with data from the latest JEDEC List
- ID:425 - Disable USB interface for OS X/darwin
- ID:426 - Fallback to run-time detection of PAGESIZE if
  compile-time detection is not supported
- ID:426 - Include sys/socket.h instead of asm/socket.h
- ID:426 - Include wchar.h instead of defining wchar_t ourselves
- ID:427 - Cleanup comment in ipmi_sdr_get_header()
- ID:427 - The first two bytes of dumped raw SDR data is wrong.
- ID:428 - Update IANA numbers / Product Name for IBM and ADLINK
- ID:430 - Change Nokia Siemens Networks to Nokia Solutions
  and Networks
- ID:431 - Fix correct interpretation of led states
- ID:437 - sel: Fix "sel time set <time>"
- Make bootstrap script part of dist packages
- Remove #if 0 code aka not-compiled-in
- Remove trailing white-spaces in lib/log.c
- git-ignore autoconf-generated files

* Sun Nov 22 2015 <gilles.buloz@kontron.com>  1.8.16-1
- Add _ipmi_get_channel_access() and _ipmi_get_channel_info()
- Add _ipmi_get_user_access() and _ipmi_set_user_access()
- Add _ipmi_get_user_name()
- Add _ipmi_set_channel_access() function
- Add _ipmi_set_user_password() function
- Add limits check in get_cmdline_macaddr()
- Change expression in ipmi_pef_get_info() in order to silence Coverity
- Change expression in ipmi_pef_list_policies() in order to silence Coverity
- Code cleanup in ipmi_user_main()
- Create ask_password() and re-use code
- Delete dead code from ipmi_sunoem_echo() - CID#1261338
- Don't output pidfile before parsing command line arguments
- Don't use tmp variable since it's not necessary in ipmi_user_test()
- Fix 'user help' output
- Fix Assign instead of compare in KfwumGetDeviceInfo() - CID#1149034
- Fix Identical code for different branches in ipmi_tsol_main() -
  CID#1261346
- Fix big parameter passed by value in ipmi_sel_oem_match() - CID#1261347
- Fix dead code in ipmi_firewall_reset() - CID#1261342
- Fix eval logic in ipmi_user_priv()
- Fix file descriptor leak in ipmi_exec_main() - CID#1149040
- Fix identical code for diff branches in DellOEM - CID#1261326
- Fix memory leak in get_supermicro_evt_desc()
- Fix memory leak in ipmi_ek_display_board_info_area() - CID#1149051
- Fix missing return in ipmi_kontronoem_main() - CID#1261317
- Fix of previous commit - memset() expects pointer
- Fix out-of-bound-reads in get_supermicro_evt_desc()
- Fix resource leak in fru_area_print_board() - CDI#1149048
- Fix resource leak in fru_area_print_chassis() - CID#1149047
- Fix resource leak in fru_area_print_product() - CID#1149046
- Fix resource leak in ipmi_kontron_set_serial_number() - CID#1149041
- Fix typo vlan->VLAN in ipmi_lan_set_vlan_id() and
  ipmi_lan_set_vlan_priority()
- Fix uninitialized struct in ipmi_fru_upg_ekeying() - CID#1149065
- Fix user input validation in Channel and User sub-commands
- Fix wrong size argument in ipmi_sdr_list_cache_fromfile() - CID#1149056
- Fix/remove pointer cast in _ipmi_set_user_access()
- Hook functions in ipmi_user to _ipmi_set_user_password()
- Hook ipmi_get_channel_info() to _ipmi_get_*()
- Hook ipmi_get_channel_medium() to new _ipmi_get_*() functions
- Hook ipmi_lan_set_password() to _ipmi_set_user_password()
- Hook ipmi_print_user_list() and friends to _ipmi_* functions
- Hook ipmi_set_alert_enable() to _ipmi_*()
- Hook ipmi_set_user_access() to _ipmi_set_user_access()
- Hook ipmi_user_priv() to _ipmi_set_user_access()
- ID:307 - Intel I82751 super pass through mode fixup
- ID:355 - Fix compiler warnings for Dummy Interface
- ID:380 - raw commands override retry and timeout values
- ID:319 - Interface safe re-open
- ID:320 - Add VITA 46.11 support
- ID:333 - Set read timeout to 15s in OpenIPMI interface
- ID:336 - ipmitool does not fall back to IPv4 for IPMI v2 / RMCP+ sessions
- ID:343 - Print actual sensor thresholds in 'sensors' comand
- ID:343 - Remove AC_FUNC_MALLOC
- ID:344 - Fix HPM.2 long message support
- ID:345 - Do not do several close session retries when catching SIGINT
- ID:346 - lib/ipmi_sdradd.c ipmi_sdr_read_record has a file descriptor leak
- ID:347 - Incorrect reserved channel number
- ID:348 - Add support for the "System Firmware Version"
- ID:349 - user set password - add option to choose 16/20 byte password
- ID:354 - Replace obsolete u_int with uint32_t in dimm_spd.c
- ID:354 - Replace obsolete u_int[0-9]+_t with standardized types in Free
  iface
- ID:354 - forcefully switch to C99 and more strict CFLAGS
- ID:354 - replace/drop caddr_t in IMB
- ID:354 - struct member h_addr has been replaced
- ID:354 - uint8_t >= 0 is always true, don't test it
- ID:355 - Fix Enumeration value not handled in ipmi_get_event_desc()
- ID:355 - Fix ``ISO C forbids omitting the middle term of a ?: expression''
- ID:355 - Fix ``obsolete use of designated initializer with ¿:¿'' warning
- ID:355 - Fix comparison of unsigned expression
- ID:355 - Fix compiler warnings
- ID:355 - Fix compiler warnings in dimm_spd.c
- ID:355 - Fix couple compiler warnings in ipmi_lanp.h
- ID:355 - Fix formatting warning in get_cmdline_ipaddr()
- ID:355 - Fix zero-length format string warning in
  get_supermicro_evt_desc()
- ID:355 - Remove defined but unused variable in _set_command_enables()
- ID:355 - remove unused variables from ipmi_dcmi.c
- ID:357 - out-of-bound access in DDR4 code ID:356 -  DIMM4 Die Count is
  unreachable
- ID:357 - out-of-bound access in DDR4 code
- ID:358 - check data length in else branch of ipmi_spd_print()
- ID:361 - Add a OEM IANA information
- ID:363 - Node Manager feature patch.
- ID:363 - fix Coverity issues in NM implementation
- ID:364 - Fix for serial-basic interface bridging
- ID:365 - Fix for ipmitool crash when using serial-terminal interface
- ID:366 - Properly clean LAN and LAN+ interfaces on close
- ID:367 - Fix building of non-bridged LAN interface commands
- ID:368 - Fix handling of bridging-related parameters
- ID:369 - Fix lanplus interface bridging and response matching
- ID:370 - add anonymous union support in CFLAGS for older gcc
- ID:371 - add ericsson oem
- ID:373 - Fix compilation of IMB on Windows
- ID:374 - Check/set LED Duration correctly
- ID:376 - Add means to configure "Bad Password Threshold"
- ID:381 - Script to log installation status as SEL events
- ID:382 - Fix memcpy() params in HpmFwupgActionUploadFirmware()
- ID:383 - Fix compile-time error in src/plugins/lan/lan.c
- ID:384 - Fix compilation under cygwin64
- ID:388 - Fix Error message always printed if BMC does not support VITA
- ID:388 - Handle ccode 0xCC as well in VITA discovery
- ID:388 - Turn all messages into LOG_INFO in VITA discovery
- ID:389 - Add on of Advantech IANA number
- ID:390 - Support for new Communication Interface (USB Medium)
- ID:391 - changing data_len from 17 to 16 according to ipmi spec 22.29,
  first byte is completion code
- ID:392 - _ipmi_get_user_name() work-around for some BMCs
- ID:393 - ipmitool man page addition for Node Manager support.
- ID:394 - close fp if isn't NULL and set it NULL afterwards in USB plugin
- ID:394 - plugins/usb: Fix probe for SCSI devices
- ID:395 - Fix fru string without resizing it
- ID:396 - Fixed invalid length check in picmg led cap command.
- ID:397 - Fixed picmg policy set command.
- ID:398 - Fixed channel setaccess command.
- ID:399 - Fixed channel getciphers command.
- ID:401 - Fixed 30 second delay when activating SOL on 'dumb' Intel MACs.
- ID:402 - Misguiding error print-out when using some 'lan' commands.
- Init user_access_t struct in ipmi_user_priv()
- Make user User Privilege Limit is within range
- Node Manager Feature, correct 1268194 missing break.
- Output pidfile only in verbose mode
- Print error message to STDERR in ipmi_channel.c
- Re-work 'channel getaccess' and 'channel setaccess'
- Re-work ccode eval in ipmi_get_channel_medium()
- Remove commented-out code in ipmi_picmg_clk_set() - CID#1261339
- Remove dead code - rsp can't be NULL at this point - CID#1149005
- Remove dead code in fru_area_print_board() - CID#1149001
- Remove dead code in fru_area_print_chassis() - CID#1149000
- Remove dead code in fru_area_print_product() - CID#1148999
- Remove dead(duplicate) code from ipmi_sol_main() - CID#1148996
- Remove get_channel_access_rsp and get_channel_info_rsp structs
- Remove ipmi_user_set_password()
- Remove length checks in get_supermicro_evt_desc()
- Remove redundant user-input conversion from ipmi_sel_delete()
- Remove trailing white-spaces in ipmi_user.c
- Remove trailing white-spaces in ipmi_user.c
- Remove trailing white-spaces in src/plugins/dummy/dummy.c
- Remove unused variable from ipmi_get_channel_cipher_suites()
- Replace deprecated bzero() with memset()
- Replace s6_addr16 with s6_addr since Mac OS X does not have it
- Rewrite ipmi_set_channel_access()
- Split ipmi_user_main() into smaller functions
- ipmi_print_user_summary() to utilize _ipmi_get_user_access()
- ipmitool delloem: ipmitool delloem extension always return success - fix
  it

* Mon Nov 24 2014 <gilles.buloz@kontron.com>  1.8.15-1
- ID: 340 - ipmitool sol session improperly closes on packet retry
- ID: 277 - support for hostnames longer than 64 chars
- ID: 313 - ipmitool doesn't support hostname long than 64 symbols
- ID: 277 - Minor issue with ipmi_intf_session_set_hostname()
- ID: 247 - 'sensor thresh' help output is wrong
- ID: 324 - conflicting declaration write_fru_area()
- ID: 337 - Add support for 13G Dell PowerEdge
- ID: 325 - DDR4 DIMM Decoding Logic
- ID: 328 - HPM.2 fixes
- ID: 329 - hpm.1 upgrade fixes
- ID: 103 - picmg discover messages should be DEBUG, not INFO
- ID: 331 - Passwords provided in file (-f option) truncated on space
- ID: 318 - ipmi_tsol.c: fix buffer overflow
- ID: 306 - "fru print" command prints the FRU #0 twice
- ID: 305 - HPM.1 deferred activation support fixup
- ID: 317 - ipmi_fwum.c: fix typo
- ID: 315 - buildsystem: configure.in is deprecated
- ID: 316 - Directory debian is outdated
- ID: 103 - 'lib/ipmi_ekanalyzer.c' needs a re-work
- ID: 46 - SEL OEM record corner case

* Mon May 5 2014 <gilles.buloz@kontron.com>  1.8.14-1
- ID: 299 - openipmi plugin writes zero to wrong byte
- ID: 301 - Add OS/Hypervisor installation status events
- ID: 298 - fix LANplus retry
- ID: 295 - inform user if SOL session disconnected
- ID: 297 - don't print-out SEL entry if ID not present
- ID: 296 - Fix PSD size decoding
- ID: 293 - Use of uninitialized variable in ipmi_main()
- ID: 278 - Error in sol looptest
- ID: 290 - ipmi_sol.c needs a clean-up
- ID: 85 - Supermicro memory ECC error display
- ID: 290 - ipmi_sol.c needs a clean-up
- ID: 286 - Open session retries hit assert in ipmi_lanplus_send_payload
- ID: 285 - Fix SEGV in ipmi_lanplus_open_session
- ID: 284 - Fix SEGV in ipmi_main
- ID: 283 - ipmi_intf_socket_connect fails with IPv4 hosts
- ID: 46 -  ipmi_fwum needs some re-work
- ID: 50 - ipmi_hpmfwupg needs a clean up
- ID: 279 - ipmitool sdr list broken
- ID: 44 - dummy interface support - fake-ipmistack project
- ID: 48 - Remove hard-coded FRU inventory access length restriction
- ID: 276 - HPM.1 upgrade combined patch
- ID: 90 - Add options to chassis bootparam set bootflag
- ID: 292 -Properly handle plugin non-zero target adddress with -t
- Numerous Fixes based on running Coverity
- Use TIOCFLUSH if TCFLSH is missing to get the serial plugin building on
  Hurd.
- Disable imb and open plugins by default on Hurd.  The platform lack
  the required kernel support.
- Change serial plugin to only try to disable the IUCLC serial line flag on
  platforms supporting it.  Fixes build problem on Hurd and FreeBSD.
- PA: 83 -  Revised IPv6 patch
- FR: 24 -  Exchange OS Name Hostname BMC URL during startup
- ID: 304 - Incorect byteswap in SOL maximum payload
- ID: 303 - Fix build error in HPM.2 code
- ID: 300 - new sunoem functionality
- ID: 144 - Fix 'dcmi power set_limit action <value>'
- ID: 302 - HPM.2 long message support
- ID: 309 - Add new SEL entries for ipmi 2.0 rev 1.1
- ID: 280 - man page cleanup
- ID: 311 - man page update for new sunoem commands

* Mon Sep 9 2013 <gilles.buloz@kontron.com>  1.8.13-1
- ID: 3611905 - Direct Serial Basic/Terminal Mode Interface drivers
- ID: 3577766 - configure's knobs and switches don't work
- ID: 3611253 - do not override OS-default values for interfaces
- ID: 65 - Fixes for configure.in for cross compilation
- ID: 3571153 - OpenIPMI/ipmievd fails to compile on Solaris
- numerous ipmitool man page updates
- ID: 3611226 - Bridging support for PICMG Platforms
- Add support for getsysinfo/setsysinfo commands to ipmi mc
- Cleanup Dell OEM code to use new sysinfo interface
- ID: 93 - str-to-int conversion is weak
- ID: 3582307 - ipmi_fru - ipmi_fru_main() return codes
- ID: 3582310 - ipmi_fru - ipmi_fru_main() - misuse of printf()
- ID: 3576213 - ipmi_fru - unused variable
- ID: 3578276 - ipmi_fru - free() on freed memory possible
- ID: 3578275 - ipmi_fru - memory leaks
- ID: 3528271 - ipmi_fru - possible *flow via FRUID
- ID: 3578277 - ipmi_fru - possible NULL pointer
- ID: 3612372 - Recognize Broadcom IANA number and BCM5725 product
- ID: 3608758 - add IPMI_NETFN_OEM
- ID: 143 - Reversed 'channel authcap' capabilities
  Fixes reversed IPMIv1.5/2.0 'channel authcap' capabilities
- ID: 3587318 - "dcmi discover" is not DCMI 1.5 compatible
- ID: 3608757 - ipmi_fru - various fixes
- ID: 3598203 - 'mc getsysinfo|setsysinfo' needs a bit of re-work
- ID: 3597782 - ipmi_mc - sysinfo_param() has two consecutive returns
- ID: 3597781 - 'mc getsysinfo|setsysinfo' help has typos
- ID: 3608763 - ipmi_sdr - code cleanup & output display cleanup
- ID: 3610286 - ipmi_sdr - ipmi_sdr_print_type - incorrect eval
- ID: 3600930 - ipmi_sdr - code cleanup
- ID: 3602439 - ipmi_sdr - memory leaks
- ID: 3595199 - ipmi_sdr - Add support for 'ipmitool sdr <list|elist> help'
- ID: 3592773 - 'ipmitool sdr info'; prints incorrect info
- ID: 3592770 - 'ipmitool sdr list|elist INV_INPUT' return code
- ID: 3577159 - ipmi_sdr - uint32_t cast to uint8_t and back
- ID: 3528368 - ipmi_sdr - possible int *flow
- ID: 226 - ipmi_sdradd - typo
- ID: 258 - ipmi_sdradd - error printed on STDOUT
- Fixed ipmievd start under systemd.
- ID: 3608760 - Add bswap.h to ipmi_chassis.c and ipmi_pef.c
- ID: 3564701 - ipmitool 1.8.12 doesn't build on big endian architectures
- ID: 3600907 - defined value for "Chassis may not support Force Identify"
- ID: 256 - ipmitool could crash when IPv6 address is returned
- ID: 211 - 'lib/ipmi_dcmi.c' - typo & error printed on STDOUT
- ID: 3612237 - If DCMI command fails, incorrect completion code is printed
- ID: 3608149 - ipmitool - set pointer to NULL after free()
- ID: 3603419 - DCMI - waste of resources
- ID: 3600908 - DMCI - crash in ipmi_print_sensor_info(), NULL ref
- ID: 3609985 - delloem : Wrong MAC returned when flex addressing is enabled
- ID: 113 - delloem exec file won't handle more than one command
- ID: 28 - delloem - clean up the code
- ID: 3608261 - delloem - code formatting
- ID: 3528247 - delloem - fix possible *int flows
- ID: 3600910 - delloem - code cleanup
- ID: 3576211 - delloem - unused variable
- ID: 3578022 - delloem - fix typos
- ID: 263 - ipmi_ek* - cleanup
- ID: 3308765 - ipmi_ek* - cleanup
- ID: 3586228 - ipmi_ek* - ipmi_ekanalyzer_usage() rework
- ID: 3528388 - ipmi_ek* - a typo in error message
- ID: 3576212 - ipmi_event - better rsp handling
- ID: 3607393 - ipmi_event - redundant '\n' in error message
- ID: 153 - ipmi_firewall - printf() used instead of lprintf()
- ID: 3608003 - ipmi_fru - atol() should be replaced with str2*()
- ID: 3600911 - ipmi_fru - fix multiple increments in args to printf
- ID: 3600914 - no more crash on no response. allow more send/recv loops of waiting.
- ID: 70 - Fixes and updates for ipmitool hpm
- ID: 3528308 - ipmi_hpmfwupg - possible int *flow
- ID: 3608762 - ipmi_hpmfwup - Fixed help messages for hpm command
- ID: 3607981 - ipmi_lanp - replace atoi() calls
- ID: 3607320 - ipmi_lanp - possible NULL reference
- ID: 3600926 - ipmi_lanp - code cleanup
- ID: 3613575 - memory leak - ipmi_password_file_read()
- ID: 3522740 - reading password from file is limited to 16byte passwords
- ID: 3613605 - ipmi_main - call free() on pointer to static data
- ID: 3608761 - ipmi_main - PICMG Get Device Locator was never run
- ID: 3577155 - ipmi_main' - memory leaks
- ID: 239 - typo in 'mc selftest', add details
- ID: 3597471 - ipmi_mc - needs a bit of re-work - rc, inv. options
- ID: 3597468 - ipmi_mc - print_mc_usage() prints to STDOUT
- ID: 3597469 - 'mc watchdog off' prints on STDERR, should be STDOUT
- ID: 3597470 - 'mc watchdog reset' prints on STDERR, should be STDOUT
- ID: 3611254 - OEM handle for Intel 82751 in SPT mode
- ID: 3600927 - change eval order of input param in ipmi_oem_setup()
- ID: 3600928 - ipmi_pef - code cleanup
- ID: 3592732 - ipmi_picmg.c - printf() misuse
- ID: 3528310 - ipmi_picmg.c - NULL reference
- ID: 3528347 - ipmi_raw.c - possible int *flow
- ID: 3587913 - Command % ipmitool raw help; returns 1
- Added code to support sensors on other luns (On behalf of Kontron Germany)
- ID: 3611912 - Add missing newlines when cvs output is specified
- ID: 244 - ipmi_sel - "0.0" displayed for unspecified threshold values
- ID: 3612371 - Typo in impi_sel debug output
- ID: 3016359 - ipmi_sel - Get SEL Alloc Information is incorrect
- ID: 3568976 - 'sel set time' behaviour is inconsistent
- ID: 3528371 - ipmi_sensor - possible int *flow
- ID: 3601265 - 'ipmitool sensor get' leaks memory
- ID: 3601106 - 'ipmitool sensor get NACname' output incorrect/inconsistent
- ID: 3608007 - ipmi_session - typo in error message
- ID: 101 - ipmi_sol - possible int *flow
- ID: 3600933 - ipmi_sol - use of deprecated bzero()
- ID: 3609472 - ipmi_sol - Add the instance to the SOL commands
- ID: 3588726 - 'ipmitool sol payload status ...;'segfaults on no rsp
- ID: 3522731 - ipmi_sol - ipmi_get_sol_info() returns always 0
- ID: 3613042 - add missing Entity IDs
- ID: 3611306 - ipmi_tsol - fix always fail in case of error
- ID: 259 - ipmi_user - memory leak
- ID: 260 - ipmi_user - replace atoi() call
- ID: 2871903 - ipmitool user priv incorrectly sets Link Auth
- ID: 3600960 - check the copy of password exists
- ID: 3609473 - Add assertion/deassertion to threshold events
- ID: 104 - ipmishell - possible int *flow
- ID: 262 - 'set' segfaults when no IPMI inf present
- ID: 257 ipmitool exec segfaults if invalid input given
- ID: 254 - Fix retry of authentication capabilities retrieval
- ID: 3611303 - lan - error check is missing braces
- ID: 253 - Fix lanplus retransmission
- ID: 212 - 'lib/ipmi_dcmi.c' - possible int *flow
- ID: 264 - incorrect array index in get_lan_param_select()
- ID: 269 - Fixes for configure.in for cross compilation
- ID: 267 - Corruption in "lan alert print" output
- ID: 41 - ipmi_sel_interpret() - clean up formatting, indentation
- ID: 242 - Incorrect DCMI Power Reading "IPMI timestamp" interpretation
- ID: 229 - 'lib/ipmi_ekanalyzer.c' - a typo ``Too few argument!''
- ID: 266 - file descriptor leak in ipmi_fwum and ipmi_ekanalyzer
- ID: 99 - 'lib/ipmi_sel.c' - possible int *flow
- ID: 222 - 'lib/ipmi_sdr.c' - a typo 'Not Reading' -> 'No Reading'
- ID: 35 - Script to setup redirection of SNMP to/from BMC
- ID: 273 - Reduce SOL Input buffer size by SOL header size


* Thu Aug 9 2012 <gilles.buloz@kontron.com>  1.8.12-1
- Added IPMB dual bridge support (no need for driver support)
- Enable compiler warnings and resolve all compiler warning so that
  ipmitool compiles and links with no warning or error messages
- add ipmishell line to configure
- fail configure when no curses or readline is found
- support sensor bridging in free interface
- applied fix for issue #2865160 (AIX build)
- Document the ipmitool dcmi commands in the ipmitool man page
- Document that some commands are blocked by OpenIPMI.   ID 2962306
- Document the -N and -R options per tracker ID 3489643
- fix manpage misdocumentation on cipher suite privilige configuration
- Add build support for Dell OEM commands
- Add new Dell OEM commands and update man page
- added hpm and fwum in man page
- man page update for fwum and hpm commands
- Added documentation for 'ime' operating mode, used to update Intel ME.
- add new -Y option to prompt user to enter kgkey
- Add DCMI module (Data Center Management Interface)
- fixed oem/iana data type to allow 24 bits definition
- Fixed AMC point-to-point record parsing in FRU
- Fixed detection of packing support in GCC
- Added packing support detection magic on all packed structures
  in project
- Dell specific mac sub command is updated to support the latest 12G
  Dell servers.  Support for virtual mac is also implemented.
- Use consistent netfn/cmd for getsysinfo command
- Add Dell OEM network commands
- Resolve incorect Board Mfg Data due to incorrect date constant
- Update ipmi_fru.h to SMBIOS spec 2.6.1 - ID 2916398
- Support for analog readings in discrete sensors on HP platforms.
- Change device id mask (IPM_DEV_DEVICE_ID_REV_MASK) 0x07 for 0x0F.
  As per in IPMI spec V2:
- Added PICMG clock e-keying and bused resource control identifiers
- Added PICMG major version (ATCA/AMC/uTCA) identifiers
- Correct Threshold/Discrete Sensor Display - Patch Tracker ID 3508759
- Sensor units now handle percentage units - ID 3014014
- Fixes ID 3421347 Sensor list command should use channel field from SDR
- Added packing directive for ARM cross compile with GCC 3.4.5,
  otherwise the sdr structures gets padded and the pointer cast
  result in incorrect alignement
- Added 'sdr fill sensors nosats' support to speed up SDR discovery
- Added SDR name display during discovery (with -v)
- Added support for sensor types - Processor related sensor
  type 0x07, system incharectorization 0x20, Memory sensor type.
- Give more description for SEL which is generated for Uncorrectable
  ECC and errors with respect to each Memory Bank,Card or DIMM.
  The Sensor type supporting this are 0x0C and 0x10.
- Add more details about Version Change event (source of
  firmware update)
- enhanced PICMG fru control
- Integrated Andy Wray's DDR3 SPD parser patch
- Adds function str2uint() to convert from string to uint32_t with
  checks for valid input.
- Fix possible buffer overflow in buf2str()
- Fixes ID 3485004 - misuse of strtol()
- Replaces calls to strtol() with str2uchar() calls and adds error
  messages if invalid input is given.
- Don't overwite the iflags bits prior to setting the boot parameters.
  This fixes ipmitool so that
  chassis bootdev bios clear-cmos=yes
  will correctly clear the bios cmos.
- Clarify DCMI get limit activation (add if activate or not).
- Bug fixes for delloem lan command. This includes the support for 12G
  Dell license and 12G LAN Specific command.
- delloem commands should not be executed before parsing command line.
- Fix stack overflow in delloem setled
- Fix delloem powermonitor on big-endian platforms.
- ipmitool delloem powermonitor command should convert data from
  network-format to the native one, otherwise it shows garbage
  on ppc/ppc64 platform.
- Add ipmi_getsysinfo command
- Add support for drive backplane SetLED functionality
- Fix for Platform Event Message incorrect Generator ID
- Fix fru print so that it will display FRU info from satellite
  controllers.
- Add support for AMC type 17h record.
- Fix in fru edit.   It is now possible to edit field 0 of sections
- New FRU get OEM record command
- fixed segfault for fru edit when "field id" is not supported and
  added user feedback for string substitution(success or failure)
- Improvement to hpm upgrade during activation. This resolves issue
  where activation seems to have failed because ipmitool received
  an unsupported completion code.
- hpm Fixes for multi-platform support.
- hpm Fix for timeouts during firmware rollback. If completion code
  is C3, wait till timeout has expired before reporting it.
- hpm During manual rollback, code now gets target capabilities
  instead of using a default timeout of 60 seconds.
- Added firmware auxilliary bytes to hpm outputs
- hpm Add support for BIG Buffer (Use when -z option is used)
- Fix the case where ipmitool loses the iol connection during the upload
  block process.  Once IPMITool was successfully sent the first
  byte, IPMITool will not resize the block size.
- Fix the problem when we try to upgrade specific component and the
  component is already updated,
- updated HPM firmware agent to version 1.04
- Fix exit code to return zero on '-o list' or '-o help' option
- limit length of user name and password that can be supplied by user.
  Password is limited to 16 bytes, resp. 20 bytes, for LAN, resp.
  LAN+, interface. User name is limited to 16 bytes, no interface
  limitations.  ID 3184687, ID 3001519
- Add retry / timeout options for LAN
- Changed default cipher suite to 1 instead of 3 for iol20
- added fix for tracker ID 2849300 "Incorrect Firmware Revision"
- avoid reopening the interface when already opened
- Remove message for unsupported PEF capabilities that return valid
  CC (80h)
- Added OEM byte (47) to verbose output
- Add option to provide a list when filling sdr repository
- SDR discovery speedups
- Added support for Dell specific sensors
- Fix segmentation fault on unrecognize OEM events.
- changed SEL timestamp formatting for 'preinit' SEL entries, allowing
  the number of seconds to be displayed.
- Added sensor raw data in verbose mode. Useful for OEM sensor type.
- Add sensor hysteresis (positive & negative) to the following command
  ipmitool sensor -v
- Fixes bug ID 3484936 - missing user input validation
- Add missing RMCP+ auth type strings
- Add new Kontron Product in ipmi_strings for product ID.  Kontron
  KTC5520/EATX Server Motherboard with integrated iBMC/KVM/VM
  added identification support for Kontron AT8050 ATCA board
- Constrain setting of the username to no greater than 16 characters
  per the IPMI specification.   ID 3001519
- Constrain User ID between 1 and 63.  ID 3519225
- Fixes ID 3485340 - user input not handled in 'lib/ipmi_user.c'
- Fixes ignorance of existing daemon PID file which results in PID being
  overwritten.  Adds proper umask() before writing PID file.
- applied fix for ID 2865111 (AIX build)
- Fix a proplem when using bridged IPMI commands on the lanplus
  interface (-I lanplus with -b -t or -m switches)  resulting in
  "Close Session command failure".
- Add fix with usage of CFh (duplicate request).  Usefull for
  slow commands
- Fix issue with sequence number. (Speed up transfer)

* Wed Feb 25 2009 <pere@hungry.com>  1.8.11-1
- Fix new GCC compilation issues in regards to Packing
- Fix Tracker bug #1642710 - ipmi_kcs_drv being loaded/unloaded
  for 2.4 kernel instead of ipmi_si_drv driver module
- New -y option added to allow specification of kg keys with
  non-printable characters
- New -K option added to allow kgkey settings via environmental
  variable IPMI_KGKEY
- Generic device support added for EEPROM with SDR Type 10h (gendev)
- Fix to lan-bridging for a double-bridging crash and to fix
  an issue with bridging multiple concurrent requests and
  erroneous handling of raw Send Message
- Lanplus fix for commands like 'sensor list' without the -t option
  causing wrong double bridged requests of a sensor is located
  on another satellite controller
- Fix lan and lanplus request list entry removal bugs
- Fix non-working issue when trying to send a bridge message with
  Cipher 3
- Change bridge message handling to reuse command ipmi_lan_poll_recv
- Added PICMG 2.0 and 2.3 support
- Fix PICMG (ATCA) extension verification and reversal of BCD encoded
  values for "major" and "minor" fields
- Add IANA support for Pigeon Point
- Add OEM SW/FW Record identification
- Fix to include I2C and LUN addresses so sensors are correctly managed
- Patch ID 1990560 to get readings from non-linear analog sensors
- Add support for SOL payload status command
- SOL set parameter range checking added
- Fixed SOL activate options usage 
- Fixed crashes when parsing 'sol payload' and 'tsol' cmds (#216967)
- Added retries to SOL keepalive
- Fixed wrong mask values for Front Panel disable/enable status
- Add support to access fru internal use area
- Add support for new PICMG 3.0 R3.0 (March 24, 2008) to allow
  blocks of data within the FRU storage area to be write protected.
- Fix node reporting in GUID; Tracker bug #2339675
- Fix watchdog use/action print strings
- Fix endian bug in SDR add from file; Tracker bug #2075258
- Fix crash when dumping SDRs in a file and there's an error
  getting an SDR; improve algorithm for optimal packet size
- Fix occasional SDR dump segfault; #1793076
- Allow ipmitool sel delete to accept hex list entry numbers
- Fix SEL total space reporting.
- Fix for garbage sensor threshold values reported when none 
  returned.  Tracker Bug #863748
- ipmievd change to Monitor %used in SEL buffer and log warnings when
  the buffer is 80% and 100% full

* Fri Aug 08 2008 <pere@hungry.com>  1.8.10-1
 - Added support for BULL IANA number.
 - Fixed contrib build so the oem_ibm_sel_map file gets included in rpm 
   builds again.
 - Added support for Debian packages to be built from CVS
 - Fix for sdr and sel timestamp reporting issues
 - Fix for discrete sensor state print routines to address state bits 8-14
 - Change ipmi_chassis_status() to non-static so it can be used externally
 - Added retries to SOL keepalive
 - Fix to stop sensor list command from reporting a failure due to missing 
   sensor
 - Fix bug in sdr free space reporting
 - Add support for IANA number to vendor name conversion for many vendors
 - Fix segfault bug in lan set command
 - Fix bug in population of raw i2c wdata buffer
 - Fix bug in ipmb sensor reading
 - Fix misspellings, typos, incorrect strncmp lengths, white space
 - Update/fix printed help and usages for many commands
 - Add and update support for all commands in ipmitool man page
 - Fix for lanplus session re-open when the target becomes unavailable following
   a fw upgrade activation
 - Add support for watchdog timer shutoff, reset, and get info
 - Add support for more ibm systems in oem_ibm_sel_map
 - Add more JEDEC support info for DIMMs; decrease request size for DIMM FRU
   info to 16 bytes at a time to allow more DIMM FRUs to respond.
 - Fix to change hpmfwupg to version 1.02; fix to reduce hpmfwupg buffer 
   length more aggressively when no response from iol
 - Fix HPM firmware activation via IOL; fake a timeout after IOL session 
   re-open to force get upgrade status retry; Added retries on 0xD3 
   completion code
 - Add support for freeipmi 0.6.0; adjust autoconf for changes
 - Fix for oemval2str size
 - Add support for product name resolution in mc info
 - Fix FRU display format
 - Added PICMG ekeying analyzer module support (ekanalyzer); display point
   to point physical connectivity and power supply information between 
   carriers and AMC modules; display matched results of ekeying match 
   between an on-carrier device and AMC module or between 2 AMC modules
 - Fix AMC GUID display support
 - Improved amcportstate operations
 - Added resolution for new sensor types
 - Fix segfault in SOL
 - Fix bug that caused infinite loop on BMCs with empty SDRs
 - Fix to move out Kontron OEM sensor resolution for other OEMs which could 
   lead to bad event descriptions
 - Add new FRU edit mode thereby allowing serial numbers, etc. to be changed;
    improvements to OEM edit mode
 - Added SPD support for parms: channel number, max read size
 - Add SDR support for adding SDR records from a dumped file, clearing SDR, 
   adding partial SDR records
 - Add updates and fixes to hpmfwupg: upload block size to 32 bytes for KCS,
   handle long response option, implement rollback override, garbage output fix
 - Add double bridge lan support , fix bridging issue
 - Add HPM support to pre-check which components need to be skipped
 - Fix autodetection of maximum packet size when using IPMB
 - Add new Kontron OEM command to set the BIOS boot option sequence
 - Add support for dual-bridge/ dual send message
 - Add auto-detect for local IPMB address using PICMG 2.X extension
 - Add support for HPM.1 1.0 specification compliance
 - Fix for improper lan/lanplus addressing
 - Added transit_channel and transit_addr to ipmi_intf struct
 - Fix bad password assertion bug due to rakp2 HMAC not being checked properly
 - Added ability to interpret PPS shelf manager clia sel dump
 - Corrected PICMG M7 state event definition macros
 - Added FRU parsing enhancements
 - Added "isol info", "isol set" and "isol activate" commands to support 
   Intel IPMI v1.5 SOL functionality. Removed "isol setup" command.
 - Fix bug in ipmi_lan_recv_packet() in lan and lanplus interfaces.
 - Fix bug in "chassis poh" command.
 - Fix HPM.1 upgrade to apply to only given component when instructed to do so
 - Added configure auto-detection if dual bridge extension is supported 
   by OpenIPMI

* Tue Mar  6 2007 <pere@hungry.com>  1.8.9-1
 - Added initial AMC ekey query operation support
 - Improvements to ekeying support (PICMG 3.x only)
 - Added initial interactive edition support for multirec; added IANA
   verification before interpreting PICMG records.
 - Added edit support for AMC activation "Maximum Internal Current"
 - Fix bug generating garbage on the screen when handling GetDeviceId
   and sol traffic occurs
 - Added ability to map OEM sensor types to OEM description string using 
   IANA number; moved IANA number table
 - Fix lan set access command to use value already saved within parameters 
   for PEF and authentication
 - Fix bug in cmd ipmitool lan stats get 1
 - Add support to allow ipmitool/ipmievd to target specific device nodes 
   on multi-BMC systems
 - Add support for name+privilege lookup for lanplus sessions
 - Fix time_t conversion bug for 64-bit OS
 - Added prefix of hostname on sel ipmievd sessions
 - Fixed FWUM Get Info
 - Fix ipmievd fd closing bug
 - Add set-in-progress flag support to chassis bootdev
 - Added new chassis bootdev options
 - Add sol payload enable/disable comman
 - Fix SOL set errors when commit-write not supported
 - Fix reset of session timeout for lanplus interface
 - Fixed lan interface accessibility timeout handling
 - Fix bug with Function Get Channel Cipher Suites command when more 
   than 1 page used.
 - Fix missing firmware firewall top-level command
 - Fix bug in SOL keepalive functionality
 - Fix SOLv2 NACK and retry handling for Intel ESB2 BMC
 - Added ipmi_sel_get_oem_sensor* APIs
 - Added HPM.1 support 
 - Fix segfault when incorrect oem option supplied
 - Fix bus problem with spd command
 - Fix segfault in SOL when remote BMC does not return packet
 - Adjust packet length for AMC.0 retricting IPMB packets to 32 bytes
 - Added lan packet size reduction mechanism
 - Fix bug with sendMessage of bad length with different target
 - Fix for big endian (PPC) architecture
 - NetBSD fixes
 - Fix segfault and channel problem with user priv command
 - Add support for bus/chan on i2c raw command
 - Add freeipmi interface support
 - Add remote spd printing
 - Add better detection of linux/compiler.h to config
 - Makefile changes to fix makedistcheck, etc. 

* Tue May 02 2006 <duncan@iceblink.org>  1.8.8-1
 - Fix segfaults in sensor data repository list
 - Fix ipmievd to open interface before daemonizing
 - Fix IPMIv1.5 authtype NONE to ignore supplied password
 - Fix cipher suite display bug in lan print
 - Fix typo in IPMIv2 SOL output when sending break
 - Fix improper LUN handling with Tyan SOL
 - Add LUN support to OpenIPMI interface
 - Add support for Kontron OEM commands
 - Update to Kontron Firmware Update command

* Sun Mar 19 2006 <duncan@iceblink.org>  1.8.7-1
 - Add Sun OEM command for blades
 - Increase argument size for raw commands in shell/exec
 - Fix handling of LUNs for LAN interfaces
 - Add IPMIv2 SOL loopback test
 - Add support for IBM OEM SEL messages
 - Disable file paranoia checks on read files by default
 - Support IPMIv2 SOL on older Intel boxes
 - Display message and exit if keepalive fails during SOL
 - Add support for setting VLAN id and priority
 - Add support for FreeBSD OpenIPMI-compatible driver
 - Add support for IPMIv2 Firmware Firewall
 - Fix gcc4 compile warnings
 - Make ipmievd generate pidfile
 - Add initscripts for ipmievd

* Tue Jan 17 2006 <duncan@iceblink.org>  1.8.6-1
 - Fix memory corruption when sending encrypted SOL traffic
 - Add keepalive timer to IPMIv2 SOL sessions

* Sat Jan 14 2006 <duncan@iceblink.org>  1.8.5-1
 - Raise privilege level after creating IPMIv2 session
 - Add support for settable SOL escape character with -e option
 - Add support for Kg BMC key for IPMIv2 authentication with -k option
 - Add support for Tyan IPMIv1.5 SOL with tsol command
 - Add support for PICMG devices
 - Add support for OEM SEL event parsing
 - Add support for command bridging over lan and lanplus interfaces
 - New 'chassis selftest' command
 - Many bufxies and patches from contributors

* Wed May 18 2005 <duncan@iceblink.org>  1.8.2-1
 - Fix FRU reading for large (>255 bytes) areas.
 - Overhaul to ipmievd to support SEL polling in addition to OpenIPMI.
 - Fix LAN parameter segfault when no Ciphers supported by BMC.
 - Fix IPMIv2 support on Intel v2 BMCs (use -o intelplus).
 - Separate option parsing code from main ipmitool source file.
 - Add raw I2C support with IPMI Master Read-Write command.
 - Add support for new 'sdr elist' extended output format.
 - Add support for listing sensors by type with 'sdr type' command.
 - Add support for new 'sel elist' extended output format that
   cross-references events with sensors.
 - Add support for sending dynamically generated platform events
   based on existing sensor information.
 - New '-S' argument to read local SDR cache created with 'sdr dump'.
 - Updated manpage for ipmitool and ipmievd.

* Wed Apr 06 2005 <duncan@iceblink.org>  1.8.1-1
 - Install ipmievd into /usr/sbin

* Wed Mar 16 2005 <duncan@iceblink.org>  1.8.0-1
 - Fix IPMIv2.0 issues
 - Fix chassis boot parameter support
 - Add support for linear sensors
 - Update bmc plugin to work with new Solaris bmc driver (new ioctl
   for interface detection and new STREAMS message-based interface)

* Tue Jan 18 2005 <duncan@iceblink.org>  1.7.0-1
 - Propogate errors correctly so exit status will be useful
 - More consistent display of errors including completion code text
 - Errors and debug is send to stderr now
 - New "sel get" command that will print details about SEL entry
   and corresponding SDR records as well as FRUs via entity association
 - Improved event generator, now supports reading events from text file
 - New "-o oemtype" option for specifying OEM boards
   exsting types are "supermicro" and "intelwv2"
 - New PEF subsystem from Tim Murphy at Dell
 - New "bmc" plugin for Solaris 10 x86
 - Many bugfixes and contributed patches
 - Support for Supermicro BMC OEM authentication method
 - Fix minor problem with LAN parameter setting

* Wed Aug 18 2004 <duncan@iceblink.org>  1.6.0-1
 - Add a README
 - Add support for IPMIv2 and Serial-over-LAN from Newisys
 - Add Solaris x86 lipmi interface
 - Add support for building Solaris packages
 - Add support for building RPMs as non-root user
 - Fix segfault when doing "sel list" (from Matthew Braithwaite)
 - Fix "chassis identify" on some BMCs (from ebrower@sourceforge)
 - Add "bmc info" and related output (from ebrower@sourceforge)
 - new "shell" and "exec" commands
 - lots of other contributed patches

* Thu May 27 2004 <duncan@iceblink.org>  1.5.9-1
 - Add ability to get a particular sensor by name
 - Add ability to set a particular sensor threshold
 - Add support for displaying V2 channel authentication levels
 - Add README for rrdtool scripts in contrib directory
 - Improve lan interface retry handling
 - Support prompting for password or reading from environment
 - Move chaninfo command into channel subcommand
 - Fix reservation ID handling when two sessions open to BMC
 - Fix reading of large FRU data
 - Add configure option for changing binary to ipmiadm for Solaris
 - Fix compile problem on Solaris 8

* Tue Jan 27 2004 <duncan@iceblink.org>  1.5.8-1
 - Enable static compilation of interfaces
 - Fix types to be 64-bit safe
 - Fix compilation problems on Solaris
 - Fix multiple big-endian problems for Solaris/SPARC
 - Fix channel access to save settings to NVRAM
 - Set channel privilege limit to ADMIN during "access on"
 - Enable gratuitous ARP in bmcautoconf.sh
 - Add support for Linux kernel panic messages in SEL output
 - Add support for type 3 SDR records

* Mon Jan  5 2004 <duncan@iceblink.org>  1.5.7-1
 - add IPMIv1.5 eratta fixes
 - additions to FRU printing and FRU multirecords
 - better handling of SDR printing
 - contrib scripts for creating rrdtool graphs

* Thu Dec  4 2003 <duncan@iceblink.org>  1.5.6-1
 - Fix SEL event decoding for generic events
 - Handle empty SEL gracefully when doing "sel list"
 - Fix sdr handling of sensors that do not return a reading
 - Fix for CSV display of sensor readings/units from Fredrik Öhrn

* Tue Nov 25 2003 <duncan@iceblink.org>  1.5.5-1
 - Add -U option for setting LAN username
 - Fix -v usage for plugin interfaces

* Fri Nov 14 2003 <duncan@iceblink.org>  1.5.4-1
 - pull interface plugin api into library
 - fix ipmievd

* Fri Oct 31 2003 <duncan@iceblink.org>  1.5.3-1
 - add -g optin for pedantic ipmi-over-lan communication

* Fri Oct 24 2003 <duncan@iceblink.org>  1.5.2-1
 - add gratuitous arp interval setting

* Wed Oct  8 2003 <duncan@iceblink.org>  1.5.1-1
 - better SEL support
 - fix display bug in SDR list

* Fri Sep  5 2003 <duncan@iceblink.org>  1.5.0-1
 - use automake/autoconf/libtool
 - dynamic loading interface plugins

* Wed May 28 2003 <duncan@iceblink.org>  1.4.0-1
 - make UDP packet handling more robust
 - fix imb driver support

* Thu May 22 2003 <duncan@iceblink.org>  1.3-1
 - update manpage
 - rework of low-level network handling
 - add basic imb driver support

* Wed Apr  2 2003 <duncan@iceblink.org>  1.2-1
 - change command line option parsing
 - support for more chassis commands

* Tue Apr  1 2003 <duncan@iceblink.org>  1.1-1
 - minor fixes.

* Sun Mar 30 2003 <duncan@iceblink.org>  1.0-1
 - Initial release.

