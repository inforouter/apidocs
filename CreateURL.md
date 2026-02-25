# CreateURL API

Creates a new URL document or updates the target address of an existing URL document at the specified path. URL documents are infoRouter items that store a hyperlink — when opened, they redirect the user to the stored web address.

When the target `Path` does not exist, a new URL document is created. When it already exists, a new version is created with the updated address.

## Endpoint

```
/srv.asmx/CreateURL
```

## Methods

- **GET** `/srv.asmx/CreateURL?authenticationTicket=...&Path=...&AddressURL=...`
- **POST** `/srv.asmx/CreateURL` (form data)
- **SOAP** Action: `http://tempuri.org/CreateURL`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path for the URL document to create or update (e.g. `/MyLibrary/Links/CompanyWebsite`). The document name must **not** end with the `.url` extension. |
| `AddressURL` | string | Yes | The target web address to store in the URL document (e.g. `https://www.example.com`). |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

- **Creating a new URL document**: The authenticated user must have **Add Document** permission on the destination folder (the parent of `Path`).
- **Updating an existing URL document**: The authenticated user must have **Check Out** and **Publish** permissions on the existing document at `Path`. If the document is already checked out by another user, the call fails.

---

## Example

### GET Request — Create new URL document

```
GET /srv.asmx/CreateURL
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/MyLibrary/Links/CompanyWebsite
  &AddressURL=https://www.example.com
HTTP/1.1
```

### POST Request — Create new URL document

```
POST /srv.asmx/CreateURL HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Links/CompanyWebsite
&AddressURL=https://www.example.com
```

### POST Request — Update existing URL document

```
POST /srv.asmx/CreateURL HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Links/CompanyWebsite
&AddressURL=https://www.newaddress.com
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateURL>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/MyLibrary/Links/CompanyWebsite</tns:Path>
      <tns:AddressURL>https://www.example.com</tns:AddressURL>
    </tns:CreateURL>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The document name in `Path` must **not** include the `.url` file extension. infoRouter stores the URL address internally and does not use Windows-style `.url` files.
- The destination folder (the parent of `Path`) must already exist before calling this API.
- When updating an existing URL document that is not currently checked out, the API automatically checks the document out and then publishes a new version, leaving the document checked in afterward.
- When updating a document that is **already checked out by the current user**, the document remains checked out after the call.
- If the document at `Path` is checked out by a **different user**, the call fails with an error.

---

## Related APIs

- [CreateDocumentShortcut](CreateDocumentShortcut) - Create a shortcut to another infoRouter document
- [GetDocument](GetDocument) - Retrieve properties of a document including its stored URL address
- [GetDocumentVersions](GetDocumentVersions) - List all versions of a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `The document file extension must be "url"` | The `Path` ends with the `.url` extension, which is not permitted. Remove the extension from the document name. |
| `Folder not found` | The destination folder (parent of `Path`) does not exist or is not accessible. |
| `This document has been checked out by another user.` | The document at `Path` is checked out by a different user; it cannot be updated. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateURL*
