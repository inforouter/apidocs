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
<root success="false" error="[ErrorCode] Error message" />
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
