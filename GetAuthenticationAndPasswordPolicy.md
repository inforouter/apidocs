# GetAuthenticationAndPasswordPolicy API

Returns the authentication and password policy settings including password complexity requirements and password re-prompt actions.

## Endpoint

```
/srv.asmx/GetAuthenticationAndPasswordPolicy
```

## Methods

- **GET** `/srv.asmx/GetAuthenticationAndPasswordPolicy?authenticationTicket=...`
- **POST** `/srv.asmx/GetAuthenticationAndPasswordPolicy` (form data)
- **SOAP** Action: `http://tempuri.org/GetAuthenticationAndPasswordPolicy`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response


```xml
<response success="true">
  <AuthenticationAndPasswordPolicy>
    <PasswordPolicy>
      <Expires>90</Expires>
      <MinLen>8</MinLen>
      <MustIncludeAlphaNumericCharacters>true</MustIncludeAlphaNumericCharacters>
      <MustIncludeNumericCharacters>true</MustIncludeNumericCharacters>
      <MustIncludeNonAlphaNumericCharacters>false</MustIncludeNonAlphaNumericCharacters>
      <MustNotEqualEmailAddress>true</MustNotEqualEmailAddress>
      <MustNotEqualUserName>true</MustNotEqualUserName>
      <MustNotInCommonPasswordList>true</MustNotInCommonPasswordList>
    </PasswordPolicy>
    <PasswordRePromptActions>
      <DomainDelete>true</DomainDelete>
      <OnDelete>true</OnDelete>
      <UserDelete>true</UserDelete>
      <SecurityApply>true</SecurityApply>
      <OnOwnerChange>false</OnOwnerChange>
      <OnClassify>false</OnClassify>
      <OnReviewTask>false</OnReviewTask>
    </PasswordRePromptActions>
  </AuthenticationAndPasswordPolicy>
</response>
```


### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## AuthenticationAndPasswordPolicy Properties

| Property | Type | Admin Only | Description |
|----------|------|------------|-------------|
| `PasswordPolicy` | object | No | Password complexity and expiration settings |
| `PasswordRePromptActions` | object | No | Actions that require password re-confirmation |

**Admin Only**: Fields marked "Yes" are only populated for administrators with `UpdateApplicationSettingsAndPolicies` permission. Regular users receive default value (`false`).

## PasswordPolicy Properties

