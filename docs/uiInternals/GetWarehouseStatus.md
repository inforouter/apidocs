---
search:
  exclude: true
---

# GetWarehouseStatus API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Returns warehouse storage status information including total document count, total warehouse size, per-warehouse path statistics, and disk drive information. This API is restricted to system administrators with the `ViewWarehouseStatus` permission.

## Endpoint

```
/api/UIInternals/GetWarehouseStatus
```

## Methods

- **GET** `/api/UIInternals/GetWarehouseStatus?authenticationTicket=...`
- **POST** `/api/UIInternals/GetWarehouseStatus` (form data)

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true" TotalWarehouseSize="5368709120" TotalDocumentCount="12450">
  <WarehousePaths>
    <WarehousePath WhNo="00" Path="C:\websites\example.com\WH\00" RootDrive="C:\" Size="1073741824" DocCount="2500" />
    <WarehousePath WhNo="01" Path="C:\websites\example.com\WH\01" RootDrive="C:\" Size="536870912" DocCount="1200" />
    <WarehousePath WhNo="02" Path="D:\warehouse\WH\02" RootDrive="D:\" Size="268435456" DocCount="800" />
    <!-- ... up to 100 warehouse paths (00-99) ... -->
  </WarehousePaths>
  <Disks>
    <Disk VolumeName="C:\" DiskSize="500107862016" FreeSpace="250053931008" DiskType="Fixed" DriveTypeExplanation="Non-removable Hard Disk" CriticalFreeSpace="false" />
    <Disk VolumeName="D:\" DiskSize="1000204886016" FreeSpace="750153664512" DiskType="Fixed" DriveTypeExplanation="Non-removable Hard Disk" CriticalFreeSpace="false" />
  </Disks>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Response Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `TotalWarehouseSize` | double | Total size of all warehouse paths in bytes |
| `TotalDocumentCount` | integer | Total number of documents across all warehouse paths |

## WarehousePath Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `WhNo` | string | Warehouse number (00-99), zero-padded |
| `Path` | string | Physical file system path for this warehouse |
| `RootDrive` | string | Root drive of the warehouse path (e.g., `C:\`) |
| `Size` | double | Total size of documents in this warehouse path (bytes) |
| `DocCount` | integer | Number of documents in this warehouse path |

## Disk Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `VolumeName` | string | Drive volume name (e.g., `C:\`) |
| `DiskSize` | double | Total disk capacity in bytes |
| `FreeSpace` | double | Available free space in bytes |
| `DiskType` | string | Drive type enum value (Fixed, Network, Removable, etc.) |
| `DriveTypeExplanation` | string | Human-readable drive type description |
| `CriticalFreeSpace` | boolean | `true` if free space is less than 10% of total capacity |

## Drive Type Values

| DiskType | DriveTypeExplanation |
|----------|---------------------|
| `NoRootDirectory` | Drive does have root directory |
| `Removable` | Removable Disk |
| `Fixed` | Non-removable Hard Disk |
| `Network` | Remote Network drive |
| `CDRom` | CD-ROM drive |
| `Ram` | RAM disk |
| `Unknown` | Unrecognized |

## Required Permissions

- Administrators only: User must have `ViewWarehouseStatus` admin permission
- Non-admin users will receive an insufficient rights error

## Use Cases

1. **Storage Monitoring**
   - Monitor warehouse disk usage and remaining capacity
   - Alert on critical free space conditions (less than 10%)

2. **Capacity Planning**
   - Review document distribution across warehouse paths
   - Plan storage expansion based on usage trends

3. **System Administration**
   - Verify warehouse path configuration
   - Identify warehouse paths on different physical drives

## Example Requests

### Request (GET)

```
GET /api/UIInternals/GetWarehouseStatus?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /api/UIInternals/GetWarehouseStatus HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getWarehouseStatus() {
    const ticket = getUserAuthTicket();
    const url = `/api/UIInternals/GetWarehouseStatus?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const totalSize = parseFloat(root.getAttribute("TotalWarehouseSize"));
        const totalDocs = parseInt(root.getAttribute("TotalDocumentCount"));

        const paths = [];
        xmlDoc.querySelectorAll("WarehousePath").forEach(wp => {
            paths.push({
                whNo: wp.getAttribute("WhNo"),
                path: wp.getAttribute("Path"),
                rootDrive: wp.getAttribute("RootDrive"),
                size: parseFloat(wp.getAttribute("Size")),
                docCount: parseInt(wp.getAttribute("DocCount"))
            });
        });

        const disks = [];
        xmlDoc.querySelectorAll("Disk").forEach(d => {
            disks.push({
                volumeName: d.getAttribute("VolumeName"),
                diskSize: parseFloat(d.getAttribute("DiskSize")),
                freeSpace: parseFloat(d.getAttribute("FreeSpace")),
                diskType: d.getAttribute("DiskType"),
                driveTypeExplanation: d.getAttribute("DriveTypeExplanation"),
                criticalFreeSpace: d.getAttribute("CriticalFreeSpace") === "true"
            });
        });

        return { totalSize, totalDocs, paths, disks };
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function displayWarehouseStatus() {
    try {
        const status = await getWarehouseStatus();
        const totalSizeGB = (status.totalSize / 1024 / 1024 / 1024).toFixed(2);

        console.log(`Total documents: ${status.totalDocs}`);
        console.log(`Total warehouse size: ${totalSizeGB} GB`);

        status.disks.forEach(disk => {
            const freePercent = ((disk.freeSpace / disk.diskSize) * 100).toFixed(1);
            console.log(`${disk.volumeName} - ${freePercent}% free ${disk.criticalFreeSpace ? "(CRITICAL)" : ""}`);
        });
    } catch (error) {
        console.error("Failed to get warehouse status:", error);
    }
}
```

## Notes

- The response contains 100 warehouse paths (00 through 99), each mapping to a physical storage directory.
- **CriticalFreeSpace** is `true` when free space is less than 10% of total disk capacity.
- The `Disks` element contains only unique drives used by warehouse paths, avoiding duplicate entries.
- Sizes are returned in bytes as floating-point values.
- Document counts and sizes are retrieved from the database via warehouse statistics queries.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller may not view server status - including a caller with no ticket |


Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | User does not have `ViewWarehouseStatus` admin permission |

## Related APIs

- `ServerInfo` - Get basic server information (no authentication required)
- `GetMaintenanceJobsStatus` - Get maintenance jobs status
- `FlushApplicationCache` - Flush application cache
- `GetLicenseInfo` - Get license information
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Provides programmatic access to warehouse storage status
- Admin-only for security reasons (exposes file system paths)
