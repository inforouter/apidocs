# AddToFavorites API

Adds the specified document or folder to the favorites list of the currently authenticated user. Both documents and folders are supported. Document shortcuts are resolved to their target document before being added.

## Endpoint

```
/srv.asmx/AddToFavorites
```

## Methods

- **GET** `/srv.asmx/AddToFavorites?authenticationTicket=...&itemPath=...`
- **POST** `/srv.asmx/AddToFavorites` (form data)
- **SOAP** Action: `http://tempuri.org/AddToFavorites`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `itemPath` | string | Yes | Full infoRouter path of the document or folder to add to favorites (e.g. `/Finance/Reports/Q1Report.pdf` or `/Finance/Reports`). |

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

- The caller must be an **authenticated, non-anonymous user**.
- The caller must have at least **Read** access to the document or folder at the given path (the item must be resolvable by the user).
- Anonymous guest users cannot add favorites and will receive an error.
- No special administrative permission is required.

---

## Example

### GET Request -" Document

```
GET /srv.asmx/AddToFavorites?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&itemPath=/Finance/Reports/Q1Report.pdf HTTP/1.1
```

### GET Request -" Folder

```
GET /srv.asmx/AddToFavorites?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&itemPath=/Finance/Reports HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AddToFavorites HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&itemPath=/Finance/Reports/Q1Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AddToFavorites>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:itemPath>/Finance/Reports/Q1Report.pdf</tns:itemPath>
    </tns:AddToFavorites>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Documents and folders** are both supported. The API first attempts to resolve `itemPath` as a document; if no document is found, it falls back to resolving it as a folder.
- **Document shortcuts** are resolved to their target document before being added. The target document is what appears in the user's favorites list, not the shortcut itself.
- **Duplicate behavior differs by item type:**
  - If a **document** is already in the user's favorites, the API returns `success="false"` with an error message.
  - If a **folder** is already in the user's favorites, the API returns `success="true"` silently (idempotent).
- Favorites are **per-user** -" adding an item to favorites does not affect any other user's favorites list.
- Use `RemoveFromFavorites` to remove an item and `GetFavorites` to retrieve the current user's favorites list.

---

## Related APIs

- [RemoveFromFavorites](RemoveFromFavorites.md) - Remove a document or folder from the current user's favorites
- [GetFavorites](GetFavorites.md) - Retrieve the current user's favorites list

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Anonymous users cannot create favorites | The authenticated user is an anonymous/guest user. |
| This Document has already been added to favorites | The document is already in the user's favorites list. |
| Item not found | The specified `itemPath` does not exist or the user does not have access to it. |

---
