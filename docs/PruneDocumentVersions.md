# PruneDocumentVersions API

Deletes old versions of a document, retaining the N most recent published and M most recent unpublished versions. All older versions are permanently deleted.

## Endpoint

```
/srv.asmx/PruneDocumentVersions
```

## Methods

- **GET** `/srv.asmx/PruneDocumentVersions?authenticationTicket=...&documentPath=...&keepPublished=...&keepUnpublished=...`
- **POST** `/srv.asmx/PruneDocumentVersions` (form data)
- **SOAP** Action: `http://tempuri.org/PruneDocumentVersions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Summary.pdf`). |
| `keepPublished` | integer | Yes | Number of most recent published versions to retain. Must be 1 or greater. |
| `keepUnpublished` | integer | Yes | Number of most recent unpublished versions to retain. Must be 0 or greater. |

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

The calling user must have sufficient permissions to delete document versions.

## Pruning Rules

The following versions are **never deleted** regardless of the keep counts:

- Unpublished versions created after the latest published version.
- Versions currently checked out.
- Versions involved in an active workflow.
- Approved versions.
- Versions protected by a retention or disposition schedule.

## Example

### Request (POST)

Keep the 3 most recent published versions and 1 most recent unpublished version:

```
POST /srv.asmx/PruneDocumentVersions HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf&keepPublished=3&keepUnpublished=1
```

### Request (GET)

```
GET /srv.asmx/PruneDocumentVersions?authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf&keepPublished=3&keepUnpublished=1
```

## Notes

- This operation is **irreversible**. Deleted versions cannot be recovered.
- `keepPublished` must be at least 1 — it is not possible to delete all published versions.
- `keepUnpublished` may be 0 to delete all unpublished versions (subject to the pruning rules above).
- Use `GetDocumentVersions` to inspect the current version history before pruning.

## Related APIs

- [GetDocumentVersions](GetDocumentVersions.md) — Get the complete version history for a document.
- [DeleteDocumentVersion](DeleteDocumentVersion.md) — Permanently delete a single specific version.
