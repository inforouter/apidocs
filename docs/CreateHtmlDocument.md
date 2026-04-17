# CreateHtmlDocument API

Creates a new HTML document in the specified folder. The HTML content is stored in the document's MetaTag field as an XML-encoded form data structure, which is the native infoRouter format for HTML form documents.

## Endpoint

```
/srv.asmx/CreateHtmlDocument
```

## Methods

- **GET** `/srv.asmx/CreateHtmlDocument?authenticationTicket=...&folderPath=...&name=...&htmlContent=...&description=...&sendMail=...&publishOption=...`
- **POST** `/srv.asmx/CreateHtmlDocument` (form data)
- **SOAP** Action: `http://tempuri.org/CreateHtmlDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `folderPath` | string | Yes | Full infoRouter path of the destination folder (e.g. `/Finance/Reports`). |
| `name` | string | Yes | Document name. The `.htm` extension is appended automatically if the name does not already end with `.htm` or `.html`. |
| `htmlContent` | string | Yes | Raw HTML body text to store as the document content. |
| `description` | string | Yes | Document description. Pass an empty string for no description. |
| `sendMail` | bool | Yes | Whether to send subscription notification emails to folder subscribers after creation. |
| `publishOption` | integer | Yes | Controls how the new document version is published. `0` = ServerDefault, `1` = Publish, `2` = DontPublish. |

## publishOption Values

| Value | Name | Behaviour |
|-------|------|-----------|
| `0` | ServerDefault | Applies the folder's configured publishing rule. |
| `1` | Publish | Forces the new document to be published immediately. |
| `2` | DontPublish | Saves the document without publishing it. |

## Response

### Success Response

```xml
<root success="true" documentId="1234" />
```

| Attribute | Description |
|-----------|-------------|
| `documentId` | Integer ID of the newly created document. |

### Error Response

```xml
<root success="false" error="Error message" />
```

## Required Permissions

The calling user must have Add Document permission on the destination folder.

## Document Format

infoRouter HTML documents store their content as XML in the document's MetaTag field rather than as a binary file. The API wraps the provided `htmlContent` in the standard infoRouter form data XML structure:

```xml
<FORMDATA>
  <Prompt Name="textcontent">...html content...</Prompt>
</FORMDATA>
```

This format is compatible with the infoRouter HTML document editor and can be read back using `GetDocumentAbstract`.

## Example

### Request (POST)

```
POST /srv.asmx/CreateHtmlDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&folderPath=/Finance/Reports&name=Q1Summary&htmlContent=<h1>Q1 Summary</h1><p>Results were positive.</p>&description=Q1 financial summary&sendMail=false
```

### Request (GET)

```
GET /srv.asmx/CreateHtmlDocument?authenticationTicket=abc123&folderPath=/Finance/Reports&name=Q1Summary&htmlContent=<h1>Q1</h1>&description=Summary&sendMail=false
```

## Notes

- The `.htm` extension is appended to `name` automatically if the name has no HTML extension. For example, `Q1Summary` becomes `Q1Summary.htm`.
- The publishing behaviour after creation follows the folder's configured publishing rule (`ServerDefault`).
- Special XML characters in `htmlContent` (such as `<`, `>`, `&`) are escaped automatically before storage.
- To update an existing HTML document, use `UpdateURLDocument` is not applicable — use `UploadDocument` with the HTML bytes, or re-submit via the HTML editor workflow.

## Related APIs

- [GetDocumentAbstract](GetDocumentAbstract.md) — Retrieve the stored HTML content of an HTML form document.
- [CreateURL](CreateURL.md) — Create a URL shortcut document.
- [UploadDocument](UploadDocument.md) — Upload a binary document file.
- [CreateFolder](CreateFolder.md) — Create a folder to hold HTML documents.
