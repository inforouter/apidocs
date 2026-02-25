# GetFoldersAndDocuments2 API

Returns the list of documents and folders at the specified path in a lightweight ("ultra-fast") format. This API is optimized for speed and returns a minimal set of attributes for each item. Use this when you need a quick listing and do not require full property details.

## Endpoint

```
/srv.asmx/GetFoldersAndDocuments2
```

## Methods

- **GET** `/srv.asmx/GetFoldersAndDocuments2?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetFoldersAndDocuments2` (form data)
- **SOAP** Action: `http://tempuri.org/GetFoldersAndDocuments2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |

---

## Response

### Success Response

```xml
<response success="true">
  <folder id="456" name="2024" />
  <folder id="457" name="2023" />
  <document id="1001" name="Q1-Report.pdf" versionid="1000045" />
  <document id="1002" name="Q2-Report.pdf" versionid="1000067" />
</response>
```

### Error Response

```xml
<response success="false" error="Folder not found." />
```

---

## Required Permissions

The calling user must have **read** permission on the folder. Only items the user has access to are returned.

---

## Example

### GET Request

```
GET /srv.asmx/GetFoldersAndDocuments2
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFoldersAndDocuments2 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFoldersAndDocuments2>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
    </tns:GetFoldersAndDocuments2>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns only **direct** children (one level deep) of the specified path.
- This API uses an ultra-fast internal query that returns minimal metadata per item.
- No filtering, sorting, or paging is supported. All accessible items at the path are returned.
- For full property details (rules, property sets, security), use `GetFoldersAndDocuments` or `GetFoldersAndDocuments1`.
- For filtering and paging, use `GetFoldersAndDocumentsByPage` or `GetFoldersAndDocumentsByPage2`.

---

## Related APIs

- [GetFoldersAndDocuments](GetFoldersAndDocuments) - Full property listing
- [GetFoldersAndDocuments1](GetFoldersAndDocuments1) - Short-form listing
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage) - Paged listing with filtering
- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2) - Advanced paged listing with sorting

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetFoldersAndDocuments2*
