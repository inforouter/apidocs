# GetDomainStatistics API

Returns statistics for the specified domain/library.

## Endpoint

```
/srv.asmx/GetDomainStatistics
```

## Methods

- **GET** `/srv.asmx/GetDomainStatistics?authenticationTicket=...&domainName=...`
- **POST** `/srv.asmx/GetDomainStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `domainName` | string | Yes | Name of the domain/library to get statistics for |

## Response

### Success Response

```xml
<root success="true">
  <LibraryStatistics>
    <FolderCount>78</FolderCount>
    <LocalUserCount>25</LocalUserCount>
    <LocalGroupCount>5</LocalGroupCount>
    <DocumentCount>1234</DocumentCount>
    <CheckedOutCount>56</CheckedOutCount>
    <MemberUserCount>100</MemberUserCount>
    <MemberGroupCount>10</MemberGroupCount>
    <WorkflowDefinitionCount>3</WorkflowDefinitionCount>
    <TotalDocumentSize>1073741824</TotalDocumentSize>
  </LibraryStatistics>
</root>
```

### LibraryStatistics Properties

| Property | Type | Description |
|----------|------|-------------|
| `FolderCount` | integer | Total number of folders in the domain |
| `LocalUserCount` | integer | Number of users created locally in this domain |
| `LocalGroupCount` | integer | Number of user groups created locally in this domain |
| `DocumentCount` | integer | Total number of documents in the domain |
| `CheckedOutCount` | integer | Number of documents currently checked out |
| `MemberUserCount` | integer | Number of users who are members of this domain |
| `MemberGroupCount` | integer | Number of user groups who are members of this domain |
| `WorkflowDefinitionCount` | integer | Number of workflow definitions in this domain |
| `TotalDocumentSize` | long | Total size of all documents in bytes |

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The caller must be an authenticated user. Anonymous users cannot access this API.

## Example

### Request (GET)

```
GET /srv.asmx/GetDomainStatistics?authenticationTicket=abc123-def456&domainName=MyLibrary HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetDomainStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&domainName=MyLibrary
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetDomainStatistics"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetDomainStatistics xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <domainName>MyLibrary</domainName>
    </GetDomainStatistics>
  </soap:Body>
</soap:Envelope>
```

### Response Example

```xml
<root success="true"
      documentCount="5432"
      checkedOutCount="12"
      folderCount="234"
      totalDocumentSize="2147483648"
      localUserCount="50"
      localGroupCount="8"
      memberUserCount="150"
      memberGroupCount="15"
      workflowDefinitionCount="5" />
```

## Notes

- The `totalDocumentSize` is returned in bytes. To convert to human-readable format:
  - Divide by 1024 for KB
  - Divide by 1048576 for MB
  - Divide by 1073741824 for GB
- `localUserCount` and `localGroupCount` refer to users/groups created within this domain
- `memberUserCount` and `memberGroupCount` include both local and global members assigned to this domain
- Statistics are calculated in real-time and may take longer for domains with large amounts of content
