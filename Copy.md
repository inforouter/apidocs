# Copy API

Copies an existing document or folder to the specified destination path. The copy is placed inside the destination folder under the name derived from `DestinationPath`. Both documents and folders are supported; the source path is resolved as a document first, and as a folder if no document is found.

## Endpoint

```
/srv.asmx/Copy
```

## Methods

- **GET** `/srv.asmx/Copy?authenticationTicket=...&SourcePath=...&DestinationPath=...`
- **POST** `/srv.asmx/Copy` (form data)
- **SOAP** Action: `http://tempuri.org/Copy`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `SourcePath` | string | Yes | Full infoRouter path of the document or folder to copy (e.g. `/Finance/Reports/Q1Report.pdf` or `/Finance/Reports`). |
| `DestinationPath` | string | Yes | Target location for the copy. See **DestinationPath formats** below. |

### DestinationPath Formats

The `DestinationPath` parameter controls both where the copy is placed and what it is named.

| Format | Example | Behaviour |
|--------|---------|-----------|
| Full path | `/Finance/Archive/Q1Report_copy.pdf` | Copy is placed in `/Finance/Archive/` and named `Q1Report_copy.pdf`. The parent folder must already exist. |
| Short folder ID | `~F12345` | Copy is placed in folder ID 12345 using the **original source name**. Useful when working with folder IDs rather than full paths. |

## Response

### Success Response

```xml
<root success="true" />
```

### Folder Copy — Partial-failure Response

When copying a folder, individual sub-item errors are logged. If any errors occurred the response includes the log:

```xml
<Response success="false" error="[log]">
  <item path="/Finance/Reports/locked.pdf" error="Document is locked by another user." />
</Response>
```

### Error Response

```xml
<root success="false" error="Source: Folder not found" />
<root success="false" error="Destination: Folder not found" />
```

Error messages are prefixed with `Source:` or `Destination:` to indicate which path caused the problem.

---

## Required Permissions

- The caller must be an **authenticated user** with a valid ticket.
- **Read** access is required on the source document or folder.
- **Create Document** (or **Create Folder**) permission is required in the destination folder.
- Copying a document with **Confidential** or higher classification level requires the caller to have the corresponding classification clearance in the destination domain.
- The destination folder must not have a **cutoff date** that prevents new document creation.

---

## Example

### GET Request — Copy a Document

```
GET /srv.asmx/Copy?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&SourcePath=/Finance/Reports/Q1Report.pdf&DestinationPath=/Finance/Archive/Q1Report_v2.pdf HTTP/1.1
```

### GET Request — Copy a Document to Folder by ID

```
GET /srv.asmx/Copy?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&SourcePath=/Finance/Reports/Q1Report.pdf&DestinationPath=~F4201 HTTP/1.1
```

### GET Request — Copy a Folder

```
GET /srv.asmx/Copy?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&SourcePath=/Finance/Reports&DestinationPath=/Finance/Archive/Reports HTTP/1.1
```

### POST Request

```
POST /srv.asmx/Copy HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&SourcePath=/Finance/Reports/Q1Report.pdf
&DestinationPath=/Finance/Archive/Q1Report_copy.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:Copy>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:SourcePath>/Finance/Reports/Q1Report.pdf</tns:SourcePath>
      <tns:DestinationPath>/Finance/Archive/Q1Report_copy.pdf</tns:DestinationPath>
    </tns:Copy>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The source path is resolved as a **document first**. If no document is found at `SourcePath`, it is resolved as a **folder**.
- When using a full `DestinationPath`, the **parent folder** of that path must already exist. The copy operation does not create intermediate folders.
- When using the `~F<folderId>` short format, the copy retains the **original source name**. The `~F` prefix is case-insensitive.
- Copying a document creates a **new independent document** — changes to the copy do not affect the original.
- For **folder copies**, all accessible sub-folders and documents are recursively copied. Items that cannot be copied (e.g. due to permissions or locks) are skipped and reported in the response log rather than failing the entire operation.
- The `DestinationPath` parent folder for a document copy is derived by stripping the last path segment. For example, `/Finance/Archive/Q1Report_copy.pdf` → destination folder `/Finance/Archive/`, new name `Q1Report_copy.pdf`.
- To **rename** the copy, provide a different file name in `DestinationPath`. To keep the original name, point `DestinationPath` to the target folder using the `~F<folderId>` format.

---

## Related APIs

- [Move](Move) - Move a document or folder to a different path
- [CreateDocumentShortcut](CreateDocumentShortcut) - Create a shortcut to a document instead of a full copy
- [GetDocument](GetDocument) - Retrieve properties of a document
- [GetFolder](GetFolder) - Retrieve properties of a folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Source: <message>` | The source document or folder could not be found or accessed. |
| `Destination: <message>` | The destination folder could not be found or the user lacks create permission. |
| Access denied (read) | The calling user does not have Read access on the source item. |
| Access denied (create) | The calling user does not have Create permission in the destination folder. |
| Destination folder has a cutoff date | Documents cannot be added to a folder that has reached its cutoff date. |
| Document name already exists | A document with the same name already exists in the destination folder. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/Copy*
