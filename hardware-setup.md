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

#### CPU Upgrade Options

After researching potential CPU upgrades for the T40, I've identified several compatible Xeon E-series processors that would provide significant performance improvements over the current E-2224G:

| Processor | Cores/Threads | Base Freq | Turbo Freq | TDP  | Cache | Key Benefit |
|-----------|---------------|-----------|------------|------|-------|-------------|
| E-2224G (current) | 4C/4T | 3.5 GHz | 4.7 GHz | 71W | 8MB | Current baseline |
| E-2278G   | 8C/16T | 3.4 GHz | 5.0 GHz | 80W | 16MB | Best balance of cores and TDP |
| E-2286G   | 6C/12T | 4.0 GHz | 4.9 GHz | 95W | 12MB | Highest base clock |
| E-2288G   | 8C/16T | 3.7 GHz | 5.0 GHz | 95W | 16MB | Maximum performance |

The E-2278G appears to be the optimal upgrade choice for several reasons:
- Doubles the core/thread count (8C/16T vs 4C/4T)
- Maintains a reasonable 80W TDP (only 9W higher than current)
- Provides 16MB cache (double the current amount)
- Supports higher turbo frequency for single-threaded workloads
- Offers substantial multi-threaded performance improvement for Kubernetes workloads

All these processors use the LGA1151 socket compatible with the T40 motherboard. Note that the motherboard's memory controller limits RAM to a maximum of 64GB (4×16GB), regardless of the CPU's theoretical support for higher capacities.

A BIOS update would be recommended before performing any CPU upgrade.

#### Other Future Considerations

- Possibility of adding more disks if storage needs grow beyond current capacity
- Evaluating power consumption and cooling requirements as the system scales
- Investigating data on the removed drives for potentially useful content
