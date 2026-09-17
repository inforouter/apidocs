# UploadZip API

Imports a ZIP archive as a folder and document structure into the specified folder.

## Endpoint

```
/srv.asmx/UploadZip
```

## Methods

- **POST** `/srv.asmx/UploadZip` (form data)
- **SOAP** Action: `http://tempuri.org/UploadZip`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `folderPath` | string | Yes | Full infoRouter path of the destination folder (e.g. `/Domain/Folder`). The folder must exist |
| `zipContent` | byte[] | Yes | Raw ZIP file bytes; Base64-encoded when sent over HTTP |
| `changedOnly` | bool | Yes | When `true`, existing documents are updated only if the uploaded content differs from the current version. When `false`, all matching documents are updated regardless |
| `checkOutCheckIn` | bool | Yes | When `true`, existing documents are checked out before update and checked back in afterwards. Automatically set to `true` when `changedOnly` is `true` |
| `sendEmail` | bool | Yes | When `true`, email notifications are sent to folder subscribers |

## Response

### Success

```xml
<root success="true">
  <logs />
</root>
```

The `<logs>` element is empty on a fully successful import. Log entries are only written for items that could not be processed.

### Failure

When the ZIP extraction or import fails, `success="false"` is returned. The `<logs>` element contains an entry for each item that could not be processed:

```xml
<root success="false">
  <logs>
    <log><item>upload.zip</item><error>Unzip operation failed: invalid ZIP format</error></log>
  </logs>
</root>
```

### Error (authentication or folder not found)

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

- User must be authenticated.
- Caller must have document creation permission on the destination folder.
- If the folder rule `DisallowNewDocument` is set, the import will be rejected.

## Example Requests

### Request (POST)

```
POST /srv.asmx/UploadZip HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&folderPath=/MyDomain/Imports&zipContent=<base64-encoded-zip>&changedOnly=true&checkOutCheckIn=true&sendEmail=false
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/UploadZip"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <UploadZip xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <folderPath>/MyDomain/Imports</folderPath>
      <zipContent><!-- Base64-encoded ZIP bytes --></zipContent>
      <changedOnly>true</changedOnly>
      <checkOutCheckIn>true</checkOutCheckIn>
      <sendEmail>false</sendEmail>
    </UploadZip>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at `folderPath` |
| `4030` | the caller may not add documents there, or the folder rules forbid the file type |
| `HTTP 415` | the call was a GET; the content can only be posted |
| `HTTP 400` | a required parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Folder not found | The specified `folderPath` does not exist |
| Access denied | Caller lacks document creation permission on the destination folder |
| Unzip operation failed | The uploaded bytes are not a valid ZIP archive |

## JavaScript

```javascript
// Anything carrying bytes is POST-only: a byte[] cannot be bound from a query string, and a GET is
// answered HTTP 415 before the operation runs.
async function post(action, fields) {
  const response = await fetch(`/srv.asmx/${action}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ authenticationTicket: ticket, ...fields })
  });

  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}

const base64 = bytes => btoa(String.fromCharCode(...bytes));
```

```javascript
await post('UploadZip', {
  folderPath: '/Finance/Reports',
  zipContent: base64(zipBytes),
  changedOnly: 'false',
  checkOutCheckIn: 'false',
  sendEmail: 'false'
});
```

The archive is unpacked into the folder, keeping the paths inside it - so a zip holding
`reports/Q1.pdf` produces a `reports` folder. `changedOnly` skips entries whose content matches what
is already there, `checkOutCheckIn` checks documents out and back in around each write, and
`sendEmail` notifies subscribers.

**The answer's root element is `<root>`, not the `<response>` almost every other operation returns**,
and what could not be unpacked is listed inside `<logs>`.

## Notes

- The ZIP archive's internal folder structure is recreated under the destination folder. Subfolders in the archive become subfolders in infoRouter.
- `changedOnly=true` implicitly enables `checkOutCheckIn` behavior.
- The following parameters are always applied with system defaults during import: classification level (`NoMarkings`), importance (`0`), retention schedule (`none`), declassify/downgrade dates (`none`).
- The response `<log>` children are always emitted regardless of success or failure and describe each item processed during import.

## Related APIs

- `GetFoldersAndDocuments` — Browse folder contents to find the destination folder ID
- `UploadDocument` — Upload a single document
- `CreateFolder` — Create a subfolder manually before importing
