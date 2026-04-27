# UploadZip API

Imports a ZIP archive as a folder and document structure into the specified folder.

## Endpoint

```
/srv.asmx/UploadZip
```

## Methods

- **GET** `/srv.asmx/UploadZip?authenticationTicket=...&folderPath=...&zipContent=...&changedOnly=...&checkOutCheckIn=...&sendEmail=...`
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
  <logs>
    <log><item>documents/report.pdf</item><error>Imported successfully</error></log>
    <log><item>documents/notes.docx</item><error>Updated (changed)</error></log>
  </logs>
</root>
```

### Failure

When the ZIP extraction or import fails, `success="false"` is returned. All log entries describing what was processed before failure are inside `<logs>`:

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

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Folder not found | The specified `folderPath` does not exist |
| Access denied | Caller lacks document creation permission on the destination folder |
| Unzip operation failed | The uploaded bytes are not a valid ZIP archive |

## Notes

- The ZIP archive's internal folder structure is recreated under the destination folder. Subfolders in the archive become subfolders in infoRouter.
- `changedOnly=true` implicitly enables `checkOutCheckIn` behavior.
- The following parameters are always applied with system defaults during import: classification level (`NoMarkings`), importance (`0`), retention schedule (`none`), declassify/downgrade dates (`none`).
- The response `<log>` children are always emitted regardless of success or failure and describe each item processed during import.

## Related APIs

- `GetFoldersAndDocuments` — Browse folder contents to find the destination folder ID
- `UploadDocument` — Upload a single document
- `CreateFolder` — Create a subfolder manually before importing
