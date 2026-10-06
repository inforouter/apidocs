# UseFormTemplate API

<!-- {% raw %} -->

Prepares a new form from a form template, for the user to fill in. What comes back depends on the template's file type:

| Template | Recognised by | Response `formType` | What the UI gets | What the UI does |
|---|---|---|---|---|
| **HTML form** | any template that is not `.pdf` or `.docx` (e.g. `.htm`, `.html`) | `html` | the rendered form, a complete HTML page | Shows the page (in an iframe) and collects its inputs on submit. |
| **PDF form** | `.pdf` | `fields` | a list of the PDF's form fields | Builds its own form from the list. |
| **Word template** | `.docx` | `fields` | a list of the document's `{{placeholders}}` | Builds its own form from the list. |

All three are saved the same way: post the values as `<FORMDATA>` to [SaveFilledForm](SaveFilledForm.md). This call creates nothing.

## Endpoint

```
/srv.asmx/UseFormTemplate
```

## Methods

- **GET** `/srv.asmx/UseFormTemplate?authenticationTicket=...&targetFolderPath=...&templatePath=...&submitUrl=...`
- **POST** `/srv.asmx/UseFormTemplate` (form data)
- **SOAP** Action: `http://tempuri.org/UseFormTemplate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `templatePath` | string | Yes | Full infoRouter path of the template document (e.g. `/Templates/ExpenseForm.htm`), or `~D<id>` with its document id (e.g. `~D42`). The template must have a published version. |
| `targetFolderPath` | string | HTML form only | The folder the new document will be created in (e.g. `/Finance/Reports`). Required for an HTML form, whose rendered page carries the folder's id. Optional for a PDF or Word template; when given, it must be an existing folder. |
| `submitUrl` | string | No | HTML form only: the `action` of the rendered `<form>`. Left out or empty, it is `IRDOC.ASPX`, which has no handler in this server, so always intercept the submit (see [Showing an HTML form](#showing-an-html-form)). Ignored for a PDF or Word template. |

---

## Response: HTML form template (`formType="html"`)

```xml
<root success="true" formType="html"><![CDATA[
<html>
  ...the template, with its inputs set to their defaults...
  <form ACTION="IRDOC.ASPX" METHOD="POST">
    <input type="hidden" value="1329" name="InfoRouter_FolderID" id="InfoRouter_FolderID">
    <input type="hidden" value="100826" name="InfoRouter_TemplateID" id="InfoRouter_TemplateID">
    <input type="hidden" value="" name="InfoRouter_Ticket" id="InfoRouter_Ticket">
    <input type="hidden" value="7" name="InfoRouter_UserID" id="InfoRouter_UserID">
    <input type="hidden" value="jdoe" name="InfoRouter_UserName" id="InfoRouter_UserName">
    ...the template's own inputs...
    <input type="hidden" value="'IR_Subject','DATE','Y','N',..." name="InfoRouter_Fields" id="InfoRouter_Fields">
  </form>
</html>
]]></root>
```

The root element's text (CDATA) is the template's HTML with the server's additions. Read it with `textContent`.

- **Defaults.** Each input's `value` attribute is kept as the default, with two special values: `TODAY()` becomes today's date as `yyyy-MM-dd`, and `NOW()` the current date and time.
- **Hidden inputs.** The server adds `InfoRouter_FolderID`, `InfoRouter_TemplateID`, `InfoRouter_Ticket`, `InfoRouter_UserID` and `InfoRouter_UserName` at the start of the form, and `InfoRouter_Fields` at its end.
- **`InfoRouter_Ticket`** holds the caller's ticket only when the server setting `ShareTicketWithCustomPageAndForms` is `true` in `appsettings.json`. It is `false` by default, and the field is empty.

### `InfoRouter_Fields`

A comma-separated list with four quoted tokens for every `<input>`, `<textarea>` and `<select>` in the form, in document order:

```
'IR_Subject','DATE','Y','N','IR_','CHAR','N','N','IR_Country','CHAR','N','N'
```

| Token | Meaning |
|---|---|
| 1. `'IR_<name>'` | The input's `name` with `IR_` in front. **`'IR_'` alone is an input with no name**, such as a submit button: skip it. A checkbox or radio group lists its name once per input: keep the first. |
| 2. `'CHAR'`, `'DATE'`, `'NUMBER'` or `'BOOLEAN'` | The data type the **template author** gave the input with a `datatype` attribute (`<input name="Due" datatype="DATE">`). `CHAR` when there is none. It is not taken from the input's own `type`: an `<input type="date">` without `datatype` is `CHAR`. |
| 3. `'Y'` or `'N'` | `Y` when the author gave the input a `required="true"` attribute. |
| 4. `'N'` | Reserved. |

The server checks neither the data type nor required when the form is saved. Use them to validate in the UI if you like.

---

## Response: PDF or Word template (`formType="fields"`)

A PDF or Word template has no HTML. The response lists its fields for the UI to build a form from.

### PDF example

```xml
<root success="true" formType="fields" templateType="pdf" templateId="123">
  <FORMDATA>
    <Prompt Name="Customer" title="Customer" type="text" required="true" maxLength="40">Acme Ltd</Prompt>
    <Prompt Name="Address" title="Address" type="multiline" required="false"></Prompt>
    <Prompt Name="Approved" title="Approved" type="checkbox" required="false">false</Prompt>
    <Prompt Name="Region" title="Region" type="radio" required="false">EU</Prompt>
    <Prompt Name="Country" title="Country" type="choice" required="false">TR</Prompt>
  </FORMDATA>
  <Options Name="Region">
    <Option value="EU" text="EU" />
    <Option value="US" text="US" />
  </Options>
  <Options Name="Country">
    <Option value="TR" text="Turkey" />
    <Option value="NL" text="Netherlands" />
  </Options>
