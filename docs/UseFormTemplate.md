# UseFormTemplate API

Returns the rendered HTML form for a content template. The response is the complete HTML that the user's browser can display and submit to create a new document in the specified destination folder.

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
| `targetFolderPath` | string | Yes | Full infoRouter path of the destination folder where the new document will be created (e.g. `/Finance/Reports`). |
| `templatePath` | string | Yes | Full infoRouter path of the template document (e.g. `/Templates/ExpenseForm.htm`), or `~D<id>` short form (e.g. `~D42`). Use `~D999` for the built-in HTML document type. |
| `submitUrl` | string | Yes | URL to set as the HTML form `action` attribute. Pass an empty string `""` to use the default legacy `IRDOC.ASPX` handler. Pass the route of a React/SPA page to intercept the submission client-side instead. This parameter must always be present in the request; omitting it entirely from the query string or form body will cause a server error. |

---

## Response

### Success Response

```xml
<root success="true"><![CDATA[
<!DOCTYPE html>
<html>
  ...rendered form HTML...
</html>
]]></root>
```

The element content is the complete rendered HTML form wrapped in a CDATA section to preserve HTML characters (`<`, `>`, `&`) without XML encoding.

### Error Response

```xml
<root success="false" error="Error message" />
```

---

## Required Permissions

- **Read** permission on the template document.
- **Add Document** permission on the destination folder (`targetFolderPath`).

---

## Example

### POST Request

```
POST /srv.asmx/UseFormTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&targetFolderPath=/Finance/Reports
&templatePath=/Templates/ExpenseReport.htm
&submitUrl=
```

### Using ~D999 for HTML Documents

To render the built-in HTML document form (not tied to a specific template file):

```
POST /srv.asmx/UseFormTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&targetFolderPath=/Finance/Reports
&templatePath=~D999
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

### Step 1 — Fetch the form

```javascript
const res = await fetch(
  `/srv.asmx/UseFormTemplate?authenticationTicket=${ticket}` +
  `&targetFolderPath=${encodeURIComponent(targetFolderPath)}` +
  `&templatePath=${encodeURIComponent(templatePath)}` +
  `&submitUrl=`
);
const xml = new DOMParser().parseFromString(await res.text(), 'text/xml');
const renderedHtml = xml.querySelector('root').textContent;
```

### Step 2 — Render inside an iframe and intercept submit

```jsx
import { useRef } from 'react';

