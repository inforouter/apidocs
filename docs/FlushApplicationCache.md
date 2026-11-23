# FlushApplicationCache API

**Available in:** infoRouter 9.0 and later

Flushes the in-memory application cache, forcing the system to reload configuration and cached data from the database and file system. It also reads the content search settings file, `config\content-search-setting.json`, the SMTP settings file, `config\smtp-setting.json`, the infoRouter Connect settings file, `config\irconnect-setting.json`, and the sign-on settings file, `config\signon-setting.json`, again and puts them in effect, so a change made to any of these files by hand needs no restart. Only administrators can call it: the `sysadmin` account and members of `[Administrators]`.

## Endpoint

```
/srv.asmx/FlushApplicationCache
```

## Methods

- **GET** `/srv.asmx/FlushApplicationCache?authenticationTicket=...`
- **POST** `/srv.asmx/FlushApplicationCache` (form data)
- **SOAP** Action: `http://tempuri.org/FlushApplicationCache`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- Administrators only: the `sysadmin` account and members of `[Administrators]`. No other role, User Managers included, may flush the cache.
- Anyone else is refused with `errorCode="4030"`.

## Use Cases

1. **Configuration Changes**
   - Force reload after direct database changes to application settings
   - Refresh cached data after bulk operations

2. **Troubleshooting**
   - Clear stale cached data that may cause unexpected behavior
   - Reset application state without restarting the service

3. **Maintenance**
   - Refresh after license file updates
   - Clear cache after system migrations or upgrades

## Example Requests

### Request (GET)

```
GET /srv.asmx/FlushApplicationCache?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/FlushApplicationCache HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/FlushApplicationCache"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <FlushApplicationCache xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </FlushApplicationCache>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function flushApplicationCache() {
    const ticket = getUserAuthTicket();

    const response = await fetch("/srv.asmx/FlushApplicationCache", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `authenticationTicket=${encodeURIComponent(ticket)}`
    });

    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        console.log("Application cache flushed successfully.");
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.FlushApplicationCacheAsync(authTicket);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            Console.WriteLine("Application cache flushed successfully.");
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

- This operation calls `Settings.FlushCache()` which clears the in-memory application settings cache.
- The content search settings file is read again, as at start, and content search switches to it at once; searches already running finish with the settings they started with. The file's content never makes the call fail:
  - no file: content search is off;
  - a file that cannot be read: content search is off, the problem is written to the error log, and [GetContentSearchSettings](GetContentSearchSettings.md) returns it as `SettingsProblem`;
  - a catalog that cannot be used here (`SYSTEMINDEX` on an infoRouter that does not run on Windows, or neither an http:// or https:// address nor `SYSTEMINDEX`): the settings are kept and the problem is written to the error log; keyword searches fail, saying why, until the settings are corrected.
- The SMTP settings file is read again the same way, and email sent from then on uses it. No file means no SMTP server (email is queued but not sent); a file that cannot be read means none either, the problem is written to the error log, and [GetSmtpSettings](GetSmtpSettings.md) returns it as `SettingsProblem`. A password typed into the file in plain text is encrypted in the file. When the system email address changed, email still queued under the previous one is sent with the new settings.
- The infoRouter Connect settings file is read again the same way, and the Connect calls and the AI job queue use it from then on. No file means Connect is not configured; a file that cannot be read means not configured either, and the problem is written to the error log. An `ApiKey` pasted into the file in plain text is encrypted in the file.
- The sign-on settings file is read again the same way ([GetSignOnSettings](GetSignOnSettings.md)): authentication authorities, the sysadmin check and trusted LDAP accounts and the temporary sysadmin password apply at once, and the OpenID Connect providers follow: a new one is offered and can be signed in with, a changed one uses its new settings from its next sign-in, a removed one is no longer offered. Entries that cannot be used, and a file that cannot be read, are written to the error log.
- The cache will be repopulated on the next request that accesses cached settings.
- This operation does not affect user sessions or authentication tickets.
- Use sparingly in production environments as cache rebuilding may temporarily impact performance.
- This does not restart the application or recycle the application pool.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | a caller with no ticket, or a signed-in caller who is not an administrator |


Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | The caller is not an administrator |

## Related APIs

- `GetMaintenanceJobsStatus` - Get maintenance jobs status
- `GetWarehouseStatus` - Get warehouse storage status
- `ServerInfo` - Get basic server information
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Provides programmatic cache management for system administrators
- Admin-only for security and stability reasons
