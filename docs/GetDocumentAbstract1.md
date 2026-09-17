# GetDocumentAbstract1 API

Returns the full-text abstract (indexed text content) of a specified version of a document. This is the current preferred API for retrieving document abstracts. It uses a consistent XML response structure for both success and error cases, unlike the obsolete [`GetDocumentAbstract`](GetDocumentAbstract.md).

## Endpoint

```

/srv.asmx/GetDocumentAbstract1

```

## Methods

- **GET** `/srv.asmx/GetDocumentAbstract1?authenticationTicket=...&path=...&versionNumber=...`

- **POST** `/srv.asmx/GetDocumentAbstract1` (form data)

- **SOAP** Action: `http://tempuri.org/GetDocumentAbstract1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `versionNumber` | int | Yes | Version number to retrieve the abstract for. Pass `0` for the published version, or for the latest version when the document has never been published. Must be `0` or a version number in the modern format (--- 1,000,000). Values between `1` and `999,999` are rejected with an error. |

### Version Number Format

infoRouter uses a large-integer version numbering scheme where version numbers pack a major, a minor and a revision into one integer as `major * 1000000 + minor * 1000 + revision`, so the first version is `1000000` and the second is `1000001` - not `2000000`, which would be major version 2. Pass `0` to get the published version's abstract, or the latest version's when the document has never been published.

---

## Response

### Success Response

On success, the abstract text is returned inside a `<Value>` child element:

```xml

<response success="true" error="">

  <Value AppliedById="3" AppliedBy="SYSTEM" DateApplied="2024-03-15T14:32:07.000Z">This document covers the Q1 2024 financial results including

revenue figures, expense breakdowns, and year-over-year comparisons...</Value>

</response>

```

| Element / Attribute | Description |
|--------------------|-------------|
| `success` | `"true"` on success. |
| `error` | Empty string on success. |
| `<Value>` | Child element containing the full-text abstract (indexed content) of the requested document version. Carries the author as attributes - see below. |

### Who wrote the abstract

The element carries the author, in the same three attributes
[GetPropertySets](GetPropertySets.md) uses on its `<Log>` node and
[GetDocumentSummary](GetDocumentSummary.md) uses on its `<Value>`.

| Attribute | Meaning |
|-----------|---------|
| `AppliedById` | ID of the user recorded against the abstract. Use this to identify them - a username is a label, not a key. |
| `AppliedBy` | Their display name. |
| `DateApplied` | When the abstract was written, in universal format. |

An abstract is always produced by the server - from the email parser or the content index, never
typed - so in practice this is the system account. It is read from the stored row rather than
assumed, which is why **all three are absent** on an abstract written before the author was
recorded, and on a `-` where there is none.

### Error Response

```xml

<response success="false" error="[900] Authentication failed" />

```

Both success and error use the same `<response>` root element -" the only difference is the presence of the `<Value>` child on success. This consistent structure is what makes `GetDocumentAbstract1` the preferred API over the obsolete [`GetDocumentAbstract`](GetDocumentAbstract.md).

---

## Required Permissions

The calling user must have at least read access to the document. The abstract is extracted from the full-text search index; if the document has not been indexed, the returned abstract may be empty.

---

## Example

### GET Request

```

GET /srv.asmx/GetDocumentAbstract1

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &path=/Finance/Reports/Q1-2024-Report.pdf

  &versionNumber=0

HTTP/1.1

```

### GET Request (specific version)

```

GET /srv.asmx/GetDocumentAbstract1

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &path=/Finance/Reports/Q1-2024-Report.pdf

  &versionNumber=2000000

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/GetDocumentAbstract1 HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&path=/Finance/Reports/Q1-2024-Report.pdf

&versionNumber=0

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:GetDocumentAbstract1>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>

      <tns:versionNumber>0</tns:versionNumber>

    </tns:GetDocumentAbstract1>

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

Reads the indexed text of one document version, in a `<Value>` element.

```javascript
const root = await call('GetDocumentAbstract1', {
  authenticationTicket: ticket,
  path: '/Finance/Reports/Q1.pdf',
  versionNumber: 0            // 0 means the published version
});

console.log(root.querySelector('Value').textContent);
```

**The only difference between the two is the element name.** `GetDocumentAbstract` writes the text
into `<abstract>`, which is what it has always done; `GetDocumentAbstract1` writes the identical text,
with the identical attributes, into `<Value>` - the element the rest of the API uses for a single
returned value. Same parameters, same content, same author attributes. Prefer the numbered one in new
code and keep reading `<abstract>` in anything already written against it.

## Notes

- `versionNumber=0` retrieves the abstract for the **published version** of the document, or for its **latest version** when it has never been published.

- Version numbers between `1` and `999,999` are rejected. Use `0` for the published version, or a number a document actually carries - the first version is `1000000` and the second `1000001`.

- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `path` parameter.

- The abstract is sourced from the full-text search index. If the document has not been indexed, the `<Value>` element may be empty.

- This API supersedes the obsolete [`GetDocumentAbstract`](GetDocumentAbstract.md), which used an `<abstract>` child element on success and had inconsistent XML structure between success and error cases.

---

## Related APIs

- [GetDocumentAbstract](GetDocumentAbstract.md) - Obsolete predecessor with inconsistent XML structure

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
| Invalid version number | `versionNumber` is between 1 and 999,999 (must be 0 or --- 1,000,000). |
| `SystemError:...` | An unexpected server-side error occurred. |

---

