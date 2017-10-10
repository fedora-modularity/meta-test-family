% tools (1) Container Image Pages
% Tomas Tomecek
% September 11th, 2017

# NAME
tools - container with all the management tools you miss in Atomic Host 


# DESCRIPTION
You find plenty of well-known tools within this container. Here comes the full list:

| Package         | Summary                                                                                     | Executables                        |
| --------------- | ------------------------------------------------------------------------------------------- | ---------------------------------- |
| bash-completion | Programmable completion for Bash                                                            |                                    |
| bc              | GNU's bc (a numeric processing language) and dc (a calculator)                              | /usr/bin/bc                        |
|                 |                                                                                             | /usr/bin/dc                        |
| bind-utils      | Utilities for querying DNS name servers                                                     | /usr/bin/arpaname                  |
|                 |                                                                                             | /usr/bin/delv                      |
|                 |                                                                                             | /usr/bin/dig                       |
|                 |                                                                                             | /usr/bin/host                      |
|                 |                                                                                             | /usr/bin/nslookup                  |
|                 |                                                                                             | /usr/bin/nsupdate                  |
|                 |                                                                                             | /usr/sbin/ddns-confgen             |
|                 |                                                                                             | /usr/sbin/dnssec-checkds           |
|                 |                                                                                             | /usr/sbin/dnssec-coverage          |
|                 |                                                                                             | /usr/sbin/dnssec-dsfromkey         |
|                 |                                                                                             | /usr/sbin/dnssec-importkey         |
|                 |                                                                                             | /usr/sbin/dnssec-keyfromlabel      |
|                 |                                                                                             | /usr/sbin/dnssec-keygen            |
|                 |                                                                                             | /usr/sbin/dnssec-keymgr            |
|                 |                                                                                             | /usr/sbin/dnssec-revoke            |
|                 |                                                                                             | /usr/sbin/dnssec-settime           |
|                 |                                                                                             | /usr/sbin/dnssec-signzone          |
|                 |                                                                                             | /usr/sbin/dnssec-verify            |
|                 |                                                                                             | /usr/sbin/genrandom                |
|                 |                                                                                             | /usr/sbin/isc-hmac-fixup           |
|                 |                                                                                             | /usr/sbin/named-checkzone          |
|                 |                                                                                             | /usr/sbin/named-compilezone        |
|                 |                                                                                             | /usr/sbin/nsec3hash                |
|                 |                                                                                             | /usr/sbin/tsig-keygen              |
| blktrace        | Utilities for performing block layer IO tracing in the Linux kernel                         | /usr/bin/blkiomon                  |
|                 |                                                                                             | /usr/bin/blkparse                  |
|                 |                                                                                             | /usr/bin/blkrawverify              |
|                 |                                                                                             | /usr/bin/blktrace                  |
|                 |                                                                                             | /usr/bin/bno_plot.py               |
|                 |                                                                                             | /usr/bin/btrace                    |
|                 |                                                                                             | /usr/bin/btrecord                  |
|                 |                                                                                             | /usr/bin/btreplay                  |
|                 |                                                                                             | /usr/bin/btt                       |
|                 |                                                                                             | /usr/bin/verify_blkparse           |
| crash           | Kernel analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles | /usr/bin/crash                     |
| e2fsprogs       | Utilities for managing ext2, ext3, and ext4 filesystems                                     | /usr/bin/chattr                    |
|                 |                                                                                             | /usr/bin/lsattr                    |
|                 |                                                                                             | /usr/sbin/badblocks                |
|                 |                                                                                             | /usr/sbin/debugfs                  |
|                 |                                                                                             | /usr/sbin/dumpe2fs                 |
|                 |                                                                                             | /usr/sbin/e2freefrag               |
|                 |                                                                                             | /usr/sbin/e2fsck                   |
|                 |                                                                                             | /usr/sbin/e2image                  |
|                 |                                                                                             | /usr/sbin/e2label                  |
|                 |                                                                                             | /usr/sbin/e2undo                   |
|                 |                                                                                             | /usr/sbin/e4crypt                  |
|                 |                                                                                             | /usr/sbin/e4defrag                 |
|                 |                                                                                             | /usr/sbin/filefrag                 |
|                 |                                                                                             | /usr/sbin/fsck.ext2                |
|                 |                                                                                             | /usr/sbin/fsck.ext3                |
|                 |                                                                                             | /usr/sbin/fsck.ext4                |
|                 |                                                                                             | /usr/sbin/fuse2fs                  |
|                 |                                                                                             | /usr/sbin/logsave                  |
|                 |                                                                                             | /usr/sbin/mke2fs                   |
|                 |                                                                                             | /usr/sbin/mkfs.ext2                |
|                 |                                                                                             | /usr/sbin/mkfs.ext3                |
|                 |                                                                                             | /usr/sbin/mkfs.ext4                |
|                 |                                                                                             | /usr/sbin/mklost+found             |
|                 |                                                                                             | /usr/sbin/resize2fs                |
|                 |                                                                                             | /usr/sbin/tune2fs                  |
| ethtool         | Settings tool for Ethernet NICs                                                             | /usr/sbin/ethtool                  |
| file            | A utility for determining file types                                                        | /usr/bin/file                      |
| gcc             | Various compilers (C, C++, Objective-C, Java, ...)                                          | /usr/bin/c89                       |
|                 |                                                                                             | /usr/bin/c99                       |
|                 |                                                                                             | /usr/bin/cc                        |
|                 |                                                                                             | /usr/bin/gcc                       |
|                 |                                                                                             | /usr/bin/gcc-ar                    |
|                 |                                                                                             | /usr/bin/gcc-nm                    |
|                 |                                                                                             | /usr/bin/gcc-ranlib                |
|                 |                                                                                             | /usr/bin/gcov                      |
|                 |                                                                                             | /usr/bin/gcov-tool                 |
|                 |                                                                                             | /usr/bin/x86_64-redhat-linux-gcc   |
|                 |                                                                                             | /usr/bin/x86_64-redhat-linux-gcc-7 |
| gdb             | A stub package for GNU source-level debugger                                                | /usr/bin/gcore                     |
|                 |                                                                                             | /usr/bin/gdb                       |
|                 |                                                                                             | /usr/bin/gstack                    |
|                 |                                                                                             | /usr/bin/pstack                    |
| git-core        | Core package of git with minimal functionality                                              | /usr/bin/git                       |
|                 |                                                                                             | /usr/bin/git-receive-pack          |
|                 |                                                                                             | /usr/bin/git-shell                 |
|                 |                                                                                             | /usr/bin/git-upload-archive        |
|                 |                                                                                             | /usr/bin/git-upload-pack           |
| glibc-utils     | Development utilities from GNU C library                                                    | /usr/bin/memusage                  |
|                 |                                                                                             | /usr/bin/memusagestat              |
|                 |                                                                                             | /usr/bin/mtrace                    |
|                 |                                                                                             | /usr/bin/pcprofiledump             |
|                 |                                                                                             | /usr/bin/xtrace                    |
| gomtree         | Go CLI tool for mtree support                                                               | /usr/bin/gomtree                   |
| htop            | Interactive process viewer                                                                  | /usr/bin/htop                      |
| hwloc           | Portable Hardware Locality - portable abstraction of hierarchical architectures             | /usr/bin/hwloc-annotate            |
|                 |                                                                                             | /usr/bin/hwloc-assembler           |
|                 |                                                                                             | /usr/bin/hwloc-assembler-remote    |
|                 |                                                                                             | /usr/bin/hwloc-bind                |
|                 |                                                                                             | /usr/bin/hwloc-calc                |
|                 |                                                                                             | /usr/bin/hwloc-compress-dir        |
|                 |                                                                                             | /usr/bin/hwloc-diff                |
|                 |                                                                                             | /usr/bin/hwloc-distances           |
|                 |                                                                                             | /usr/bin/hwloc-distrib             |
|                 |                                                                                             | /usr/bin/hwloc-gather-topology     |
|                 |                                                                                             | /usr/bin/hwloc-info                |
|                 |                                                                                             | /usr/bin/hwloc-ls                  |
|                 |                                                                                             | /usr/bin/hwloc-patch               |
|                 |                                                                                             | /usr/bin/hwloc-ps                  |
|                 |                                                                                             | /usr/bin/lstopo-no-graphics        |
|                 |                                                                                             | /usr/sbin/hwloc-dump-hwdata        |
| iotop           | Top like utility for I/O                                                                    | /usr/sbin/iotop                    |
| iproute         | Advanced IP routing and network device configuration tools                                  | /usr/sbin/arpd                     |
|                 |                                                                                             | /usr/sbin/bridge                   |
|                 |                                                                                             | /usr/sbin/ctstat                   |
|                 |                                                                                             | /usr/sbin/devlink                  |
|                 |                                                                                             | /usr/sbin/genl                     |
|                 |                                                                                             | /usr/sbin/ifcfg                    |
|                 |                                                                                             | /usr/sbin/ifstat                   |
|                 |                                                                                             | /usr/sbin/ip                       |
|                 |                                                                                             | /usr/sbin/lnstat                   |
|                 |                                                                                             | /usr/sbin/nstat                    |
|                 |                                                                                             | /usr/sbin/routef                   |
|                 |                                                                                             | /usr/sbin/routel                   |
|                 |                                                                                             | /usr/sbin/rtacct                   |
|                 |                                                                                             | /usr/sbin/rtmon                    |
|                 |                                                                                             | /usr/sbin/rtpr                     |
|                 |                                                                                             | /usr/sbin/rtstat                   |
|                 |                                                                                             | /usr/sbin/ss                       |
|                 |                                                                                             | /usr/sbin/tipc                     |
| iputils         | Network monitoring tools including ping                                                     | /usr/bin/ping                      |
|                 |                                                                                             | /usr/bin/tracepath                 |
|                 |                                                                                             | /usr/sbin/arping                   |
|                 |                                                                                             | /usr/sbin/clockdiff                |
|                 |                                                                                             | /usr/sbin/ifenslave                |
|                 |                                                                                             | /usr/sbin/ping                     |
|                 |                                                                                             | /usr/sbin/ping6                    |
|                 |                                                                                             | /usr/sbin/rdisc                    |
|                 |                                                                                             | /usr/sbin/tracepath                |
|                 |                                                                                             | /usr/sbin/tracepath6               |
| less            | A text file browser similar to more, but better                                             | /usr/bin/less                      |
|                 |                                                                                             | /usr/bin/lessecho                  |
|                 |                                                                                             | /usr/bin/lesskey                   |
|                 |                                                                                             | /usr/bin/lesspipe.sh               |
| ltrace          | Tracks runtime library calls from dynamically linked executables                            | /usr/bin/ltrace                    |
| mailx           | Enhanced implementation of the mailx command                                                | /usr/bin/Mail                      |
|                 |                                                                                             | /usr/bin/nail                      |
| net-tools       | Basic networking tools                                                                      | /usr/bin/netstat                   |
|                 |                                                                                             | /usr/sbin/arp                      |
|                 |                                                                                             | /usr/sbin/ether-wake               |
|                 |                                                                                             | /usr/sbin/ifconfig                 |
|                 |                                                                                             | /usr/sbin/ipmaddr                  |
|                 |                                                                                             | /usr/sbin/iptunnel                 |
|                 |                                                                                             | /usr/sbin/mii-diag                 |
|                 |                                                                                             | /usr/sbin/mii-tool                 |
|                 |                                                                                             | /usr/sbin/nameif                   |
|                 |                                                                                             | /usr/sbin/plipconfig               |
|                 |                                                                                             | /usr/sbin/route                    |
|                 |                                                                                             | /usr/sbin/slattach                 |
| netsniff-ng     | Packet sniffing beast                                                                       | /usr/sbin/astraceroute             |
|                 |                                                                                             | /usr/sbin/bpfc                     |
|                 |                                                                                             | /usr/sbin/curvetun                 |
|                 |                                                                                             | /usr/sbin/flowtop                  |
|                 |                                                                                             | /usr/sbin/ifpps                    |
|                 |                                                                                             | /usr/sbin/mausezahn                |
|                 |                                                                                             | /usr/sbin/netsniff-ng              |
|                 |                                                                                             | /usr/sbin/trafgen                  |
| nmap-ncat       | Nmap's Netcat replacement                                                                   | /usr/bin/nc                        |
|                 |                                                                                             | /usr/bin/ncat                      |
| numactl         | Library for tuning for Non Uniform Memory Access machines                                   | /usr/bin/memhog                    |
|                 |                                                                                             | /usr/bin/migratepages              |
|                 |                                                                                             | /usr/bin/migspeed                  |
|                 |                                                                                             | /usr/bin/numactl                   |
|                 |                                                                                             | /usr/bin/numademo                  |
|                 |                                                                                             | /usr/bin/numastat                  |
| numactl-devel   | Development package for building Applications that use numa                                 |                                    |
| parted          | The GNU disk partition manipulation program                                                 |                                    |
| pciutils        | PCI bus related utilities                                                                   | /usr/sbin/update-pciids            |
| perf            | Performance monitoring for the Linux kernel                                                 | /usr/bin/perf                      |
| procps-ng       | System and process monitoring utilities                                                     | /usr/bin/free                      |
|                 |                                                                                             | /usr/bin/pgrep                     |
|                 |                                                                                             | /usr/bin/pidof                     |
|                 |                                                                                             | /usr/bin/pkill                     |
|                 |                                                                                             | /usr/bin/pmap                      |
|                 |                                                                                             | /usr/bin/ps                        |
|                 |                                                                                             | /usr/bin/pwdx                      |
|                 |                                                                                             | /usr/bin/skill                     |
|                 |                                                                                             | /usr/bin/slabtop                   |
|                 |                                                                                             | /usr/bin/snice                     |
|                 |                                                                                             | /usr/bin/tload                     |
|                 |                                                                                             | /usr/bin/top                       |
|                 |                                                                                             | /usr/bin/uptime                    |
|                 |                                                                                             | /usr/bin/vmstat                    |
|                 |                                                                                             | /usr/bin/w                         |
|                 |                                                                                             | /usr/bin/watch                     |
|                 |                                                                                             | /usr/sbin/pidof                    |
|                 |                                                                                             | /usr/sbin/sysctl                   |
| psmisc          | Utilities for managing processes on your system                                             | /usr/bin/killall                   |
|                 |                                                                                             | /usr/bin/peekfd                    |
|                 |                                                                                             | /usr/bin/prtstat                   |
|                 |                                                                                             | /usr/bin/pstree                    |
|                 |                                                                                             | /usr/bin/pstree.x11                |
|                 |                                                                                             | /usr/sbin/fuser                    |
| screen          | A screen manager that supports multiple logins on one terminal                              | /usr/bin/screen                    |
| sos             | A set of tools to gather troubleshooting information from a system                          | /usr/sbin/sosreport                |
| strace          | Tracks and displays system calls associated with a running process                          | /usr/bin/strace                    |
|                 |                                                                                             | /usr/bin/strace-log-merge          |
| sysstat         | Collection of performance monitoring tools for Linux                                        | /usr/bin/cifsiostat                |
|                 |                                                                                             | /usr/bin/iostat                    |
|                 |                                                                                             | /usr/bin/mpstat                    |
|                 |                                                                                             | /usr/bin/pidstat                   |
|                 |                                                                                             | /usr/bin/sadf                      |
|                 |                                                                                             | /usr/bin/sar                       |
|                 |                                                                                             | /usr/bin/tapestat                  |
| tcpdump         | A network traffic monitoring tool                                                           | /usr/sbin/tcpdump                  |
|                 |                                                                                             | /usr/sbin/tcpslice                 |
| tmux            | A terminal multiplexer                                                                      | /usr/bin/tmux                      |
| vim-enhanced    | A version of the VIM editor which includes recent enhancements                              | /usr/bin/rvim                      |
|                 |                                                                                             | /usr/bin/vim                       |
|                 |                                                                                             | /usr/bin/vimdiff                   |
|                 |                                                                                             | /usr/bin/vimtutor                  |
| xfsprogs        | Utilities for managing the XFS filesystem                                                   | /usr/sbin/fsck.xfs                 |
|                 |                                                                                             | /usr/sbin/mkfs.xfs                 |
|                 |                                                                                             | /usr/sbin/xfs_admin                |
|                 |                                                                                             | /usr/sbin/xfs_bmap                 |
|                 |                                                                                             | /usr/sbin/xfs_copy                 |
|                 |                                                                                             | /usr/sbin/xfs_db                   |
|                 |                                                                                             | /usr/sbin/xfs_estimate             |
|                 |                                                                                             | /usr/sbin/xfs_freeze               |
|                 |                                                                                             | /usr/sbin/xfs_fsr                  |
|                 |                                                                                             | /usr/sbin/xfs_growfs               |
|                 |                                                                                             | /usr/sbin/xfs_info                 |
|                 |                                                                                             | /usr/sbin/xfs_io                   |
|                 |                                                                                             | /usr/sbin/xfs_logprint             |
|                 |                                                                                             | /usr/sbin/xfs_mdrestore            |
|                 |                                                                                             | /usr/sbin/xfs_metadump             |
|                 |                                                                                             | /usr/sbin/xfs_mkfile               |
|                 |                                                                                             | /usr/sbin/xfs_ncheck               |
|                 |                                                                                             | /usr/sbin/xfs_quota                |
|                 |                                                                                             | /usr/sbin/xfs_repair               |
|                 |                                                                                             | /usr/sbin/xfs_rtcp                 |


# USAGE
You should invoke this container using `atomic` command:

```
$ atomic run f26/tools
```


# SECURITY IMPLICATIONS
This container runs as a super-privileged container: it has full root access.


# HISTORY
Release 1: initial release
