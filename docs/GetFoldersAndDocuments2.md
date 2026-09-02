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

Folders come back as `<f>` and documents as `<d>`. The `<d>` element here is **not** the one
[GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) returns: this API carries the published version
checksum and the template id instead of the dates and the checkout, which is what makes it useful for
comparing a local copy against the server.

```xml
<response success="true"
          error=""
          id="1329"
          name="Reports"
          itemcount="4">

  <!-- Folder items - id and name only -->
  <f id="42" n="2024" />
  <f id="43" n="2023" />

  <!-- Document items -->
  <d id="1494" n="Q1-Report.pdf" sz="308" pv="1000000" lv="1000000" chksum="BFDB77A6" tid="0" />
  <d id="1495" n="Q2-Report.pdf" sz="512" pv="1000000" lv="2000000" chksum="1A2B3C4D" tid="0" />

</response>
```

#### Root attributes

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the request succeeded. |
| `error` | Error message if `success` is `false`; otherwise empty. |
| `id` | Integer ID of the queried folder (the folder at `Path`). |
| `name` | Name of the queried folder. |
| `itemcount` | Count of folders plus documents returned. |

#### `<f>` - folder items

| Attribute | Description |
|-----------|-------------|
| `id` | Unique integer ID of the sub-folder. |
| `n` | Name of the sub-folder. |

#### `<d>` - document items

| Attribute | Description |
|-----------|-------------|
| `id` | Unique integer ID of the document. |
| `n` | Document file name (including extension). |
| `sz` | File size in bytes. |
| `pv` | Published version number (`0` if no version is published). |
| `lv` | Latest version number. Both are in the large-integer scheme, where version 1 is `1000000`. |
| `chksum` | Checksum of the published version, for telling a changed file from an unchanged one without downloading it. Empty where none is stored. |
| `tid` | Template ID the document was created from (`0` if none). |

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
- This lightweight API returns the short-form `<f>` / `<d>` elements. Extended attributes - property sets, security, rules, `UserViewStatus`, `AIEnhanced` - are not included. Use [GetFoldersAndDocuments](GetFoldersAndDocuments.md) for the full `<document>` element.

---

## Related APIs

- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Full property listing
- [GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) - Short-form listing
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Paged listing with filtering
- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2.md) - Advanced paged listing with sorting

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