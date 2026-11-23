---
search:
  exclude: true
---

# SetSystemBehaviorSettings API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Updates the system behavior settings including login logging configuration and login delay (anti-brute-force) settings.

## Endpoint

```
/api/UIInternals/SetSystemBehaviorSettings
```

## Methods

- **GET** `/api/UIInternals/SetSystemBehaviorSettings?authenticationTicket=...&settingsXml=...`
- **POST** `/api/UIInternals/SetSystemBehaviorSettings` (form data)

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
| `LoginDelay` | integer | Yes | Delay in milliseconds added to every failed login response (successful logins are not delayed). Values outside 0–2000 are clamped on save. | 0-2000 |
| `AllowLibraryManagersToEditPolicy` | boolean | Yes | Whether library managers can view and edit the library policies (per-action rights and logging, via GetDomainPolicies/SetDomainPolicies) of the libraries they manage. It does not affect the password policy, which is system-wide and needs an administrator or Policy Manager. Default TRUE. | `true` or `false` |
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
GET /api/UIInternals/SetSystemBehaviorSettings?authenticationTicket=abc123-def456&settingsXml=%3CSystemBehaviorSettings%3E%3CLogLogins%3Etrue%3C%2FLogLogins%3E%3CLogLoginAttempts%3Etrue%3C%2FLogLoginAttempts%3E%3CLoginDelay%3E500%3C%2FLoginDelay%3E%3C%2FSystemBehaviorSettings%3E HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /api/UIInternals/SetSystemBehaviorSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&settingsXml=<SystemBehaviorSettings><LogLogins>true</LogLogins><LogLoginAttempts>true</LogLoginAttempts><LoginDelay>500</LoginDelay></SystemBehaviorSettings>
```

## Workflow

1. **Get Current Settings**: Call `GetSystemBehaviorSettings` to retrieve current configuration
2. **Modify Settings**: Update the desired properties in the XML
3. **Apply Changes**: Call `SetSystemBehaviorSettings` with the updated XML
4. **Verify**: Call `GetSystemBehaviorSettings` again to confirm changes were applied

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/api/UIInternals/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Takes what `GetSystemBehaviorSettings` returns, **once the root element is renamed**. The reader answers
under `<Value>`; this deserializes against `<SystemBehaviorSettings>`, so sending the reading back
untouched fails. Read, rename, change what you mean to change, send the whole document back:
anything left out goes back to its default rather than staying as it was.

```javascript
const current = await call('GetSystemBehaviorSettings', { authenticationTicket: ticket });

// the reader says <Value>, the writer wants <SystemBehaviorSettings>
const settings = current.querySelector('Value');
const renamed = document.createElementNS(null, 'SystemBehaviorSettings');
while (settings.firstChild) renamed.appendChild(settings.firstChild);

// ... change what you mean to change ...

await call('SetSystemBehaviorSettings', {
  authenticationTicket: ticket,
  settingsXml: new XMLSerializer().serializeToString(renamed)
});
```

## Notes

- **LoginDelay**: Values outside the range 0-2000 will be automatically normalized:
  - Values less than 0 are set to 0
  - Values greater than 2000 are set to 2000
- **Immediate Effect**: Changes take effect immediately after a successful update
- **Cache Reset**: The settings cache is automatically reset after update
- **Audit Trail**: Consider enabling login logging for compliance and security monitoring

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | a caller with no ticket, or one who may not update settings |
| `4000` | `settingsXml` is not well formed, or does not deserialize into the settings document |


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
