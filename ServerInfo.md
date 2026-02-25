# ServerInfo API

Returns information about the infoRouter Server instance including version, server time, license details, and configuration settings.

## Endpoint

```
/srv.asmx/ServerInfo
```

## Methods

- **GET** `/srv.asmx/ServerInfo`
- **POST** `/srv.asmx/ServerInfo`
- **SOAP** Action: `http://tempuri.org/ServerInfo`

> This API does not require authentication. It is publicly accessible for server information retrieval.

## Parameters

This API does not require any parameters.

## Response

### Success

```xml
<root 
    success="true"
    VersionNumber="8.7.0.0"
    Server_date_time="2024-01-15T14:30:45"
    Coordinated_Universal_Time="2024-01-15T19:30:45Z"
    UTC_Offset="-5"
    Company="Acme Corporation"
    ServerName="IRSERVER01"
    LicenseCount="100"
    SubscriptionEndDate="2024-12-31T23:59:59Z"
    WindowsAuthenticationIsOn="true" />
```

### Error

```xml
<root success="false" error="Error message details" />
```

## Response Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | boolean | Always "true" for successful responses |
| `VersionNumber` | string | infoRouter version number (e.g., "8.7.0.0") |
| `Server_date_time` | datetime | Current server date and time in ISO 8601 format |
| `Coordinated_Universal_Time` | datetime | Current UTC time in universal date format |
| `UTC_Offset` | decimal | Server's UTC offset in hours (e.g., "-5" for EST) |
| `Company` | string | Licensed company name from license file |
| `ServerName` | string | Windows machine/server name |
| `LicenseCount` | integer | Number of licensed users |
| `SubscriptionEndDate` | datetime | License subscription end date in universal format |
| `WindowsAuthenticationIsOn` | boolean | Whether Windows Authentication is enabled ("true"/"false") |

## Required Permissions

- **None** - This is a public API endpoint that does not require authentication
- Can be called anonymously to retrieve server information

## Example (REST GET)

```
GET /srv.asmx/ServerInfo HTTP/1.1
Host: your-inforouter-server.com
```

### SOAP Request

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/ServerInfo"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ServerInfo xmlns="http://tempuri.org/" />
  </soap:Body>
</soap:Envelope>
```

### SOAP Response

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ServerInfoResponse xmlns="http://tempuri.org/">
      <ServerInfoResult>
        <root 
            success="true"
            VersionNumber="8.7.0.0"
            Server_date_time="2024-01-15T14:30:45"
            Coordinated_Universal_Time="2024-01-15T19:30:45Z"
            UTC_Offset="-5"
            Company="Acme Corporation"
            ServerName="IRSERVER01"
            LicenseCount="100"
            SubscriptionEndDate="2024-12-31T23:59:59Z"
            WindowsAuthenticationIsOn="true" />
      </ServerInfoResult>
    </ServerInfoResponse>
  </soap:Body>
</soap:Envelope>
```

## Use Cases

### 1. Server Health Check
Use this API to verify that the infoRouter server is running and accessible:

```javascript
fetch('/srv.asmx/ServerInfo')
  .then(response => response.text())
  .then(xml => {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xml, 'text/xml');
    const root = xmlDoc.documentElement;
    
    if (root.getAttribute('success') === 'true') {
      console.log('Server is online');
      console.log('Version:', root.getAttribute('VersionNumber'));
    }
  });
```

### 2. Version Compatibility Check
Verify the server version before making API calls:

```csharp
var client = new ServiceReference.SrvSoapClient();
var serverInfo = await client.ServerInfoAsync();

var versionAttr = serverInfo.Root.Attribute("VersionNumber");
if (versionAttr != null)
{
    var version = new Version(versionAttr.Value);
    if (version >= new Version("8.7.0.0"))
    {
        // Server supports new API features
        Console.WriteLine($"Server version {version} is compatible");
    }
}
```

### 3. License Information Display
Display license and server information in admin dashboard:

```csharp
var serverInfo = await client.ServerInfoAsync();
var root = serverInfo.Root;

Console.WriteLine($"Company: {root.Attribute("Company")?.Value}");
Console.WriteLine($"Licensed Users: {root.Attribute("LicenseCount")?.Value}");
Console.WriteLine($"Subscription Expires: {root.Attribute("SubscriptionEndDate")?.Value}");
Console.WriteLine($"Server: {root.Attribute("ServerName")?.Value}");
```

### 4. Time Synchronization
Get server time for time-sensitive operations:

```csharp
var serverInfo = await client.ServerInfoAsync();
var serverTime = DateTime.Parse(serverInfo.Root.Attribute("Server_date_time").Value);
var utcOffset = double.Parse(serverInfo.Root.Attribute("UTC_Offset").Value);

Console.WriteLine($"Server Time: {serverTime}");
Console.WriteLine($"UTC Offset: {utcOffset} hours");
```

## Integration Example (C#)

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Xml.Linq;

public class ServerInfoClient
{
    private readonly string _baseUrl;
    private readonly HttpClient _httpClient;

    public ServerInfoClient(string baseUrl)
    {
        _baseUrl = baseUrl;
        _httpClient = new HttpClient();
    }

