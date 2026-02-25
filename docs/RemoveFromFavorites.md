# RemoveFromFavorites API

Removes the specified document or folder from the currently authenticated user's favorites list. If the item is not currently in the favorites list, the call completes successfully without making any changes.

## Endpoint

```
/srv.asmx/RemoveFromFavorites
```

## Methods

- **GET** `/srv.asmx/RemoveFromFavorites?authenticationTicket=...&itemPath=...`
- **POST** `/srv.asmx/RemoveFromFavorites` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveFromFavorites`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `itemPath` | string | Yes | Full infoRouter path to the document or folder to remove from favorites (e.g. `/Finance/Reports/Q1-Report.pdf` or `/Finance/Reports`). Short document ID paths (`~D{id}` or `~D{id}.ext`) are also accepted. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Document/Folder not found." />
```

---

## Required Permissions

No special permissions are required beyond authentication. The call always operates on the **currently authenticated user's** favorites list; a user cannot modify another user's favorites through this API.

---

## Example

### GET Request (document)

```
GET /srv.asmx/RemoveFromFavorites
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &itemPath=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### GET Request (folder)

```
GET /srv.asmx/RemoveFromFavorites
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &itemPath=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveFromFavorites HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&itemPath=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveFromFavorites>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:itemPath>/Finance/Reports/Q1-2024-Report.pdf</tns:itemPath>
    </tns:RemoveFromFavorites>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Both **documents** and **folders** can be removed from favorites using this API. The path is resolved as a document first; if no document is found at the path, it is resolved as a folder.
- The call always modifies the **currently authenticated user's** favorites list only.
- If the item is **not in the favorites list**, the call still returns success -" it is a safe no-op.
- Use `GetFavorites` to retrieve the current favorites list before calling this API.
- Use `AddToFavorites` to add a document or folder to the favorites list.

---

## Related APIs

- [AddToFavorites](AddToFavorites.md) - Add a document or folder to the current user's favorites list
- [GetFavorites](GetFavorites.md) - Get the list of documents and folders marked as favorites by the current user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document/Folder not found | The specified path does not resolve to an existing document or folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
