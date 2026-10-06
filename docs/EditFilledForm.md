# EditFilledForm API

Opens a document that was saved from a form, for the user to edit its values, and checks the document out to the caller. It is the edit counterpart of [UseFormTemplate](UseFormTemplate.md), and answers in the same two shapes, with the saved values filled in:

| The document was saved from | Response `formType` | What the UI gets | What the UI does |
|---|---|---|---|
| an **HTML form** template | `html` | the form rendered as a complete HTML page, with the saved values in its inputs | Shows the page (in an iframe) and collects its inputs on submit. |
| a **PDF form** template | `fields` | the PDF's form fields, each with its saved value | Builds its own form from the list. |
| a **Word template** | `fields` | the template's `{{placeholders}}`, each with its saved value | Builds its own form from the list. |

All three are saved the same way: post the values as `<FORMDATA>` to [SaveFilledForm](SaveFilledForm.md) with the document's own path. That stores a new version of the document.

## Endpoint

```
/srv.asmx/EditFilledForm
```

## Methods

- **GET** `/srv.asmx/EditFilledForm?authenticationTicket=...&documentPath=...&submitUrl=...`
- **POST** `/srv.asmx/EditFilledForm` (form data)
- **SOAP** Action: `http://tempuri.org/EditFilledForm`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document saved from a form (e.g. `/Finance/Reports/ExpenseReport.htm`, `/Finance/Contracts/Acme.pdf`), or `~D<id>`. |
| `submitUrl` | string | No | HTML form only: the `action` of the rendered `<form>`. Left out or empty, it is `IRDOC.ASPX`, which has no handler in this server, so always intercept the submit (see [Showing an HTML form](#showing-an-html-form)). Ignored for a PDF or Word template. |

---

## Checkout

The call checks the document out before it answers:

- If the document is not checked out, it is checked out to the caller.
- If the caller already has it checked out, that checkout is kept.
- If someone else has it checked out, the call fails with `4230`.
- If the call fails after it checked the document out (for example, the document was not saved from a form), it releases that checkout before answering. A checkout the caller already held is left as it was.

**Saving does not check the document back in.** [SaveFilledForm](SaveFilledForm.md) stores the new version and keeps a checkout the caller already holds, so after EditFilledForm and SaveFilledForm the document is **still checked out** to the user. Call [UnLock](UnLock.md) after saving, or when the user cancels the edit, to release it.

---

## Response: saved from an HTML form (`formType="html"`)

```xml
<root success="true" formType="html"><![CDATA[
<html>
  ...the template, with its inputs set to the saved values...
  <form ACTION="IRDOC.ASPX" METHOD="POST">
    <input type="hidden" value="100829" name="InfoRouter_DocumentID" id="InfoRouter_DocumentID">
    <input type="hidden" value="100828" name="InfoRouter_TemplateID" id="InfoRouter_TemplateID">
    <input type="hidden" value="" name="InfoRouter_Ticket" id="InfoRouter_Ticket">
    <input type="hidden" value="7" name="InfoRouter_UserID" id="InfoRouter_UserID">
    <input type="hidden" value="jdoe" name="InfoRouter_UserName" id="InfoRouter_UserName">
    <input type="text" name="Subject" VALUE="Quarterly figures">
    <input type="hidden" value="'IR_Subject','CHAR','N','N'" name="InfoRouter_Fields" id="InfoRouter_Fields">
  </form>
</html>
]]></root>
```

The root element's text (CDATA) is the form's HTML. Read it with `textContent`.

- **Values.** Each input, textarea and select holds the value the document's last version was saved with.
- **Hidden inputs.** As for [UseFormTemplate](UseFormTemplate.md#response-html-form-template-formtypehtml), except that `InfoRouter_DocumentID` (the document being edited) replaces `InfoRouter_FolderID`.
- **`InfoRouter_TemplateID`** is the template the document was saved from. Pass it to SaveFilledForm as `templatePath=~D<id>`.
- **`InfoRouter_Ticket`** holds the caller's ticket only when the server setting `ShareTicketWithCustomPageAndForms` is `true`. It is `false` by default, and the field is empty.
- **`InfoRouter_Fields`** lists the inputs with the data type and required flag the template author gave them. See [`InfoRouter_Fields`](UseFormTemplate.md#inforouter_fields): skip `'IR_'` (an input with no name), and keep only the first entry for a repeated name.

---

## Response: saved from a PDF or Word template (`formType="fields"`)

The response is the template's fields, each holding the value the document's last version was saved with. It has the same shape as [UseFormTemplate](UseFormTemplate.md#response-pdf-or-word-template-formtypefields), where every attribute, `type`, and `<Options>` is described.

### PDF example

```xml
<root success="true" formType="fields" templateType="pdf" templateId="123">
  <FORMDATA>
    <Prompt Name="Customer" title="Customer" type="text" required="true" maxLength="40">Acme Ltd</Prompt>
    <Prompt Name="Address" title="Address" type="multiline" required="false">1 Harbour Road</Prompt>
    <Prompt Name="Approved" title="Approved" type="checkbox" required="false">true</Prompt>
    <Prompt Name="Region" title="Region" type="radio" required="false">EU</Prompt>
    <Prompt Name="Country" title="Country" type="choice" required="false">NL</Prompt>
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

```xml
<root success="true" formType="fields" templateType="docx" templateId="124">
  <FORMDATA>
    <Prompt Name="Customer_name" title="Customer name" type="text" required="true">Acme Ltd</Prompt>
    <Prompt Name="Due" title="Due" type="date" required="false">2026-10-31</Prompt>
    <Prompt Name="Total" title="Total" type="number" required="false">1234.5</Prompt>
  </FORMDATA>
</root>
```

### In short

| Item | PDF | Word |
|---|---|---|
| `templateId` | The template the document was saved from. Pass it to SaveFilledForm as `templatePath=~D<templateId>`. | same |
| `Prompt/@Name` | The field's name. Send it back unchanged. | same |
| `Prompt/@title` | The label to show. | same |
| `Prompt/@type` | `text`, `multiline`, `checkbox`, `radio` or `choice` | `text`, `date` or `number` |
| `Prompt/@required`, `@maxLength` | Reported for the UI to enforce. The server does not check them. | `required` only |
| `Prompt` text | The saved value, in the form it is sent: `true`/`false` for a checkbox, an `Option/@value` for radio and choice | The saved value as it was sent: `yyyy-MM-dd` for a date, `1234.5` for a number |
| `<Options>` | One for each `radio` and `choice` field, beside `<FORMDATA>` | never present |

### Which fields are listed

- The fields come from the template's **current** published version, not from the version the document was saved with. A field added to the template since then comes back empty, and a saved value for a field the template no longer has is not listed.
- A field the saved data has no value for comes back empty.
- The Word rules (titles, types, the `*` for required) are in [Writing a Word template](SaveFilledForm.md#writing-a-word-template).

---

## Saving the edit

Post the edited values to [SaveFilledForm](SaveFilledForm.md) with the **document's own path**. An existing path stores a new version; it does not create another document. `templatePath` is required: pass the template the document was saved from.

```
POST /srv.asmx/SaveFilledForm
authenticationTicket=...&path=/Finance/Contracts/Acme.pdf&templatePath=~D123
&xmlContent=<FORMDATA><Prompt Name="Customer">Acme Ltd</Prompt><Prompt Name="Country">TR</Prompt></FORMDATA>
```

For a PDF or Word template, take the id from the response's `templateId`. For an HTML form, take it from the `InfoRouter_TemplateID` hidden input. Then release the checkout with [UnLock](UnLock.md).

---

## Error Response

```xml
<root success="false" errorCode="4230" error="..." />
```

| `errorCode` | When |
|---:|---|
| `4000` | The document was not saved from a form. |
| `4010` | The ticket is expired or unknown, or there is no ticket. |
| `4041` | No document at `documentPath`, or its template no longer exists. |
| `4230` | Someone else has the document checked out, or its PDF or Word template is marked offline. |
| `5000` | The PDF or Word template could not be read as a form template (e.g. a damaged file). |
| HTTP 400 | `documentPath` was missing or empty: the request is refused before it reaches the API, and there is no XML error document. |

A failed call never leaves behind a checkout that it took itself.

## Required Permissions

- Permission to check the document out.
- Saving the edit with SaveFilledForm needs permission to add a version to the document.

---

## Showing an HTML form

Show the HTML in an **`<iframe srcdoc>`**, as for [UseFormTemplate](UseFormTemplate.md#showing-an-html-form). The helper functions `escapeXml`, `fieldValue`, `templateFields` and `formData` are defined there.

```javascript
async function loadForEdit(ticket, documentPath) {
  const res = await fetch('/srv.asmx/EditFilledForm', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ authenticationTicket: ticket, documentPath }),
  });
  const root = new DOMParser().parseFromString(await res.text(), 'text/xml').documentElement;
  if (root.getAttribute('success') !== 'true') {
    // 4230: someone else is editing it. Nothing is checked out by this call.
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root.getAttribute('formType') === 'html'
    ? { kind: 'html', html: root.textContent }
    : { kind: 'fields', root, templatePath: `~D${root.getAttribute('templateId')}` };
}

async function post(action, params) {
  const res = await fetch(`/srv.asmx/${action}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(params),
  });
  const root = new DOMParser().parseFromString(await res.text(), 'text/xml').documentElement;
  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

```jsx
import { useRef, useCallback } from 'react';

function EditHtmlForm({ html, ticket, documentPath, onDone }) {
  const iframeRef = useRef(null);

  const handleLoad = useCallback(() => {
    const doc = iframeRef.current.contentDocument;
    const form = doc.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', async e => {
      e.preventDefault();                              // IRDOC.ASPX has no handler: never let it post
      const templateId = doc.getElementById('InfoRouter_TemplateID').value;
      await post('SaveFilledForm', {
        authenticationTicket: ticket,
        path: documentPath,                            // the same document: a new version
        templatePath: `~D${templateId}`,
        xmlContent: formData(doc),
      });
      await post('UnLock', { authenticationTicket: ticket, path: documentPath, force: 'false' });  // saving leaves it checked out
      onDone?.();
    });
  }, [ticket, documentPath, onDone]);

  return (
    <iframe
      ref={iframeRef}
      srcDoc={html}
      onLoad={handleLoad}
      sandbox="allow-scripts allow-forms allow-same-origin"
      style={{ width: '100%', height: 600, border: 'none' }}
      title="Edit form"
    />
  );
}
```

When the user cancels instead, call `UnLock` too: the document stays checked out to them until it is released.

---

## Notes

- Only a document saved from a form can be opened. Others return `4000`; [GetDocument](GetDocument.md) shows the document's `TemplateID` (`0` when it has none).
- A document saved with `detachDocumentFromTemplate=true` no longer has a template, so it cannot be edited here.

## Related APIs

- [UseFormTemplate](UseFormTemplate.md): Open a template as a new, empty form.
- [SaveFilledForm](SaveFilledForm.md): Save the form as a new document, or a new version of an existing one.
- [UnLock](UnLock.md): Release the checkout this call takes.
