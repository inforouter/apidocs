# GetGeneralAppSettings API

Returns the general application settings including upload limits, work days configuration, holidays, and system preferences.

## Endpoint

```
/srv.asmx/GetGeneralAppSettings
```

## Methods

- **GET** `/srv.asmx/GetGeneralAppSettings?authenticationTicket=...`
- **POST** `/srv.asmx/GetGeneralAppSettings` (form data)
- **SOAP** Action: `http://tempuri.org/GetGeneralAppSettings`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true">
  <GeneralSettings>
    <UploadSettings>
      <DocumentMaxSize>78643200</DocumentMaxSize>
      <FileUploadTimeOut>900</FileUploadTimeOut>
      <DefaultUploadFileChunkSize>262144</DefaultUploadFileChunkSize>
    </UploadSettings>
    <AllowOwnershipTransfer>false</AllowOwnershipTransfer>
    <WebDav>false</WebDav>
    <DisplayAddIns>true</DisplayAddIns>
    <MinYearInDateControls>1900</MinYearInDateControls>
    <SystemRecycleBinAutoPurgeOption>0</SystemRecycleBinAutoPurgeOption>
    <MoveUsersRecycleBinToSystemRecycleBinIn>0</MoveUsersRecycleBinToSystemRecycleBinIn>
    <RerouteRedirections>false</RerouteRedirections>
    <SendDiagnosticsAndStatistics>true</SendDiagnosticsAndStatistics>
    <Workdays>
      <Monday>true</Monday>
      <Tuesday>true</Tuesday>
      <Wednesday>true</Wednesday>
      <Thursday>true</Thursday>
      <Friday>true</Friday>
      <Saturday>false</Saturday>
      <Sunday>false</Sunday>
      <StartHour>8</StartHour>
      <StartMinute>0</StartMinute>
      <EndHour>17</EndHour>
      <EndMinute>0</EndMinute>
    </Workdays>
    <HolidayList>
      <Holiday>
        <HolidayDate>2025-07-04T00:00:00</HolidayDate>
        <Description>Independence Day</Description>
      </Holiday>
      <Holiday>
        <HolidayDate>2000-12-25T00:00:00</HolidayDate>
        <Description>Christmas Day</Description>
      </Holiday>
    </HolidayList>
    <ZipDownloadSetting>
      <Enabled>true</Enabled>
      <MaxTotalSize>78643200</MaxTotalSize>
      <MaxTotalCount>1000</MaxTotalCount>
    </ZipDownloadSetting>
    <SearchPageSize>20</SearchPageSize>
  </GeneralSettings>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## GeneralSettings Properties

| Property | Type | Description |
|----------|------|-------------|
| `UploadSettings` | object | Upload configuration settings |
| `AllowOwnershipTransfer` | boolean | Whether document ownership transfer is allowed |
| `WebDav` | boolean | Whether WebDAV protocol is enabled |
| `DisplayAddIns` | boolean | Whether to display add-ins in the UI |
| `MinYearInDateControls` | integer | Minimum year allowed in date picker controls |
| `SystemRecycleBinAutoPurgeOption` | integer | Auto-purge option for system recycle bin (0-36 months) |
| `MoveUsersRecycleBinToSystemRecycleBinIn` | integer | Days before moving user recycle bin items to system |
| `RerouteRedirections` | boolean | Whether to reroute URL redirections |
| `SendDiagnosticsAndStatistics` | boolean | Whether to send anonymous diagnostics |
| `Workdays` | object | Work days and hours configuration |
| `HolidayList` | array | List of Holiday objects — see Holiday Properties below |
| `ZipDownloadSetting` | object | ZIP download configuration |
| `SearchPageSize` | integer | Default number of results per search page |

## UploadSettings Properties

| Property | Type | Description |
|----------|------|-------------|
| `DocumentMaxSize` | long | Maximum document size in bytes (default: 75 MB = 78643200, max: 1 GB) |
| `FileUploadTimeOut` | integer | Upload timeout in seconds |
| `DefaultUploadFileChunkSize` | integer | Chunk size for chunked uploads in bytes (min: 256 KB, max: 32 MB) |

## Workdays Properties

| Property | Type | Description |
|----------|------|-------------|
| `Monday` – `Sunday` | boolean | Whether each day is a work day |
| `StartHour` | integer | Work day start hour (0–23) |
| `StartMinute` | integer | Work day start minute (0–59) |
| `EndHour` | integer | Work day end hour (0–23) |
| `EndMinute` | integer | Work day end minute (0–59) |

## Holiday Properties

| Property | Type | Description |
|----------|------|-------------|
| `HolidayDate` | DateTime | Date of the holiday (ISO 8601, e.g. `2025-07-04T00:00:00`) |
| `Description` | string | Name or description of the holiday |

### Recurring Holidays

A holiday whose `HolidayDate` year is **2000** is a **recurring (annual) holiday** — it applies on that month and day every year, regardless of the actual year value stored.

```xml
<!-- Recurring holiday: applies every December 25th -->
<Holiday>
  <HolidayDate>2000-12-25T00:00:00</HolidayDate>
  <Description>Christmas Day</Description>
</Holiday>

<!-- One-time holiday: applies only on July 4, 2025 -->
<Holiday>
  <HolidayDate>2025-07-04T00:00:00</HolidayDate>
  <Description>Independence Day</Description>
</Holiday>
```

