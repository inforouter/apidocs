# SetAuthenticationAndPasswordPolicy API

Updates the authentication and password policy settings by sending a serialized `AuthenticationAndPasswordPolicy` object. This API allows you to configure password complexity rules, expiration policies, and actions that require password re-confirmation.

## Endpoint

```
/srv.asmx/SetAuthenticationAndPasswordPolicy
```

## Methods

- **GET** `/srv.asmx/SetAuthenticationAndPasswordPolicy?authenticationTicket=...&settingsXml=...`
- **POST** `/srv.asmx/SetAuthenticationAndPasswordPolicy` (form data)
- **SOAP** Action: `http://tempuri.org/SetAuthenticationAndPasswordPolicy`

> The `settingsXml` value must contain the `AuthenticationAndPasswordPolicy` XML. Always URL-encode the XML when calling the GET endpoint.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Ticket returned by `AuthenticateUser`. The caller must have `UpdateApplicationSettingsAndPolicies` admin permission. |
| `settingsXml` | string | Yes | XML representation of the `AuthenticationAndPasswordPolicy` object. Obtain the current structure via `GetAuthenticationAndPasswordPolicy`, update the desired values, then submit the modified XML here. |

## Response

### Success

```xml
<root success="true" />
```

### Error

```xml
<root success="false" error="[ErrorCode] Error message" />
```

Typical errors:
- `[2730]` when the user is not authenticated
- Admin permission error when the user lacks `UpdateApplicationSettingsAndPolicies` permission
- `Invalid settings XML format` when the payload cannot be deserialized
- The message returned by `UpdateAuthenticationAndPasswordPolicySettings` (for validation failures)

## Required Permissions

- `UpdateApplicationSettingsAndPolicies` admin permission
- Only authenticated administrators can invoke this method

## Example (REST POST)

```
POST /srv.asmx/SetAuthenticationAndPasswordPolicy HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=6F9C2A...&
settingsXml=%3CAuthenticationAndPasswordPolicy%3E...%3C%2FAuthenticationAndPasswordPolicy%3E
```

### SOAP Request

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/SetAuthenticationAndPasswordPolicy"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetAuthenticationAndPasswordPolicy xmlns="http://tempuri.org/">
      <authenticationTicket>6F9C2A...</authenticationTicket>
      <settingsXml><![CDATA[
        <AuthenticationAndPasswordPolicy>
          <PasswordPolicy>
            <Expires>90</Expires>
            <MinLen>8</MinLen>
            <MustIncludeAlphaNumericCharacters>true</MustIncludeAlphaNumericCharacters>
            <MustIncludeNumericCharacters>true</MustIncludeNumericCharacters>
            <MustIncludeNonAlphaNumericCharacters>true</MustIncludeNonAlphaNumericCharacters>
            <MustNotEqualEmailAddress>true</MustNotEqualEmailAddress>
            <MustNotEqualUserName>true</MustNotEqualUserName>
            <MustNotInCommonPasswordList>true</MustNotInCommonPasswordList>
          </PasswordPolicy>
          <PasswordRePromptActions>
            <DomainDelete>true</DomainDelete>
            <OnDelete>true</OnDelete>
            <UserDelete>true</UserDelete>
            <SecurityApply>true</SecurityApply>
            <OnOwnerChange>true</OnOwnerChange>
            <OnClassify>false</OnClassify>
            <OnReviewTask>false</OnReviewTask>
          </PasswordRePromptActions>
        </AuthenticationAndPasswordPolicy>
      ]]></settingsXml>
    </SetAuthenticationAndPasswordPolicy>
  </soap:Body>
</soap:Envelope>
```

## Sample `settingsXml` Payload

```xml
<AuthenticationAndPasswordPolicy>
  <PasswordPolicy>
    <Expires>90</Expires>
    <MinLen>8</MinLen>
    <MustIncludeAlphaNumericCharacters>true</MustIncludeAlphaNumericCharacters>
    <MustIncludeNumericCharacters>true</MustIncludeNumericCharacters>
    <MustIncludeNonAlphaNumericCharacters>true</MustIncludeNonAlphaNumericCharacters>
    <MustNotEqualEmailAddress>true</MustNotEqualEmailAddress>
    <MustNotEqualUserName>true</MustNotEqualUserName>
    <MustNotInCommonPasswordList>true</MustNotInCommonPasswordList>
  </PasswordPolicy>
  <PasswordRePromptActions>
    <DomainDelete>true</DomainDelete>
    <OnDelete>true</OnDelete>
    <UserDelete>true</UserDelete>
    <SecurityApply>true</SecurityApply>
    <OnOwnerChange>true</OnOwnerChange>
    <OnClassify>false</OnClassify>
    <OnReviewTask>false</OnReviewTask>
  </PasswordRePromptActions>
