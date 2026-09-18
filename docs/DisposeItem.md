# DisposeItem API

Disposes a document or folder by path per its active Retention and Disposition (R&D) schedule. The path type is auto-detected — document paths dispose the single document; folder paths recursively dispose all eligible documents within the folder and the folder itself.

## Endpoint

```
/srv.asmx/DisposeItem
```

## Methods

- **GET** `/srv.asmx/DisposeItem?authenticationTicket=...&path=...&disposeComments=...`
- **POST** `/srv.asmx/DisposeItem` (form data)
- **SOAP** Action: `http://tempuri.org/DisposeItem`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `path` | string | Yes | Full path of the document or folder to dispose |
| `disposeComments` | string | No | Disposition comment. Omit or pass empty string if not required. |

## Response

### Success Response (document, or folder with no per-item errors)

```xml
<root success="true" />
```

### Success Response (folder with per-item failures)

The operation completes but individual documents that could not be disposed are reported as `<log>` child elements:

```xml
<root success="true">
  <log>
    <item>document-name.pdf</item>
    <error>Document is checked out</error>
  </log>
</root>
```

### Error Response

```xml
<root success="false" error="Error message" errorCode="4000" />
```

## Required Permissions

The caller must have **Delete** permission on the document or folder. The item must have an active R&D schedule.

## Example

### Dispose a document (GET)

```
GET /srv.asmx/DisposeItem?authenticationTicket=abc123-def456&path=/Library/Records/contract.pdf&disposeComments=Retention+period+expired HTTP/1.1
```

### Dispose a folder (POST)

```
POST /srv.asmx/DisposeItem HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&path=/Library/Records/2020&disposeComments=7-year+retention+complete
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/DisposeItem"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DisposeItem xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <path>/Library/Records/2020</path>
      <disposeComments>7-year retention complete</disposeComments>
    </DisposeItem>
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

Carries out the disposition of a document or a folder whose disposition date has passed.

```javascript
const root = await call('DisposeItem', {
  authenticationTicket: ticket,
  path: '/Finance/Invoices/inv-1001.pdf',
  disposeComments: 'Disposed under FIN-001'
});
```

**An item can only be disposed once its disposition date has arrived**, and that date comes from the
schedule rather than from this call. A document with no disposition date - because it has no
schedule, because its schedule is permanent, or because the date is still in the future - is refused
`4000` with "no disposition date has been assigned to this document".

Where the date comes from is worth knowing before building against this:

- `RetentionTrigger="1"` (on create) computes the retention date from the document's creation date,
  and the disposition date from the end of retention. The shortest period the API accepts is one day,
  so a document created today cannot be disposed today.
- `RetentionTrigger="2"` (on cut off) computes nothing until the item has a cut-off date - and
  there is no operation that puts one on a document. `SetFolderCutoffDate` refuses a folder until
  everything inside it is already cut off, which nothing else in the API can do.

**The folder form answers MultiStatus when it could not do all of it.** It walks the contents and
logs one `<log><item>…</item><error>…</error></log>` per item it could not dispose; if there is at
least one, the answer is `success="false"` with `errorCode="2070"` and the log says what was
refused. Until 9.0 it reported `success="true"` even when that was every item in the folder, so a
caller branching on `success` concluded the work was done when nothing was.

```xml
<root success="false" errorCode="2070" error="MultiStatus">
  <log><item>inv-1001.pdf</item><error>No disposition date has been assigned to this document.</error></log>
  <log><item>Invoices</item><error>No disposition date has been assigned to this folder.</error></log>
</root>
```

`disposeComments` is declared optional, so an empty one reaches the operation.

## Notes

- Disposal is **permanent and irreversible** — items are purged, not moved to the Recycle Bin
- The path type is resolved automatically: document paths trigger single-document disposal; folder paths trigger recursive folder disposal
- If the path resolves to neither a document nor a folder, an error is returned
- For folder paths, per-item failures (checked-out documents, active workflows, etc.) do **not** abort the operation — they are reported as `<log>` child elements alongside `success="true"`
- A disposition log entry is written for each successfully disposed document (see `GetDispositionLog`)

## Related APIs

- [`SetDocumentRandDSchedule`](SetDocumentRandDSchedule.md) — Assign an R&D schedule to a document
- [`SetFolderRandDSchedule`](SetFolderRandDSchedule.md) — Assign an R&D schedule to a folder
- [`GetDispositionLog`](GetDispositionLog.md) — Get disposition log entries

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document and no folder at that path |
| `4000` | the item has no disposition date, or the date has not arrived |
| `4030` | the caller may not dispose it |
| *(none)* | the folder form reports `success="true"` even when every item inside was refused; read the `<log>` entries |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
