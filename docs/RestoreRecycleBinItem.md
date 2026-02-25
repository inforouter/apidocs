# RestoreRecycleBinItem API

Restores a single document or folder from the Recycle Bin back into the infoRouter folder hierarchy. The item is identified by its `Handler` value, which is obtained from `GetRecycleBinContent`. Optionally, a different target folder can be specified; if omitted the item is restored to its original location. Use this API to recover accidentally deleted content programmatically.

## Endpoint

```
/srv.asmx/RestoreRecycleBinItem
```

## Methods

- **GET** `/srv.asmx/RestoreRecycleBinItem?AuthenticationTicket=...&ItemHandler=...&RestorePath=...`
- **POST** `/srv.asmx/RestoreRecycleBinItem` (form data)
- **SOAP** Action: `http://tempuri.org/RestoreRecycleBinItem`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `ItemHandler` | string | Yes | Handler string identifying the recycled item to restore. Obtained from the `Handler` attribute returned by `GetRecycleBinContent`. Format: `D{id}` for a document (e.g. `D9871`), `F{id}` for a folder (e.g. `F4312`). Case-insensitive. |
| `RestorePath` | string | No | Full infoRouter path of the target folder to restore the item into (e.g. `/Finance/Archive`). If omitted or empty, the item is restored to its original location at the time it was deleted. The target folder must already exist and the caller must have create rights within it. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Access denied." />
```

---

## Required Permissions

- **Any authenticated user** may restore items they personally deleted (the item's `DeletedById` must match the calling user).
- **System administrators** may restore any item regardless of who deleted it.
- The calling user must also have **create document** (or **create folder**) rights in the target restore folder.

---

## Example

### GET Request -" restore to original location

```
GET /srv.asmx/RestoreRecycleBinItem
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &ItemHandler=D9871
HTTP/1.1
```

### GET Request -" restore to an alternate location

```
GET /srv.asmx/RestoreRecycleBinItem
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &ItemHandler=D9871
  &RestorePath=/Finance/Archive
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RestoreRecycleBinItem HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&ItemHandler=D9871
&RestorePath=/Finance/Archive
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RestoreRecycleBinItem>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:ItemHandler>D9871</tns:ItemHandler>
      <tns:RestorePath>/Finance/Archive</tns:RestorePath>
    </tns:RestoreRecycleBinItem>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Handler Source**: The `ItemHandler` value must be obtained from the `Handler` attribute of a recycled item returned by `GetRecycleBinContent` or `SearchRecycledItems`. Format is `D{id}` for documents and `F{id}` for folders.
- **Original Location**: When `RestorePath` is omitted or empty, the item is restored to the folder it was in when deleted. If that original folder no longer exists, an error is returned.
- **Alternate Location**: When `RestorePath` is provided, the item is placed in that folder instead of the original location. The path must resolve to an existing folder.
- **Name Conflict**: If an item with the same name already exists in the target folder, the restore may fail. Rename or move the conflicting item first.
- **Permissions at Target**: Even if the user owns the recycled item, they must have sufficient rights (create document or create folder) in the target restore folder.
- **Published Document Reset**: If the library requires a document type for publishing and the restored document has no document type assigned, the published version number is reset to 0 on restore.
- **Folder Restore**: Restoring a folder recursively restores all of its contained documents and sub-folders that were in the recycle bin as part of that folder deletion.
- **Invalid Handler**: If the `ItemHandler` string cannot be parsed or refers to an unsupported object type, `"Invalid ItemHandler"` is returned.

---

## Related APIs

- [GetRecycleBinContent](GetRecycleBinContent.md) - List recycled items (use to obtain the `Handler` value)
- [SearchRecycledItems](SearchRecycledItems.md) - Search for recycled items with filter criteria
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a single Recycle Bin item instead of restoring it
- [EmptyRecycleBin](EmptyRecycleBin.md) - Permanently delete all items in the current user's Recycle Bin

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid ItemHandler` | The `ItemHandler` string is empty, cannot be parsed, or refers to an unsupported object type. |
| `Document is no longer in the recycle bin.` | The document has already been purged or previously restored. |
| `Folder is no longer in the recycle bin.` | The folder has already been purged or previously restored. |
| `Access denied.` | The calling user did not delete this item and is not a system administrator. |
| `The original location no longer exists.` | `RestorePath` was not specified and the original folder has since been deleted. |
| `Target folder not found` | The specified `RestorePath` does not resolve to an existing folder. |
| `Insufficient rights` | The caller does not have create rights in the target restore folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
