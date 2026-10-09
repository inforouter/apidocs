# GetAllUsers3 API

Returns a list of users with paging, filtering and sorting, and one filter more than [GetAllUsers2](GetAllUsers2.md): the users who belong to no library.

A user who is not a member of any library, and is in no user group that is, can sign in and reach nothing. `membershipFilter=0` finds them.

## Endpoint

```
/srv.asmx/GetAllUsers3
```

## Methods

- **GET** `/srv.asmx/GetAllUsers3?authenticationTicket=...&startingRowNumber=...&numberOfRow=...&...&membershipFilter=...`
- **POST** `/srv.asmx/GetAllUsers3` (form data)
- **SOAP** Action: `http://tempuri.org/GetAllUsers3`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `startingRowNumber` | int | Yes | The first row to return, counted from `1`. `0` returns every row and `numberOfRow` is then not used. |
| `numberOfRow` | int | Yes | Number of rows per page. |
| `firstNameFilter` | string | No | Filter by first name. Empty for no filter. |
| `lastNameFilter` | string | No | Filter by last name. Empty for no filter. |
| `userNameFilter` | string | No | Filter by user name. Matched exactly, unless it contains `*`, which stands for any run of characters. Empty for no filter. |
| `emailFilter` | string | No | Filter by email address. Empty for no filter. |
| `authenticationSourceFilter` | string | No | Filter by authentication source. Empty for no filter. |
| `domainNameFilter` | string | No | The library that local users belong to. Empty for no filter. |
| `userStatusFilter` | int | Yes | `-1` no filter, `0` disabled, `1` enabled. |
| `userTypeFilter` | int | Yes | `-1` no filter, `1` author, `2` reader. |
| `sortBy` | int | Yes | Sort column, as in `GetAllUsers2`. |
| `sortAscending` | bool | Yes | `true` for ascending order. |
| `membershipFilter` | int | Yes | `-1` no filter: the call is then `GetAllUsers2`. `0` only the users who belong to no library. |

## Response

### Success Response

The response of [GetAllUsers2](GetAllUsers2.md): a `<users>` collection, and `totalusercount` on the root with the number of users all the filters match, not the number on the page.

```xml
<response success="true" error="" totalusercount="2">
  <users>
    <User Domain="" UserID="2101" FirstName="Ada" LastName="Byron" Email="abyron@example.com" UserName="abyron" ... />
    <User Domain="" UserID="2102" FirstName="Alan" LastName="Hope" Email="ahope@example.com" UserName="ahope" ... />
  </users>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The permissions of `GetAllUsers2`.

## Example

### Request (POST)

```
POST /srv.asmx/GetAllUsers3 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&startingRowNumber=1&numberOfRow=25&userStatusFilter=1&userTypeFilter=-1&sortBy=1&sortAscending=true&membershipFilter=0
```

## Notes

- **What "belongs to a library" means.** The user is a member of a library, or is in a user group that is a member of one. This is the rule the server uses to decide whether a user is a library member.
- **The built-in roles do not count.** Being in `[Administrators]` or another bracketed role group is not library membership; the system administrator account is listed if it is a member of no library.
- **Being a local user does not count by itself.** A user created in a library is listed if that library has not also been given the user as a member.
- **The other filters apply too.** `userStatusFilter=1` with `membershipFilter=0` returns the enabled users who belong to nothing.
- **Which groups are the cause.** [GetGlobalGroups](GetGlobalGroups.md) returns `MemberOfLibraryCount` for each group; a group with `0` gives its users no library.

## Related APIs

- [GetAllUsers2](GetAllUsers2.md) - The same list without the membership filter
- [GetGlobalGroups](GetGlobalGroups.md) - The global groups, with how many libraries each is a member of
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Make a user a member of a library
- [GetMembersWithoutAccess](GetMembersWithoutAccess.md) - Members of a library who cannot open its documents

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | `membershipFilter` is neither `-1` nor `0`, or `sortBy`, `userStatusFilter` or `userTypeFilter` is not a known value |
| `4010` | `[901]` the ticket is expired or unknown |
| `4030` | The caller may not list users |
