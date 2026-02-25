# CreateDocumentUsingTemplate API

Creates a new HTML document or a new version of an existing document at the specified path, using an infoRouter template document and XML content data to populate the template fields.

When the target `Path` does not exist, a new document is created. When it already exists, a new version of that document is created using the template.

## Endpoint

```
/srv.asmx/CreateDocumentUsingTemplate
```

## Methods

- **GET** `/srv.asmx/CreateDocumentUsingTemplate?authenticationTicket=...&Path=...&TemplatePath=...&xmlContent=...`
- **POST** `/srv.asmx/CreateDocumentUsingTemplate` (form data)
- **SOAP** Action: `http://tempuri.org/CreateDocumentUsingTemplate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path for the document to create or update (e.g. `/MyLibrary/Reports/Summary.htm`). If the path does not yet exist, a new document is created. If it already exists, a new version is created. |
| `TemplatePath` | string | Yes | Full infoRouter path of the existing HTML template document to use (e.g. `/Templates/ReportTemplate.htm`). Pass `"999"` to use a blank/empty template. |
| `xmlContent` | string | Yes | XML-formatted data used to populate the template fields. Pass an empty string if no field data is required. |

## Response

### Success Response — New Document Created

```xml
<response success="true" error="" DocumentID="42" DocumentName="Summary.htm" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the document was created successfully. |
| `DocumentID` | The integer ID of the newly created document. |
| `DocumentName` | The name of the created file (`.htm` extension is added automatically if the path does not end with `.html` or `.htm`). |

### Success Response — New Version Created

```xml
<root success="true" />
```

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

- **Creating a new document**: The authenticated user must have **Add Document** permission on the destination folder (the parent of `Path`).
- **Creating a new version**: The authenticated user must have **Check Out** and **Publish** permissions on the existing document at `Path`. If the document is already checked out by another user, the call fails.

---

## Example

### GET Request — Create new document

```
GET /srv.asmx/CreateDocumentUsingTemplate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/MyLibrary/Reports/Q1Summary.htm
  &TemplatePath=/Templates/QuarterlyReport.htm
  &xmlContent=%3Cfields%3E%3Ctitle%3EQ1+2026%3C%2Ftitle%3E%3C%2Ffields%3E
HTTP/1.1
```

### POST Request — Create new document

```
POST /srv.asmx/CreateDocumentUsingTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Reports/Q1Summary.htm
&TemplatePath=/Templates/QuarterlyReport.htm
&xmlContent=<fields><title>Q1 2026</title><author>Jane Smith</author></fields>
```

### POST Request — Create new version using blank template

```
POST /srv.asmx/CreateDocumentUsingTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Reports/Q1Summary.htm
&TemplatePath=999
&xmlContent=<fields><title>Q1 2026 (revised)</title></fields>
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateDocumentUsingTemplate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/MyLibrary/Reports/Q1Summary.htm</tns:Path>
      <tns:TemplatePath>/Templates/QuarterlyReport.htm</tns:TemplatePath>
      <tns:xmlContent>&lt;fields&gt;&lt;title&gt;Q1 2026&lt;/title&gt;&lt;/fields&gt;</tns:xmlContent>
    </tns:CreateDocumentUsingTemplate>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API produces **HTML documents** (`.html` / `.htm`). If the document name in `Path` does not end with `.html` or `.htm`, the extension `.htm` is automatically appended to the created file name.
- The destination folder (the parent of `Path`) must already exist. It is not created automatically.
- When creating a **new version** of an existing document that is not currently checked out, the API automatically checks the document out and then publishes the new version (leaving the document checked in).
- When creating a **new version** of a document that is **already checked out by the current user**, the document remains checked out after the call.
- If the document at `Path` is checked out by a **different user**, the call fails with an error.
- Pass `TemplatePath = "999"` to generate the document content from a blank template rather than an existing template file.
- The response root element differs between the two modes: `<response>` when creating a new document, `<root>` when creating a new version.

---

## Related APIs

- [UploadDocument](UploadDocument.md) - Upload a document from raw file bytes
- [GetDocument](GetDocument.md) - Retrieve properties of a document
- [GetDocumentVersions](GetDocumentVersions.md) - List all versions of a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The destination folder (parent of `Path`) does not exist or is not accessible. |
| `Document not found` | The `TemplatePath` does not refer to an existing document. |
| `This document has been checked out by another user.` | The document at `Path` is checked out by a different user; a new version cannot be created. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateDocumentUsingTemplate*