When processing holidays for business-day calculations, check the year of `HolidayDate`:
- Year `2000` → recurring: compare only month and day against the target date
- Any other year → one-time: compare the full date

## ZipDownloadSetting Properties

| Property | Type | Description |
|----------|------|-------------|
| `Enabled` | boolean | Whether ZIP downloads are enabled |
| `MaxTotalSize` | long | Maximum total size of all files in a ZIP download (bytes) |
| `MaxTotalCount` | integer | Maximum number of files in a ZIP download |

## Required Permissions

- User must be authenticated (anonymous users cannot access this API)
- No specific administrative permissions required to read settings

## Use Cases

1. **Client Configuration**
   - Retrieve upload limits before file upload
   - Configure client-side upload chunking
   - Display appropriate date picker ranges

2. **Application Integration**
   - Determine WebDAV availability
   - Configure business day calculations including workday schedule and holidays
   - Respect system-wide preferences

3. **Administration Dashboard**
   - Display current system configuration
   - Monitor settings state
   - Pre-populate settings forms

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetGeneralAppSettings?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetGeneralAppSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetGeneralAppSettings"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetGeneralAppSettings xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetGeneralAppSettings>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getGeneralAppSettings() {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetGeneralAppSettings?authenticationTicket=${encodeURIComponent(ticket)}`;
    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") !== "true") {
        throw new Error(root.getAttribute("error"));
    }

    const settings = xmlDoc.querySelector("GeneralSettings");
    const uploadSettings = settings.querySelector("UploadSettings");
    const workdays = settings.querySelector("Workdays");

    // Parse holidays — year 2000 = recurring
    const holidays = Array.from(settings.querySelectorAll("HolidayList > Holiday")).map(h => {
        const date = new Date(h.querySelector("HolidayDate").textContent);
        return {
            date,
            description: h.querySelector("Description").textContent,
            recurring: date.getFullYear() === 2000
        };
    });

    return {
        uploadSettings: {
            documentMaxSize: parseInt(uploadSettings.querySelector("DocumentMaxSize").textContent),
            fileUploadTimeOut: parseInt(uploadSettings.querySelector("FileUploadTimeOut").textContent),
            defaultUploadFileChunkSize: parseInt(uploadSettings.querySelector("DefaultUploadFileChunkSize").textContent)
        },
        allowOwnershipTransfer: settings.querySelector("AllowOwnershipTransfer").textContent === "true",
        webDav: settings.querySelector("WebDav").textContent === "true",
        searchPageSize: parseInt(settings.querySelector("SearchPageSize").textContent),
        workdays,
        holidays
    };
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    var response = await client.GetGeneralAppSettingsAsync(authTicket);
    var root = XElement.Parse(response.ToString());

    if (root.Attribute("success")?.Value == "true")
    {
        var settings = root.Element("GeneralSettings");
        var uploadSettings = settings.Element("UploadSettings");
        var zipSettings = settings.Element("ZipDownloadSetting");

        var config = new
        {
            DocumentMaxSize = long.Parse(uploadSettings.Element("DocumentMaxSize")?.Value ?? "0"),
            FileUploadTimeOut = int.Parse(uploadSettings.Element("FileUploadTimeOut")?.Value ?? "900"),
            ChunkSize = int.Parse(uploadSettings.Element("DefaultUploadFileChunkSize")?.Value ?? "262144"),
            WebDavEnabled = bool.Parse(settings.Element("WebDav")?.Value ?? "false"),
            SearchPageSize = int.Parse(settings.Element("SearchPageSize")?.Value ?? "20"),
            ZipEnabled = bool.Parse(zipSettings.Element("Enabled")?.Value ?? "false")
        };

        // Parse holidays — year 2000 = recurring
        var holidays = settings.Element("HolidayList")?
            .Elements("Holiday")
            .Select(h => new {
                Date = DateTime.Parse(h.Element("HolidayDate")?.Value ?? ""),
                Description = h.Element("Description")?.Value ?? "",
                IsRecurring = DateTime.Parse(h.Element("HolidayDate")?.Value ?? "").Year == 2000
            }).ToList();
    }
    else
    {
        Console.WriteLine($"Error: {root.Attribute("error")?.Value}");
    }
}
```

## Notes

- **DocumentMaxSize**: Value in bytes. Default is 75 MB (78643200). Maximum is 1 GB (1073741824). Values below 1 MB are clamped to 1 MB.
- **DefaultUploadFileChunkSize**: Minimum 256 KB (262144), maximum 32 MB (33554432).
- **SystemRecycleBinAutoPurgeOption**: 0 means disabled; 1–36 represents months.
- **Workdays**: Used for business day calculations in workflows and due dates.
- **Recurring Holidays**: A `HolidayDate` with year `2000` means the holiday recurs on that month/day every year.

## Error Codes

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |

## Related APIs

- `SetGeneralAppSettings` - Update general application settings
- `GetAuthenticationAndPasswordPolicy` - Get authentication and password policy settings
- `GetSystemBehaviorSettings` - Get system behavior settings

## See Also

- Control Panel UI: `ApplicationSettingsApply.aspx` — Application settings configuration page
