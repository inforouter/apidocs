# getApplicationParameters API

Returns infoRouter application parameters and system configuration settings. The response varies based on the authenticated user's role: anonymous users receive a limited set of public parameters, regular users receive the same public parameters, and system administrators receive the full configuration including SMTP settings, password policies, server information, and warehouse paths.

## Endpoint

```
/srv.asmx/getApplicationParameters
```

## Methods

- **GET** `/srv.asmx/getApplicationParameters?AuthenticationTicket=...`
- **POST** `/srv.asmx/getApplicationParameters` (form data)
- **SOAP** Action: `http://tempuri.org/getApplicationParameters`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

The response content depends on the role of the authenticated user. There are three levels of detail.

### Success Response (All Authenticated Users)

All authenticated users (including anonymous) receive the following public parameters:

```xml
<response success="true" error="">
  <PARAMETERS>
    <WEBDAV>TRUE</WEBDAV>
    <ALLOWEMAILATTACHMENTS>TRUE</ALLOWEMAILATTACHMENTS>
    <ATTACHMENTSIZELIMIT>0</ATTACHMENTSIZELIMIT>
    <APPLICATIONURL>http://server.example.com/</APPLICATIONURL>
    <SYSTEMEMAILADDRESS>support@example.com</SYSTEMEMAILADDRESS>
    <INDEXSRV>TRUE</INDEXSRV>
    <SEARCHPAGESIZE>50</SEARCHPAGESIZE>
    <FILEUPLOADLIMIT>1072693248</FILEUPLOADLIMIT>
    <ALLOWPARTIALEMAILUPLOADS>TRUE</ALLOWPARTIALEMAILUPLOADS>
  </PARAMETERS>
</response>
```

### Success Response (System Administrator)

System administrators receive all public parameters plus additional configuration details:

