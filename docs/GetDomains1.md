# GetDomains1 API

Returns the list of domains/libraries, optionally with the managers of each one. It is [GetDomains](GetDomains.md) with one parameter, `withManagers`; with it, a list of libraries needs no [GetManagers](GetManagers.md) call per row.

## Endpoint

```
/srv.asmx/GetDomains1
```

## Methods

- **GET** `/srv.asmx/GetDomains1?authenticationTicket=...&withManagers=...`
- **POST** `/srv.asmx/GetDomains1` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomains1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `withManagers` | bool | Yes | `true` to include a `<Managers>` element in each `<domain>`. `false` returns exactly what `GetDomains` returns. |

## Response

### Success Response

The `<domains>` collection of [GetDomains](GetDomains.md), sorted by name. With `withManagers=true` every `<domain>` has a `<Managers>` element holding the `<User>` elements [GetManagers](GetManagers.md) returns for that library, sorted by user name. A library with no manager has an empty `<Managers />`.

```xml
<response success="true" error="">
  <domains>
    <domain DomainID="123" DomainName="Finance" AnonymousDomain="FALSE" IsArchive="FALSE" IsHidden="FALSE" WelcomeMessage="">
      <Managers>
        <User Domain="" UserID="2018" FirstName="Priya" LastName="Sharma" Email="psharma@example.com" UserName="psharma" ... />
        <User Domain="" UserID="2003" FirstName="Nancy" LastName="Kim" Email="nkim@example.com" UserName="nkim" ... />
      </Managers>
    </domain>
    <domain DomainID="456" DomainName="HR" AnonymousDomain="FALSE" IsArchive="FALSE" IsHidden="FALSE" WelcomeMessage="">
      <Managers />
    </domain>
  </domains>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The same as `GetDomains` for the list. With `withManagers=true` the caller must be an authenticated (not anonymous) user, the same rule `GetManagers` has.

## Example

### Request (POST)

```
POST /srv.asmx/GetDomains1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&withManagers=true
```

## Notes

- The managers of all the libraries are read with one query, whatever the number of libraries.
- Only libraries in the list get managers; a library the caller does not see in `GetDomains` is not revealed through its managers.

## Related APIs

- [GetDomains](GetDomains.md) - The list without managers
- [GetManagers](GetManagers.md) - The managers of one library
- [GetManagedDomainsByUser](GetManagedDomainsByUser.md) - The libraries one user manages

## Error Codes

| `errorCode` | When |
|---:|---|
| `4010` | `[901]` the ticket is expired or unknown, or `withManagers=true` was asked by an anonymous user |
