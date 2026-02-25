# CreateEditDocumentURL API

Creates a time-limited WebDAV URL for directly opening and editing a specific document in a WebDAV-enabled application such as Microsoft Office. The returned URL points to the document file and can be passed to Office applications to open it for in-place editing via WebDAV.

## Endpoint

```
/srv.asmx/CreateEditDocumentURL
```

## Methods

- **GET** `/srv.asmx/CreateEditDocumentURL?authenticationTicket=...&DocumentPath=...`
- **POST** `/srv.asmx/CreateEditDocumentURL` (form data)
- **SOAP** Action: `http://tempuri.org/CreateEditDocumentURL`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path of the document to edit (e.g. `/MyLibrary/Reports/Budget.xlsx`). The document must exist and be of a WebDAV-editable type (e.g. Office documents). |

## Response

### Success Response

```xml
<response success="true">
  <Value>/dav/sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301/MyLibrary/Reports/Budget.xlsx</Value>
</response>
```

| Element / Attribute | Description |
|---------------------|-------------|
| `success` | `true` if the URL was generated successfully. |
| `Value` | The WebDAV path to the document. Prepend the server base URL (e.g. `https://yourserver`) to form the full URL to pass to a WebDAV client or Office application. |

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

Any authenticated non-anonymous user may call this API. The document at `DocumentPath` must be accessible to the user (Read permission is sufficient to generate the URL).

---

## Example

### GET Request

```
GET /srv.asmx/CreateEditDocumentURL
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentPath=/MyLibrary/Reports/Budget.xlsx
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateEditDocumentURL HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentPath=/MyLibrary/Reports/Budget.xlsx
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateEditDocumentURL>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:DocumentPath>/MyLibrary/Reports/Budget.xlsx</tns:DocumentPath>
    </tns:CreateEditDocumentURL>
  </soap:Body>
</soap:Envelope>
```

### Using the returned URL

Prepend your server's base URL to form the complete WebDAV address:

```
https://yourserver/dav/sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301/MyLibrary/Reports/Budget.xlsx
```

Pass this full URL to an Office application (e.g. via `ShellExecute` on Windows, or the Office URI scheme `ms-word:ofe|u|<url>`) to open the document for direct editing.

---

## Notes

- The returned `Value` is a **document-specific** WebDAV path. It points directly to the file and is intended for single-document edit sessions. To mount the entire infoRouter file system as a drive, use `CreateDiskMountURL` instead.
- Each call creates a new dedicated **OfficeEdit** DAV session ticket for the current user. This session is separate from the user's main authentication ticket.
- If the full WebDAV URL would exceed 215 characters (combined server base URL and encoded document path), the server automatically uses a short path format instead: `/dav/sid-{ticket}/~D{documentId}.{extension}`.
- The session ticket embedded in the URL has a limited lifetime. Generate the URL immediately before opening the document; do not cache and reuse it later.
- The document does not need to be checked out before calling this API. The WebDAV client is responsible for checkout/check-in via the DAV protocol during the edit session.

---

## Related APIs

- [CreateDiskMountURL](CreateDiskMountURL) - Create a root-level WebDAV mount URL for the entire infoRouter file system
- [GetDocument](GetDocument) - Retrieve properties and metadata of a document
- [GetDownloadInfo](GetDownloadInfo) - Get download URL and metadata for a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found` | The `DocumentPath` does not refer to an existing document. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateEditDocumentURL*
