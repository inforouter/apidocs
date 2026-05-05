# CreateHtmlDocument API

Creates a new HTML document in the specified folder. The HTML content is stored in the document's MetaTag field as an XML-encoded form data structure, which is the native infoRouter format for HTML form documents.

## Endpoint

```
/srv.asmx/CreateHtmlDocument
```

## Methods

- **GET** `/srv.asmx/CreateHtmlDocument?authenticationTicket=...&folderPath=...&name=...&htmlContent=...&xmlParameters=...`
- **POST** `/srv.asmx/CreateHtmlDocument` (form data)
- **SOAP** Action: `http://tempuri.org/CreateHtmlDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `folderPath` | string | Yes | Full infoRouter path of the destination folder (e.g. `/Finance/Reports`). |
| `name` | string | Yes | Document name. The `.htm` extension is appended automatically if the name does not already end with `.htm` or `.html`. |
| `htmlContent` | string | Yes | Raw HTML body text to store as the document content. |
| `xmlParameters` | string | No | XML string containing optional upload options. Pass an empty string to use server defaults. See format below. |

## xmlParameters Format

The `xmlParameters` value is an XML string. The root element is `<xmlparameters>` and each option is an `<item>` element with `NAME` and `VALUE` attributes:

```xml
<xmlparameters>
  <item NAME="DESCRIPTION" VALUE="Q1 financial summary"/>
  <item NAME="KEYWORDS" VALUE="finance quarterly"/>
  <item NAME="VERSIONCOMMENT" VALUE="Initial draft"/>
  <item NAME="CHECKOUT" VALUE="TRUE"/>
  <item NAME="PUBLISHOPTION" VALUE="Publish"/>
  <item NAME="SENDEMAILS" VALUE="true"/>
  <item NAME="CREATIONDATE" VALUE="2025-01-15"/>
  <item NAME="MODIFICATIONDATE" VALUE="2025-01-15"/>
  <item NAME="MPVERSIONMAJOR" VALUE="1"/>
  <item NAME="MPVERSIONMINOR" VALUE="0"/>
  <item NAME="MPVERSIONREVISION" VALUE="0"/>
</xmlparameters>
```

All `NAME` values are case-insensitive. If `VALUE` is omitted the element's inner text is used instead.

### Supported Parameter Names

| Name | Type | Description |
|------|------|-------------|
| `DESCRIPTION` | string | Document description. |
| `KEYWORDS` | string | Space- or comma-separated user-defined keywords. |
| `VERSIONCOMMENT` | string | Comment attached to the first document version. |
| `CHECKOUT` | bool (`true`/`false`) | Lock document immediately after creation. |
| `PUBLISHOPTION` | enum | Controls publishing after creation. Values: `ServerDefault`, `Publish`, `DontPublish`. Defaults to `ServerDefault`. |
| `SENDEMAILS` | bool (`true`/`false`) | Whether to send subscription notification emails to folder subscribers. Default: `true`. |
| `CREATIONDATE` | DateTime | Override the document creation date (e.g. `2025-01-15`). |
| `MODIFICATIONDATE` | DateTime | Override the document modification date (e.g. `2025-01-15`). |
| `MPVERSIONMAJOR` | short | Manual version major number (1–2400). |
| `MPVERSIONMINOR` | short | Manual version minor number (0–999). |
| `MPVERSIONREVISION` | short | Manual version revision number (0–999). |

### PublishOption Values

| Value | Behaviour |
|-------|-----------|
| `ServerDefault` | Applies the folder's configured publishing rule. |
| `Publish` | Forces the new document to be published immediately. |
| `DontPublish` | Saves the document without publishing it. |

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

authenticationTicket=abc123&folderPath=/Finance/Reports&name=Q1Summary&htmlContent=<h1>Q1 Summary</h1><p>Results were positive.</p>&xmlParameters=<xmlparameters><item NAME="DESCRIPTION" VALUE="Q1 financial summary"/><item NAME="SENDEMAILS" VALUE="false"/><item NAME="PUBLISHOPTION" VALUE="Publish"/></xmlparameters>
```

### Request (GET)

```
GET /srv.asmx/CreateHtmlDocument?authenticationTicket=abc123&folderPath=/Finance/Reports&name=Q1Summary&htmlContent=<h1>Q1</h1>&xmlParameters=<xmlparameters><item NAME="DESCRIPTION" VALUE="Summary"/></xmlparameters>
```

### Minimal Request (no xmlParameters)

```
GET /srv.asmx/CreateHtmlDocument?authenticationTicket=abc123&folderPath=/Finance/Reports&name=Q1Summary&htmlContent=<h1>Q1</h1>&xmlParameters=
```

## Notes

- The `.htm` extension is appended to `name` automatically if the name has no HTML extension. For example, `Q1Summary` becomes `Q1Summary.htm`.
- Parameter names in `xmlParameters` are case-insensitive.
- If `xmlParameters` is empty or omitted, server defaults apply for all options.
- Special XML characters in `htmlContent` (such as `<`, `>`, `&`) are escaped automatically before storage.

## Related APIs

- [GetDocumentAbstract](GetDocumentAbstract.md) — Retrieve the stored HTML content of an HTML form document.
- [CreateURL](CreateURL.md) — Create a URL shortcut document.
- [UploadDocument](UploadDocument.md) — Upload a binary document file.
- [CreateFolder](CreateFolder.md) — Create a folder to hold HTML documents.
