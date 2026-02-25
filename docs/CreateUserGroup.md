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

## Notes

- When `DomainName` is empty or omitted, a global user group is created
- When `DomainName` is specified, a local user group is created within that domain/library
- This API does not include a `showMembers` parameter; members are hidden by default. Use `CreateUserGroup1` if you need to control member visibility.
- Group names must be unique within their scope (global or domain-level)
