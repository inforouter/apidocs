# GetCurrentUser API

Returns the properties of the currently authenticated user. This is a convenience wrapper around `GetUser` that does not require a `userName` parameter " the user is determined from the authentication ticket.

## Endpoint

```
/srv.asmx/GetCurrentUser
```

## Methods

- **GET** `/srv.asmx/GetCurrentUser?authenticationTicket=...`
- **POST** `/srv.asmx/GetCurrentUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetCurrentUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response

### Success Response

```xml
<root success="true">
  <User exists="true"
        UserID="42"
        FirstName="John"
        LastName="Smith"
        Email="jsmith@example.com"
        Enabled="TRUE"
        UserName="jsmith"
        Domain="MyLibrary"
        LastLogonDate="2026-02-15T10:30:00"
        LastPasswordChangeDate="2026-01-10T08:00:00"
        AuthenticationAuthority="Native"
        ReadOnlyUser="FALSE">
    <Preferences>
      <!-- User preferences -->
    </Preferences>
    <TaskRedirection>
      <!-- Task redirection settings -->
    </TaskRedirection>
  </User>
</root>
```

### Response Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `exists` | string | `true` if the user exists |
| `UserID` | int | Unique identifier of the user |
| `FirstName` | string | User's first name |
| `LastName` | string | User's last name |
| `Email` | string | User's email address |
| `Enabled` | string | `TRUE` if the user account is enabled, `FALSE` if disabled |
| `UserName` | string | User's login name |
| `Domain` | string | Domain/library the user belongs to |
| `LastLogonDate` | string | Date of last login (empty if never logged in) |
| `LastPasswordChangeDate` | string | Date of last password change (empty if never changed) |
| `AuthenticationAuthority` | string | Authentication source (e.g., `Native`, `LDAP`, `OAuth`) |
| `ReadOnlyUser` | string | `TRUE` if the user is a read-only (reader) user, `FALSE` otherwise |

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The caller must be authenticated. Anonymous users cannot call this API.

## Example

### Request (GET)

```
GET /srv.asmx/GetCurrentUser?authenticationTicket=abc123-def456 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetCurrentUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetCurrentUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCurrentUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetCurrentUser>
  </soap:Body>
</soap:Envelope>
```

## Notes

- This API internally calls the same logic as `GetUser` with the username resolved from the authentication ticket
- The response includes user preferences and task redirection settings in detail mode
- See also: `GetUser` to retrieve properties of any user by username
