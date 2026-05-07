# GetFormFromDocument API

Returns the rendered HTML form for an existing HTML document, pre-filled with its current saved values, and automatically checks the document out for editing. This is the edit counterpart to `CreateFormFromTemplate`.

## Endpoint

```
/srv.asmx/GetFormFromDocument
```

## Methods

- **GET** `/srv.asmx/GetFormFromDocument?authenticationTicket=...&documentPath=...&submitUrl=...`
- **POST** `/srv.asmx/GetFormFromDocument` (form data)
- **SOAP** Action: `http://tempuri.org/GetFormFromDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the existing HTML document to edit (e.g. `/Finance/Reports/ExpenseReport.htm`). |
| `submitUrl` | string | No | URL to set as the HTML form `action` attribute. When empty the form posts to the legacy `IRDOC.ASPX` handler. Pass the route of a React/SPA page to intercept the submission client-side instead. |

---

## Response

### Success Response

```xml
<root success="true"><![CDATA[
<!DOCTYPE html>
<html>
  ...pre-filled form HTML...
</html>
]]></root>
```

The element content is the complete rendered HTML form wrapped in a CDATA section. All form fields are pre-populated with the document's current saved values.

### Error Response

```xml
<root success="false" error="Error message" />
```

---

## Required Permissions

- **Read** permission on the document.
- **Check Out** permission on the document.

---

## Checkout Behaviour

The document is automatically checked out as part of this call:

- If the document is **not checked out**, it is checked out to the calling user.
- If the document is **already checked out by the calling user**, the checkout is left as-is and the form is returned.
- If the document is **checked out by another user**, the call fails with an error.

After editing, submit the updated form values to `CreateDocumentUsingTemplate` to save and check the document back in.

---

## Example

### POST Request

```
POST /srv.asmx/GetFormFromDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&documentPath=/Finance/Reports/ExpenseReport.htm
&submitUrl=
```

### Using submitUrl for React/SPA Integration

**Do not use `submitUrl` when embedding inside a React app via iframe** — see the React section below. The `submitUrl` parameter is only useful when an external page submits to a known server-side route.

---

## React Integration

The rendered HTML is a complete standalone page (`<html>`, `<head>`, `<style>`, `<body>`). The correct way to embed it in a React application is inside an **`<iframe srcdoc>`**, not via `dangerouslySetInnerHTML`.

**Why iframe and not `dangerouslySetInnerHTML`:**

| | `dangerouslySetInnerHTML` | `<iframe srcdoc>` |
|---|---|---|
| `<script>` tags execute | No | Yes |
| `<style>` isolated from React app | No — leaks into host page | Yes |
| Full HTML document supported | No — strips `<html>/<head>/<body>` | Yes |
| Submit interception | Requires `querySelector` on container | `contentDocument.querySelector` on load |

`srcdoc` iframes are always same-origin with their parent, so `contentDocument` access is always permitted regardless of the host the React app is served from.

The rendered HTML has `InfoRouter_Ticket` set to an empty string. The React app must inject the live session ticket in the `onLoad` handler before the user submits.

### Step 1 — Fetch the pre-filled form (no submitUrl needed)

```javascript
const res = await fetch(
  `/srv.asmx/GetFormFromDocument?authenticationTicket=${ticket}` +
  `&documentPath=${encodeURIComponent(documentPath)}`
);
const xml = new DOMParser().parseFromString(await res.text(), 'text/xml');
const renderedHtml = xml.querySelector('root').textContent;
```

### Step 2 — Render inside an iframe and intercept submit

```jsx
import { useRef } from 'react';

