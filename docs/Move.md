# Move API

Moves a document or folder from the source path to the destination path. Both documents and folders can be moved in a single call. The destination path must specify the target location including the new name.

## Endpoint

```
/srv.asmx/Move
```

## Methods

- **GET** `/srv.asmx/Move?authenticationTicket=...&SourcePath=...&DestinationPath=...`
- **POST** `/srv.asmx/Move` (form data)
- **SOAP** Action: `http://tempuri.org/Move`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `SourcePath` | string | Yes | Full infoRouter path to the document or folder to move (e.g. `/Finance/Reports/Q1.pdf`). |
| `DestinationPath` | string | Yes | Full infoRouter path to the destination (e.g. `/Finance/Archive/Q1.pdf`). The destination folder must exist. |

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

The calling user must have:
- **Read** permission on the source item.
- **Delete** permission on the source item (to remove it from the source location).
- **Write** permission on the destination folder (to place the item there).

---

## Example

### GET Request (move a document)

```
GET /srv.asmx/Move
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &SourcePath=/Finance/Reports/Q1-2024.pdf
  &DestinationPath=/Finance/Archive/Q1-2024.pdf
HTTP/1.1
```

### GET Request (move a folder)

```
GET /srv.asmx/Move
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &SourcePath=/Finance/Reports
  &DestinationPath=/Finance/Archive/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/Move HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&SourcePath=/Finance/Reports/Q1-2024.pdf
&DestinationPath=/Finance/Archive/Q1-2024.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:Move>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:SourcePath>/Finance/Reports/Q1-2024.pdf</tns:SourcePath>
      <tns:DestinationPath>/Finance/Archive/Q1-2024.pdf</tns:DestinationPath>
    </tns:Move>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The destination folder must already exist before calling this API.
- The item name at the destination is determined by the last component of `DestinationPath`. You can effectively rename an item during the move by using a different name in the destination path.
- Moving a folder moves all its contents (subfolders and documents) as well.
- Checked-out documents within the folder may prevent the move operation.
- This API works for both documents and folders in a single call.

---

## Related APIs

- [Copy](Copy.md) - Copy a document or folder to a new location
- [CreateFolder](CreateFolder.md) - Create a target folder before moving
- [DeleteFolder](DeleteFolder.md) - Delete a folder
- [DeleteDocument](DeleteDocument.md) - Delete a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Source not found | The source path does not resolve to an existing document or folder. |
| Destination folder not found | The destination folder does not exist. |
| Access denied | The user does not have the required permissions. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/Move*
