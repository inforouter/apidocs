# GetSignOnSettings API

Returns the sign-on settings in effect: the external authentication authorities, the OpenID Connect providers, the account sysadmin's password is also checked against, the trusted LDAP account, and whether a temporary sysadmin password is set. Secrets are never returned: a client secret only masked, the temporary password not at all. Administrators only. Read-only: the settings are changed in their file (see Notes).

## Endpoint

```
/srv.asmx/GetSignOnSettings
```

## Methods

- **GET** `/srv.asmx/GetSignOnSettings?authenticationTicket=...`
- **POST** `/srv.asmx/GetSignOnSettings` (form data)
- **SOAP** Action: `http://tempuri.org/GetSignOnSettings`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response

### Success Response
```xml
<response success="true" error="">
  <SignOnSettings>
    <AuthenticationAuthorities>
      <AuthenticationAuthority Name="LDAP1" Url="http://ldap-gw:8080/IRExternalAuthSrv.asmx" />
    </AuthenticationAuthorities>
    <OidcProviders>
      <OidcProvider Name="auth0" DisplayName="Sign in with Auth0" Authority="https://dev-x.us.auth0.com"
                    ClientId="MiykO4tiD6Ya" ClientSecret="********ZmOZg_11Uv" ClientSecretSet="true"
                    Scopes="openid profile email" UsernameClaim="preferred_username"
                    UsePkce="false" GetClaimsFromUserInfoEndpoint="true" />
    </OidcProviders>
    <SysadminCheckAccount>admin@LDAP1</SysadminCheckAccount>
    <TrustedLDAPAccount>svc-tickets@LDAP1</TrustedLDAPAccount>
    <SysadminTempPasswordSet>false</SysadminTempPasswordSet>
    <Warnings />
  </SignOnSettings>
</response>
```

| Element | Description |
|---------|-------------|
| `AuthenticationAuthorities` | The external authentication services. A user whose authentication source is an authority's `Name` signs in through the service at its `Url`. |
| `OidcProviders` | The OpenID Connect providers the sign-in page offers (see [GetSignInOptions](GetSignInOptions.md)). `ClientSecret` is masked: eight asterisks and the secret's last 10 characters, enough to tell which secret is in use (a secret shorter than 20 characters shows only its last half). `ClientSecretSet` says whether there is one. `Scopes` is space separated. The callback address registered with the provider is `/oidc/callback/{Name}`. |
| `SysadminCheckAccount` | `user@authority`. When set, sysadmin's password is also accepted when that authority accepts it for that account. Empty: not used. |
| `TrustedLDAPAccount` | `user@authority`. [CreateTicketforUser](CreateTicketforUser.md) callers sign in with this account's password. Empty: not used. |
| `SysadminTempPasswordSet` | Whether a temporary password is set for sysadmin. It is stored only as a salted hash and cannot be read back. |
| `Warnings` | Entries in the file that are not in use (a provider without a ClientId, a name listed twice, ...), and accounts naming an authority that is not listed. Empty when all is in use. |
| `SettingsProblem` | Present only when the file could not be read at all. Only infoRouter passwords are accepted until it is corrected. |

### Error Response
```xml
<response success="false" error="[ErrorCode] Error message" errorCode="4030" />
```

| errorCode | When |
|-----------|------|
| 4010 | No authentication ticket, or an invalid or expired one |
| 4030 | The user is not allowed to change application settings |

## Required Permissions

The `UpdateApplicationSettingsAndPolicies` administrative right (system administrators), the same as the other application settings APIs.

## Example

### Request (POST)
```
POST /srv.asmx/GetSignOnSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

## Notes

- The settings are kept in their own file, `config\signon-setting.json` in infoRouter's application folder, not in `appsettings.json`:

  ```json
  {
    "AuthenticationAuthorities": [ { "Name": "LDAP1", "Url": "http://ldap-gw:8080/IRExternalAuthSrv.asmx" } ],
    "OidcProviders": [ { "Name": "auth0", "DisplayName": "Sign in with Auth0", "Authority": "https://dev-x.us.auth0.com",
                         "ClientId": "...", "ClientSecret": "...", "Scopes": [ "openid", "profile", "email" ],
                         "UsernameClaim": "preferred_username", "UsePkce": false, "GetClaimsFromUserInfoEndpoint": true } ],
    "SysadminCheckAccount": "admin@LDAP1",
    "TrustedLDAPAccount": "svc-tickets@LDAP1",
    "SysadminTempPassword": "..."
  }
  ```

  Without the file only infoRouter's own passwords are accepted. An authority may also be written the 8.7 way, `AuthorityName` and `AuthorityUrl`.
- A `ClientSecret` typed into the file in plain text is encrypted in the file, and a `SysadminTempPassword` typed in plain text is replaced by its salted hash, when infoRouter reads it.
- Edit the file and call [FlushApplicationCache](FlushApplicationCache.md) to apply a change without a restart. OpenID Connect providers follow too: a new one can be signed in with at once, a changed one uses its new settings from its next sign-in, a removed one is no longer offered.
- Every sign-in with the temporary password is written to the error log, unless it is also sysadmin's own password. Remove `SysadminTempPassword` from the file once it is no longer needed.
- infoRouter 8.7 kept the authorities, `TrustedLDAPAccount`, `SysadminCheckAccount` and `SysadminTempPassword` in `web.config`; the upgrade to 9.0 moves them to this file.
- [GetSignInOptions](GetSignInOptions.md) returns the provider and authority names to everyone, and [GetApplicationParameters](getApplicationParameters.md) the authority names to administrators.