</AuthenticationAndPasswordPolicy>
```

## AuthenticationAndPasswordPolicy Structure

### PasswordPolicy Properties

| Property | Type | Description |
|----------|------|-------------|
| `Expires` | integer | Password expiration in days (0 = never expires) |
| `MinLen` | short | Minimum password length (1-14 characters) |
| `MustIncludeAlphaNumericCharacters` | boolean | Require alphabetic characters |
| `MustIncludeNumericCharacters` | boolean | Require numeric characters |
| `MustIncludeNonAlphaNumericCharacters` | boolean | Require special characters (!@#$%^&*) |
| `MustNotEqualEmailAddress` | boolean | Password cannot equal user's email |
| `MustNotEqualUserName` | boolean | Password cannot equal username |
| `MustNotInCommonPasswordList` | boolean | Reject common/weak passwords |

### PasswordRePromptActions Properties

| Property | Type | Description |
|----------|------|-------------|
| `DomainDelete` | boolean | Re-prompt password when deleting a domain |
| `OnDelete` | boolean | Re-prompt password when deleting items |
| `UserDelete` | boolean | Re-prompt password when deleting users |
| `SecurityApply` | boolean | Re-prompt password when applying security |
| `OnOwnerChange` | boolean | Re-prompt password when changing ownership |
| `OnClassify` | boolean | Re-prompt password when classifying documents |
| `OnReviewTask` | boolean | Re-prompt password on review tasks |

## Usage Guidelines

1. Call `GetAuthenticationAndPasswordPolicy` to retrieve the current settings
2. Modify only the values you need to change; keep the structure intact
3. Validate business rules:
   - Password expiration: 0 or positive integer (days)
   - Minimum length: 1-14 characters
   - At least one complexity requirement should be enabled
4. Submit the updated XML via `SetAuthenticationAndPasswordPolicy`
5. Settings take effect immediately for new password changes

## Notes

- **Password Expiration**: Set to `0` to disable password expiration
- **Minimum Length**: Automatically clamped to range 1-14
- **Complexity Requirements**: Multiple requirements can be enabled simultaneously for stronger security
- **Re-Prompt Actions**: Controls which administrative actions require password re-confirmation for security
- **Existing Users**: Changes do not force existing users to change passwords immediately
- **Next Password Change**: New policy applies when users change their passwords
- Settings are stored in the database and automatically refreshed in memory cache
- Audit logging should be handled at the application level

## Security Recommendations

### Strong Password Policy Example
```xml
<PasswordPolicy>
  <Expires>90</Expires>
  <MinLen>12</MinLen>
  <MustIncludeAlphaNumericCharacters>true</MustIncludeAlphaNumericCharacters>
  <MustIncludeNumericCharacters>true</MustIncludeNumericCharacters>
  <MustIncludeNonAlphaNumericCharacters>true</MustIncludeNonAlphaNumericCharacters>
  <MustNotEqualEmailAddress>true</MustNotEqualEmailAddress>
  <MustNotEqualUserName>true</MustNotEqualUserName>
  <MustNotInCommonPasswordList>true</MustNotInCommonPasswordList>
</PasswordPolicy>
```

### Critical Operations Protection
```xml
<PasswordRePromptActions>
  <DomainDelete>true</DomainDelete>
  <OnDelete>true</OnDelete>
  <UserDelete>true</UserDelete>
  <SecurityApply>true</SecurityApply>
  <OnOwnerChange>true</OnOwnerChange>
  <!-- Less critical operations -->
  <OnClassify>false</OnClassify>
  <OnReviewTask>false</OnReviewTask>
</PasswordRePromptActions>
```

## Related APIs

- `GetAuthenticationAndPasswordPolicy` - Retrieve current policy settings
- `GetSystemBehaviorSettings` - Get login logging and delay settings
- `SetSystemBehaviorSettings` - Update system behavior settings
- `ChangeUserPassword` - Change a user's password
- `CreateUser` - Create new user with password

## Integration Example (C#)

```csharp
using System.Xml.Linq;
using System.Xml.Serialization;

// Get current policy
var getPolicyResponse = await client.GetAuthenticationAndPasswordPolicyAsync(authTicket);
var currentPolicy = DeserializePolicy(getPolicyResponse);

// Modify policy
currentPolicy.PasswordPolicy.Expires = 90;
currentPolicy.PasswordPolicy.MinLen = 12;
currentPolicy.PasswordPolicy.MustIncludeNumericCharacters = true;
currentPolicy.PasswordPolicy.MustIncludeNonAlphaNumericCharacters = true;

// Serialize to XML
var serializer = new XmlSerializer(typeof(AuthenticationAndPasswordPolicy));
string settingsXml;
using (var writer = new StringWriter())
{
    serializer.Serialize(writer, currentPolicy);
    settingsXml = writer.ToString();
}

// Update policy
var updateResponse = await client.SetAuthenticationAndPasswordPolicyAsync(
    authTicket,
    settingsXml
);

if (updateResponse.Root.Attribute("success")?.Value == "true")
{
    Console.WriteLine("Password policy updated successfully");
}
else
{
    var error = updateResponse.Root.Attribute("error")?.Value;
    Console.WriteLine($"Error updating policy: {error}");
}
```

## Version History

- Compatible with infoRouter 8.7 and later
- `AuthenticationAndPasswordPolicy` is serializable for XML transport
- Supports both SOAP and REST endpoints
- Requires Workflow and Security modules for full functionality
