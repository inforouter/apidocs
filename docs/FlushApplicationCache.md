# FlushApplicationCache API

Flushes the in-memory application cache, forcing the system to reload configuration and cached data from the database and file system. This API is restricted to system administrators with the `FlushApplicationCache` permission.

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

- Administrators only: User must have `FlushApplicationCache` admin permission
- Non-admin users will receive an insufficient rights error

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
- The cache will be repopulated on the next request that accesses cached settings.
- This operation does not affect user sessions or authentication tickets.
- Use sparingly in production environments as cache rebuilding may temporarily impact performance.
- This does not restart the application or recycle the application pool.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | User does not have `FlushApplicationCache` admin permission |

## Related APIs

- `GetMaintenanceJobsStatus` - Get maintenance jobs status
- `GetWarehouseStatus` - Get warehouse storage status
- `ServerInfo` - Get basic server information
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Provides programmatic cache management for system administrators
- Admin-only for security and stability reasons
