# GetFolderCatalog API

Returns the catalog information for the specified folder. The catalog provides a structured XML description of the folder's contents, metadata, and configuration as used by the infoRouter portal and UI components.

## Endpoint

```
/srv.asmx/GetFolderCatalog
```

## Methods

- **GET** `/srv.asmx/GetFolderCatalog?authenticationTicket=...&folderPath=...`
- **POST** `/srv.asmx/GetFolderCatalog` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderCatalog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `folderPath` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |

---

## Response

### Success Response

```xml
<response success="true">
  <!-- Catalog XML content from the folder's catalog definition -->
  <catalog>...</catalog>
</response>
```

### Error Response

```xml
<response error="Folder not found." />
```

---

## Required Permissions

The calling user must have **read** permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolderCatalog
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &folderPath=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolderCatalog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&folderPath=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolderCatalog>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:folderPath>/Finance/Reports</tns:folderPath>
    </tns:GetFolderCatalog>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The catalog XML content varies depending on the folder's configuration in infoRouter.
- This API is primarily used by the infoRouter portal and UI to render folder views.

---

## Related APIs

- [GetFolder](GetFolder) - Get folder metadata and properties
- [GetFolderRules](GetFolderRules) - Get folder rules
- [GetFolderStatistics](GetFolderStatistics) - Get folder statistics

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetFolderCatalog*
