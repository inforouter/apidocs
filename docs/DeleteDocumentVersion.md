# DeleteDocumentVersion API

Permanently deletes a specific version of a document. The deletion is irreversible -" the version's file content and metadata are removed from the warehouse.

## Endpoint

```

/srv.asmx/DeleteDocumentVersion

```

## Methods

- **GET** `/srv.asmx/DeleteDocumentVersion?authenticationTicket=...&DocumentPath=...&VersionNumber=...`

- **POST** `/srv.asmx/DeleteDocumentVersion` (form data)

- **SOAP** Action: `http://tempuri.org/DeleteDocumentVersion`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path of the document (e.g. `/MyLibrary/Reports/Report.pdf`). |
| `VersionNumber` | int | Yes | Version number to delete. Must be --- 1,000,000 (modernized version number format). Use `GetDocumentVersions` to retrieve valid version numbers for a document. |

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

The authenticated user must have **VersionDelete** permission on the document.

Additionally:

- If the document is **checked out by another user**, the deletion is blocked. The user who has it checked out may delete versions.

- The specified version must exist (not already deleted).

---

## Example

### GET Request

```

GET /srv.asmx/DeleteDocumentVersion

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &DocumentPath=/MyLibrary/Reports/Report.pdf

  &VersionNumber=3000000

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/DeleteDocumentVersion HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&DocumentPath=/MyLibrary/Reports/Report.pdf

&VersionNumber=3000000

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:DeleteDocumentVersion>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:DocumentPath>/MyLibrary/Reports/Report.pdf</tns:DocumentPath>

      <tns:VersionNumber>3000000</tns:VersionNumber>

    </tns:DeleteDocumentVersion>

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

Removes one version of a document.

```javascript
await call('DeleteDocumentVersion', {
  authenticationTicket: ticket,
  DocumentPath: '/Finance/Reports/Q1.pdf',
  VersionNumber: 1000001
});
```

**The published version cannot be removed.** Publish another version first - see
[SetDocumentPublishingRule](SetDocumentPublishingRule.md) - and then delete the old one. On a document
with a single version there is nothing this operation can do.

**A version number nothing uses is `4041`.** Read the version list from
[GetDocument](GetDocument.md) with `withVersions=true` rather than guessing. This used to answer
`4000` "the version file is in use, try again later", which invited a retry that could never work.

## Notes

- infoRouter packs a major, a minor and a revision into one integer as `major * 1000000 + minor * 1000 + revision`. The first version of a document is `1000000` and the second is `1000001`; `2000000` is major version 2, not the second version. Values between `1` and `999,999` are rejected. Use `GetDocumentVersions` to read the numbers a document actually has rather than computing them.

- Always retrieve current version numbers using `GetDocumentVersions` before calling this API.

- This deletion is **permanent and irreversible**. The version's content and metadata are removed from the warehouse.

- If the document has legacy version numbers stored in the database (below 1,000,000), the system automatically upgrades them to the new format before performing the deletion.

- If the document is **checked out by another user**, the operation fails. The document owner or a domain manager can unlock the document first using `UnLock`.

---

## Related APIs

- [GetDocumentVersions](GetDocumentVersions.md) - List all versions of a document (use to retrieve valid VersionNumber values)

- [GetDocumentVersion](GetDocumentVersion.md) - Get details of a specific document version

- [UnLock](UnLock.md) - Unlock a checked-out document

- [PublishDocument](PublishDocument.md) - Publish a specific version of a document

- [DeleteDocument](DeleteDocument.md) - Move a document to the recycle bin

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | the version is the published one, or `VersionNumber` is below 1,000,000 |
| `4041` | no document at that path, or no version of it carries that number |
| `4030` | the caller may not delete versions here |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found` | The `DocumentPath` does not refer to an existing document. |
| Invalid version number | `VersionNumber` is below 1,000,000 (not in the modernized format). |
| `Version not found` | The specified version does not exist or has already been deleted. |
| `Access denied` | The caller does not have `VersionDelete` permission on the document. |
| `Checked out by another user` | The document is currently checked out by a different user. |

---

