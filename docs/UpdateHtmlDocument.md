# UpdateHtmlDocument API

Updates the HTML content (and optionally the description) of an existing HTML document. The document is checked out, a new version is created with the provided HTML body, and then published according to `publishOption`.

## Endpoint

```
/srv.asmx/UpdateHtmlDocument
```

## Methods

- **GET** `/srv.asmx/UpdateHtmlDocument?authenticationTicket=...&documentPath=...&htmlContent=...&description=...&sendMail=...&publishOption=...`
- **POST** `/srv.asmx/UpdateHtmlDocument` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateHtmlDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the existing HTML document (e.g. `/Finance/Reports/Q1Summary.htm`). |
| `htmlContent` | string | Yes | New raw HTML body text to store as the document content. |
| `description` | string | No | New document description. Pass `null` to leave the existing description unchanged. |
| `sendMail` | bool | Yes | Whether to send subscription notification emails to folder subscribers after the update. |
| `publishOption` | integer | Yes | Controls how the new document version is published. `0` = ServerDefault, `1` = Publish, `2` = DontPublish. |

## publishOption Values

| Value | Name | Behaviour |
|-------|------|-----------|
| `0` | ServerDefault | Applies the folder's configured publishing rule. |
| `1` | Publish | Forces the new document version to be published immediately. |
| `2` | DontPublish | Saves the new version without publishing it. |

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

The calling user must have Check Out permission on the document. If the document is already checked out by a different user the call fails with an access-denied error.

## Document Format

The provided `htmlContent` is wrapped in the standard infoRouter HTML form data structure before storage:

```xml
<FORMDATA>
  <Prompt Name="textcontent">...html content...</Prompt>
</FORMDATA>
```

Special XML characters in `htmlContent` (such as `<`, `>`, `&`) are escaped automatically before storage.

## Checkout Behaviour

- If the document is not checked out, the API checks it out automatically before creating the new version.
- If the document is already checked out by the **calling user**, the existing checkout is reused.
- If the document is checked out by a **different user**, the call fails immediately without modifying the document.

## Example

### Request (POST)

```
POST /srv.asmx/UpdateHtmlDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.htm&htmlContent=<h1>Q1 Summary</h1><p>Updated results.</p>&description=Updated Q1 summary&sendMail=false&publishOption=1
```

### Request (GET)

```
GET /srv.asmx/UpdateHtmlDocument?authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.htm&htmlContent=<h1>Q1</h1>&description=&sendMail=false&publishOption=0
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

Replaces the content of an HTML document, creating a new version.

```javascript
await call('UpdateHtmlDocument', {
  authenticationTicket: ticket,
  documentPath: '/Finance/Reports/summary.htm',
  htmlContent: '<html><body><h1>Q1</h1></body></html>',
  description: 'Revised after review',
  sendMail: false,
  publishOption: 0
});
```

**Every call makes a new version.** A document updated three times carries `1000000`, `1000001` and
`1000002` - it does not overwrite in place, and no checkout is needed.

**`publishOption` is checked** against the three values it has - `0` server default, `1` publish,
`2` do not publish - and anything else is refused `4000`. Until 9.0 it was cast straight into the
enum, so `99` was accepted as readily as `0`. [UpdateURLDocument](UpdateURLDocument.md) had the same
unchecked cast and checks it too.

Use [UpdateURLDocument](UpdateURLDocument.md) for a `.url` document. Pointing this one at a `.url`
or a shortcut is refused with `4000`, and the document is not checked out.

## Notes

- To create a new HTML document instead of updating an existing one, use `CreateHtmlDocument`.
- Passing `null` for `description` preserves the document's current description; passing an empty string clears it.
- The document path must point to an existing HTML (`.htm` / `.html`) document.

## Related APIs

- [CreateHtmlDocument](CreateHtmlDocument.md) — Create a new HTML document in a folder.
- [GetDocumentAbstract](GetDocumentAbstract.md) — Retrieve the stored HTML content of an HTML form document.
- [UpdateURLDocument](UpdateURLDocument.md) — Update the hyperlink address of an existing URL shortcut document.
- [UploadDocument](UploadDocument.md) — Upload a binary document file as a new version.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4030` | the caller may not change this document |
| `4000` | the document is a `.url` or a shortcut rather than an HTML document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