</root>
```

### Word example

For a template containing `{{Customer_name*}}`, `{{Due}:format(dd.MM.yyyy)}` and `{{Total}:format(N2)}`:

```xml
<root success="true" formType="fields" templateType="docx" templateId="124">
  <FORMDATA>
    <Prompt Name="Customer_name" title="Customer name" type="text" required="true"></Prompt>
    <Prompt Name="Due" title="Due" type="date" required="false"></Prompt>
    <Prompt Name="Total" title="Total" type="number" required="false"></Prompt>
  </FORMDATA>
</root>
```

A Word response never has `maxLength` or `<Options>`, and its values are always empty.

### Attributes

| Item | PDF | Word |
|---|---|---|
| `templateType` | `pdf` | `docx` |
| `templateId` | The template's document id. Pass it to [SaveFilledForm](SaveFilledForm.md) as `templatePath=~D<templateId>`. | same |
| `Prompt/@Name` | The field's name: the last part of the AcroForm name, without its index (`form1[0].page1[0].Customer[0]` is `Customer`). Send it back unchanged. | The placeholder's name, without the `*` marking a required field. |
| `Prompt/@title` | The label to show, made from `Name`: underscores become spaces, CamelCase is split, and the first letter is capitalised (`RecipientName` and `recipient_name` are both "Recipient name"). | same |
| `Prompt/@type` | `text`, `multiline`, `checkbox`, `radio` or `choice` | `text`, `date` or `number` |
| `Prompt/@required` | `true` when the PDF field is marked required | `true` when the placeholder ends in `*` |
| `Prompt/@maxLength` | The most characters the field takes. Absent when there is no limit. | never present |
| `Prompt` text | The value the field holds in the template (its default) | always empty |
| `<Options>` | One for each `radio` and `choice` field | never present |

### `type`: the control to show and the value to send

`type` is a single attribute that tells you both things: which control to show, and in what form to send its value back. Every value is sent as text in the `<Prompt>`.

| `type` | From | Show | Send |
|---|---|---|---|
| `text` | PDF, Word | a one-line text box (for Word, a multi-line box also works: line breaks are kept) | the text |
| `multiline` | PDF | a multi-line text box | the text, lines separated by line breaks |
| `checkbox` | PDF | a checkbox | `true` or `false` |
| `radio` | PDF | radio buttons, one per `<Option>` | one `Option/@value`. An empty or unknown value leaves the template's selection as it was. |
| `choice` | PDF | a drop-down, one entry per `<Option>` | one `Option/@value` |
| `date` | Word | a date picker | `yyyy-MM-dd`, optionally with a time: `yyyy-MM-ddTHH:mm` |
| `number` | Word | a number box | digits with a dot as the decimal separator and no thousands separator: `1234.5` |

For a `date` or `number`, the template formats the value itself (`06.10.2026`, `1,234.50`). A value in any other form is printed exactly as sent. See [Writing a Word template](SaveFilledForm.md#writing-a-word-template).

### `<Options>`: the entries of a radio or choice field

```xml
<Options Name="Country">
  <Option value="TR" text="Turkey" />
  <Option value="NL" text="Netherlands" />
