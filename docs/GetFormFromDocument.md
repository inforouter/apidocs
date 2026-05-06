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
