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
| `xmlContent` | string | Yes | XML-formatted data used to populate the template fields. Must use the `<FORMDATA>` structure described below. Pass an empty string if the template has no fields. |



## Response



### Success Response -" New Document Created



```xml

<response success="true" error="" DocumentID="42" DocumentName="Summary.htm" />

```



| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the document was created successfully. |
| `DocumentID` | The integer ID of the newly created document. |
| `DocumentName` | The name of the created file (`.htm` extension is added automatically if the path does not end with `.html` or `.htm`). |



### Success Response -" New Version Created



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



## xmlContent Format

The `xmlContent` parameter must use the `<FORMDATA>` structure. Each template field is represented as a `<Prompt>` element whose `Name` attribute is the field name and whose text content is the field value:

```xml
<FORMDATA>
  <Prompt Name="title">Q1 2026</Prompt>
  <Prompt Name="author">Jane Smith</Prompt>
  <Prompt Name="textcontent">Body text of the document...</Prompt>
</FORMDATA>
```

Pass an empty string for `xmlContent` only when the template has no user-defined fields.

### Obtaining field names from a rendered form

When calling this API after presenting the form to the user via [`CreateFormFromTemplate`](CreateFormFromTemplate.md), the rendered HTML contains a hidden input named `InfoRouter_Fields` that lists all template fields. Its value is a comma-separated array of 4-token groups:

```
'IR_title','CHAR','N','N','IR_author','CHAR','Y','N','IR_duedate','DATE','Y','N'
```

Each group of 4 tokens describes one field:

| Token (0-based position in group) | Meaning |
|---|---|
| 0 — `'IR_{fieldname}'` | Field name with `'IR_` prefix and trailing `'`. Strip those to get the HTML input name. |
| 1 — `'CHAR'` \| `'DATE'` \| `'NUMBER'` \| `'BOOLEAN'` | Data type of the field. |
| 2 — `'Y'` \| `'N'` | Whether the field is required. |
| 3 — `'N'` | Reserved, always `'N'`. |

To extract the field name from token 0: remove the leading `'IR_` (4 characters) and the trailing `'`.

**JavaScript example** — parse `InfoRouter_Fields` and build `xmlContent`:

```javascript
function parseInfoRouterFields(iframeDoc, form) {
  const fieldsInput = iframeDoc.getElementById('InfoRouter_Fields');
  if (!fieldsInput || !fieldsInput.value.trim()) return [];

  const tokens = fieldsInput.value.split(',');
  const fields = [];
  for (let i = 0; i + 3 < tokens.length; i += 4) {
    const raw      = tokens[i].trim();                    // e.g. "'IR_title'"
    const name     = raw.slice(4, raw.length - 1);        // strip 'IR_ prefix and trailing '
    const dataType = tokens[i + 1].trim().replace(/'/g, ''); // CHAR | DATE | NUMBER | BOOLEAN
    const required = tokens[i + 2].trim() === "'Y'";
    const el       = form.elements[name];
    const value    = el ? el.value : '';
    fields.push({ name, value, dataType, required });
  }
  return fields;
}

function buildXmlContent(fields) {
  if (!fields.length) return '';
  return '<FORMDATA>' +
    fields.map(f => `<Prompt Name="${f.name}">${escapeXml(f.value)}</Prompt>`).join('') +
    '</FORMDATA>';
}
```

---

## Example

### GET Request — Create new document

```
GET /srv.asmx/CreateDocumentUsingTemplate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/MyLibrary/Reports/Q1Summary.htm
  &TemplatePath=/Templates/QuarterlyReport.htm
  &xmlContent=%3CFORMDATA%3E%3CPrompt+Name%3D%22title%22%3EQ1+2026%3C%2FPrompt%3E%3C%2FFORMDATA%3E
HTTP/1.1
```

### POST Request — Create new document

```
POST /srv.asmx/CreateDocumentUsingTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Reports/Q1Summary.htm
&TemplatePath=/Templates/QuarterlyReport.htm
&xmlContent=<FORMDATA><Prompt Name="title">Q1 2026</Prompt><Prompt Name="author">Jane Smith</Prompt></FORMDATA>
```

### POST Request — Create new version using blank template

```
POST /srv.asmx/CreateDocumentUsingTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Reports/Q1Summary.htm
&TemplatePath=999
&xmlContent=<FORMDATA><Prompt Name="title">Q1 2026 (revised)</Prompt></FORMDATA>
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
      <tns:xmlContent>&lt;FORMDATA&gt;&lt;Prompt Name="title"&gt;Q1 2026&lt;/Prompt&gt;&lt;/FORMDATA&gt;</tns:xmlContent>
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

## React Implementer Guide

Production-ready patterns derived from the reference demo at `IRWebCore/wwwRoot/form-template-demo.html`. This API is always called after `CreateFormFromTemplate` (create flow) or `GetFormFromDocument` (update flow) has collected the user's form data via an iframe.

### Building xmlContent from iframe form data

```javascript
function escapeXml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}

