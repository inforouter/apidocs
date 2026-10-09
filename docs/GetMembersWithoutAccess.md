# GetMembersWithoutAccess API

Returns the members of a domain/library whose right on the library is below a minimum: by default, the members who cannot read its documents.

Membership of a library gives no right of its own. A member with no access list entry gets the **Library Members** entry, and a new library has that as **List**, so a user who is only made a member (by a bulk import, for instance) can see the library and open nothing in it. This call finds those users.

## Endpoint

```
/srv.asmx/GetMembersWithoutAccess
```

## Methods

- **GET** `/srv.asmx/GetMembersWithoutAccess?authenticationTicket=...&domainName=...&minimumRight=...`
- **POST** `/srv.asmx/GetMembersWithoutAccess` (form data)
- **SOAP** Action: `http://tempuri.org/GetMembersWithoutAccess`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | No | The library to look at. Empty looks at every library for a system administrator, and at the libraries the caller manages for anybody else. |
| `minimumRight` | int | Yes | Members below this right are returned. `0` or less means `2` (Read). See the values below. |

### Right Values

| Right | Name | Description |
|-------|------|-------------|
| `0` | `NOACCESS` | No Access |
| `1` | `LIST` | List |
| `2` | `READ` | Read |
| `3` | `ADD` | Add |
| `4` | `ADDREAD` | Add & Read |
| `5` | `CHANGE` | Change |
| `6` | `FULLCONTROL` | Full Control |

## Response

### Success Response

One `<domain>` per library looked at, sorted by name, each with one `<User>` per member below the minimum, sorted by user name. A library where every member has the minimum has an empty `<domain>`.

```xml
<response success="true" error="">
  <domains>
    <domain DomainID="123" DomainName="Finance">
      <User UserID="2018" UserName="psharma" FullName="Priya Sharma" EffectiveRight="1" RightName="LIST" Source="DomainMembers" IsManager="FALSE" />
      <User UserID="2003" UserName="nkim" FullName="Nancy Kim" EffectiveRight="0" RightName="NOACCESS" Source="Group" IsManager="FALSE" />
    </domain>
    <domain DomainID="456" DomainName="HR" />
  </domains>
</response>
```

### User Attributes

| Attribute | Description |
|-----------|-------------|
| `UserID`, `UserName`, `FullName` | The member. Members are the users who belong to the library directly or through a group that does. |
| `EffectiveRight` | The right the library's access list gives the member, `0` to `6`. |
| `RightName` | The same right by name. |
| `Source` | Which entry of the access list decided it: `Own` (the member's own entry), `Group` (a group the member is in), `DomainMembers` (the Library Members entry), or `None` (no entry applies, which is no access). |
| `IsManager` | `TRUE` when the member is a manager of the library. Managers are let in by library policy whatever the list says, so a row with `TRUE` is usually not a problem. |

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

System administrators, for any library. A library manager, for the libraries they manage.

## Example

### Request (POST)

```
POST /srv.asmx/GetMembersWithoutAccess HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&domainName=Finance&minimumRight=2
```

## Notes

- **How the right is worked out.** It is the rule every permission check uses: the member's own entry if there is one; otherwise the entries of the groups the member is in, where one group with No Access means no access and otherwise the highest wins; otherwise the Library Members entry. A group counts when it belongs to the library or is a member of it.
- **The library's own access list only.** The right is read from the access list of the library's root folder. A folder further down can have a list of its own that gives a member more, or less; those are not looked at.
- **Not the whole of what a user may do.** The owner of a folder or document, and the library's managers, are let in by library policy; `IsManager` marks the managers. Read-only users never get more than Read whatever the list gives them.
- **Cost.** The access list, the groups in it and their members are read once per library, not once per member.

## Related APIs

- [GetAccessList](GetAccessList.md) - The access list of a folder or document
- [SetAccessList](SetAccessList.md) - Change it, to give the members found here a right
- [GetDomainUsers](GetDomainUsers.md) - Every member of a library

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | `minimumRight` is greater than 6 |
| `4010` | `[901]` the ticket is expired or unknown, or the caller is anonymous |
| `4030` | The caller is neither an administrator nor a manager of the library named |
| `4041` | `domainName` is not a library the caller can see |
