# CreateDocumentShortcut API

Creates a document shortcut (`.lnk` file) at the specified path that points to an existing target document. Shortcuts allow the same document to appear in multiple locations without duplicating the file content.

## Endpoint

```

/srv.asmx/CreateDocumentShortcut

```

## Methods

- **GET** `/srv.asmx/CreateDocumentShortcut?authenticationTicket=...&Path=...&TargetDocumentPath=...`

- **POST** `/srv.asmx/CreateDocumentShortcut` (form data)

- **SOAP** Action: `http://tempuri.org/CreateDocumentShortcut`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path for the new shortcut document to be created (e.g. `/MyLibrary/Shortcuts/AnnualReport.lnk`). The file name portion **must** end with the `.lnk` extension. |
| `TargetDocumentPath` | string | Yes | Full infoRouter path of the existing document the shortcut will point to (e.g. `/MyLibrary/Finance/AnnualReport.pdf`). |

## Response

### Success Response

```xml

<response success="true" error="" />

```

### Error Response

```xml

<response success="false" error="Error message" />

```

---

## Required Permissions

The authenticated user must have **Add Document** permission on the destination folder (the parent folder of the `Path` parameter). The target document specified by `TargetDocumentPath` must also be accessible to the user.

---

## Example

### GET Request

```

GET /srv.asmx/CreateDocumentShortcut

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/MyLibrary/Shortcuts/AnnualReport.lnk

  &TargetDocumentPath=/MyLibrary/Finance/Reports/AnnualReport.pdf

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/CreateDocumentShortcut HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/MyLibrary/Shortcuts/AnnualReport.lnk

&TargetDocumentPath=/MyLibrary/Finance/Reports/AnnualReport.pdf

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:CreateDocumentShortcut>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:Path>/MyLibrary/Shortcuts/AnnualReport.lnk</tns:Path>

      <tns:TargetDocumentPath>/MyLibrary/Finance/Reports/AnnualReport.pdf</tns:TargetDocumentPath>

    </tns:CreateDocumentShortcut>

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

Creates a shortcut document pointing at another document.

```javascript
await call('CreateDocumentShortcut', {
  authenticationTicket: ticket,
  Path: '/Finance/Shortcuts/Q1.lnk',        // must end in .lnk
  TargetDocumentPath: '/Finance/Reports/Q1.pdf'
});
```

**The name must end in `.lnk`**, and that is checked before the target is looked at - so a shortcut
named `.htm` pointing at a document that does not exist is answered with the extension complaint, not
with "not found". Get the extension right first, then worry about the target.

## Notes

- The `Path` parameter specifies both the destination folder and the shortcut file name. The file name (last segment of the path) **must** end with `.lnk`. If it does not, the API returns an error.

- The destination folder (the parent of `Path`) must already exist before calling this API; the folder is not created automatically.

- The shortcut file name can differ from the target document name.

- Deleting a shortcut does not delete the original document.

- When the shortcut is opened in infoRouter, it redirects the user to the target document.

---

## Related APIs

- [Copy](Copy.md) - Copy a document or folder to another location (creates a full copy, not a shortcut)

- [AddToFavorites](AddToFavorites.md) - Add a document to the current user's favorites list

- [GetDocument](GetDocument.md) - Retrieve properties of a document (works on both shortcuts and regular documents)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is refused |
| `4000` | the name does not end in `.lnk`; checked before the target is |
| `4090` | a document of that name is already in the folder |
| `4041` | no document at `TargetDocumentPath` |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid shortcut name. Extention must be .lnk` | The `Path` file name does not end with `.lnk`. |
| `Folder not found` | The destination folder (parent of `Path`) does not exist or is not accessible. |
| `Document not found` | The `TargetDocumentPath` does not refer to an existing document. |

---

