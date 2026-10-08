# GetSignInOptions API

Returns what a user can sign in with on this server: the user name and password form, Windows authentication, anonymous access, the OpenID Connect providers and the authentication authorities. A sign-in page calls it to decide what to show.

## Endpoint

```
/srv.asmx/GetSignInOptions
```

## Methods

- **GET** `/srv.asmx/GetSignInOptions`
- **POST** `/srv.asmx/GetSignInOptions`
- **SOAP** Action: `http://tempuri.org/GetSignInOptions`

> This API does not require authentication. It is the call a sign-in page makes before anybody has signed in.

## Parameters

This API does not take any parameters.

## Response

### Success Response

```xml
<response success="true" error="">
  <SignInOptions PasswordSignIn="true" WindowsAuthentication="false" AnonymousAccess="true">
    <OidcProviders>
      <OidcProvider Name="AzureAD" DisplayName="Sign in with Microsoft" LoginUrl="/oidc/login/AzureAD" />
      <OidcProvider Name="okta" DisplayName="okta" LoginUrl="/oidc/login/okta" />
    </OidcProviders>
    <AuthenticationAuthorities>
      <AuthenticationAuthority Name="CORPLDAP" />
    </AuthenticationAuthorities>
  </SignInOptions>
</response>
```

A server with no single sign-on and no external authority returns the two lists empty:

```xml
<response success="true" error="">
  <SignInOptions PasswordSignIn="true" WindowsAuthentication="false" AnonymousAccess="false">
    <OidcProviders />
    <AuthenticationAuthorities />
  </SignInOptions>
</response>
```

### Error Response

```xml
<response success="false" error="Error message" />
```

## SignInOptions Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `PasswordSignIn` | boolean | Whether to show the user name and password form, which signs in with [AuthenticateUser](AuthenticateUser.md). Always `true` today; read it rather than assuming. |
| `WindowsAuthentication` | boolean | Whether Windows authentication is on. When `true`, offer a sign-in that calls [AuthenticateUserViaWindows](AuthenticateUserViaWindows.md). The same value as `WindowsAuthenticationIsOn` in [ServerInfo](ServerInfo.md). |
| `AnonymousAccess` | boolean | Whether this server allows anonymous access. When `true`, a guest entry can be offered. The same value as `AnonymousAccessIsOn` in [ServerInfo](ServerInfo.md). |

## OidcProvider Attributes

One `<OidcProvider>` for each OpenID Connect provider configured on the server, in the order they are configured.

| Attribute | Type | Description |
|-----------|------|-------------|
| `Name` | string | The provider's name in the server configuration. |
| `DisplayName` | string | What to show on the sign-in button, for example "Sign in with Microsoft". When the server has no display name for the provider this is the same as `Name`. |
| `LoginUrl` | string | Root-relative address that starts the sign-in with this provider. Send the browser there (a normal navigation, not a background request). An optional `returnUrl` query parameter, itself a root-relative address, says where to land afterwards. |

## AuthenticationAuthority Attributes

One `<AuthenticationAuthority>` for each external authentication authority configured on the server (for example an LDAP directory).

| Attribute | Type | Description |
|-----------|------|-------------|
| `Name` | string | The authority's name. It is the value stored as a user's authentication source. |

A sign-in page does not have to ask the user to choose an authority: the user types a user name and password, and the server checks them against the authority recorded on that user's account. The names are listed so a page can say which directories this server signs in with.

## Required Permissions

None. Anyone who can reach the server can call it, signed in or not.

## What Is Not Returned

Because the call needs no ticket, it returns names and sign-in links only. It never returns a provider's authority address, client id, client secret, scopes or claim settings, or the address of an authentication authority. A system administrator can read the authority names in [getApplicationParameters](getApplicationParameters.md) as well.

## Example

### Request (GET)

```
GET /srv.asmx/GetSignInOptions HTTP/1.1
Host: yourserver
```

### Request (POST)

```
POST /srv.asmx/GetSignInOptions HTTP/1.1
Host: yourserver
Content-Length: 0
```

### SOAP 1.1 Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSignInOptions xmlns="http://tempuri.org/" />
  </soap:Body>
</soap:Envelope>
```

## JavaScript

Builds the sign-in page's choices from the answer.

```javascript
const response = await fetch('/srv.asmx/GetSignInOptions');
const root = new DOMParser()
  .parseFromString(await response.text(), 'text/xml')
  .documentElement;

if (root.getAttribute('success') !== 'true') {
  throw new Error(root.getAttribute('error'));
}

const options = root.querySelector('SignInOptions');
const showPasswordForm = options.getAttribute('PasswordSignIn') === 'true';
const showWindowsSignIn = options.getAttribute('WindowsAuthentication') === 'true';
const showGuestEntry = options.getAttribute('AnonymousAccess') === 'true';

// One button per provider. Clicking it leaves the page for the provider's own sign-in.
const providers = [...options.querySelectorAll('OidcProvider')].map(p => ({
  label: p.getAttribute('DisplayName'),
  href: p.getAttribute('LoginUrl') + '?returnUrl=' + encodeURIComponent('/inforouter-doclib/')
}));
```

## Server Configuration

The providers and authorities come from the `AppSettings` section of the server's `appsettings.json`. `DisplayName` is optional; without it the provider's `Name` is shown.

```json
"OidcProviders": [
  {
    "Name": "AzureAD",
    "DisplayName": "Sign in with Microsoft",
    "Authority": "https://login.microsoftonline.com/your-tenant/v2.0",
    "ClientId": "...",
    "ClientSecret": "..."
  }
],
"AuthenticationAuthorities": [
  { "AuthorityName": "CORPLDAP", "AuthorityUrl": "http://authserver/irAuthenticationSrv.asmx" }
]
```

A change to these takes effect when the server is restarted.

## Notes

- Introduced in 9.0.
- The two lists are always present; an empty list means none is configured.
- `LoginUrl` includes the application's virtual path when the server runs under one.
- Windows authentication, anonymous access and each provider are independent: any combination can be on.

## Related APIs

- [AuthenticateUser](AuthenticateUser.md) - Sign in with a user name and password.
- [AuthenticateUserViaWindows](AuthenticateUserViaWindows.md) - Sign in with the Windows identity of the request.
- [ServerInfo](ServerInfo.md) - Server version and feature switches, also callable before sign-in.
- [getApplicationParameters](getApplicationParameters.md) - Application parameters, including the authority names for an administrator.

## Error Codes

This operation takes no ticket and no parameters, so it has no refusals of its own. A failure inside the server is answered with `success="false"` and the error text.
