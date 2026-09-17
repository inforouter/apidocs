# VerifyVersionHash API

Verifies the integrity of a specific version of a document by comparing the stored content hash against the actual file in the warehouse storage. Returns whether the hash matches, indicating the file has not been corrupted or tampered with since it was stored.

## Endpoint

```
/srv.asmx/VerifyVersionHash
```

## Methods

- **GET** `/srv.asmx/VerifyVersionHash?authenticationTicket=...&path=...&versionNumber=...`
- **POST** `/srv.asmx/VerifyVersionHash` (form data)
- **SOAP** Action: `http://tempuri.org/VerifyVersionHash`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `versionNumber` | int | Yes | The internal version number to verify. Use `GetDocumentVersions` to retrieve available version numbers. |

---

## Response

### Success Response -" Hash Verified

```xml
<root success="true" hashVerified="true" />
```

### Success Response -" Hash Mismatch (file corrupted or tampered)

```xml
<root success="true" hashVerified="false" />
```

### Error Response

```xml
<root success="false" error="Document not found." />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` if the verification check ran (regardless of hash result). `"false"` if the check could not run (auth error, document not found). |
| `hashVerified` | `"true"` if the file's current content matches the stored hash. `"false"` if there is a mismatch, indicating possible corruption or tampering. |

---

## Required Permissions

The calling user must have **read** permission on the document or its containing folder.

---

## Example

### GET Request

```
GET /srv.asmx/VerifyVersionHash
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &versionNumber=1000001
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/VerifyVersionHash HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&versionNumber=1000001
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:VerifyVersionHash>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:versionNumber>1000001</tns:versionNumber>
    </tns:VerifyVersionHash>
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

Checks one stored version against the checksum recorded for it - whether what is in the warehouse is
still what was put there.

```javascript
const root = await call('VerifyVersionHash', {
  authenticationTicket: ticket,
  path: '/Finance/Reports/Q1.pdf',
  versionNumber: 0            // 0 means the published version
});

const intact = root.querySelector('Value').textContent === 'true';
```

A version that fails is a success carrying `false`, not an error - the call worked, the answer is bad
news. A version number nothing uses, or a path naming no document, is `4041`.

## Notes

- A `hashVerified="false"` result indicates the file content in warehouse storage does not match the hash recorded at upload time. This may indicate storage corruption, unauthorized file system modification, or a storage migration issue.
- Use `GetDocumentVersions` to retrieve the list of internal version numbers before calling this API.
- This API is useful for compliance audits and storage integrity checks.

---

## Related APIs

- [GetDocumentVersions](GetDocumentVersions.md) - Retrieve all version numbers for a document
- [GetDocumentVersion](GetDocumentVersion.md) - Get metadata for a specific version
- [DownloadDocumentVersion](DownloadDocumentVersion.md) - Download a specific document version

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path, or no version carries that number |
| `HTTP 400` | a required parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Version not found | The specified version number does not exist for this document. |
| Access denied | The user does not have read permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---