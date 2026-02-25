# UploadDocumentWithHandler2 API

Finalizes a chunked file upload and creates a new document or a new version of an existing document at the specified path, with an optional version comment and explicit manual version numbers (Major.Minor.Revision). This extends `UploadDocumentWithHandler1` by supporting the three-part manual version label that appears in the document's version list.

## Endpoint

```
/srv.asmx/UploadDocumentWithHandler2
```

## Methods

- **GET** `/srv.asmx/UploadDocumentWithHandler2?authenticationTicket=...&path=...&uploadHandler=...&versionComments=...&mpVersionMajor=...&mpVersionMinor=...&mpVersionRevision=...`
- **POST** `/srv.asmx/UploadDocumentWithHandler2` (form data)
- **SOAP** Action: `http://tempuri.org/UploadDocumentWithHandler2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `uploadHandler` | string (GUID) | Yes | The upload handler GUID returned by `CreateUploadHandler` after all chunks have been uploaded. |
| `versionComments` | string | No | A comment describing the changes in this version. |
| `mpVersionMajor` | short | Yes | Major component of the manual version label (e.g. `2` for version `2.0.1`). Range: 1–2400. |
| `mpVersionMinor` | short | Yes | Minor component of the manual version label (e.g. `0` for version `2.0.1`). Range: 0–999. |
| `mpVersionRevision` | short | Yes | Revision component of the manual version label (e.g. `1` for version `2.0.1`). Range: 0–999. |

---

## Chunked Upload Workflow

```
1. CreateUploadHandler        → returns UploadHandler GUID + ChunkSize
2. UploadFileChunk            → repeat until LastChunk=true
3. UploadDocumentWithHandler2 → finalize with version comment and manual version number
```

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000003" />
```

### Error Response

```xml
<root success="false" error="Invalid upload handler." />
```

---

## Required Permissions

The calling user must have **write** (upload) permission on the destination folder.

---

## Example

### POST Request

```
POST /srv.asmx/UploadDocumentWithHandler2 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&uploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
&versionComments=Released for review
&mpVersionMajor=2
&mpVersionMinor=0
&mpVersionRevision=1
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadDocumentWithHandler2>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:uploadHandler>a1b2c3d4-e5f6-7890-abcd-ef1234567890</tns:uploadHandler>
      <tns:versionComments>Released for review</tns:versionComments>
      <tns:mpVersionMajor>2</tns:mpVersionMajor>
      <tns:mpVersionMinor>0</tns:mpVersionMinor>
      <tns:mpVersionRevision>1</tns:mpVersionRevision>
    </tns:UploadDocumentWithHandler2>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The manual version label (e.g. `2.0.1`) is a human-readable label separate from the internal infoRouter version ID.
- Valid ranges: `mpVersionMajor` 1–2400, `mpVersionMinor` 0–999, `mpVersionRevision` 0–999. Out-of-range values return an error.
- Use `UploadDocumentWithHandler3` for the most flexible option set (XML parameters string).

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler) - Create an upload handler for chunked uploads
- [UploadFileChunk](UploadFileChunk) - Upload a single chunk
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1) - Finalize with version comment only
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3) - Finalize with XML parameters

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid upload handler.` | The GUID is not a valid or active upload handler. |
| Invalid version number component | `mpVersionMajor`, `mpVersionMinor`, or `mpVersionRevision` is out of the valid range. |
| Folder not found | The destination folder in the path does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadDocumentWithHandler2*
