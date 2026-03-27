# GetFoldersOwnedByUser API

Returns a paged list of folders owned by the specified user. Supports offset-based paging via `startingRow` and `rowCount`.

## Endpoint

```
/srv.asmx/GetFoldersOwnedByUser
```

## Methods

- **GET** `/srv.asmx/GetFoldersOwnedByUser?authenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetFoldersOwnedByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetFoldersOwnedByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | The username whose owned folders are to be retrieved. |
| `startingRow` | int | Yes | Zero-based row offset. Pass `0` to start from the first result. Pass `100` to skip the first 100 results. |
| `rowCount` | int | Yes | Number of rows to return (page size). |

---

## Required Permissions

| Scenario | Required permission |
|----------|---------------------|
| Caller queries their own folders | None — authenticated user only |
| Caller queries another user's folders | **ListingAuditLogOfUser** admin permission for the target user |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing zero or more `<folder>` child elements.

```xml
<response success="true">
  <folder id="42" name="Reports" path="\MyLibrary\Reports"
          domainid="1" ownerid="5" ownername="jsmith" ... />
  <folder id="43" name="Archive" path="\MyLibrary\Archive"
          domainid="1" ownerid="5" ownername="jsmith" ... />
</response>
```

### Folder Attribute Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | int | Unique folder identifier. |
| `name` | string | Folder name. |
| `path` | string | Full infoRouter path of the folder. |
| `domainid` | int | Internal ID of the library the folder belongs to. |
| `ownerid` | int | Internal user ID of the folder owner. |
| `ownername` | string | Username of the folder owner. |

Additional standard folder attributes are included based on system configuration.

### Empty Result

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Paging

Use `startingRow` and `rowCount` to page through large result sets.

| Goal | startingRow | rowCount |
|------|-------------|----------|
| First page of 50 | `0` | `50` |
| Second page of 50 | `50` | `50` |
| Rows 1001–1100 | `1000` | `100` |

`startingRow` is the number of records to **skip**. `rowCount` is the number of records to **return**.

---

## Example Requests

### GET — first page

```
GET /srv.asmx/GetFoldersOwnedByUser?authenticationTicket=abc123-def456&userName=jsmith&startingRow=0&rowCount=50 HTTP/1.1
Host: server.example.com
```

### GET — second page

```
GET /srv.asmx/GetFoldersOwnedByUser?authenticationTicket=abc123-def456&userName=jsmith&startingRow=50&rowCount=50 HTTP/1.1
Host: server.example.com
```

### POST

```
POST /srv.asmx/GetFoldersOwnedByUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith&startingRow=0&rowCount=50
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetFoldersOwnedByUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetFoldersOwnedByUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
      <startingRow>0</startingRow>
      <rowCount>50</rowCount>
    </GetFoldersOwnedByUser>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- `startingRow` is zero-based: `startingRow=0` returns from the first record, `startingRow=50` skips the first 50.
- To retrieve all folders without paging, pass `startingRow=0` and a sufficiently large `rowCount`.
- Ownership is determined by the folder owner field. Library root folders (domains) are not included.

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Insufficient rights.` | The caller does not have `ListingAuditLogOfUser` permission for the target user. |
| User not found | The specified `userName` does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## Related APIs

- [GetDocumentsOwnedByUser](GetDocumentsOwnedByUser.md) - Get a paged list of documents owned by a user
- [GetAuthoredDocuments](GetAuthoredDocuments.md) - Get documents authored (created) by a user
- [GetFoldersByUser](GetFoldersByUser.md) - Get folders accessible to a user
