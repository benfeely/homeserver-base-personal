# Personal Hardware Setup

## Dell PowerEdge T40 Server

This document outlines my specific hardware configuration and choices for implementing the homeserver-base project on my personal Dell PowerEdge T40 server.

### Hardware Specifications

- **Server Model**: Dell PowerEdge T40
- **CPU**: Intel Xeon E-2224G (stock, no upgrades at this time)
- **RAM**: Upgraded to 64GB from original 8GB
- **Storage**:
  - **Primary Disk**: Samsung 970 Pro NVMe (512GB) installed using a PCIe to NVMe adapter
  - **Data Storage**: 3 × 8TB Western Digital Red Pro disks configured in ZFS pool
  - **Disk Installation**: Purchased and installed additional disk carrier trays to accommodate the WD Red Pro drives

### Hardware Upgrades Notes

The RAM upgrade from 8GB to 64GB provides sufficient memory for running multiple Kubernetes workloads smoothly, while the storage configuration gives me both speed (NVMe for OS/system) and capacity (24TB raw storage in the WD Red Pro drives).

I considered a CPU upgrade but decided the existing Xeon E-2224G is adequate for my current needs. This can be revisited in the future if workloads demand more processing power.

The Samsung 970 Pro NVMe drive is connected via a PCIe adapter card since the T40 doesn't have a native M.2 slot on the motherboard. This provides much better performance than the standard SATA connections.

### ZFS Configuration

The three 8TB Western Digital Red Pro disks are configured as a ZFS pool in Proxmox, providing redundancy and data protection. See the [proxmox-zfs-guide.md](/docs/proxmox-zfs-guide.md) document for details on the ZFS configuration approach used.

### Hardware Changes (June 2025)

When setting up this server for the homeserver-base project, I made several changes to the original configuration:

- Removed 2 × 1TB drives and 1 × 8TB drive (shucked from an external USB 3.0 backup drive)
  - These drives are currently set aside but may contain useful data to investigate
- Installed the Samsung 970 Pro NVMe drive using a PCIe adapter card
- Added disk carrier trays to accommodate the new Western Digital Red Pro drives

### Future Considerations

- Potential CPU upgrade if workloads become more demanding
- Possibility of adding more disks if storage needs grow beyond current capacity
- Evaluating power consumption and cooling requirements as the system scales
- Investigating data on the removed drives for potentially useful content
