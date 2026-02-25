# SetSystemBehaviorSettings API

Updates the system behavior settings including login logging configuration and login delay (anti-brute-force) settings.

## Endpoint

```
/srv.asmx/SetSystemBehaviorSettings
```

## Methods

- **GET** `/srv.asmx/SetSystemBehaviorSettings?authenticationTicket=...&settingsXml=...`
- **POST** `/srv.asmx/SetSystemBehaviorSettings` (form data)
- **SOAP** Action: `http://tempuri.org/SetSystemBehaviorSettings`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `settingsXml` | string | Yes | XML representation of the SystemBehaviorSettings object |

## Request XML Structure

```xml
<SystemBehaviorSettings>
  <LogLogins>true</LogLogins>
  <LogLoginAttempts>true</LogLoginAttempts>
  <LoginDelay>500</LoginDelay>
  <AllowLibraryManagersToEditPolicy>false</AllowLibraryManagersToEditPolicy>

</SystemBehaviorSettings>
```

## SystemBehaviorSettings Properties

| Property | Type | Required | Description | Valid Range |
|----------|------|----------|-------------|-------------|
| `LogLogins` | boolean | Yes | Whether to log successful login events | `true` or `false` |
| `LogLoginAttempts` | boolean | Yes | Whether to log failed login attempts | `true` or `false` |
| `LoginDelay` | integer | Yes | Delay in milliseconds between login attempts | 0-2000 |
| `AllowLibraryManagersToEditPolicy` | boolean | Yes | Whether library managers can edit their domain's password policy | `true` or `false` |
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

- User must have `UpdateApplicationSettingsAndPolicies` admin permission
- Regular users will receive an access denied error

## Example Requests

### Request (GET)

```
GET /srv.asmx/SetSystemBehaviorSettings?authenticationTicket=abc123-def456&settingsXml=%3CSystemBehaviorSettings%3E%3CLogLogins%3Etrue%3C%2FLogLogins%3E%3CLogLoginAttempts%3Etrue%3C%2FLogLoginAttempts%3E%3CLoginDelay%3E500%3C%2FLoginDelay%3E%3C%2FSystemBehaviorSettings%3E HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/SetSystemBehaviorSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&settingsXml=<SystemBehaviorSettings><LogLogins>true</LogLogins><LogLoginAttempts>true</LogLoginAttempts><LoginDelay>500</LoginDelay></SystemBehaviorSettings>
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/SetSystemBehaviorSettings"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetSystemBehaviorSettings xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <settingsXml><![CDATA[<SystemBehaviorSettings>
      <LogLogins>true</LogLogins>
      <LogLoginAttempts>true</LogLoginAttempts>
      <LoginDelay>500</LoginDelay>
      <AllowLibraryManagersToEditPolicy>true</AllowLibraryManagersToEditPolicy>
      </SystemBehaviorSettings>]]></settingsXml>
    </SetSystemBehaviorSettings>
  </soap:Body>
</soap:Envelope>
```


## Workflow

1. **Get Current Settings**: Call `GetSystemBehaviorSettings` to retrieve current configuration
2. **Modify Settings**: Update the desired properties in the XML
3. **Apply Changes**: Call `SetSystemBehaviorSettings` with the updated XML
4. **Verify**: Call `GetSystemBehaviorSettings` again to confirm changes were applied

## Notes

- **LoginDelay**: Values outside the range 0-2000 will be automatically normalized:
  - Values less than 0 are set to 0
  - Values greater than 2000 are set to 2000
- **Immediate Effect**: Changes take effect immediately after a successful update
- **Cache Reset**: The settings cache is automatically reset after update
- **Audit Trail**: Consider enabling login logging for compliance and security monitoring

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[921]Insufficient rights` | User does not have admin permission |
| `Failed to deserialize settings XML` | Invalid XML structure |
| `Invalid settings XML format` | Malformed XML |

## Security Recommendations

1. **Enable Login Logging**: Enable both `LogLogins` and `LogLoginAttempts` for security compliance
2. **Set Login Delay**: A delay of 500-1000ms provides good protection against brute-force attacks without significantly impacting user experience
3. **Monitor Logs**: Regularly review login attempt logs for suspicious activity

## Related APIs

- `GetSystemBehaviorSettings` - Retrieve current system behavior settings
- `GetAuthenticationAndPasswordPolicy` - Get password policy and re-prompt actions
- `SetGeneralAppSettings` - Update general application settings
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Separated from AuthenticationAndPasswordPolicy for independent management
- Settings are admin-only for security reasons

## See Also

- Control Panel UI: `ApplicationSettingsApply.aspx` - System behavior configuration page