function InfoRouterForm({ renderedHtml, authTicket, targetFolderPath, documentName }) {
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

      // Parse InfoRouter_Fields to discover field names and build xmlContent
      const fieldsInput = doc.getElementById('InfoRouter_Fields');
      const tokens = fieldsInput ? fieldsInput.value.split(',') : [];
      let xmlContent = '<FORMDATA>';
      for (let i = 0; i + 3 < tokens.length; i += 4) {
        const raw   = tokens[i].trim();                 // e.g. "'IR_title'"
        const name  = raw.slice(4, raw.length - 1);    // strip 'IR_ prefix and trailing '
        const value = (form.elements[name]?.value ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
        xmlContent += `<Prompt Name="${name}">${value}</Prompt>`;
      }
      xmlContent += '</FORMDATA>';

      const body = new URLSearchParams({
        AuthenticationTicket: authTicket,
        Path:         targetFolderPath.replace(/\/+$/, '') + '/' + documentName,
        TemplatePath: templatePath,
        xmlContent,
      });

      const res = await fetch('/srv.asmx/CreateDocumentUsingTemplate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString(),
      });

      const xml = new DOMParser().parseFromString(await res.text(), 'text/xml');
      const root = xml.querySelector('root') ?? xml.querySelector('response');
      if (root?.getAttribute('success') === 'true') {
        // handle success — root may have DocumentID and DocumentName attributes
      } else {
        console.error('Submit failed:', root?.getAttribute('error'));
      }
    });
  };

  return (
    <iframe
      ref={iframeRef}
      srcdoc={renderedHtml}
      onLoad={handleLoad}
      style={{ width: '100%', height: '600px', border: 'none' }}
      title="Document Form"
    />
  );
}
```

### The `InfoRouter_Fields` hidden input

The rendered HTML always contains a hidden input named `InfoRouter_Fields`. Its value is a comma-separated list of 4-token descriptors — one group per template field:

```
'IR_title','CHAR','N','N','IR_author','CHAR','Y','N','IR_duedate','DATE','Y','N'
```

Each group of 4 tokens:

| Position in group | Meaning |
|---|---|
| 0 — `'IR_{fieldname}'` | HTML input name with `'IR_` prefix and trailing `'`. Strip those to get the bare field name. |
| 1 — `'CHAR'` \| `'DATE'` \| `'NUMBER'` \| `'BOOLEAN'` | Data type. |
| 2 — `'Y'` \| `'N'` | Required flag. |
| 3 — `'N'` | Reserved. |

You must parse this value to know which form inputs to collect and to build the correct `xmlContent` for [`CreateDocumentUsingTemplate`](CreateDocumentUsingTemplate.md).

### Key points

- `submitUrl` must always be included in the request. Pass an empty string `""` when embedding via iframe — the iframe's `onLoad` handler takes over submit interception entirely, so the form's `action` attribute is irrelevant.
- `e.preventDefault()` must be called to stop the browser from navigating away when the user clicks Submit.
- The `InfoRouter_Ticket` hidden field is empty in the rendered HTML by design. Always overwrite it with the current session ticket in `handleLoad` and again in the submit handler.
- Read `InfoRouter_Fields` from `iframeDoc` in the `onLoad` handler to discover all template field names and their data types before building `xmlContent`.
- If `renderedHtml` changes (user picks a different template), the iframe re-renders and `onLoad` fires again, re-attaching the listener cleanly.

---

## Notes

- The `templatePath` accepts either a full document path or the `~D<id>` short form. `~D999` is the reserved identifier for the built-in HTML document type and does not correspond to a physical document in the repository.
- The rendered HTML is returned inside a CDATA section. Extract the element's text content before rendering it in a browser.
- `submitUrl` must always be present in the request. When passed as an empty string `""`, the form `action` defaults to `IRDOC.ASPX` (legacy handler). This parameter is only meaningful for non-React integrations where a server-side route must receive the POST. In a React app using `<iframe srcdoc>`, pass `submitUrl=""` and intercept submit via `contentDocument` instead.
- The `InfoRouter_Ticket` hidden field inside the rendered form is always empty. The React app must inject the live session ticket in the iframe `onLoad` handler.
- Use this API to embed infoRouter form templates inside custom applications or portals.

---

## Related APIs

- [CreateHtmlDocument](CreateHtmlDocument.md) — Store a completed HTML document in a folder.
- [Search](Search.md) — Find documents rendered from a specific template using the `TEMPLATEPATH` criterion.

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The `targetFolderPath` does not exist or is not accessible. |
| Document not found | The `templatePath` does not resolve to an existing document. |
| Access denied | The user lacks Read permission on the template or Add Document permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## React Implementer Guide

Production-ready patterns derived from the reference demo at `IRWebCore/wwwRoot/form-template-demo.html`.

### Shared helper functions

These functions are used across all three form APIs (`UseFormTemplate`, `GetFormFromDocument`, `CreateDocumentUsingTemplate`). Define them once in a shared module.

```javascript
// XML-escape a value before placing it inside a <Prompt> element
function escapeXml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

