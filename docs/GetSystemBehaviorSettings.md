# GetSystemBehaviorSettings API

Returns the system behavior settings including login logging configuration, login delay (anti-brute-force) settings, and library manager policy editing permissions. This API is restricted to system administrators with the `UpdateApplicationSettingsAndPolicies` permission.

## Endpoint

```
/srv.asmx/GetSystemBehaviorSettings
```

## Methods

- **GET** `/srv.asmx/GetSystemBehaviorSettings?authenticationTicket=...`
- **POST** `/srv.asmx/GetSystemBehaviorSettings` (form data)
- **SOAP** Action: `http://tempuri.org/GetSystemBehaviorSettings`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true">
  <SystemBehaviorSettings>
    <LogLogins>true</LogLogins>
    <LogLoginAttempts>true</LogLoginAttempts>
    <LoginDelay>500</LoginDelay>
    <AllowLibraryManagersToEditPolicy>false</AllowLibraryManagersToEditPolicy>
  </SystemBehaviorSettings>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## SystemBehaviorSettings Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `LogLogins` | boolean | false | Whether to log successful login events to the audit log |
| `LogLoginAttempts` | boolean | false | Whether to log failed login attempts to the audit log |
| `LoginDelay` | integer | 0 | Delay in milliseconds between login attempts (anti-brute-force protection). Range: 0-2000 |
| `AllowLibraryManagersToEditPolicy` | boolean | true | Whether library managers can edit their domain's password policy |

## Required Permissions

- Administrators only: User must have `UpdateApplicationSettingsAndPolicies` admin permission
- Non-admin users will receive an insufficient rights error

## Use Cases

1. **Security Monitoring Configuration**
   - Check current login logging configuration
   - Verify anti-brute-force settings are properly configured
   - Pre-populate admin settings forms

2. **Compliance Auditing**
   - Verify login logging is enabled for compliance requirements
   - Document security configuration

3. **Security Hardening**
   - Review and adjust login delay settings
   - Enable/disable login attempt logging

4. **Domain Management**
   - Check whether library managers are permitted to edit password policies for their domains

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetSystemBehaviorSettings?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetSystemBehaviorSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSystemBehaviorSettings"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSystemBehaviorSettings xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetSystemBehaviorSettings>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getSystemBehaviorSettings() {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetSystemBehaviorSettings?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const settings = xmlDoc.querySelector("SystemBehaviorSettings");
        return {
            logLogins: settings.querySelector("LogLogins").textContent === "true",
            logLoginAttempts: settings.querySelector("LogLoginAttempts").textContent === "true",
            loginDelay: parseInt(settings.querySelector("LoginDelay").textContent),
            allowLibraryManagersToEditPolicy: settings.querySelector("AllowLibraryManagersToEditPolicy").textContent === "true"
        };
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function displaySecuritySettings() {
    try {
        const settings = await getSystemBehaviorSettings();

        console.log(`Log logins: ${settings.logLogins}`);
        console.log(`Log login attempts: ${settings.logLoginAttempts}`);
        console.log(`Login delay: ${settings.loginDelay}ms`);
        console.log(`Library managers can edit policy: ${settings.allowLibraryManagersToEditPolicy}`);

    } catch (error) {
        console.error("Failed to get system behavior settings:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetSystemBehaviorSettingsAsync(authTicket);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            var settings = root.Element("SystemBehaviorSettings");
            var config = new
            {
                LogLogins = bool.Parse(settings.Element("LogLogins")?.Value ?? "false"),
                LogLoginAttempts = bool.Parse(settings.Element("LogLoginAttempts")?.Value ?? "false"),
                LoginDelay = int.Parse(settings.Element("LoginDelay")?.Value ?? "0"),
                AllowLibraryManagersToEditPolicy = bool.Parse(settings.Element("AllowLibraryManagersToEditPolicy")?.Value ?? "false")
            };

            Console.WriteLine($"Log logins: {config.LogLogins}");
            Console.WriteLine($"Log login attempts: {config.LogLoginAttempts}");
            Console.WriteLine($"Login delay: {config.LoginDelay}ms");
            Console.WriteLine($"Library managers can edit policy: {config.AllowLibraryManagersToEditPolicy}");
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

- **LoginDelay**: Introduces a delay between login attempts to prevent brute-force attacks. Value is in milliseconds and is clamped to the range 0-2000. Values above 2000 are automatically normalized to 2000.
- **LogLogins**: When enabled, successful logins are recorded in the audit log for security monitoring.
- **LogLoginAttempts**: When enabled, failed login attempts are recorded in the audit log, useful for detecting potential security threats.
- **AllowLibraryManagersToEditPolicy**: When enabled, library managers can modify the password policy for their own domain. Defaults to true.
- These settings are system-wide and affect all users.
- Settings are cached in memory with a 15-minute sliding expiration. Changes made via `SetSystemBehaviorSettings` reset the cache immediately.
- Changes to these settings require a call to `SetSystemBehaviorSettings`.

## Database Setting Keys

The following database keys in the `ApplicationSettings` table map to these properties:

| Database Key | Property | Default |
|--------------|----------|---------|
| `LOGLOGINS` | LogLogins | FALSE |
| `LOGLOGINATTEMPTS` | LogLoginAttempts | FALSE |
| `LOGINDELAY` | LoginDelay | 0 |
| `LIBMANAGERS_EDITPOLICY` | AllowLibraryManagersToEditPolicy | TRUE |

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | User does not have `UpdateApplicationSettingsAndPolicies` admin permission |

## Related APIs

- `SetSystemBehaviorSettings` - Update system behavior settings
- `GetAuthenticationAndPasswordPolicy` - Get password policy and authentication settings
- `SetAuthenticationAndPasswordPolicy` - Update password policy and authentication settings
- `GetGeneralAppSettings` - Get general application settings
- `SetGeneralAppSettings` - Update general application settings
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Separated from `AuthenticationAndPasswordPolicy` for independent management
- Settings are admin-only for security reasons
- Settings model is serializable for client-side deserialization

## See Also

- Control Panel UI: `ApplicationSettingsApply.aspx` - System behavior configuration page