</Options>
```

- `Options/@Name` is the `Name` of the `<Prompt>` it belongs to.
- `value` is what to send, and `text` is what to show. For a radio group the two are the same.
- The `<Prompt>` text holds the selected `value`, or nothing.

**Why the options are not inside the `<Prompt>`:** the `<FORMDATA>` is meant to be posted back to [SaveFilledForm](SaveFilledForm.md) as it is, and the server takes the whole text of a `<Prompt>` as its value. With the `<Option>`s inside the `<Prompt>`, their texts would become part of the saved value. Keeping them in a sibling `<Options>` element leaves each `<Prompt>` holding its value and nothing else.

### Rules the UI must enforce

The server reports these rules but does not check them when the form is saved:

- `required="true"`: refuse to submit an empty value.
- `maxLength`: limit the input's length.
- `choice`: the server stores any text sent, so offer only the listed options.

### What is listed

- **PDF**: the AcroForm fields that can be filled, in the PDF's order. Read-only fields, signatures and push buttons are not listed. Fields sharing a short name are filled with the same value, so they are listed once.
- **Word**: every `{{placeholder}}` and every name used in a `{?{condition}}`, in the order they first appear: the body, then headers, footers, footnotes and endnotes. Each name is listed once. Loops (`{{#Items}}`) and dotted names (`{{Customer.Name}}`) are not listed, because no single form value can fill them. The title, type and required flag are read from the placeholder; see [Writing a Word template](SaveFilledForm.md#writing-a-word-template).

### Saving

Post the `<FORMDATA>` element to [SaveFilledForm](SaveFilledForm.md) with the values filled in. The attributes other than `Name` (`title`, `type`, `required`, `maxLength`) may be left on or removed, as they are ignored, and the `<Options>` elements are not sent:

```
POST /srv.asmx/SaveFilledForm
authenticationTicket=...&path=/Finance/Contracts/Acme.pdf&templatePath=~D123
&xmlContent=<FORMDATA><Prompt Name="Customer">Acme Ltd</Prompt><Prompt Name="Approved">true</Prompt><Prompt Name="Country">NL</Prompt></FORMDATA>
```

---

## Error Response

```xml
<root success="false" errorCode="4041" error="Document not found." />
```

| `errorCode` | When |
|---:|---|
| `4000` | The template has no published version. An HTML template that is marked offline also returns `4000`. |
| `4010` | The ticket is expired or unknown, or there is no ticket. |
| `4041` | No template at `templatePath`, or it is in a library the caller cannot see. Also returned when no folder exists at `targetFolderPath`, including when none was given for an HTML form template. |
| `4230` | A PDF or Word template that is marked offline. |
| `5000` | The PDF or Word file could not be read as a form template (e.g. a damaged file). |
| HTTP 400 | `templatePath` was missing or empty: the request is refused before it reaches the API, and there is no XML error document. |

## Required Permissions

- An authenticated user.
- The template must be in a library the caller can see.
- No permission is checked on `targetFolderPath` here, because this call creates nothing. The folder permission is checked by [SaveFilledForm](SaveFilledForm.md) when the document is created.

---

## Showing an HTML form

The rendered HTML is a complete page with its own `<html>`, `<style>` and `<script>`. Show it in an **`<iframe srcdoc>`**, not with `innerHTML` or `dangerouslySetInnerHTML`:

| | `innerHTML` / `dangerouslySetInnerHTML` | `<iframe srcdoc>` |
|---|---|---|
| The form's `<script>`s run | No | Yes |
| The form's `<style>` stays out of the host page | No | Yes |
| A full HTML document is supported | No: `<html>`, `<head>` and `<body>` are stripped | Yes |

A `srcdoc` iframe is same-origin with its parent (keep `allow-same-origin` if you sandbox it), so the host page can reach the form through `contentDocument`.

### Fetch the form

```javascript
async function loadForm(ticket, targetFolderPath, templatePath) {
  const res = await fetch('/srv.asmx/UseFormTemplate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ authenticationTicket: ticket, targetFolderPath, templatePath }),
  });
  const root = new DOMParser().parseFromString(await res.text(), 'text/xml').documentElement;
  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root.getAttribute('formType') === 'html'
    ? { kind: 'html', html: root.textContent }
    : { kind: 'fields', root };            // a PDF or Word template: build the form yourself
}
```

### Collect the inputs and save

```javascript
function escapeXml(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// The value to send for one input name:
// - a single checkbox: its value when ticked, '' otherwise
// - a checkbox group (several checkboxes sharing the name): the ticked values joined with ';'
// - a radio group or any other control: its value
function fieldValue(el) {
  if (!el) return '';
  if (!el.tagName) {                                   // RadioNodeList: several inputs share the name
    const items = Array.from(el);
    if (items.every(i => i.type === 'checkbox')) {
      return items.filter(i => i.checked).map(i => i.value).join(';');
    }
    return el.value;
  }
  if (el.type === 'checkbox') return el.checked ? el.value : '';
  return el.value;
}

// The template's inputs, read from InfoRouter_Fields: [{ name, dataType, required }]
function templateFields(doc) {
  const tokens = (doc.getElementById('InfoRouter_Fields')?.value ?? '')
    .split(',').map(t => t.trim().replace(/^'|'$/g, ''));
  const fields = [];
  for (let i = 0; i + 3 < tokens.length; i += 4) {
    const name = tokens[i].slice(3);                   // drop the IR_ prefix
    if (!name || fields.some(f => f.name === name)) continue;   // unnamed button, or a repeated group
    fields.push({ name, dataType: tokens[i + 1], required: tokens[i + 2] === 'Y' });
  }
  return fields;
}

function formData(doc) {
  const form = doc.querySelector('form');
  return '<FORMDATA>' +
    templateFields(doc)
      .map(f => `<Prompt Name="${escapeXml(f.name)}">${escapeXml(fieldValue(form.elements[f.name]))}</Prompt>`)
      .join('') +
    '</FORMDATA>';
}
```

### React

```jsx
import { useRef, useCallback } from 'react';

function HtmlForm({ html, ticket, templatePath, documentPath, onSaved }) {
  const iframeRef = useRef(null);

  const handleLoad = useCallback(() => {
    const doc = iframeRef.current.contentDocument;
    const form = doc.querySelector('form');
    if (!form) return;

    // Scripts inside the form may read the ticket; it is empty unless the server shares it.
    const ticketField = doc.getElementById('InfoRouter_Ticket');
    if (ticketField) ticketField.value = ticket;

    form.addEventListener('submit', async e => {
      e.preventDefault();                              // IRDOC.ASPX has no handler: never let it post
      const res = await fetch('/srv.asmx/SaveFilledForm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          authenticationTicket: ticket,
          path: documentPath,                          // full path of the document to create
          templatePath,
          xmlContent: formData(doc),
        }),
      });
      const root = new DOMParser().parseFromString(await res.text(), 'text/xml').documentElement;
      if (root.getAttribute('success') === 'true') onSaved?.(root);
      else console.error(root.getAttribute('errorCode'), root.getAttribute('error'));
    });
  }, [ticket, templatePath, documentPath, onSaved]);

  return (
    <iframe
      ref={iframeRef}
      srcDoc={html}
      onLoad={handleLoad}
      sandbox="allow-scripts allow-forms allow-same-origin"
      style={{ width: '100%', height: 600, border: 'none' }}
      title="Form"
    />
  );
}
```

| Rule | Reason |
|---|---|
| Use `srcDoc`, not `src` | The HTML is a string; there is no URL to load it from. |
| `sandbox="allow-scripts allow-forms allow-same-origin"` | The form's scripts run, and the host can reach `contentDocument`. |
| `e.preventDefault()` on submit | The form's `action` has no handler; the save is the separate SaveFilledForm call. |
| Re-attach in `onLoad` | When `html` changes the iframe reloads and `onLoad` fires again. |

---

## Notes

- `targetFolderPath` is only used by an HTML form, whose page carries the folder's id. For a PDF or Word template, where the document will be saved is decided by the `path` given to [SaveFilledForm](SaveFilledForm.md).
- To edit a document already saved from a form, use [EditFilledForm](EditFilledForm.md). It answers in the same two shapes, with the saved values filled in.
- `~D999` is not a template this API can open: it returns `4041`. The blank HTML document is a [SaveFilledForm](SaveFilledForm.md) feature (`templatePath=999`), with no form to render.

## Related APIs

- [SaveFilledForm](SaveFilledForm.md): Save the filled form as a new document.
- [EditFilledForm](EditFilledForm.md): Open a saved form for editing.
- [Search](Search.md): Find documents created from a template with the `TEMPLATEPATH` criterion.

<!-- {% endraw %} -->
