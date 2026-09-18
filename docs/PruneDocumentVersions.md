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

Removes old versions of a document, keeping the most recent few.

```javascript
await call('PruneDocumentVersions', {
  authenticationTicket: ticket,
  documentPath: '/Finance/Reports/Q1.pdf',
  keepPublished: 3,
  keepUnpublished: 1
});
```

**Both counts must be 1 or greater.** `0` and negative values are refused with `4000` - there is no
way to ask this operation to leave a document with no versions, which is the point of it. The refusal
is a translated message; it used to be an untranslated English literal.

A document with fewer versions than the counts allow is a success that removes nothing.

## Notes

- This operation is **irreversible**. Deleted versions cannot be recovered.
- `keepPublished` must be at least 1 — it is not possible to delete all published versions.
- `keepUnpublished` may be 0 to delete all unpublished versions (subject to the pruning rules above).
- Use `GetDocumentVersions` to inspect the current version history before pruning.

## Related APIs

- [GetDocumentVersions](GetDocumentVersions.md) — Get the complete version history for a document.
- [DeleteDocumentVersion](DeleteDocumentVersion.md) — Permanently delete a single specific version.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | `keepPublished` or `keepUnpublished` is less than 1 |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4030` | the caller may not delete versions here |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

