# DeleteDocument API

Moves a document to the recycle bin. The document is not permanently removed -" it can be restored using `RestoreRecycleBinItem` or permanently purged using `PurgeRecycleBinItem`.

## Endpoint

```
/srv.asmx/DeleteDocument
```

## Methods

- **GET** `/srv.asmx/DeleteDocument?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/DeleteDocument` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path of the document to delete (e.g. `/MyLibrary/Reports/OldReport.pdf`). |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
```

---

## Required Permissions

The authenticated user must be the **document owner**, a **domain manager** of the containing library, or have **Delete** permission on the document or its parent folder.

---

## Example

### GET Request

```
GET /srv.asmx/DeleteDocument
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/MyLibrary/Reports/OldReport.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Reports/OldReport.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteDocument>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/MyLibrary/Reports/OldReport.pdf</tns:Path>
    </tns:DeleteDocument>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API moves the document to the **recycle bin**. The document is not permanently deleted and its content and metadata remain intact until explicitly purged.
- To restore a deleted document, use `RestoreRecycleBinItem`.
- To permanently remove a document from the recycle bin, use `PurgeRecycleBinItem`.
- To empty the entire recycle bin at once, use `EmptyRecycleBin`.
- A document that is currently **checked out** may still be deleted; the checkout state is cleared when it is moved to the recycle bin.
- Deleting a document shortcut (`.lnk` file) removes only the shortcut -" the original target document is unaffected.

---

## Related APIs

- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a document from the recycle bin
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a document from the recycle bin
- [EmptyRecycleBin](EmptyRecycleBin.md) - Permanently delete all items in the current user's recycle bin
- [GetRecycleBinContent](GetRecycleBinContent.md) - List documents currently in the recycle bin
- [DeleteFolder](DeleteFolder.md) - Move a folder to the recycle bin

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found` | The `Path` does not refer to an existing document. |

---
