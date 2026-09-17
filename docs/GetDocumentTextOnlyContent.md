# GetDocumentTextOnlyContent API

Returns the plain-text alternative content stored alongside the published version of a document, or alongside its latest version when the document has never been published. This text-only content is a separately stored artifact in the document warehouse -" it is only present if it has been explicitly set (for example, by a conversion process or via `SetDocumentTextOnlyContent`). If the document has no versions at all, is offline, or is a shortcut or URL type, an error is returned.

## Endpoint

```

/srv.asmx/GetDocumentTextOnlyContent

```

## Methods

- **GET** `/srv.asmx/GetDocumentTextOnlyContent?AuthenticationTicket=...&Path=...`

- **POST** `/srv.asmx/GetDocumentTextOnlyContent` (form data)

- **SOAP** Action: `http://tempuri.org/GetDocumentTextOnlyContent`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

> **Note:** This API always retrieves the text-only content for the **published version** of the document - or its **latest version**, when the document has never been published. There is no version number parameter.

---

## Response

### Success Response

On success, the plain text content is returned as the body of the `<response>` element (not inside a child element):

```xml

<response success="true" error="">This is the plain text content of the document.

It may span multiple lines and represents the text-only

alternative stored in the document warehouse.</response>

```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` on success. |
| `error` | Empty string on success. |
| *(element body)* | The plain text content of the resolved version. May be an empty string if text-only content has never been set for this document. |

### Error Response

```xml

<response success="false" error="No version number was given, and this document has no published version to process." />

```

---

## Required Permissions

The calling user must have at least read access to the document and its published version.

---

## Example

### GET Request

```

GET /srv.asmx/GetDocumentTextOnlyContent

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/Finance/Reports/Q1-2024-Report.pdf

HTTP/1.1

```

### GET Request (short ID path)

```

GET /srv.asmx/GetDocumentTextOnlyContent

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=~D1051

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/GetDocumentTextOnlyContent HTTP/1.1

Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/Finance/Reports/Q1-2024-Report.pdf

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:GetDocumentTextOnlyContent>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>

    </tns:GetDocumentTextOnlyContent>

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

Reads the plain-text rendition stored against a document - what
[SetDocumentTextOnlyContent](SetDocumentTextOnlyContent.md) wrote, and what full-text search reads.

```javascript
const root = await call('GetDocumentTextOnlyContent', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf'
});

const text = root.textContent;    // on the root itself, not in a child element
```

The text is the root element's own content rather than a child element. A document with nothing
stored is a success with an empty root, not an error, so there is no way to tell "never generated"
from "generated and empty".

## Notes

- The text content is returned directly as the body of the `<response>` element, not inside a named child element.

- This API retrieves a **separately stored** plain-text artifact from the document warehouse. It is distinct from the full-text search index abstract returned by `GetDocumentAbstract1`. The content is only present if it was previously written (e.g. by a document conversion process or via `SetDocumentTextOnlyContent`).

- Only the **published version** is accessible through this API - or the **latest version**, when the document has never been published. Reading an unpublished version still requires the caller to be the document's owner, an author of one of its versions, an active task assignee, or a domain manager. Documents with no versions at all return an error.

- Offline documents, URL documents, and shortcut documents do not have text-only content and will return an error.

- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.

---

## Related APIs

- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Get the full-text search index abstract for a document version

- [GetDocument](GetDocument.md) - Get full document metadata and properties

- [GetDocumentVersions](GetDocumentVersions.md) - Get the version history list for a document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A call with no ticket signs in as the anonymous user, so a document in a library flagged as anonymous
can be read without authenticating.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| No version number was given, and this document has no published version to process. | The document has no versions at all. |
| Document is offline | The document is marked as offline and its content is unavailable. |
| URL or shortcut | URL documents and shortcuts do not have text-only content. |
| Access denied | The user does not have read access to the document or its published version. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

