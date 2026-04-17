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

## Notes

- To create a new HTML document instead of updating an existing one, use `CreateHtmlDocument`.
- Passing `null` for `description` preserves the document's current description; passing an empty string clears it.
- The document path must point to an existing HTML (`.htm` / `.html`) document.

## Related APIs

- [CreateHtmlDocument](CreateHtmlDocument.md) — Create a new HTML document in a folder.
- [GetDocumentAbstract](GetDocumentAbstract.md) — Retrieve the stored HTML content of an HTML form document.
- [UpdateURLDocument](UpdateURLDocument.md) — Update the hyperlink address of an existing URL shortcut document.
- [UploadDocument](UploadDocument.md) — Upload a binary document file as a new version.
