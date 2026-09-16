# GetSystemStatistics API

Retrieves system-wide statistics including user counts, document counts, total document storage size, the number of checked-out documents, and the number of documents registered in the last 30, 60, and 90 days.

## Endpoint

```
/srv.asmx/GetSystemStatistics
```

## Methods

- **GET** `/srv.asmx/GetSystemStatistics?authenticationTicket=...`
- **POST** `/srv.asmx/GetSystemStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetSystemStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |

## Response

### Success Response
```xml
<root success="true">
  <SystemStatistics>
    <TotalUserCount>150</TotalUserCount>
    <ActiveUserCount>140</ActiveUserCount>
    <DisabledUserCount>10</DisabledUserCount>
    <TotalDocumentCount>25000</TotalDocumentCount>
    <TotalDocumentSize>10737418240</TotalDocumentSize>
    <TotalCheckedOutDocuments>12</TotalCheckedOutDocuments>
    <RegisteredDocumentsIn30Days>87</RegisteredDocumentsIn30Days>
    <RegisteredDocumentsIn60Days>210</RegisteredDocumentsIn60Days>
    <RegisteredDocumentsIn90Days>345</RegisteredDocumentsIn90Days>
  </SystemStatistics>
</root>
```

### Error Response
```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `TotalUserCount` | int | Total number of user accounts (active + disabled), excluding the system admin account |
| `ActiveUserCount` | int | Number of active (non-disabled) users (authors + read-only users) |
| `DisabledUserCount` | int | Number of disabled user accounts |
| `TotalDocumentCount` | int | Total number of documents stored in the system |
| `TotalDocumentSize` | long | Total size of all document versions in bytes |
| `TotalCheckedOutDocuments` | int | Number of documents currently checked out |
| `RegisteredDocumentsIn30Days` | int | Number of documents registered within the last 30 days |
| `RegisteredDocumentsIn60Days` | int | Number of documents registered within the last 60 days |
| `RegisteredDocumentsIn90Days` | int | Number of documents registered within the last 90 days |

## Required Permissions

The caller must have the **ViewServerStatus** admin permission.

## Example

### Request (GET)
```
GET /srv.asmx/GetSystemStatistics?authenticationTicket=abc123-...
```

### Request (POST)
```
POST /srv.asmx/GetSystemStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-...
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

Counts of users, documents and activity, under `<SystemStatistics>`. The user counts agree with
`GetLicenseInfo`.

```javascript
const root = await call('GetSystemStatistics', { authenticationTicket: ticket });
console.log(root.querySelector('TotalDocumentCount').textContent, 'documents');
```

## Notes

- `TotalUserCount` excludes the built-in system administrator account.
- `TotalDocumentSize` is calculated from the VERSIONS table and reflects the sum of all stored version sizes in bytes.
- `TotalCheckedOutDocuments` counts all documents currently locked for editing across all libraries.
- `RegisteredDocumentsIn30Days`, `RegisteredDocumentsIn60Days`, and `RegisteredDocumentsIn90Days` count documents whose `REGISTERDATE` falls within the last 30, 60, or 90 days respectively. Only documents in active libraries (`DOMAINTYPE=0`) are included; recycle bin documents are excluded.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller may not view server status - including a caller with no ticket |

