# GetRdFreezeLogs API

Returns the R&D freeze flag change history for a document or folder by path. Each log entry records when the freeze flag was set or cleared, by whom, and with what comment. The path type is auto-detected.

## Endpoint

```
/srv.asmx/GetRdFreezeLogs
```

## Methods

- **GET** `/srv.asmx/GetRdFreezeLogs?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/GetRdFreezeLogs` (form data)
- **SOAP** Action: `http://tempuri.org/GetRdFreezeLogs`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `path` | string | Yes | Full path of the document or folder |

## Response

### Success Response

```xml
<root success="true">
  <log rdFreezeFlag="true" actionDate="2024-01-15T10:30:00.0000000" userId="42" userFullName="John Doe" actionComments="Legal hold" />
  <log rdFreezeFlag="false" actionDate="2024-03-01T09:00:00.0000000" userId="42" userFullName="John Doe" actionComments="" />
</root>
```

Returns an empty `<root success="true" />` if no log entries exist.

### Error Response

```xml
<root success="false" error="Error message" errorCode="4000" />
```

## Log Entry Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `rdFreezeFlag` | bool | `true` if the flag was set (frozen); `false` if cleared (unfrozen) |
| `actionDate` | ISO 8601 datetime | Date and time the change was made |
| `userId` | int | ID of the user who made the change |
| `userFullName` | string | Full name of the user who made the change |
| `actionComments` | string | Comment provided at the time of the change (may be empty) |

## Required Permissions

The caller must have read access to the document or folder.

## Example

### Get logs for a document (GET)

```
GET /srv.asmx/GetRdFreezeLogs?authenticationTicket=abc123-def456&path=/Library/Records/contract.pdf HTTP/1.1
```

### Get logs for a folder (POST)

```
POST /srv.asmx/GetRdFreezeLogs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&path=/Library/Records/2020
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetRdFreezeLogs"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetRdFreezeLogs xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <path>/Library/Records/contract.pdf</path>
    </GetRdFreezeLogs>
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

Reads an item's freeze and release history.

```javascript
const root = await call('GetRdFreezeLogs', {
  authenticationTicket: ticket,
  path: '/Finance/Invoices/inv-1001.pdf'
});

for (const entry of root.children) {
  console.log(entry.outerHTML);
}
```

**The root element is not the same on success and on failure.** A successful read answers `<root>`;
a failure answers `<response>`, like the rest of the API - the same split as
[GetAppliedRDScheduleLogs](GetAppliedRDScheduleLogs.md). An item that was never frozen answers an
empty `<root success="true" />`, and a call with no ticket is answered rather than refused.

## Notes

- The path type is resolved automatically: document paths return the document's log; folder paths return the folder's log
- Log entries are returned in the order stored; most recent entries are typically last
- `actionDate` is formatted as ISO 8601 with full precision

## Related APIs

- [`SetRdFreezeFlag`](SetRdFreezeFlag.md) — Set or clear the R&D freeze flag on a document or folder
- [`GetAppliedRDScheduleLogs`](GetAppliedRDScheduleLogs.md) — Get history of R&D schedules applied to a document or folder
- [`DisposeItem`](DisposeItem.md) — Dispose a document or folder by path

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document and no folder at that path |
| `4030` | the caller may not see it |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
