# DocumentExists API

Checks whether a document exists at the specified path and returns CRC32 checksums for the latest version and the published version. A successful response confirms the document exists; an error response indicates the path was not found.

## Endpoint

```

/srv.asmx/DocumentExists

```

## Methods

- **GET** `/srv.asmx/DocumentExists?authenticationTicket=...&Path=...`

- **POST** `/srv.asmx/DocumentExists` (form data)

- **SOAP** Action: `http://tempuri.org/DocumentExists`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path of the document (e.g. `/MyLibrary/Reports/Report.pdf`), or a short document path in the form `~D{documentId}.{ext}` (e.g. `~D4217.pdf`). |

## Response

### Success Response

```xml

<response success="true" CRC32LASTVERSION="a3f1c29d" CRC32="b7e4d80c" />

```

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the document was found. |
| `CRC32LASTVERSION` | CRC32 checksum of the latest version's file content. |
| `CRC32` | CRC32 checksum of the published version's file content. Empty string if no version has been published. |

### Error Response

```xml

<response success="false" error="Error message" />

```

---

## Required Permissions

Any authenticated user may call this API. The document must be accessible to the authenticated user.

---

## Example

### GET Request

```

GET /srv.asmx/DocumentExists

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/MyLibrary/Reports/Report.pdf

HTTP/1.1

```

### GET Request with Short Path

```

GET /srv.asmx/DocumentExists

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=~D4217.pdf

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/DocumentExists HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/MyLibrary/Reports/Report.pdf

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:DocumentExists>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:Path>/MyLibrary/Reports/Report.pdf</tns:Path>

    </tns:DocumentExists>

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

Asks whether a path names a document, and answers with the checksums of its versions.

```javascript
async function documentState(path) {
  const response = await fetch('/srv.asmx/DocumentExists?' + new URLSearchParams({
    authenticationTicket: ticket, Path: path
  }));
  const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') !== 'true') {
    if (root.getAttribute('errorCode') === '4041') return null;   // not there
    throw new Error(root.getAttribute('error'));
  }

  return {
    published: root.getAttribute('CRC32'),
    latest: root.getAttribute('CRC32LASTVERSION')
  };
}
```

Like [FolderExists](FolderExists.md) it answers by succeeding or failing rather than returning a
boolean - but unlike it, a success carries something useful: comparing `CRC32LASTVERSION` against a
local copy tells you whether to download without downloading. A folder path is `4041`; this asks
about documents only.

## Notes

- Despite its name, this API does more than confirm existence -" it also returns CRC32 checksums that can be used to verify document content without downloading the file.

- The `CRC32` (published version checksum) attribute is an empty string when no version of the document has been published.

- Short document paths in the form `~D{documentId}.{ext}` are accepted as an alternative to full folder paths. Any other path starting with `~` (but not `~D`) is rejected with an `InvalidDocumentIdentifer` error.

- Use `DocumentExists1` to look up a document by folder path and document name separately instead of a combined full path.

---

## Related APIs

- [DocumentExists1](DocumentExists1.md) - Check document existence using a folder path and document name as separate parameters

- [GetDocument](GetDocument.md) - Get full document properties

- [FolderExists](FolderExists.md) - Check whether a folder exists at a given path

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found` | No document exists at the specified `Path`. |
| `InvalidDocumentIdentifer` | `Path` starts with `~` but is not a valid short document path (`~D` prefix). |

---