function InfoRouterEditForm({ renderedHtml, authTicket, documentPath }) {
  const iframeRef = useRef(null);

  const handleLoad = () => {
    const doc = iframeRef.current.contentDocument;
    const form = doc.querySelector('form');
    if (!form) return;

    // Inject the live ticket — the rendered HTML has this field empty
    const ticketField = doc.getElementById('InfoRouter_Ticket');
    if (ticketField) ticketField.value = authTicket;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const formData = new FormData(form);
      formData.set('InfoRouter_Ticket', authTicket); // ensure current value

      // Build TemplatePath from the hidden InfoRouter_TemplateID field
      const templateId = doc.getElementById('InfoRouter_TemplateID')?.value;
      const templatePath = templateId ? `~D${templateId}` : '';

      const res = await fetch('/srv.asmx/CreateDocumentUsingTemplate', {
        method: 'POST',
        body: new URLSearchParams({
          authenticationTicket: authTicket,
          Path: documentPath,
          TemplatePath: templatePath,
          xmlContent: new XMLSerializer().serializeToString(
            buildXmlFromFormData(formData)
          ),
        }),
      });

      const xml = new DOMParser().parseFromString(await res.text(), 'text/xml');
      const success = xml.querySelector('root')?.getAttribute('success');
      if (success === 'true') {
        // document saved and checked back in
      } else {
        const error = xml.querySelector('root')?.getAttribute('error');
        console.error('Save failed:', error);
      }
    });
  };

  return (
    <iframe
      ref={iframeRef}
      srcdoc={renderedHtml}
      onLoad={handleLoad}
      style={{ width: '100%', height: '600px', border: 'none' }}
      title="Edit Document Form"
    />
  );
}
```

### Key points

- `submitUrl` is left empty when fetching the form — the iframe's `onLoad` handler takes over submit interception entirely, so the form's `action` attribute is irrelevant.
- `e.preventDefault()` must be called to stop the browser from navigating away when the user clicks Submit.
- The `InfoRouter_Ticket` hidden field is empty in the rendered HTML by design. Always overwrite it in both `handleLoad` and the submit handler.
- `InfoRouter_TemplateID` is a hidden field injected by the server into the rendered form. Use `~D{templateId}` notation to pass it as `TemplatePath` to `CreateDocumentUsingTemplate`.
- Passing the existing `documentPath` as `Path` to `CreateDocumentUsingTemplate` signals an update of the existing document rather than creation of a new one.
- If `renderedHtml` changes (user navigates to a different document), the iframe re-renders and `onLoad` fires again, re-attaching the listener cleanly.

---

## Notes

- The rendered HTML is returned inside a CDATA section. Extract the element's text content before rendering it in a browser.
- When `submitUrl` is empty or omitted, the form `action` defaults to `IRDOC.ASPX` (legacy handler). This parameter is only needed for non-React integrations where a server-side route must receive the POST. In a React app using `<iframe srcdoc>`, leave `submitUrl` empty and intercept submit via `contentDocument` instead.
- The `InfoRouter_Ticket` hidden field inside the rendered form is always empty. The React app must inject the live session ticket in the iframe `onLoad` handler.
- If the document has no associated template (it was not created from an HTML form template), this API will return an error. Use `GetDocument` to check the `TemplateId` field before calling.

---

## Related APIs

- [CreateFormFromTemplate](CreateFormFromTemplate.md) — Return a blank form from a template for creating a new document.
- [CreateDocumentUsingTemplate](CreateDocumentUsingTemplate.md) — Save the submitted form values as a new or updated HTML document.

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The `documentPath` does not resolve to an existing document. |
| Document template cannot be found | The document has no associated template (not created from an HTML form template). |
| Checked out by another user | The document is already checked out by a different user. |
| Access denied | The user lacks Read or Check Out permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## React Implementer Guide

Production-ready patterns derived from the reference demo at `IRWebCore/wwwRoot/form-template-demo.html`. The helper functions (`parseInfoRouterFields`, `buildXmlContent`, `escapeXml`, `parseXml`) are defined in the `CreateFormFromTemplate` implementer guide and are shared across all three form APIs.

### Step 1 — Fetch the pre-filled form

```javascript
async function loadDocumentForm(apiBase, ticket, documentPath) {
  const body = new URLSearchParams({
    authenticationTicket: ticket,
    documentPath,
    submitUrl: '',   // Pass '' — submit is intercepted via iframe onLoad
  });
  const res = await fetch(`${apiBase}/GetFormFromDocument`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
  const r = parseXml(await res.text());
  if (!r.ok) throw new Error(r.error);
  return r.el.textContent;  // Raw pre-filled HTML extracted from CDATA
}
```

The document is checked out the moment this call succeeds. If checkout fails the API returns `success="false"` — do not attempt to render the form in that case.

### Step 2 — Render in React and intercept submit

```jsx
import { useState, useRef, useCallback } from 'react';

function EditDocumentForm({ ticket, documentPath, apiBase, onSubmit }) {
  const [renderedHtml, setRenderedHtml] = useState('');
  const iframeRef = useRef(null);

  async function handleLoadDocument() {
    const html = await loadDocumentForm(apiBase, ticket, documentPath);
    setRenderedHtml(html);
  }

  const handleIframeLoad = useCallback(() => {
    const iframe = iframeRef.current;
    if (!iframe || !renderedHtml) return;
    const doc = iframe.contentDocument;

    // Inject live ticket — the rendered form always has InfoRouter_Ticket empty
    const ticketField = doc.getElementById('InfoRouter_Ticket');
    if (ticketField) ticketField.value = ticket;

    const form = doc.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', e => {
      e.preventDefault();
      e.stopPropagation();

      // InfoRouter_TemplateID identifies which template was used to create this document.
      // Format it as ~D{id} for the TemplatePath parameter of CreateDocumentUsingTemplate.
      const templateIdEl = doc.getElementById('InfoRouter_TemplateID');
      const templatePath = templateIdEl?.value ? `~D${templateIdEl.value}` : '';

      const fields = parseInfoRouterFields(doc, form);

      // Pass the existing documentPath so CreateDocumentUsingTemplate creates a new version
      onSubmit({ fields, templatePath, existingDocPath: documentPath });
    });
  }, [renderedHtml, ticket, documentPath]);

  return (
    <>
      <button onClick={handleLoadDocument}>Load Document for Editing</button>
      {renderedHtml && (
        <iframe
          ref={iframeRef}
          srcDoc={renderedHtml}
          onLoad={handleIframeLoad}
          sandbox="allow-scripts allow-forms allow-same-origin"
          style={{ width: '100%', height: 600, border: 'none' }}
          title="Edit Document Form"
        />
      )}
    </>
  );
}
```

### Step 3 — Save the updated document

Pass the original `documentPath` as `Path` to `CreateDocumentUsingTemplate`. Because the path already exists, the API creates a new version and checks the document back in automatically.

```javascript
async function saveDocumentUpdate({ apiBase, ticket, fields, templatePath, existingDocPath }) {
  const xmlContent = buildXmlContent(fields);
  const body = new URLSearchParams({
    AuthenticationTicket: ticket,
    Path:         existingDocPath,  // Existing path → new version, not a new document
    TemplatePath: templatePath,     // ~D{id} read from InfoRouter_TemplateID
    xmlContent,
  });
  const res = await fetch(`${apiBase}/CreateDocumentUsingTemplate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
  const doc = new DOMParser().parseFromString(await res.text(), 'text/xml');
  const root = doc.querySelector('root') ?? doc.querySelector('response');
  if (root?.getAttribute('success') !== 'true') {
    throw new Error(root?.getAttribute('error') ?? 'Update failed');
  }
  // New-version response is <root success="true"/> — no DocumentID or DocumentName attributes
}
```

### Critical rules

| Rule | Reason |
|---|---|
| Check for `success="false"` before rendering the form | The document is checked out during the API call; a failure means it is still checked in |
| Read `InfoRouter_TemplateID` from the iframe, not from application state | The server injects the correct template ID into the rendered HTML |
| Format `InfoRouter_TemplateID` as `~D{id}` for `TemplatePath` | The `~D` notation is required; a bare integer will not resolve to a template |
| Pass `existingDocPath` (not a new path) as `Path` | Reusing the existing path triggers the new-version code path in `CreateDocumentUsingTemplate` |
| The new-version response has no `DocumentID` attribute | Response element is `<root>` rather than `<response>` — check both with a fallback selector |
| `sandbox="allow-scripts allow-forms allow-same-origin"` on the iframe | Form scripts must execute; `contentDocument` access must be permitted |

---
