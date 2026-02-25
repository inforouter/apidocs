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
    <WebDav>true</WebDav>
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
        <HolidayDate>2024-12-25T00:00:00</HolidayDate>
        <Description>Christmas Day</Description>
      </Holiday>
      <Holiday>
        <HolidayDate>2024-01-01T00:00:00</HolidayDate>
        <Description>New Year's Day</Description>
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
| `HolidayList` | array | List of Holiday objects (date and description) |
| `ZipDownloadSetting` | object | ZIP download configuration |
| `SearchPageSize` | integer | Default number of results per search page |

## UploadSettings Properties

| Property | Type | Description |
|----------|------|-------------|
| `DocumentMaxSize` | long | Maximum document size in bytes (default: 75MB) |
| `FileUploadTimeOut` | integer | Upload timeout in seconds |
| `DefaultUploadFileChunkSize` | integer | Default chunk size for chunked uploads in bytes |

## Workdays Properties

| Property | Type | Description |
|----------|------|-------------|
| `Monday` - `Sunday` | boolean | Whether each day is a work day |
| `StartHour` | integer | Work day start hour (0-23) |
| `StartMinute` | integer | Work day start minute (0-59) |
| `EndHour` | integer | Work day end hour (0-23) |
| `EndMinute` | integer | Work day end minute (0-59) |

## ZipDownloadSetting Properties

| Property | Type | Description |
|----------|------|-------------|
| `Enabled` | boolean | Whether ZIP downloads are enabled |
| `MaxTotalSize` | long | Maximum total size of files in ZIP download (bytes) |
| `MaxTotalCount` | integer | Maximum number of files in ZIP download |

## Holiday Properties

| Property | Type | Description |
|----------|------|-------------|
| `HolidayDate` | DateTime | The date of the holiday |
| `Description` | string | Description or name of the holiday |

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
   - Configure business day calculations
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
    if (root.getAttribute("success") === "true") {
        const settings = xmlDoc.querySelector("GeneralSettings");
        const uploadSettings = settings.querySelector("UploadSettings");

        return {
            uploadSettings: {
                documentMaxSize: parseInt(uploadSettings.querySelector("DocumentMaxSize").textContent),
                fileUploadTimeOut: parseInt(uploadSettings.querySelector("FileUploadTimeOut").textContent),
                defaultUploadFileChunkSize: parseInt(uploadSettings.querySelector("DefaultUploadFileChunkSize").textContent)
            },
            allowOwnershipTransfer: settings.querySelector("AllowOwnershipTransfer").textContent === "true",
            webDav: settings.querySelector("WebDav").textContent === "true",
            searchPageSize: parseInt(settings.querySelector("SearchPageSize").textContent)
        };
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function configureUploader() {
    try {
        const settings = await getGeneralAppSettings();

        // Configure file uploader based on settings
        const maxSizeMB = settings.uploadSettings.documentMaxSize / 1024 / 1024;
        console.log(`Max upload size: ${maxSizeMB} MB`);
        console.log(`Chunk size: ${settings.uploadSettings.defaultUploadFileChunkSize} bytes`);
        console.log(`Timeout: ${settings.uploadSettings.fileUploadTimeOut} seconds`);

        // Configure uploader component
        uploader.setMaxFileSize(settings.uploadSettings.documentMaxSize);
        uploader.setChunkSize(settings.uploadSettings.defaultUploadFileChunkSize);
        uploader.setTimeout(settings.uploadSettings.fileUploadTimeOut * 1000);

    } catch (error) {
        console.error("Failed to get settings:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetGeneralAppSettingsAsync(authTicket);

        var root = XElement.Parse(response.ToString());
        if (root.Attribute("success")?.Value == "true")
        {
            var settings = root.Element("GeneralSettings");
            var uploadSettings = settings.Element("UploadSettings");

            var config = new
            {
                DocumentMaxSize = long.Parse(uploadSettings.Element("DocumentMaxSize")?.Value ?? "0"),
                FileUploadTimeOut = int.Parse(uploadSettings.Element("FileUploadTimeOut")?.Value ?? "900"),
                ChunkSize = int.Parse(uploadSettings.Element("DefaultUploadFileChunkSize")?.Value ?? "262144"),
                WebDavEnabled = bool.Parse(settings.Element("WebDav")?.Value ?? "false"),
                SearchPageSize = int.Parse(settings.Element("SearchPageSize")?.Value ?? "20")
            };

            Console.WriteLine($"Max Document Size: {config.DocumentMaxSize / 1024 / 1024} MB");
            Console.WriteLine($"Upload Timeout: {config.FileUploadTimeOut} seconds");
            Console.WriteLine($"WebDAV Enabled: {config.WebDavEnabled}");
        }
        else
        {
            var error = root.Attribute("error")?.Value;
            Console.WriteLine($"Error: {error}");
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Exception: {ex.Message}");
    }
}
```

## Notes

- **DocumentMaxSize**: Value in bytes. Default is 75MB (78643200 bytes), maximum is 1GB.
- **DefaultUploadFileChunkSize**: Minimum 256KB, maximum 32MB. Used for chunked uploads.
- **SystemRecycleBinAutoPurgeOption**: 0 means disabled, 1-36 represents months.
- **Workdays**: Used for business day calculations in workflows and due dates.
- **Holidays**: List of dates that should be excluded from business day calculations.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |

## Related APIs

- `getApplicationParameters` - Get basic application parameters
- `SetDefaultFolderColumns` - Set default folder display columns
- `GetAllFolderColumns` - Get all available folder columns

## Version History

- Compatible with infoRouter 8.7 and later
- Settings model is serializable for client-side deserialization
- Supports both synchronous SOAP and REST access patterns

## See Also

- Control Panel UI: `ApplicationSettingsApply.aspx` - Application settings configuration page