| Property | Type | Description |
|----------|------|-------------|
| `Expires` | integer | Password expiration in days (0 = never expires) |
| `MinLen` | short | Minimum password length (minimum: 1) |
| `MustIncludeAlphaNumericCharacters` | boolean | Password must contain both letters and numbers |
| `MustIncludeNumericCharacters` | boolean | Password must contain at least one number |
| `MustIncludeNonAlphaNumericCharacters` | boolean | Password must contain special characters (!@#$%^&*, etc.) |
| `MustNotEqualEmailAddress` | boolean | Password cannot be the same as the user's email address |
| `MustNotEqualUserName` | boolean | Password cannot be the same as the username |
| `MustNotInCommonPasswordList` | boolean | Password cannot be in the common/weak password list |

## PasswordRePromptActions Properties

| Property | Type | Description |
|----------|------|-------------|
| `DomainDelete` | boolean | Require password re-entry when deleting a domain |
| `OnDelete` | boolean | Require password re-entry when deleting documents/folders |
| `UserDelete` | boolean | Require password re-entry when deleting users |
| `SecurityApply` | boolean | Require password re-entry when applying security changes |
| `OnOwnerChange` | boolean | Require password re-entry when changing document/folder ownership |
| `OnClassify` | boolean | Require password re-entry when classifying documents |
| `OnReviewTask` | boolean | Require password re-entry when completing workflow review tasks |

## Required Permissions

- User must be authenticated (anonymous users cannot access this API)
- **Regular users**: Can access `PasswordPolicy` and `PasswordRePromptActions` fields with actual values; `LibraryManagersEditPolicy` is hidden (returns `false`)
- **Administrators** (with `UpdateApplicationSettingsAndPolicies` permission): Can access all fields with actual values

### Permission-Based Response

This API returns different data based on the user's permissions:

| Field | Regular Users | Administrators |
|-------|---------------|----------------|
| `LibraryManagersEditPolicy` | `false` (default) | Actual value |
| `PasswordPolicy` | Full object | Full object |
| `PasswordRePromptActions` | Full object | Full object |

**Note**: Regular users receive a default value for `LibraryManagersEditPolicy` to maintain a consistent response structure. The `PasswordPolicy` and `PasswordRePromptActions` objects are always returned with their actual values for all authenticated users, as these are needed for client-side password validation and security prompts.

## Use Cases

1. **Password Validation**
   - Validate password complexity before user registration
   - Display password requirements in change password forms
   - Client-side password strength validation

2. **Security Configuration**
   - Check if password re-prompt is required before sensitive operations
   - Implement appropriate confirmation dialogs

3. **Administration Dashboard**
   - Display current authentication policy
   - Monitor security configuration
   - Pre-populate policy settings forms

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetAuthenticationAndPasswordPolicy?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetAuthenticationAndPasswordPolicy HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetAuthenticationAndPasswordPolicy"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetAuthenticationAndPasswordPolicy xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetAuthenticationAndPasswordPolicy>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getAuthenticationAndPasswordPolicy() {
    const ticket = getUserAuthTicket();

    const url = `/srv.asmx/GetAuthenticationAndPasswordPolicy?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const policy = xmlDoc.querySelector("AuthenticationAndPasswordPolicy");
        const passwordPolicy = policy.querySelector("PasswordPolicy");
        const rePromptActions = policy.querySelector("PasswordRePromptActions");

        return {
            libraryManagersEditPolicy: policy.querySelector("LibraryManagersEditPolicy").textContent === "true",
            passwordPolicy: {
                expires: parseInt(passwordPolicy.querySelector("Expires").textContent),
                minLen: parseInt(passwordPolicy.querySelector("MinLen").textContent),
                mustIncludeAlphaNumeric: passwordPolicy.querySelector("MustIncludeAlphaNumericCharacters").textContent === "true",
                mustIncludeNumeric: passwordPolicy.querySelector("MustIncludeNumericCharacters").textContent === "true",
                mustIncludeNonAlphaNumeric: passwordPolicy.querySelector("MustIncludeNonAlphaNumericCharacters").textContent === "true",
                mustNotEqualEmail: passwordPolicy.querySelector("MustNotEqualEmailAddress").textContent === "true",
                mustNotEqualUserName: passwordPolicy.querySelector("MustNotEqualUserName").textContent === "true",
                mustNotInCommonList: passwordPolicy.querySelector("MustNotInCommonPasswordList").textContent === "true"
            },
            rePromptActions: {
                onDelete: rePromptActions.querySelector("OnDelete").textContent === "true",
                securityApply: rePromptActions.querySelector("SecurityApply").textContent === "true",
                onOwnerChange: rePromptActions.querySelector("OnOwnerChange").textContent === "true"
            }
        };
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example: Validate password against policy
function validatePassword(password, email, username, policy) {
    const errors = [];

    if (password.length < policy.passwordPolicy.minLen) {
        errors.push(`Password must be at least ${policy.passwordPolicy.minLen} characters`);
    }

    if (policy.passwordPolicy.mustIncludeNumeric && !/\d/.test(password)) {
        errors.push("Password must contain at least one number");
    }

    if (policy.passwordPolicy.mustIncludeNonAlphaNumeric && !/[^a-zA-Z0-9]/.test(password)) {
        errors.push("Password must contain at least one special character");
    }

    if (policy.passwordPolicy.mustNotEqualEmail && password.toLowerCase() === email.toLowerCase()) {
        errors.push("Password cannot be the same as your email address");
    }

    if (policy.passwordPolicy.mustNotEqualUserName && password.toLowerCase() === username.toLowerCase()) {
        errors.push("Password cannot be the same as your username");
    }

    return errors;
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetAuthenticationAndPasswordPolicyAsync(authTicket);

        var root = XElement.Parse(response.ToString());
        if (root.Attribute("success")?.Value == "true")
        {
            var policy = root.Element("AuthenticationAndPasswordPolicy");
            var passwordPolicy = policy.Element("PasswordPolicy");
            var rePromptActions = policy.Element("PasswordRePromptActions");

            var config = new
            {
                LibraryManagersEditPolicy = bool.Parse(policy.Element("LibraryManagersEditPolicy")?.Value ?? "false"),
                PasswordExpires = int.Parse(passwordPolicy.Element("Expires")?.Value ?? "0"),
                MinPasswordLength = int.Parse(passwordPolicy.Element("MinLen")?.Value ?? "1"),
                RequireSpecialChars = bool.Parse(passwordPolicy.Element("MustIncludeNonAlphaNumericCharacters")?.Value ?? "false"),
                RePromptOnDelete = bool.Parse(rePromptActions.Element("OnDelete")?.Value ?? "false")
            };

            Console.WriteLine($"Password expires in: {config.PasswordExpires} days");
            Console.WriteLine($"Minimum password length: {config.MinPasswordLength}");
            Console.WriteLine($"Require special characters: {config.RequireSpecialChars}");
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

- **PasswordExpires**: Value of 0 means passwords never expire. Otherwise, users must change their password after the specified number of days.
- **MinLen**: Minimum value is 1. Maximum recommended is 128 characters.
- **LibraryManagersEditPolicy**: When enabled, domain administrators can override the system password policy for their domain.
- **PasswordRePromptActions**: These settings enhance security by requiring users to re-enter their password before performing sensitive operations.

## Migration Note

**Login logging settings have been moved**: The following settings have been moved to the new `GetSystemBehaviorSettings` / `SetSystemBehaviorSettings` APIs:
- `LogLogins` - Whether to log successful login events
- `LogLoginAttempts` - Whether to log failed login attempts
- `LoginDelay` - Delay in milliseconds between login attempts

Use `GetSystemBehaviorSettings` to access these settings (requires admin permission).

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |

## Related APIs

- `GetSystemBehaviorSettings` - Get login logging and login delay settings (admin-only)
- `SetSystemBehaviorSettings` - Update login logging and login delay settings (admin-only)
- `GetGeneralAppSettings` - Get general application settings
- `getApplicationParameters` - Get basic application parameters
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- Compatible with infoRouter 8.7 and later
- **Current version**: Login logging settings (`LogLogins`, `LogLoginAttempts`, `LoginDelay`) have been moved to `SystemBehaviorSettings`
- Settings model is serializable for client-side deserialization
- Supports both synchronous SOAP and REST access patterns

## See Also

- Control Panel UI: `ApplicationSettingsApply.aspx` - Authentication and password policy configuration page
