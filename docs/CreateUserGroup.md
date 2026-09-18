# CreateUserGroup API

Creates a new user group. If a domain/library name is specified, a local user group is created within that domain. If no domain name is provided, a global user group is created.

## Endpoint

```
/srv.asmx/CreateUserGroup
```

## Methods

- **GET** `/srv.asmx/CreateUserGroup?authenticationTicket=...&DomainName=...&GroupName=...`
- **POST** `/srv.asmx/CreateUserGroup` (form data)
- **SOAP** Action: `http://tempuri.org/CreateUserGroup`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `DomainName` | string | No | Name of the domain/library to create a local group in. Leave empty to create a global group. |
| `GroupName` | string | Yes | Name of the new user group |

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
GET /srv.asmx/CreateUserGroup?AuthenticationTicket=abc123-def456&DomainName=MyLibrary&GroupName=Reviewers HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/CreateUserGroup HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&DomainName=MyLibrary&GroupName=Reviewers
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/CreateUserGroup"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateUserGroup xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <DomainName>MyLibrary</DomainName>
      <GroupName>Reviewers</GroupName>
    </CreateUserGroup>
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

Creates a user group.

```javascript
// One that belongs to a library:
await call('CreateUserGroup', {
  authenticationTicket: ticket, DomainName: 'Finance', GroupName: 'Approvers'
});

// A global one, usable from every library:
await call('CreateUserGroup', {
  authenticationTicket: ticket, DomainName: '', GroupName: 'AllStaff'
});
```

A group belongs to a library when `DomainName` names one, and is **global** when `DomainName` is
left empty. The two live in different lists: `GetDomainGroups` and `GetLocalGroups` answer a
library's own groups, `GetGlobalGroups` the global ones.

## Notes

- When `DomainName` is empty or omitted, a global user group is created
- When `DomainName` is specified, a local user group is created within that domain/library
- This API does not include a `showMembers` parameter; members are hidden by default. Use `CreateUserGroup1` if you need to control member visibility.
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
