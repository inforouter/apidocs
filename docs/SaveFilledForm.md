# SaveFilledForm API

Saves the filled form data as a new HTML document or a new version of an existing document at the specified path, using an infoRouter template document and XML content data to populate the template fields.

When the target `path` does not exist, a new document is created. When it already exists, a new version of that document is created using the template.

This API is the save step in the three-API form workflow:

```
UseFormTemplate / EditFilledForm  →  user fills in the form  →  SaveFilledForm
```

## Endpoint

```
/srv.asmx/SaveFilledForm
```

## Methods

- **GET** `/srv.asmx/SaveFilledForm?authenticationTicket=...&path=...&templatePath=...&xmlContent=...`
- **POST** `/srv.asmx/SaveFilledForm` (form data)
- **SOAP** Action: `http://tempuri.org/SaveFilledForm`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path for the document to create or update (e.g. `/MyLibrary/Reports/Summary.htm`). If the path does not yet exist, a new document is created. If it already exists, a new version is created. |
| `templatePath` | string | Yes | Full infoRouter path of the existing HTML template document to use (e.g. `/Templates/ReportTemplate.htm`), or `~D<id>` short form (e.g. `~D42`). Pass `"999"` to use a blank/empty template. |
| `xmlContent` | string | Yes | XML-formatted data used to populate the template fields. Must use the `<FORMDATA>` structure described below. Pass an empty string if the template has no fields. |
| `detachDocumentFromTemplate` | bool | No | Default `false`. When `true`, the document is saved as usual, then left an ordinary document with no link to its form template. See [Detaching from the template](#detaching-from-the-template). |

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

- **Creating a new document**: The authenticated user must have **Add Document** permission on the destination folder (the parent of `path`).
- **Creating a new version**: The authenticated user must have **Check Out** and **Publish** permissions on the existing document at `path`. If the document is already checked out by another user, the call fails.

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

### Detaching from the template

A document saved from a form template stays bound to it: every new version is rendered from the template again, [EditFilledForm](EditFilledForm.md) edits its fields, and a file checked in to it is **not** kept: the check-in succeeds, but what is stored is the template rendered again with no form data. Pass `detachDocumentFromTemplate=true` to save it as usual and then leave it an **ordinary document**, checked out and in as the `.docx`, `.pdf` or `.htm` file it became:

- The document is rendered from the template first, exactly as without the flag.
- Then its template and dynamic content flag are removed, in the same transaction as the save: a new document is created already detached; for a new version, the version is rendered and the document detached together.
- The form data stays with the version, as history; nothing reads it once the document is detached.
- [EditFilledForm](EditFilledForm.md) no longer applies to it (`4000`, not a filled form).
- A document with dynamic content is no longer rendered on every download; it keeps the content it was saved with.
- It cannot be re-attached. Detaching needs no right beyond the save itself.
- As an ordinary document, it is subject to the library's maximum document size on later versions, from which form documents are exempt.

### Filling a PDF or Word template directly

`templatePath` can name a PDF or Word document itself, with no HTML form in front of it. The form data fills it the same way as a `render-with` template (below), and the document is stored as the filled `.pdf` or `.docx`. [UseFormTemplate](UseFormTemplate.md) lists such a template's fields (`formType="fields"`), and [EditFilledForm](EditFilledForm.md) lists them again with the saved values; pass the `templateId` they return as `templatePath=~D<templateId>`.

A PDF template's text, multiline, choice, checkbox and radio fields are all filled. A checkbox is ticked by `true`, `yes`, `on`, `1` or its own on value, and cleared by anything else. A radio or choice field takes one of its `option` values; a radio group is left as it is for a value it does not have.

### Rendering into a PDF or a Word document

A form can name a document to render its data into, with a `render-with` meta tag in its `<head>`:

```html
<meta name="render-with" content="/Form Templates/business-letter.docx" />
```

When the form at `templatePath` has one, what is stored is not HTML but the filled template, named with the template's extension (`letter` or `letter.htm` becomes `letter.docx`, `letter.pdf`; a name that already ends `.docx` or `.pdf` is kept as it is):

| Template | How it is filled |
|---|---|
| `.pdf` | Its form fields (text, multiline, choice, checkbox, radio) are set from the `<Prompt>` of the same name. |
| `.docx` | Its `{{placeholders}}` are replaced with the `<Prompt>` of the same name. |

Both match a `<Prompt>` to a field or placeholder without regard to case, and a field the form data does not supply is left blank.

#### Writing a Word template

Type the placeholders into the document in Word, where the value should appear:

```
{{today}}

{{Recipient_name}}
{{Recipient_address}}

Dear {{Salutation}},

{{Body}}

{?{Enclosures.Length > 0}}Enclosures: {{Enclosures}}{{/}}
{?{cc.Length > 0}}cc: {{cc}}{{/}}
```

- A name is letters, digits and underscores, and matches the form field's `id`/`name`: `{{Recipient_name}}`. A name with a hyphen or a space (`{{customer-name}}`) is not a placeholder and stays in the document as typed.
- A value with several lines (a `<textarea>`) keeps its lines.
- `{?{...}}...{{/}}` keeps the text between only when the condition holds; a paragraph that holds nothing but the condition is removed altogether when it does not. `Name.Length > 0` tests that a value was entered. Avoid quotes in conditions: Word turns typed `""` into curly quotes, which are not quotes to the template engine.
- Placeholders work in the page headers and footers too.
- Formatting the placeholder (bold, font, colour) formats the value that replaces it.
- A template the engine cannot read, such as a `{?{...}}` with no closing `{{/}}`, fails the call with an error starting `[00100]WordFunctions.FillWordTemplate()`, and nothing is created.

A stored HTML filled form can also be rendered into a Word template on download, without storing it: `/docs/<library>/<folder>/<document>?RenderLayout=/Form Templates/business-letter.docx`.

### Obtaining field names from a rendered form

When calling this API after presenting the form to the user via [`UseFormTemplate`](UseFormTemplate.md), the rendered HTML contains a hidden input named `InfoRouter_Fields` that lists all template fields. Its value is a comma-separated array of 4-token groups:

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
GET /srv.asmx/SaveFilledForm
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/MyLibrary/Reports/Q1Summary.htm
  &templatePath=/Templates/QuarterlyReport.htm
  &xmlContent=%3CFORMDATA%3E%3CPrompt+Name%3D%22title%22%3EQ1+2026%3C%2FPrompt%3E%3C%2FFORMDATA%3E
HTTP/1.1
```

### POST Request — Create new document

```
POST /srv.asmx/SaveFilledForm HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/MyLibrary/Reports/Q1Summary.htm
&templatePath=/Templates/QuarterlyReport.htm
&xmlContent=<FORMDATA><Prompt Name="title">Q1 2026</Prompt><Prompt Name="author">Jane Smith</Prompt></FORMDATA>
```

### POST Request — Create new version using blank template

```
POST /srv.asmx/SaveFilledForm HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/MyLibrary/Reports/Q1Summary.htm
&templatePath=999
&xmlContent=<FORMDATA><Prompt Name="title">Q1 2026 (revised)</Prompt></FORMDATA>
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SaveFilledForm>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/MyLibrary/Reports/Q1Summary.htm</tns:path>
      <tns:templatePath>/Templates/QuarterlyReport.htm</tns:templatePath>
      <tns:xmlContent>&lt;FORMDATA&gt;&lt;Prompt Name="title"&gt;Q1 2026&lt;/Prompt&gt;&lt;/FORMDATA&gt;</tns:xmlContent>
    </tns:SaveFilledForm>
  </soap:Body>
</soap:Envelope>
```

---

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

Writes a filled form back as a document, from a template and the content that was entered.

```javascript
const root = await call('SaveFilledForm', {
  authenticationTicket: ticket,
  path: '/Forms/Filled/expenses-2026-03.htm',   // the document to write
  templatePath: '/Forms/Templates/expenses.htm',
  xmlContent: '<form><field name="total">412.80</field></form>'
});

console.log(root.getAttribute('DocumentID'), root.getAttribute('DocumentName'));
```

`path` is the document to create, complete with its name.
[EditFilledForm](EditFilledForm.md) is the other half of the pair - though note the warning on its
page before using it.

## Notes

- This API produces **HTML documents** (`.html` / `.htm`). If the document name in `path` does not end with `.html` or `.htm`, the extension `.htm` is automatically appended to the created file name. The exception is a PDF or Word template, used directly or as a form's `render-with`: the document is then the filled `.pdf` or `.docx`, named with that extension instead (see [Filling a PDF or Word template directly](#filling-a-pdf-or-word-template-directly)).
- The destination folder (the parent of `path`) must already exist. It is not created automatically.
- When creating a **new version** of an existing document that is not currently checked out, the API automatically checks the document out and then publishes the new version (leaving the document checked in).
- When creating a **new version** of a document that is **already checked out by the current user**, the document remains checked out after the call.
- If the document at `path` is checked out by a **different user**, the call fails with an error.
- Pass `templatePath = "999"` to generate the document content from a blank template rather than an existing template file.
- The response root element differs between the two modes: `<response>` when creating a new document, `<root>` when creating a new version.

---

## Related APIs

- [UseFormTemplate](UseFormTemplate.md) — Return a blank form from a template for the user to fill in (create flow)
- [EditFilledForm](EditFilledForm.md) — Return a pre-filled form for the user to edit (update flow)
- [UploadDocument](UploadDocument.md) — Upload a document from raw file bytes
- [GetDocument](GetDocument.md) — Retrieve properties of a document
- [GetDocumentVersions](GetDocumentVersions.md) — List all versions of a document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4090` | a document of that name is already in the folder |
| `4041` | no folder at the parent of `path`, or no document at `templatePath` |
| `4030` | the caller may not create documents there |
| `5000` | a new document: the form's PDF or Word template could not be filled |
| `4000` | a new version: the form's PDF or Word template could not be filled |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The destination folder (parent of `path`) does not exist or is not accessible. |
| `Document not found` | The `templatePath` does not refer to an existing document. |
| `This document has been checked out by another user.` | The document at `path` is checked out by a different user; a new version cannot be created. |

---

## React Implementer Guide

Production-ready patterns derived from the reference demo at `IRWebCore/wwwRoot/form-template-demo.html`. This API is always called after `UseFormTemplate` (create flow) or `EditFilledForm` (update flow) has collected the user's form data via an iframe.

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

Called after `UseFormTemplate` intercepts the iframe submit:

```javascript
async function createDocument({ apiBase, ticket, targetFolderPath, docName, templatePath, fields }) {
  const path       = targetFolderPath.replace(/\/+$/, '') + '/' + docName;
  const xmlContent = buildXmlContent(fields);

  const body = new URLSearchParams({
    authenticationTicket: ticket,
    path,                        // New path → creates document
    templatePath,                // Full path, ~D<id>, or '999' for blank template
    xmlContent,
  });
  const res = await fetch(`${apiBase}/SaveFilledForm`, {
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

Called after `EditFilledForm` intercepts the iframe submit:

```javascript
async function updateDocument({ apiBase, ticket, existingDocPath, templatePath, fields }) {
  const xmlContent = buildXmlContent(fields);

  const body = new URLSearchParams({
    authenticationTicket: ticket,
    path:         existingDocPath,  // Existing path → creates new version, checks document back in
    templatePath,                   // ~D{id} read from the InfoRouter_TemplateID hidden field
    xmlContent,
  });
  const res = await fetch(`${apiBase}/SaveFilledForm`, {
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
2. UseFormTemplate(targetFolderPath, templatePath, submitUrl='')
   → renderedHtml (HTML wrapped in CDATA — use r.el.textContent)
3. Render in <iframe srcDoc={renderedHtml} onLoad={handleLoad} sandbox="allow-scripts allow-forms allow-same-origin">
4. In onLoad: inject InfoRouter_Ticket; intercept form submit with e.preventDefault()
5. On submit: parseInfoRouterFields(iframeDoc, form) → fields[]
              buildXmlContent(fields) → xmlContent
6. SaveFilledForm(path=newPath, templatePath=templatePath, xmlContent)
   → <response success="true" DocumentID="42" DocumentName="file.htm"/>

── Update existing document ─────────────────────────────────────────────
1. AuthenticateUser → ticket
2. EditFilledForm(documentPath, submitUrl='')
   → renderedHtml (pre-filled HTML; document checked out)
3. Render in <iframe srcDoc={renderedHtml} onLoad={handleLoad} sandbox="allow-scripts allow-forms allow-same-origin">
4. In onLoad: inject InfoRouter_Ticket; intercept form submit with e.preventDefault()
             read InfoRouter_TemplateID → templatePath = '~D{id}'
5. On submit: parseInfoRouterFields(iframeDoc, form) → fields[]
              buildXmlContent(fields) → xmlContent
6. SaveFilledForm(path=existingDocPath, templatePath='~D{id}', xmlContent)
   → <root success="true"/>  (document checked back in; no DocumentID returned)
```

---
