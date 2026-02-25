# PublishDocument API

Sets the published version of a document. The published version is the one that is visible to users who browse or search the library. Pass `0` for the version number to publish the latest version, or pass an internal version number to publish a specific version.

> **Note:** Publishing is a separate concept from uploading a new version. A document can have multiple versions but only one published version at a time. Use `UnpublishDocument` to remove the published designation without replacing it.

## Endpoint

```
/srv.asmx/PublishDocument
```

## Methods

- **GET** `/srv.asmx/PublishDocument?AuthenticationTicket=...&DocumentPath=...&VersionNumber=...`
- **POST** `/srv.asmx/PublishDocument` (form data)
- **SOAP** Action: `http://tempuri.org/PublishDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `VersionNumber` | int | Yes | Internal version number of the version to publish. Pass `0` to publish the latest version. See note below for the internal version number format. |

> **Internal version number format:** infoRouter stores version numbers as multiples of 1,000,000. Version 1 = `1000000`, version 2 = `2000000`, version 3 = `3000000`, and so on. Values between `1` and `999,999`, or negative values, are explicitly rejected. Use `GetDocumentVersions` to obtain the correct internal version number for a given version label.

| User-visible version | VersionNumber value |
|----------------------|---------------------|
| Latest version | `0` |
| 1 | `1000000` |
| 2 | `2000000` |
| 3 | `3000000` |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Access denied. To publish a document you must be the owner, a domain manager, or the author of at least one version." />
```

---

## Required Permissions

The calling user must satisfy **all** of the following conditions:

1. Must have the **Set Publishing Rules** permission on the document (or its containing folder).
2. Must be **at least one** of:
   - The document owner
   - A domain/library manager for the library that contains the document
   - The author (uploader) of at least one version of the document
3. If the document is currently **checked out (locked)**, only the user who holds the lock may change the publishing rule.

Additionally, if the domain/library has a **Doctype** publishing requirement configured (see `GetPublishingRequirements`), the document must have a document type assigned before it can be published. Use `UpdateDocumentType` to assign one.

---

## Example

### GET Request — publish the latest version

```
GET /srv.asmx/PublishDocument
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentPath=/Finance/Reports/Q1-2024-Report.pdf
  &VersionNumber=0
HTTP/1.1
```

### GET Request — publish a specific version

```
GET /srv.asmx/PublishDocument
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentPath=/Finance/Reports/Q1-2024-Report.pdf
  &VersionNumber=3000000
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/PublishDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentPath=/Finance/Reports/Q1-2024-Report.pdf
&VersionNumber=3000000
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:PublishDocument>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DocumentPath>/Finance/Reports/Q1-2024-Report.pdf</tns:DocumentPath>
      <tns:VersionNumber>3000000</tns:VersionNumber>
    </tns:PublishDocument>
  </soap:Body>
</soap:Envelope>
```

### Workflow — check requirements then publish

```
1. GET /srv.asmx/GetPublishingRequirements?...&domainname=Finance
   → check if <PublishingRequirement>Doctype</PublishingRequirement> is present

2. If Doctype requirement exists:
   GET /srv.asmx/GetDocument?...&Path=/Finance/Reports/Q1-2024-Report.pdf
   → verify @DocTypeID != "0"
   → if DocTypeID is 0, call UpdateDocumentType first

3. GET /srv.asmx/PublishDocument?...&DocumentPath=/Finance/Reports/Q1-2024-Report.pdf&VersionNumber=0
```

---

## Notes

- Passing `VersionNumber=0` publishes the **latest** version of the document, equivalent to setting the publishing rule to "Latest".
- Only one version can be published at a time. Publishing a new version automatically replaces the previously published version.
- Version numbers between `1` and `999,999` and negative values are rejected. Version numbers must be exact multiples of `1,000,000` or zero.
- If the domain has publishing requirements (e.g. `Doctype`), they must be satisfied before this call will succeed. Check requirements first with `GetPublishingRequirements`.
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted.

---

## Related APIs

- [UnpublishDocument](UnpublishDocument.md) - Remove the published status from a document
- [GetPublishingRequirements](GetPublishingRequirements.md) - Get the publishing requirements configured for a domain/library
- [GetDocumentVersions](GetDocumentVersions.md) - Get the version history list to obtain internal version numbers
- [GetDocument](GetDocument.md) - Get document properties including `PublishingRule`, `PublishedVersionNumber`, and `DocTypeID`
- [UpdateDocumentType](UpdateDocumentType.md) - Assign a document type to satisfy a Doctype publishing requirement

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Invalid version number | `VersionNumber` is between 1 and 999,999 or negative (not a valid internal version number). |
| Access denied (Set Publishing Rules) | The user does not have Set Publishing Rules permission on the document. |
| Access denied (not owner/manager/author) | The user is not the document owner, a domain manager, or an author of any version. |
| Document is checked out by another user | The document is locked by someone else; only the lock holder may publish. |
| Publishing requirement not met | A domain-level publishing requirement (e.g. Doctype) is not satisfied. |
| Version not found | The specified internal version number does not correspond to an existing version. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/PublishDocument*
