# CreateUserGroup1 API

Creates a new user group with control over member visibility. If a domain/library name is specified, a local user group is created within that domain. If no domain name is provided, a global user group is created.

## Endpoint

```
/srv.asmx/CreateUserGroup1
```

## Methods

- **GET** `/srv.asmx/CreateUserGroup1?authenticationTicket=...&DomainName=...&GroupName=...&showMembers=...`
- **POST** `/srv.asmx/CreateUserGroup1` (form data)
- **SOAP** Action: `http://tempuri.org/CreateUserGroup1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `DomainName` | string | No | Name of the domain/library to create a local group in. Leave empty to create a global group. |
| `GroupName` | string | Yes | Name of the new user group |
| `showMembers` | bool | Yes | When `true`, group members are visible to other users. When `false`, group members are hidden. |

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Error message" errorCode="4000" />
```

## Required Permissions

The caller must have administrative privileges to create user groups. To create a local group, the caller must have management rights on the specified domain/library.

## Example

### Request (GET)

```
GET /srv.asmx/CreateUserGroup1?AuthenticationTicket=abc123-def456&DomainName=MyLibrary&GroupName=Reviewers&showMembers=true HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/CreateUserGroup1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&DomainName=MyLibrary&GroupName=Reviewers&showMembers=true
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/CreateUserGroup1"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateUserGroup1 xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <DomainName>MyLibrary</DomainName>
      <GroupName>Reviewers</GroupName>
      <showMembers>true</showMembers>
    </CreateUserGroup1>
  </soap:Body>
</soap:Envelope>
```

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

`CreateUserGroup` with the `showMembers` flag.

```javascript
await call('CreateUserGroup1', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  GroupName: 'Approvers',
  showMembers: true
});
```

> **The flag is stored inverted.** A group created with `showMembers=true` is read back by
> `GetUserGroup` as `public="False"`, and one created with `showMembers=false` as `public="True"` -
> which is also what plain `CreateUserGroup`, sending no flag at all, produces. Send the opposite of
> what you mean until this is fixed, or use `CreateUserGroup` and set the flag with
> `UpdateUserGroupName1`, which inverts it in the same direction.

A group belongs to a library when `DomainName` names one, and is **global** when `DomainName` is
left empty. The two live in different lists: `GetDomainGroups` and `GetLocalGroups` answer a
library's own groups, `GetGlobalGroups` the global ones.

## Notes

- This API is identical to `CreateUserGroup` but adds the `showMembers` parameter to control member visibility
- When `DomainName` is empty or omitted, a global user group is created
- When `DomainName` is specified, a local user group is created within that domain/library
- The `showMembers` setting determines whether other users can see who belongs to this group
- Group names must be unique within their scope (global or domain-level)

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not manage groups - including a caller with no ticket at all |
| `4041` | no library by that name |
| `4090` | a group of that name already exists |
| `4000` | the name uses a character object names may not have |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
