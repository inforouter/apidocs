---
search:
  exclude: true
---

# GetSystemBehaviorSettings API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Returns the system behavior settings including login logging configuration, login delay (anti-brute-force) settings, and library manager policy editing permissions. This API is restricted to system administrators with the `UpdateApplicationSettingsAndPolicies` permission.

## Endpoint

```
/api/UIInternals/GetSystemBehaviorSettings
```

## Methods

- **GET** `/api/UIInternals/GetSystemBehaviorSettings?authenticationTicket=...`
- **POST** `/api/UIInternals/GetSystemBehaviorSettings` (form data)

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
| `LoginDelay` | integer | 0 | Delay in milliseconds added to every failed login response (successful logins are not delayed). 0–2000; values outside are clamped on save. |
| `AllowLibraryManagersToEditPolicy` | boolean | true | Whether library managers can view and edit the library policies (per-action rights and logging, via GetDomainPolicies/SetDomainPolicies) of the libraries they manage. It does not affect the password policy, which is system-wide and needs an administrator or Policy Manager. Default TRUE. |

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
GET /api/UIInternals/GetSystemBehaviorSettings?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /api/UIInternals/GetSystemBehaviorSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getSystemBehaviorSettings() {
    const ticket = getUserAuthTicket();
    const url = `/api/UIInternals/GetSystemBehaviorSettings?authenticationTicket=${encodeURIComponent(ticket)}`;

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

## Notes

- **LoginDelay**: Delay in milliseconds added to every failed login response (successful logins are not delayed). 0–2000; values outside are clamped on save.
- **LogLogins**: When enabled, successful logins are recorded in the audit log for security monitoring.
- **LogLoginAttempts**: When enabled, failed login attempts are recorded in the audit log, useful for detecting potential security threats.
- **AllowLibraryManagersToEditPolicy**: Whether library managers can view and edit the library policies (per-action rights and logging, via GetDomainPolicies/SetDomainPolicies) of the libraries they manage. It does not affect the password policy, which is system-wide and needs an administrator or Policy Manager. Default TRUE.
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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | a caller with no ticket |


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