    public async Task<ServerInformation> GetServerInfoAsync()
    {
        var url = $"{_baseUrl}/srv.asmx/ServerInfo";
        var response = await _httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();

        var xmlContent = await response.Content.ReadAsStringAsync();
        var xml = XElement.Parse(xmlContent);

        return new ServerInformation
        {
            Success = xml.Attribute("success")?.Value == "true",
            VersionNumber = xml.Attribute("VersionNumber")?.Value,
            ServerDateTime = DateTime.Parse(xml.Attribute("Server_date_time")?.Value ?? ""),
            UtcDateTime = DateTime.Parse(xml.Attribute("Coordinated_Universal_Time")?.Value ?? ""),
            UtcOffset = double.Parse(xml.Attribute("UTC_Offset")?.Value ?? "0"),
            Company = xml.Attribute("Company")?.Value,
            ServerName = xml.Attribute("ServerName")?.Value,
            LicenseCount = int.Parse(xml.Attribute("LicenseCount")?.Value ?? "0"),
            SubscriptionEndDate = DateTime.Parse(xml.Attribute("SubscriptionEndDate")?.Value ?? ""),
            WindowsAuthenticationEnabled = xml.Attribute("WindowsAuthenticationIsOn")?.Value == "true"
        };
    }
}

public class ServerInformation
{
    public bool Success { get; set; }
    public string VersionNumber { get; set; }
    public DateTime ServerDateTime { get; set; }
    public DateTime UtcDateTime { get; set; }
    public double UtcOffset { get; set; }
    public string Company { get; set; }
    public string ServerName { get; set; }
    public int LicenseCount { get; set; }
    public DateTime SubscriptionEndDate { get; set; }
    public bool WindowsAuthenticationEnabled { get; set; }
}

// Usage
var client = new ServerInfoClient("https://your-inforouter-server.com");
var info = await client.GetServerInfoAsync();

Console.WriteLine($"Server Version: {info.VersionNumber}");
Console.WriteLine($"Company: {info.Company}");
Console.WriteLine($"License Expires: {info.SubscriptionEndDate:yyyy-MM-dd}");
```

## Integration Example (JavaScript/TypeScript)

```javascript
async function getServerInfo() {
    const response = await fetch('/srv.asmx/ServerInfo');
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xml = parser.parseFromString(xmlText, 'text/xml');
    const root = xml.documentElement;
    
    return {
        success: root.getAttribute('success') === 'true',
        versionNumber: root.getAttribute('VersionNumber'),
        serverDateTime: new Date(root.getAttribute('Server_date_time')),
        utcDateTime: new Date(root.getAttribute('Coordinated_Universal_Time')),
        utcOffset: parseFloat(root.getAttribute('UTC_Offset')),
        company: root.getAttribute('Company'),
        serverName: root.getAttribute('ServerName'),
        licenseCount: parseInt(root.getAttribute('LicenseCount')),
        subscriptionEndDate: new Date(root.getAttribute('SubscriptionEndDate')),
        windowsAuthEnabled: root.getAttribute('WindowsAuthenticationIsOn') === 'true'
    };
}

// Usage
const serverInfo = await getServerInfo();
console.log('Server Info:', serverInfo);
```

## Integration Example (Python)

```python
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def get_server_info(base_url):
    """Get infoRouter server information"""
    url = f"{base_url}/srv.asmx/ServerInfo"
    response = requests.get(url)
    response.raise_for_status()
    
    root = ET.fromstring(response.text)
    
    return {
        'success': root.get('success') == 'true',
        'version_number': root.get('VersionNumber'),
        'server_datetime': datetime.fromisoformat(root.get('Server_date_time')),
        'utc_datetime': datetime.fromisoformat(root.get('Coordinated_Universal_Time').replace('Z', '+00:00')),
        'utc_offset': float(root.get('UTC_Offset')),
        'company': root.get('Company'),
        'server_name': root.get('ServerName'),
        'license_count': int(root.get('LicenseCount')),
        'subscription_end_date': datetime.fromisoformat(root.get('SubscriptionEndDate').replace('Z', '+00:00')),
        'windows_auth_enabled': root.get('WindowsAuthenticationIsOn') == 'true'
    }

# Usage
server_info = get_server_info('https://your-inforouter-server.com')
print(f"Server Version: {server_info['version_number']}")
print(f"Company: {server_info['company']}")
print(f"Licensed Users: {server_info['license_count']}")
```

## Notes

- **No Authentication Required**: This is one of the few API endpoints that can be called without authentication
- **Public Information**: Only non-sensitive server information is exposed
- **Server Time**: Use this API to synchronize client-side operations with server time
- **License Validation**: Check subscription end date to warn users about expiring licenses
- **Version Detection**: Use version number to determine available API features
- **Health Monitoring**: Suitable for server monitoring and health check systems
- **CORS**: This endpoint is typically available for cross-origin requests

## Security Considerations

- While this endpoint is public, it does not expose sensitive security information
- License details (company name, user count) are from the license file, not internal system data
- Server name is the Windows machine name, which is generally considered non-sensitive
- No user data, database information, or file paths are exposed
- Consider rate limiting in high-traffic scenarios

## Troubleshooting

### Issue: "Unable to connect to server"
**Solution**: Verify the server URL and network connectivity. This is often the first API to test server availability.

### Issue: Wrong server time displayed
**Solution**: Check the server's Windows time zone settings. The `UTC_Offset` should match the server's configured time zone.

### Issue: Old version number shown
**Solution**: The version number is cached from the application settings. Restart the application pool or web service to refresh.

## Related APIs

- `GetWarehouseStatus` - Get warehouse storage and document count information
- `FlushApplicationCache` - Flush application cache (requires admin permissions)
- `AuthenticateUser` - Authenticate and get authentication ticket
- `GetApplicationSettings` - Get detailed application settings (requires authentication)

## Version History

- Available since infoRouter 8.0
- No authentication requirement added in version 8.5 for public server information
- Windows Authentication status added in version 8.6
- Compatible with infoRouter 8.7 and later

## Support

For additional information, see:
- [API Documentation](https://support.inforouter.com/api-docs/ServerInfo)
- [Server Configuration Guide](https://support.inforouter.com/server-configuration)
- [License Management](https://support.inforouter.com/license-management)
