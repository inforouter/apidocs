# UpdateApplicationLicense API

Updates the infoRouter application license by writing a new license file. This API is restricted to system administrators. The license data is validated, saved to disk, and the in-memory settings are immediately refreshed.

## Endpoint

```
/srv.asmx/UpdateApplicationLicense
```

## Methods

- **GET** `/srv.asmx/UpdateApplicationLicense?authenticationTicket=...&licenseText=...`
- **POST** `/srv.asmx/UpdateApplicationLicense` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateApplicationLicense`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `licenseText` | string | Yes | The new license XML content to apply |

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

- Administrators only: User must be a system administrator (`IsAdministrator`)
- Non-admin users will receive an insufficient rights error (resource code 921)

## Use Cases

1. **License Renewal**
   - Apply a renewed license when the subscription is extended
   - Replace an expired license with a new one

2. **License Upgrade**
   - Increase user seat count
   - Enable additional features (workflow, anonymous access)

3. **Automated Provisioning**
   - Programmatically apply licenses during automated deployment

## Example Requests

### Request (GET)

```
GET /srv.asmx/UpdateApplicationLicense?authenticationTicket=abc123-def456&licenseText=%3Clicense%3E...%3C%2Flicense%3E HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/UpdateApplicationLicense HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&licenseText=<license>...</license>
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/UpdateApplicationLicense"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <UpdateApplicationLicense xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <licenseText>&lt;license&gt;...&lt;/license&gt;</licenseText>
    </UpdateApplicationLicense>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function updateApplicationLicense(licenseText) {
    const ticket = getUserAuthTicket();

    const response = await fetch("/srv.asmx/UpdateApplicationLicense", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `authenticationTicket=${encodeURIComponent(ticket)}&licenseText=${encodeURIComponent(licenseText)}`
    });

    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        console.log("License updated successfully.");
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
        var response = await client.UpdateApplicationLicenseAsync(authTicket, licenseXml);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            Console.WriteLine("License updated successfully.");
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

- The license is written to a `license.lic` file in the application configuration directory.
- After the file is written, in-memory settings are immediately refreshed: `LicenseInfo`, `AllowedSessionCountForUser`, `InstanceName`, `NativeAuthentationType`, and `ForceOnline` are all reloaded.
- If the license XML is invalid or cannot be written, the operation fails and returns an error message.
- The POST method is recommended when the license text contains XML, to avoid URL encoding issues.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | User is not a system administrator |

## Related APIs

- `GetLicenseInfo` - Retrieve current license information
- `ServerInfo` - Get basic server and license summary
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Provides programmatic license management
- Requires full administrator privileges (not just a specific admin permission)
