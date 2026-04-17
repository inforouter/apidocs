# UpdateVersionComment API

Updates the version comment (author comment) on a specific document version.

## Endpoint

```
/srv.asmx/UpdateVersionComment
```

## Methods

- **GET** `/srv.asmx/UpdateVersionComment?authenticationTicket=...&documentPath=...&versionNumber=...&commentText=...`
- **POST** `/srv.asmx/UpdateVersionComment` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateVersionComment`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Summary.pdf`). |
| `versionNumber` | integer | Yes | Version number to update. Use `GetDocumentVersions` to retrieve valid version numbers. |
| `commentText` | string | Yes | New comment text for the version. Pass an empty string to clear the comment. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
```

## Required Permissions

Only the **author of the version** (the user who created it) may update its comment. Calls from any other user will fail with an access-denied error.

## Example

### Request (POST)

```
POST /srv.asmx/UpdateVersionComment HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf&versionNumber=1000001&commentText=Initial draft submitted for review
```

### Request (GET)

```
GET /srv.asmx/UpdateVersionComment?authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf&versionNumber=1000001&commentText=Initial+draft+submitted+for+review
```

## Notes

- The version comment is distinct from document-level comments added via `AddDocumentComment`. It is the author's note attached to a specific version at check-in time.
- Pass an empty string for `commentText` to clear an existing comment.
- Use `GetDocumentVersions` to list all versions and their numbers before calling this API.

## Related APIs

- [GetDocumentVersions](GetDocumentVersions.md) — Get the complete version history for a document, including version numbers.
- [GetDocumentVersion](GetDocumentVersion.md) — Get metadata for a specific version of a document.
