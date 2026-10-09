# GetAllDomainStatistics API

Returns the statistics of every domain/library in the caller's library list, in one call. Each entry is what [GetDomainStatistics](GetDomainStatistics.md) returns for one library, so a statistics page needs no call per library.

## Endpoint

```
/srv.asmx/GetAllDomainStatistics
```

## Methods

- **GET** `/srv.asmx/GetAllDomainStatistics?authenticationTicket=...`
- **POST** `/srv.asmx/GetAllDomainStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetAllDomainStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

## Response

### Success Response

A `<Libraries>` element with one `<LibraryStatistics>` per library, in the order of [GetDomains](GetDomains.md) (by name). `DomainId` and `DomainName` say which library an entry is of; the other elements are described in [GetDomainStatistics](GetDomainStatistics.md).

```xml
<response success="true" error="">
  <Libraries>
    <LibraryStatistics>
      <DomainId>123</DomainId>
      <DomainName>Finance</DomainName>
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
    <LibraryStatistics>
      <DomainId>456</DomainId>
      <DomainName>HR</DomainName>
      ...
    </LibraryStatistics>
  </Libraries>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

Any authenticated (not anonymous) user. The libraries are the ones `GetDomains` returns for the caller.

## Example

### Request (POST)

```
POST /srv.asmx/GetAllDomainStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

## Notes

- The numbers of each library are counted as `GetDomainStatistics` counts them, one library after the other, so the call takes as long as the libraries are many and large. It saves the request and sign-in per library, not the counting.
- Archived and hidden libraries are included when `GetDomains` lists them for the caller.

## Related APIs

- [GetDomainStatistics](GetDomainStatistics.md) - The statistics of one library
- [GetDomains](GetDomains.md) - The library list
- [GetAllWorkflowStatistics](GetAllWorkflowStatistics.md) - The statistics of every workflow in one call

## Error Codes

| `errorCode` | When |
|---:|---|
| `4010` | `[901]` the ticket is expired or unknown, or the caller is anonymous |
