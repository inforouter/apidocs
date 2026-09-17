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

### Folder Copy -" Partial-failure Response

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

- The destination folder must not have a **cutoff date**. A folder with any cutoff date, past or future, accepts no new documents or subfolders.

---

## Example

### GET Request -" Copy a Document

```

GET /srv.asmx/Copy?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&SourcePath=/Finance/Reports/Q1Report.pdf&DestinationPath=/Finance/Archive/Q1Report_v2.pdf HTTP/1.1

```

### GET Request -" Copy a Document to Folder by ID

```

GET /srv.asmx/Copy?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&SourcePath=/Finance/Reports/Q1Report.pdf&DestinationPath=~F4201 HTTP/1.1

```

### GET Request -" Copy a Folder

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

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Copies a document or a folder. Like [Move](Move.md), `DestinationPath` is the **full new path of the
copy**, not the folder to put it in: copying `/a/Q1.pdf` into `/b` means `/b/Q1.pdf`.

```javascript
await call('Copy', {
  authenticationTicket: ticket,
  SourcePath: '/Finance/Reports/Q1.pdf',
  DestinationPath: '/Finance/Archive/Q1.pdf'
});
```

A folder is copied with everything under it. The original is left where it was - that is the only
difference from `Move`.

**A successful copy carries no `errorCode` at all**, where most operations report `errorCode="0"`. A
client reading `errorCode` before checking `success` sees nothing and must not treat that as a
failure.

**"It is already there" does not have one code in this family.** `AddToDownloadQueue` reports it as
`4000`, `AddToFavorites` as `4090`, `Copy` as `4000` and `CreateDocumentShortcut` as `4090`. Branch on
the operation, not on a shared rule.

## Notes

- The source path is resolved as a **document first**. If no document is found at `SourcePath`, it is resolved as a **folder**.

- When using a full `DestinationPath`, the **parent folder** of that path must already exist. The copy operation does not create intermediate folders.

- When using the `~F<folderId>` short format, the copy retains the **original source name**. The `~F` prefix is case-insensitive.

- Copying a document creates a **new independent document** -" changes to the copy do not affect the original.

- For **folder copies**, all accessible sub-folders and documents are recursively copied. Items that cannot be copied (e.g. due to permissions or locks) are skipped and reported in the response log rather than failing the entire operation.

- The `DestinationPath` parent folder for a document copy is derived by stripping the last path segment. For example, `/Finance/Archive/Q1Report_copy.pdf` -' destination folder `/Finance/Archive/`, new name `Q1Report_copy.pdf`.

- To **rename** the copy, provide a different file name in `DestinationPath`. To keep the original name, point `DestinationPath` to the target folder using the `~F<folderId>` format.

---

## Related APIs

- [Move](Move.md) - Move a document or folder to a different path

- [CreateDocumentShortcut](CreateDocumentShortcut.md) - Create a shortcut to a document instead of a full copy

- [GetDocument](GetDocument.md) - Retrieve properties of a document

- [GetFolder](GetFolder.md) - Retrieve properties of a folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is refused |
| `4000` | something of that name is already at the destination, or there is nothing at `SourcePath` - the message is prefixed "Source:" |
| `4030` | the caller may not read the source or write at the destination |
| `none` | partial failures come back as `success="false" error="[log]"` with the items listed inside |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Source: <message>` | The source document or folder could not be found or accessed. |
| `Destination: <message>` | The destination folder could not be found or the user lacks create permission. |
| Access denied (read) | The calling user does not have Read access on the source item. |
| Access denied (create) | The calling user does not have Create permission in the destination folder. |
| `This folder has been cut-off. New documents cannot be created in this folder.` | The destination folder has a cutoff date. Any cutoff date blocks new documents, even one that is still in the future. A folder copy returns `This folder has been cut off. New folders cannot be created in this folder.` instead. |
| Document name already exists | A document with the same name already exists in the destination folder. |

---

