# SetRdFreezeFlag API

Sets or clears the Retention and Disposition (R&D) freeze flag on a document or folder by path. When frozen, the item is excluded from automatic disposition processing. The path type is auto-detected — document paths update the single document; folder paths recursively update all eligible documents within the folder.

## Endpoint

```
/srv.asmx/SetRdFreezeFlag
```

## Methods

- **GET** `/srv.asmx/SetRdFreezeFlag?authenticationTicket=...&path=...&rdFreezeFlag=...&actionComment=...`
- **POST** `/srv.asmx/SetRdFreezeFlag` (form data)
- **SOAP** Action: `http://tempuri.org/SetRdFreezeFlag`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `path` | string | Yes | Full path of the document or folder |
| `rdFreezeFlag` | bool | Yes | `true` to freeze the item; `false` to unfreeze |
| `actionComment` | string | No | Optional comment describing the reason for the change |

## Response

### Success Response (document, or folder with no per-item errors)

```xml
<root success="true" />
```

### Success Response (folder with per-item failures)

The operation completes but individual items that could not be updated are reported as `<log>` child elements:

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

The caller must have appropriate access to the document or folder. The item must have an active R&D schedule.

## Example

### Freeze a document (GET)

```
GET /srv.asmx/SetRdFreezeFlag?authenticationTicket=abc123-def456&path=/Library/Records/contract.pdf&rdFreezeFlag=true&actionComment=Under+legal+hold HTTP/1.1
```

### Freeze a folder (POST)

```
POST /srv.asmx/SetRdFreezeFlag HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&path=/Library/Records/2020&rdFreezeFlag=true&actionComment=Annual+audit+hold
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/SetRdFreezeFlag"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetRdFreezeFlag xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <path>/Library/Records/2020</path>
      <rdFreezeFlag>true</rdFreezeFlag>
      <actionComment>Annual audit hold</actionComment>
    </SetRdFreezeFlag>
  </soap:Body>
</soap:Envelope>
```

## Notes

- The path type is resolved automatically: document paths update the single document; folder paths update all eligible documents within recursively
- For folder paths, per-item failures do **not** abort the operation — they are reported as `<log>` child elements alongside `success="true"`
- A freeze flag history log entry is written for each successfully updated item (see `GetRdFreezeLogs`)
- Setting `rdFreezeFlag=false` on an already-unfrozen item completes without error

## Related APIs

- [`GetRdFreezeLogs`](GetRdFreezeLogs.md) — Get the R&D freeze flag change history for a document or folder
- [`DisposeItem`](DisposeItem.md) — Dispose a document or folder by path
- [`GetAppliedRDScheduleLogs`](GetAppliedRDScheduleLogs.md) — Get history of R&D schedules applied to a document or folder
