# Rename API

Renames a document or a folder in place. Only the name changes: the item stays in its folder and keeps its id, description, update instructions, versions, security and everything else.

## Endpoint

```
/srv.asmx/Rename
```

## Methods

- **GET** `/srv.asmx/Rename?authenticationTicket=...&Path=...&NewName=...`
- **POST** `/srv.asmx/Rename` (form data)
- **SOAP** Action: `http://tempuri.org/Rename`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path of the document or folder (e.g. `/Finance/Reports/Q1.pdf`), or `~D{id}` for a document / `~F{id}` for a folder. A full path is looked up as a document first, then as a folder. |
| `NewName` | string | Yes | The **complete** new name - a name, not a path. For a document it **includes the extension**: `Q1 final.pdf`, not `Q1 final`. |

### `NewName` for a document includes the extension

The API takes the whole file name and does not add or keep the extension for you:

| Current name | `NewName` | Result |
|---|---|---|
| `Q1.pdf` | `Q1 final.pdf` | `Q1 final.pdf` |
| `Q1.pdf` | `Q1 final` | `Q1 final` - the document no longer has an extension |
| `Q1.pdf` | `Q1.docx` | `Q1.docx` - the extension changes, the content is **not** converted |

A UI that lets the user edit only the part before the extension should append the original extension
itself, and should warn before sending a different one. Reserved extensions cannot be given or taken away,
and a folder that allows only certain file types refuses a name with another extension.

For a folder, `NewName` is simply the new folder name.

---

## Response

### Success Response

```xml
<response success="true" error="" type="document" id="96892" name="Q1 final.pdf" path="\Finance\Reports\Q1 final.pdf" />
```

| Attribute | Description |
|---|---|
| `type` | `document` or `folder`. |
| `id` | The document or folder id. It does not change. |
| `name` | The new name, trimmed of leading and trailing spaces. |
| `path` | The new full path, written with backslashes as the listing APIs write it. |

The UI can update its tree from this response without reading the item again.

### Error Response

```xml
<response success="false" error="A document with this name already exists in this folder." errorCode="4090" />
```

---

## Required Permissions

- **Document:** the right to change the document's properties. The document must not be checked out by
  another user (checked out by the caller is fine), and its file must not be open for editing (Office, WebDAV).
- **Folder:** the right to change the folder's properties.

This is the property-change right, not the delete right [Move](Move.md) needs: a user who may edit a
document's properties but not delete it can rename it here.

---

## Example

### GET Request (document)

```
GET /srv.asmx/Rename
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1.pdf
  &NewName=Q1 final.pdf
HTTP/1.1
```

### POST Request (folder)

```
POST /srv.asmx/Rename HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&NewName=Quarterly Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:Rename>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1.pdf</tns:Path>
      <tns:NewName>Q1 final.pdf</tns:NewName>
    </tns:Rename>
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

Let the user edit the name without the extension, put the extension back, and warn if they typed a
different one:

```javascript
function splitName(fileName) {
  const dot = fileName.lastIndexOf('.');
  return dot > 0 ? [fileName.slice(0, dot), fileName.slice(dot)] : [fileName, ''];
}

const [, extension] = splitName(currentName);         // ".pdf"
let newName = userInput.trim();                          // "Q1 final" or "Q1 final.docx"
const [, typedExtension] = splitName(newName);

if (typedExtension === '') {
  newName += extension;                                  // "Q1 final.pdf"
} else if (typedExtension.toLowerCase() !== extension.toLowerCase()
           && !confirm(`Change the file type from ${extension} to ${typedExtension}?`)) {
  return;
}

const renamed = await call('Rename', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/' + currentName,
  NewName: newName
});
console.log(renamed.getAttribute('path'));               // \Finance\Reports\Q1 final.pdf
```

## Notes

- **Only the name changes.** Description, update instructions, importance, author and the other properties
  are left as they are. To change them, use [UpdateDocumentProperties](UpdateDocumentProperties.md) or
  [UpdateFolderProperties](UpdateFolderProperties.md).
- **A change of case is a rename.** `q1.pdf` to `Q1.pdf` is applied. ([Move](Move.md) refuses it as "the
  same place".)
- **The current name** is answered success and nothing changes.
- **`NewName` is never a path.** A `/` or `\` in it is refused with `4000`; to move an item use [Move](Move.md).
- The same naming rules as [UpdateDocumentProperties](UpdateDocumentProperties.md) and
  [UpdateFolderProperties](UpdateFolderProperties.md) apply, and a name that breaks them is refused with `4000`
  rather than cleaned up silently.
- **A library** (a top level folder) cannot be renamed here.
- The rename is written to the rename history, and subscribers of a document are notified.
- A folder rename changes the paths of everything under it; ids do not change.

---

## Related APIs

- [Move](Move.md) - Move a document or folder to another folder
- [UpdateDocumentProperties](UpdateDocumentProperties.md) - Change a document's name, description and update instructions together
- [UpdateFolderProperties](UpdateFolderProperties.md) - Change a folder's name and description together

---

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | `NewName` is not a valid name: it holds a `/` or `\` or another character names may not have, is blank (SOAP), or has a reserved or not-allowed extension; `Path` is a library; or the document is checked out by another user or its file is open for editing |
| `4010` | the ticket is expired or unknown, or there is no ticket |
| `4030` | the caller may not change the item's properties (a read-only user, for example) |
| `4041` | nothing at `Path` |
| `4090` | another document or folder in the same folder already has that name |
| `4230` | the document is offline |
| `HTTP 400` | `Path` or `NewName` was empty or only spaces; refused by model binding, so there is no error document |