```xml
<response success="true" error="">
  <PARAMETERS>
    <!-- Public parameters (same as above) -->
    <WEBDAV>TRUE</WEBDAV>
    <ALLOWEMAILATTACHMENTS>TRUE</ALLOWEMAILATTACHMENTS>
    <ATTACHMENTSIZELIMIT>0</ATTACHMENTSIZELIMIT>
    <APPLICATIONURL>http://server.example.com/</APPLICATIONURL>
    <SYSTEMEMAILADDRESS>support@example.com</SYSTEMEMAILADDRESS>
    <INDEXSRV>TRUE</INDEXSRV>
    <SEARCHPAGESIZE>50</SEARCHPAGESIZE>
    <FILEUPLOADLIMIT>1072693248</FILEUPLOADLIMIT>
    <ALLOWPARTIALEMAILUPLOADS>TRUE</ALLOWPARTIALEMAILUPLOADS>

    <!-- Administrator-only parameters -->
    <INDEXCATALOG>SYSTEMINDEX</INDEXCATALOG>
    <LOGLOGINS>TRUE</LOGLOGINS>
    <FILEUPLOADTIMEOUT>7000</FILEUPLOADTIMEOUT>
    <ALLOWOWNERSHIPTRANSFER>FALSE</ALLOWOWNERSHIPTRANSFER>
    <SUBSCRIPTIONNOTIFICATIONS>TRUE</SUBSCRIPTIONNOTIFICATIONS>
    <SENDEMAIL>TRUE</SENDEMAIL>
    <SENDTO_DISPLAYUSERLIST>TRUE</SENDTO_DISPLAYUSERLIST>

    <!-- SMTP Configuration -->
    <SMTPSERVER>smtp.office365.com</SMTPSERVER>
    <SMTPSERVERPORT>587</SMTPSERVERPORT>
    <SMTPCONNECTIONTIMEOUT>20</SMTPCONNECTIONTIMEOUT>
    <SMTPSENDUSERNAME>support@example.com</SMTPSENDUSERNAME>
    <SMTPSENDPASSWORD>****</SMTPSENDPASSWORD>

    <!-- Password Policy -->
    <PWDMINLEN>5</PWDMINLEN>
    <PWDALPHA>FALSE</PWDALPHA>
    <PWDNUM>FALSE</PWDNUM>
    <PWDEXPIRES>60</PWDEXPIRES>
    <PWDWEAKLIST>TRUE</PWDWEAKLIST>
    <PWDNONALPHA>TRUE</PWDNONALPHA>
    <PWDNOUSERNAME>TRUE</PWDNOUSERNAME>
    <PWDNOEMAIL>TRUE</PWDNOEMAIL>

    <!-- Server Information -->
    <ServerName>SERVER-NAME</ServerName>
    <IPAddressList>
      <IPAddress>fe80::7e61:e3cf:4b41:b576%10</IPAddress>
      <IPAddress>192.168.1.100</IPAddress>
    </IPAddressList>
    <WarehousePaths>
      <wh whno="00" path="C:\websites\example.com\WH\00" />
      <wh whno="01" path="C:\websites\example.com\WH\01" />
      ...
      <wh whno="99" path="C:\websites\example.com\WH\99" />
    </WarehousePaths>
  </PARAMETERS>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Public Parameters

These parameters are returned for all authenticated users.

| Parameter | Type | Description |
|-----------|------|-------------|
| `WEBDAV` | TRUE/FALSE | Whether WebDAV protocol is enabled |
| `ALLOWEMAILATTACHMENTS` | TRUE/FALSE | Whether email attachments are allowed |
| `ATTACHMENTSIZELIMIT` | integer | Maximum attachment size in bytes (0 = unlimited) |
| `APPLICATIONURL` | string | Base URL of the infoRouter application |
| `SYSTEMEMAILADDRESS` | string | System email address used for notifications |
| `INDEXSRV` | TRUE/FALSE | Whether full-text search indexing is enabled |
| `SEARCHPAGESIZE` | integer | Default number of results per search page |
| `FILEUPLOADLIMIT` | long | Maximum file upload size in bytes |
| `ALLOWPARTIALEMAILUPLOADS` | TRUE/FALSE | Whether partial email uploads are allowed |

## Administrator-Only Parameters

These additional parameters are returned only when the authenticated user is a system administrator.

### System Settings

| Parameter | Type | Description |
|-----------|------|-------------|
| `INDEXCATALOG` | string | Name of the search index catalog |
| `LOGLOGINS` | TRUE/FALSE | Whether user logins are logged |
| `FILEUPLOADTIMEOUT` | integer | File upload timeout in seconds |
| `ALLOWOWNERSHIPTRANSFER` | TRUE/FALSE | Whether document ownership transfer is allowed |
| `SUBSCRIPTIONNOTIFICATIONS` | TRUE/FALSE | Whether subscription email notifications are enabled |
| `SENDEMAIL` | TRUE/FALSE | Whether the Send To email feature is enabled |
| `SENDTO_DISPLAYUSERLIST` | TRUE/FALSE | Whether to display the user list in Send To dialog |

### SMTP Configuration

| Parameter | Type | Description |
|-----------|------|-------------|
| `SMTPSERVER` | string | SMTP server hostname |
| `SMTPSERVERPORT` | integer | SMTP server port number |
| `SMTPCONNECTIONTIMEOUT` | integer | SMTP connection timeout in seconds |
| `SMTPSENDUSERNAME` | string | SMTP authentication username |
| `SMTPSENDPASSWORD` | string | Always returns `****` (masked for security) |

### Password Policy

| Parameter | Type | Description |
|-----------|------|-------------|
| `PWDMINLEN` | integer | Minimum password length |
| `PWDALPHA` | TRUE/FALSE | Password must include alphabetic characters |
| `PWDNUM` | TRUE/FALSE | Password must include numeric characters |
| `PWDEXPIRES` | integer | Password expiration period in days |
| `PWDWEAKLIST` | TRUE/FALSE | Password must not be in common password list |
| `PWDNONALPHA` | TRUE/FALSE | Password must include non-alphanumeric characters |
| `PWDNOUSERNAME` | TRUE/FALSE | Password must not equal the username |
| `PWDNOEMAIL` | TRUE/FALSE | Password must not equal the email address |

### Server Information

| Parameter | Type | Description |
|-----------|------|-------------|
| `ServerName` | string | Server machine name |
| `IPAddressList` | element | List of `IPAddress` elements with server IP addresses |
| `WarehousePaths` | element | List of `wh` elements with warehouse path mappings (`whno` and `path` attributes) |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- Anonymous users receive public parameters only
- Regular users receive public parameters only
- System administrators receive the full parameter set including sensitive configuration

## Example Requests

### Request (GET)

```
GET /srv.asmx/getApplicationParameters?AuthenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/getApplicationParameters HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/getApplicationParameters"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getApplicationParameters xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
    </getApplicationParameters>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getApplicationParameters() {
    const ticket = getUserAuthTicket();

    const url = `/srv.asmx/getApplicationParameters?AuthenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const params = xmlDoc.querySelector("PARAMETERS");

        return {
            webDav: params.querySelector("WEBDAV").textContent === "TRUE",
            allowEmailAttachments: params.querySelector("ALLOWEMAILATTACHMENTS").textContent === "TRUE",
            attachmentSizeLimit: parseInt(params.querySelector("ATTACHMENTSIZELIMIT").textContent),
            applicationUrl: params.querySelector("APPLICATIONURL").textContent,
            systemEmailAddress: params.querySelector("SYSTEMEMAILADDRESS").textContent,
            indexSrv: params.querySelector("INDEXSRV").textContent === "TRUE",
            searchPageSize: parseInt(params.querySelector("SEARCHPAGESIZE").textContent),
            fileUploadLimit: parseInt(params.querySelector("FILEUPLOADLIMIT").textContent),
            allowPartialEmailUploads: params.querySelector("ALLOWPARTIALEMAILUPLOADS").textContent === "TRUE"
        };
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function configureApplication() {
    try {
        const params = await getApplicationParameters();

        const maxSizeMB = params.fileUploadLimit / 1024 / 1024;
        console.log(`Max upload size: ${maxSizeMB} MB`);
        console.log(`WebDAV enabled: ${params.webDav}`);
        console.log(`Search page size: ${params.searchPageSize}`);

        // Configure uploader component
        uploader.setMaxFileSize(params.fileUploadLimit);

    } catch (error) {
        console.error("Failed to get application parameters:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = client.getApplicationParameters(authTicket);

        var root = XElement.Parse(response.ToString());
        if (root.Attribute("success")?.Value == "true")
        {
            var parameters = root.Element("PARAMETERS");

            var config = new
            {
                WebDav = parameters.Element("WEBDAV")?.Value == "TRUE",
                FileUploadLimit = long.Parse(parameters.Element("FILEUPLOADLIMIT")?.Value ?? "0"),
                SearchPageSize = int.Parse(parameters.Element("SEARCHPAGESIZE")?.Value ?? "50"),
                ApplicationUrl = parameters.Element("APPLICATIONURL")?.Value,
                IndexSrv = parameters.Element("INDEXSRV")?.Value == "TRUE"
            };

            Console.WriteLine($"Max Upload Size: {config.FileUploadLimit / 1024 / 1024} MB");
            Console.WriteLine($"WebDAV Enabled: {config.WebDav}");
            Console.WriteLine($"Application URL: {config.ApplicationUrl}");
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

- **SMTPSENDPASSWORD** is always returned as `****` for security. The actual password is never exposed through this API.
- **WarehousePaths** contains 100 warehouse path entries (00 through 99), each mapping to a physical storage directory.
- **IPAddressList** includes both IPv4 and IPv6 addresses of the server.
- **FILEUPLOADLIMIT** is in bytes. The default maximum is approximately 1 GB (1072693248 bytes).
- **ATTACHMENTSIZELIMIT** of 0 means no size limit for email attachments.
- **PWDEXPIRES** value is in days. A value of 0 means passwords never expire.
- The method name uses camelCase (`getApplicationParameters`) unlike most other APIs that use PascalCase. This is a legacy naming convention maintained for backward compatibility.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |

## Related APIs

- `GetGeneralAppSettings` - Get detailed general application settings with structured response
- `SetGeneralAppSettings` - Update general application settings
- `GetAuthenticationAndPasswordPolicy` - Get detailed authentication and password policy settings
- `SetAuthenticationAndPasswordPolicy` - Update authentication and password policy
- `GetSystemBehaviorSettings` - Get system behavior configuration
- `SetSystemBehaviorSettings` - Update system behavior settings

## Version History

- Compatible with infoRouter 8.0 and later
- Response format uses flat XML elements within a `PARAMETERS` container
- Administrator-only parameters are conditionally included based on user role
