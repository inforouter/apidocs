# CreateFormFromTemplate API

Returns the rendered HTML form for a content template. The response is the complete HTML that the user's browser can display and submit to create a new document in the specified destination folder.

## Endpoint

```
/srv.asmx/CreateFormFromTemplate
```

## Methods

- **GET** `/srv.asmx/CreateFormFromTemplate?authenticationTicket=...&targetFolderPath=...&templatePath=...`
- **POST** `/srv.asmx/CreateFormFromTemplate` (form data)
- **SOAP** Action: `http://tempuri.org/CreateFormFromTemplate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `targetFolderPath` | string | Yes | Full infoRouter path of the destination folder where the new document will be created (e.g. `/Finance/Reports`). |
| `templatePath` | string | Yes | Full infoRouter path of the template document (e.g. `/Templates/ExpenseForm.htm`), or `~D<id>` short form (e.g. `~D42`). Use `~D999` for the built-in HTML document type. |

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
POST /srv.asmx/CreateFormFromTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&targetFolderPath=/Finance/Reports
&templatePath=/Templates/ExpenseReport.htm
```

### Using ~D999 for HTML Documents

To render the built-in HTML document form (not tied to a specific template file):

```
POST /srv.asmx/CreateFormFromTemplate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&targetFolderPath=/Finance/Reports
&templatePath=~D999
```

---

## Notes

- The `templatePath` accepts either a full document path or the `~D<id>` short form. `~D999` is the reserved identifier for the built-in HTML document type and does not correspond to a physical document in the repository.
- The rendered HTML is returned inside a CDATA section. Parse the XML response and extract the element's text content before rendering it in a browser.
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
