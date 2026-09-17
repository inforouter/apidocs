# UpdateURLDocument API

Updates the hyperlink address of an existing URL shortcut document (`.url` extension) by publishing a new version with the new address stored in the document's MetaTag field.

## Endpoint

```
/srv.asmx/UpdateURLDocument
```

## Methods

- **GET** `/srv.asmx/UpdateURLDocument?authenticationTicket=...&documentPath=...&address=...&sendMail=...&publishOption=...`
- **POST** `/srv.asmx/UpdateURLDocument` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateURLDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the URL shortcut document to update (e.g. `/Finance/Links/Homepage.url`). |
| `address` | string | Yes | New hyperlink URL to store on the document. |
| `sendMail` | bool | Yes | Whether to send subscription notification emails when the new version is published. Pass `true` to notify subscribers, `false` to suppress notifications. |
| `publishOption` | integer | Yes | Controls how the new version is published. `0` = ServerDefault (use the folder/document publishing rule), `1` = Publish (force publish), `2` = DontPublish (save without publishing). |

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

The calling user must have Check Out and Publish permissions on the document. The document must not be checked out by another user.

## Checkout Behaviour

- If the document is not checked out, it is automatically checked out by the calling user before the new version is published.
- If the document is already checked out by the calling user, the update proceeds normally.
- If the document is checked out by a different user, the call returns an error.

## publishOption Values

| Value | Name | Behaviour |
|-------|------|-----------|
| `0` | ServerDefault | Applies the folder or document publishing rule configured in infoRouter. |
| `1` | Publish | Forces the new version to be published immediately regardless of the publishing rule. |
| `2` | DontPublish | Saves the new version without publishing it. |

## Example

### Request (POST)

```
POST /srv.asmx/UpdateURLDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/Finance/Links/Homepage.url&address=https://example.com/new&sendMail=true&publishOption=0
```

### Request (GET)

```
GET /srv.asmx/UpdateURLDocument?authenticationTicket=abc123&documentPath=/Finance/Links/Homepage.url&address=https://example.com/new&sendMail=true&publishOption=0
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

Changes the address a stored link points at, creating a new version.

```javascript
await call('UpdateURLDocument', {
  authenticationTicket: ticket,
  documentPath: '/Finance/Links/supplier.url',
  address: 'https://www.example.com/portal/v2',
  sendMail: false,
  publishOption: 0
});
```

Pointing this at an HTML document is refused `4000`, with a message about parsing XML content - the
document is read as a link file and is not one. Use [UpdateHtmlDocument](UpdateHtmlDocument.md) for
those. The two disagree about how to report the mismatch: this one refuses properly, the other lets an
exception out.

As with [CreateURL](CreateURL.md), the address is not checked - anything non-empty is stored as
written.

## Notes

- The document at `documentPath` must be a URL shortcut (`.url` extension). Passing a regular document path will result in an error from `PublishAsync` since the document has no binary content to update.
- To create a new URL shortcut document use `CreateURL`.
- The `address` field is stored in the document's MetaTag and is not validated as a URL — any non-empty string is accepted.

## Related APIs

- [CreateURL](CreateURL.md) — Create a new URL shortcut document.
- [GetDocument](GetDocument.md) — Retrieve document metadata including the current MetaTag (URL address).
- [UndoCheckOut](UndoCheckOut.md) — Discard a checked-out version and release the checkout lock.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4030` | the caller may not change this document |
| `4000` | the document is not a link document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

