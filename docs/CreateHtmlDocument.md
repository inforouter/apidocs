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

`xmlParameters` is an XML document with a root element containing `<Parameter>` child elements. Each element specifies a `Name` attribute (case-insensitive) and either a `Value` attribute or inner text.

```xml
<Parameters>
  <Parameter Name="Description" Value="Q1 financial summary" />
  <Parameter Name="PublishOption" Value="Publish" />
  <Parameter Name="SendEmails" Value="true" />
  <Parameter Name="Keywords" Value="finance quarterly" />
  <Parameter Name="VersionComment" Value="Initial draft" />
  <Parameter Name="CreationDate" Value="2025-01-15T09:00:00" />
  <Parameter Name="ModificationDate" Value="2025-01-15T09:00:00" />
  <Parameter Name="MpVersionMajor" Value="1" />
  <Parameter Name="MpVersionMinor" Value="0" />
  <Parameter Name="MpVersionRevision" Value="0" />
</Parameters>
```

### Supported Parameter Names

| Name | Type | Description |
|------|------|-------------|
| `Description` | string | Document description. |
| `PublishOption` | string | Controls publishing after creation. Values: `ServerDefault`, `Publish`, `DontPublish`. Defaults to `ServerDefault`. |
| `SendEmails` | bool | Whether to send subscription notification emails to folder subscribers. Values: `true`, `false`. |
| `Keywords` | string | Space-separated user-defined keywords. |
| `VersionComment` | string | Comment attached to the first document version. |
| `CreationDate` | datetime | Override the document creation date. |
| `ModificationDate` | datetime | Override the document modification date. |
| `MpVersionMajor` | short | Manual version major number (1–2400). |
| `MpVersionMinor` | short | Manual version minor number (1–999). |
| `MpVersionRevision` | short | Manual version revision number (1–999). |

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

authenticationTicket=abc123&folderPath=/Finance/Reports&name=Q1Summary&htmlContent=<h1>Q1 Summary</h1><p>Results were positive.</p>&xmlParameters=<Parameters><Parameter Name="Description" Value="Q1 financial summary" /><Parameter Name="SendEmails" Value="false" /><Parameter Name="PublishOption" Value="Publish" /></Parameters>
```

### Request (GET)

```
GET /srv.asmx/CreateHtmlDocument?authenticationTicket=abc123&folderPath=/Finance/Reports&name=Q1Summary&htmlContent=<h1>Q1</h1>&xmlParameters=<Parameters><Parameter Name="Description" Value="Summary" /></Parameters>
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
