# SetTagToDocument API

Applies a tag to the latest version of the specified document. If the document's publishing rule is set to **Tagged** and the supplied tag text matches the rule's configured tag, the latest version is also automatically published. Use this API to mark a document version with a classification or approval label as part of a review or workflow process.

## Endpoint

```
/srv.asmx/SetTagToDocument
```

## Methods

- **GET** `/srv.asmx/SetTagToDocument?authenticationTicket=...&path=...&tagText=...`
- **POST** `/srv.asmx/SetTagToDocument` (form data)
- **SOAP** Action: `http://tempuri.org/SetTagToDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `tagText` | string | Yes | Text of the tag to apply. Must be 1-"128 characters. Allowed characters: Unicode letters, digits (`0-"9`), underscore (`_`), hyphen (`-`), and space. |

---

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Insufficient rights." />
```

---

## Required Permissions

The calling user must have the **`DocumentPropertyChange`** permission on the document. This is typically granted to document owners, domain managers, and users with Edit access. Read-only users cannot apply tags.

If the document is currently checked out, only the user who checked it out may apply a tag to it.

---

## Example

### GET Request

```
GET /srv.asmx/SetTagToDocument
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &tagText=Approved
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetTagToDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&tagText=Approved
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetTagToDocument>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:tagText>Approved</tns:tagText>
    </tns:SetTagToDocument>
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

Applies a tag to the version a document is currently on.

```javascript
await call('SetTagToDocument', {
  authenticationTicket: ticket,
  path: '/Finance/Invoices/inv-1001.pdf',
  tagText: 'Checked'
});
```

The text can be anything - it does not have to be one of
[GetTagDefinitions](GetTagDefinitions.md).

**Applying the same text twice is refused** `4090`. Until 9.0 nothing checked whether the version
already carried the tag, so two rows were left differing only in their timestamp and each had to be
removed separately with its own date. The same text on a *different* version is still allowed: that
is how a `TAGGED` publishing rule moves from one version to the next.

The operation is document only: a folder path is answered "document not found".

## Notes

- **Tag is applied to the latest version**: The tag is always applied to the document's most recent version, regardless of the published version number.
- **Auto-publish on tag match**: If the document's publishing rule is set to **Tagged** and `tagText` matches the configured tag text (case-insensitive), the latest version is automatically published as a side effect of this call.
- **Checked-out documents**: If the document is checked out by another user, the operation fails. Only the user who holds the checkout can apply a tag to the document while it is checked out.
- **Shortcuts not supported**: Tags cannot be applied to shortcut documents. Calling this API on a shortcut path will return an error.
- **Tag text validation**: `tagText` must match the pattern `^(\w|[ -]){1,128}$`. This means only Unicode word characters (letters, digits, underscore), hyphens, and spaces are allowed. Any other character will cause the call to fail.
- **Duplicate tags**: the same tag text cannot be applied to the same document version twice - the second call is refused `4090`. Applying it to a different version is allowed and creates a separate record.
- **Tag definitions**: The list of tag definitions configured in the system can be retrieved via `GetTagDefintions`. However, `SetTagToDocument` does not validate `tagText` against the defined tags -" any text matching the character and length rules is accepted.

---

## Related APIs

- [RemoveTagFromDocument](RemoveTagFromDocument.md) - Remove a specific applied tag from a document
- [GetTagDefintions](GetTagDefintions.md) - Get the list of all tag definitions configured in the system
- [GetDocument](GetDocument.md) - Get document properties including applied tags

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path |
| `4030` | the caller may not change that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