// Parse the InfoRouter_Fields hidden input inside the rendered iframe form.
// Returns an array of { name, value, dataType, required }.
// Token format: 'IR_field1','CHAR','N','N','IR_field2','DATE','Y','N',...
function parseInfoRouterFields(iframeDoc, form) {
  const input = iframeDoc.getElementById('InfoRouter_Fields');
  if (!input || !input.value.trim()) return [];
  const tokens = input.value.split(',');
  const fields = [];
  for (let i = 0; i + 3 < tokens.length; i += 4) {
    const raw      = tokens[i].trim();
    if (raw.length < 5) continue;
    const name     = raw.slice(4, raw.length - 1);           // strip 'IR_ prefix + trailing '
    const dataType = tokens[i + 1].trim().replace(/'/g, ''); // CHAR | DATE | NUMBER | BOOLEAN
    const required = tokens[i + 2].trim() === "'Y'";
    const el       = form.elements[name];
    const value    = el ? el.value : '';
    fields.push({ name, value, dataType, required });
  }
  return fields;
}

// Build the <FORMDATA> XML payload for the xmlContent parameter
function buildXmlContent(fields) {
  if (!fields || fields.length === 0) return '';
  return '<FORMDATA>' +
    fields.map(f => `<Prompt Name="${f.name}">${escapeXml(f.value)}</Prompt>`).join('') +
    '</FORMDATA>';
}
```

### Create flow — new document

Called after `CreateFormFromTemplate` intercepts the iframe submit:

```javascript
async function createDocument({ apiBase, ticket, targetFolderPath, docName, templatePath, fields }) {
  const path       = targetFolderPath.replace(/\/+$/, '') + '/' + docName;
  const xmlContent = buildXmlContent(fields);

  const body = new URLSearchParams({
    AuthenticationTicket: ticket,
    Path:         path,          // New path → creates document
    TemplatePath: templatePath,  // Full path, ~D<id>, or '999' for blank template
    xmlContent,
  });
  const res = await fetch(`${apiBase}/CreateDocumentUsingTemplate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
  const doc  = new DOMParser().parseFromString(await res.text(), 'text/xml');
  const root = doc.querySelector('response') ?? doc.querySelector('root');
  if (root?.getAttribute('success') !== 'true') {
    throw new Error(root?.getAttribute('error') ?? 'Create failed');
  }
  return {
    documentId:   root.getAttribute('DocumentID'),    // numeric string
    documentName: root.getAttribute('DocumentName'),  // filename, .htm extension added automatically
    path,
  };
}
```

### Update flow — new version of an existing document

Called after `GetFormFromDocument` intercepts the iframe submit:

```javascript
async function updateDocument({ apiBase, ticket, existingDocPath, templatePath, fields }) {
  const xmlContent = buildXmlContent(fields);

  const body = new URLSearchParams({
    AuthenticationTicket: ticket,
    Path:         existingDocPath,  // Existing path → creates new version, checks document back in
    TemplatePath: templatePath,     // ~D{id} read from the InfoRouter_TemplateID hidden field
    xmlContent,
  });
  const res = await fetch(`${apiBase}/CreateDocumentUsingTemplate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
  const doc  = new DOMParser().parseFromString(await res.text(), 'text/xml');
  const root = doc.querySelector('root') ?? doc.querySelector('response');
  if (root?.getAttribute('success') !== 'true') {
    throw new Error(root?.getAttribute('error') ?? 'Update failed');
  }
  // No DocumentID or DocumentName on success — new version response is <root success="true"/>
}
```

### Response format reference

| Scenario | Root element | `DocumentID` | `DocumentName` |
|---|---|---|---|
| New document created | `<response>` | Present — numeric string | Present — filename with `.htm` |
| New version created | `<root>` | Absent | Absent |

Always query with a fallback (`doc.querySelector('response') ?? doc.querySelector('root')`) because the element name differs between the two modes.

### End-to-end flow summary

```
── Create new document ──────────────────────────────────────────────────
1. AuthenticateUser → ticket
2. CreateFormFromTemplate(targetFolderPath, templatePath, submitUrl='')
   → renderedHtml (HTML wrapped in CDATA — use r.el.textContent)
3. Render in <iframe srcDoc={renderedHtml} onLoad={handleLoad} sandbox="allow-scripts allow-forms allow-same-origin">
4. In onLoad: inject InfoRouter_Ticket; intercept form submit with e.preventDefault()
5. On submit: parseInfoRouterFields(iframeDoc, form) → fields[]
              buildXmlContent(fields) → xmlContent
6. CreateDocumentUsingTemplate(Path=newPath, TemplatePath=templatePath, xmlContent)
   → <response success="true" DocumentID="42" DocumentName="file.htm"/>

── Update existing document ─────────────────────────────────────────────
1. AuthenticateUser → ticket
2. GetFormFromDocument(documentPath, submitUrl='')
   → renderedHtml (pre-filled HTML; document checked out)
3. Render in <iframe srcDoc={renderedHtml} onLoad={handleLoad} sandbox="allow-scripts allow-forms allow-same-origin">
4. In onLoad: inject InfoRouter_Ticket; intercept form submit with e.preventDefault()
             read InfoRouter_TemplateID → templatePath = '~D{id}'
5. On submit: parseInfoRouterFields(iframeDoc, form) → fields[]
              buildXmlContent(fields) → xmlContent
6. CreateDocumentUsingTemplate(Path=existingDocPath, TemplatePath='~D{id}', xmlContent)
   → <root success="true"/>  (document checked back in; no DocumentID returned)
```

---


