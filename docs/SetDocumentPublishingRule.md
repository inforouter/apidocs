# SetDocumentPublishingRule API

Sets the publishing rule on a document, controlling which version is served as the released (published) version.

## Endpoint

```
/srv.asmx/SetDocumentPublishingRule
```

## Methods

- **GET** `/srv.asmx/SetDocumentPublishingRule?authenticationTicket=...&documentPath=...&publishingRule=...&publishedVersionNumber=...&releaseTag=...`
- **POST** `/srv.asmx/SetDocumentPublishingRule` (form data)
- **SOAP** Action: `http://tempuri.org/SetDocumentPublishingRule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Summary.pdf`). |
| `publishingRule` | string | Yes | Publishing rule to apply. See Publishing Rule Values below. Case-insensitive. |
| `publishedVersionNumber` | integer | Conditional | Internal version number to pin. Required only when `publishingRule` is `SPESIFICVERSION`; pass `0` for all other rules. |
| `releaseTag` | string | Conditional | Tag name identifying the version to publish. Required only when `publishingRule` is `TAGGED`; pass empty string for all other rules. |

## Publishing Rule Values

| Value | Description |
|-------|-------------|
| `LATEST` | Always serve the most recent version (default behavior). |
| `LASTAPPROVED` | Serve the most recently approved version. |
| `TAGGED` | Pin to the version that carries the tag specified in `releaseTag`. |
| `SPESIFICVERSION` | Pin to the exact internal version number in `publishedVersionNumber`. |
| `UNPUBLISHED` | Hide the document from read-only users (no version is published). |

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

The calling user must have **Set Publishing Rules** permission on the document (`IrAction.SetPublishingRules`). This permission is typically granted to document owners and library managers.

## Examples

### Set to latest version (POST)

```
POST /srv.asmx/SetDocumentPublishingRule HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
&publishingRule=LATEST
&publishedVersionNumber=0
&releaseTag=
```

### Pin to a specific version (GET)

```
GET /srv.asmx/SetDocumentPublishingRule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
    &publishingRule=SPESIFICVERSION
    &publishedVersionNumber=3000001
    &releaseTag=
HTTP/1.1
Host: yourserver
```

### Pin to a tagged version (POST)

```
POST /srv.asmx/SetDocumentPublishingRule HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&documentPath=%2FCorporate%2FPolicies%2FDataPolicy.pdf
&publishingRule=TAGGED
&publishedVersionNumber=0
&releaseTag=Approved-2026-Q1
```

### Unpublish a document (POST)

```
POST /srv.asmx/SetDocumentPublishingRule HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&documentPath=%2FCorporate%2FDrafts%2Fdraft.pdf
&publishingRule=UNPUBLISHED
&publishedVersionNumber=0
&releaseTag=
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

Decides which version of a document readers get.

```javascript
await call('SetDocumentPublishingRule', {
  authenticationTicket: ticket,
  documentPath: '/Finance/Reports/Q1.pdf',
  publishingRule: 'LATEST',
  publishedVersionNumber: 0,
  releaseTag: '-'              // must not be empty, even when the rule ignores it
});
```

The rule is one of `LATEST`, `LASTAPPROVED`, `TAGGED`, `SPESIFICVERSION`, `UNPUBLISHED`, and anything
else is refused `4000` with those five in the message.

**Note the spelling: `SPESIFICVERSION`.** The correctly spelled `SPECIFICVERSION` is refused. The
message is an untranslated English literal, so it reads the same in every language.

**`releaseTag` cannot be empty over REST.** It is declared as a non-nullable string, so model binding
refuses an empty one with HTTP 400 before the operation runs - even for `LATEST`, which has no tag and
ignores the value. Send any non-empty placeholder when the rule does not use it.

## Notes

- `publishingRule` is case-insensitive (`LATEST`, `latest`, and `Latest` are all accepted).
- `publishedVersionNumber` is the internal version number (e.g. `3000001` represents version `3.0.1`). Use `GetDocumentVersions` to retrieve the internal version numbers for a document.
- When `publishingRule` is `TAGGED`, the specified tag must already exist on a version of the document; the API will fail if the tag is not found.
- When `publishingRule` is `LASTAPPROVED` and no approved version exists, the document behaves as unpublished until an approved version is available.
- This API sets only the **publishing rule** (the policy). It does not upload a new version or modify version content. To upload a new version, use `UploadDocument`.
- Compare with `PublishDocument` (publishes a specific version number directly) and `UnpublishDocument` (sets the document to unpublished state directly).

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | `publishingRule` is not one of the five names |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4030` | the caller may not change the publishing rule here |
| `HTTP 400` | `releaseTag` or `publishingRule` was empty; refused by model binding, even where the rule ignores the tag |

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Document not found | `documentPath` does not refer to an existing document. |
| Access denied | The calling user does not have Set Publishing Rules permission on the document. |
| Invalid publishingRule | The `publishingRule` value is not one of the valid enum names. |
| releaseTag required | `publishingRule` is `TAGGED` but `releaseTag` is empty or whitespace. |

## Related APIs

- [PublishDocument](PublishDocument.md) - Publish a specific version number directly.
- [UnpublishDocument](UnpublishDocument.md) - Set a document to unpublished state directly.
- [GetDocumentVersions](GetDocumentVersions.md) - Retrieve version history and internal version numbers.
- [GetPublishingRequirements](GetPublishingRequirements.md) - Get the publishing requirements configured for a domain/library.
- [SetFolderPublishingRule](SetFolderPublishingRule.md) - Apply a publishing rule to all documents in a folder tree.