// Parse the InfoRouter_Fields hidden input from a rendered form inside an iframe.
// Returns an array of { name, value, dataType, required }.
// InfoRouter_Fields format: 'IR_field1','CHAR','N','N','IR_field2','DATE','Y','N',...
function parseInfoRouterFields(iframeDoc, form) {
  const input = iframeDoc.getElementById('InfoRouter_Fields');
  if (!input || !input.value.trim()) return [];
  const tokens = input.value.split(',');
  const fields = [];
  for (let i = 0; i + 3 < tokens.length; i += 4) {
    const raw      = tokens[i].trim();                       // e.g. "'IR_title'"
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

// Build the <FORMDATA> XML required by CreateDocumentUsingTemplate
function buildXmlContent(fields) {
  if (!fields || fields.length === 0) return '';
  return '<FORMDATA>' +
    fields.map(f => `<Prompt Name="${f.name}">${escapeXml(f.value)}</Prompt>`).join('') +
    '</FORMDATA>';
}

// Parse an infoRouter XML response — handles both <root> and <response> root elements
function parseXml(xmlText) {
  const doc = new DOMParser().parseFromString(xmlText, 'text/xml');
  const root = doc.querySelector('root') ?? doc.querySelector('response');
  if (!root) return { ok: false, error: 'Could not parse response' };
  return { ok: root.getAttribute('success') === 'true', error: root.getAttribute('error') ?? '', el: root };
}
```

### Step 1 — Fetch the form

```javascript
async function loadForm(apiBase, ticket, targetFolderPath, templatePath) {
  const body = new URLSearchParams({
    authenticationTicket: ticket,
    targetFolderPath,
    templatePath,
    submitUrl: '',   // Always include; pass '' when using iframe submit interception
  });
  const res = await fetch(`${apiBase}/UseFormTemplate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
  const r = parseXml(await res.text());
  if (!r.ok) throw new Error(r.error);
  return r.el.textContent;  // Raw HTML extracted from CDATA
}
```

`r.el.textContent` extracts the HTML from inside the CDATA wrapper. `submitUrl` must always be present — pass `''` to let the iframe `onLoad` handler own submit interception.

### Step 2 — Render in React and intercept submit

```jsx
import { useState, useRef, useCallback } from 'react';

function CreateDocumentForm({ ticket, targetFolderPath, templatePath, apiBase, onSubmit }) {
  const [renderedHtml, setRenderedHtml] = useState('');
  const iframeRef = useRef(null);

  async function handleLoadForm() {
    const html = await loadForm(apiBase, ticket, targetFolderPath, templatePath);
    setRenderedHtml(html);
  }

  // useCallback with full dependency array prevents stale closures in the submit handler
  const handleIframeLoad = useCallback(() => {
    const iframe = iframeRef.current;
    if (!iframe || !renderedHtml) return;
    const doc = iframe.contentDocument;

    // Always inject the live ticket — the rendered form leaves InfoRouter_Ticket empty
    const ticketField = doc.getElementById('InfoRouter_Ticket');
    if (ticketField) ticketField.value = ticket;

    const form = doc.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', e => {
      e.preventDefault();
      e.stopPropagation();
      // Collect all template fields and their current values
      const fields = parseInfoRouterFields(doc, form);
      // Hand off to the parent — it will call CreateDocumentUsingTemplate
      onSubmit({ fields, templatePath });
    });
  }, [renderedHtml, ticket, templatePath]);

  return (
    <>
      <button onClick={handleLoadForm}>Load Form</button>
      {renderedHtml && (
        <iframe
          ref={iframeRef}
          srcDoc={renderedHtml}
          onLoad={handleIframeLoad}
          sandbox="allow-scripts allow-forms allow-same-origin"
          style={{ width: '100%', height: 600, border: 'none' }}
          title="Document Form"
        />
      )}
    </>
  );
}
```

### Critical rules

| Rule | Reason |
|---|---|
| Use `srcDoc` (not `src`) on the iframe | Renders the HTML string directly without a round-trip |
| `sandbox="allow-scripts allow-forms allow-same-origin"` | Scripts inside the form execute; `contentDocument` access is permitted |
| `e.preventDefault()` + `e.stopPropagation()` | Prevents the browser from navigating away on submit |
| Inject `InfoRouter_Ticket` in `onLoad` | The rendered HTML always has this field empty by design |
| List `[renderedHtml, ticket, templatePath]` in `useCallback` deps | Prevents the submit handler from capturing stale values when inputs change |
| Call `CreateDocumentUsingTemplate` from the `onSubmit` handler | `UseFormTemplate` only renders the form; the actual save is a separate call |

---
