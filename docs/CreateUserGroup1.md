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
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
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

## Notes

- This API is identical to `CreateUserGroup` but adds the `showMembers` parameter to control member visibility
- When `DomainName` is empty or omitted, a global user group is created
- When `DomainName` is specified, a local user group is created within that domain/library
- The `showMembers` setting determines whether other users can see who belongs to this group
- Group names must be unique within their scope (global or domain-level)
