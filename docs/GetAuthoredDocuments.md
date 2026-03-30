# GetAuthoredDocuments API

Returns a paged list of documents authored by a specified user.

## Endpoint

```
/srv.asmx/GetAuthoredDocuments
```

## Methods

- **GET** `/srv.asmx/GetAuthoredDocuments?authenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetAuthoredDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/GetAuthoredDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `userName` | string | Yes | The username whose authored documents are to be retrieved |
| `startingRow` | int | Yes | Zero-based row offset for paging. Pass `0` to start from the first result |
| `rowCount` | int | Yes | Number of rows to return (page size). Pass `0` to return all results |

## Required Permissions

- No additional permissions are required when querying the authenticated user's own documents.
- To query another user's documents, the caller must have the **ListingAuditLogOfUser** admin permission for the target user.

## Response

### Success Response

```xml
<root success="true" totalcount="42">
  <document id="123" name="Report.docx" path="/Finance/Report.docx" ... />
  <document id="124" name="Summary.pdf" path="/Finance/Summary.pdf" ... />
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or invalid ticket" />
```

## Example

### Request (GET)

```
GET /srv.asmx/GetAuthoredDocuments?authenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### Request (POST)

```
POST /srv.asmx/GetAuthoredDocuments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### SOAP 1.1 Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAuthoredDocuments>
      <tns:authenticationTicket>abc-123</tns:authenticationTicket>
      <tns:userName>jsmith</tns:userName>
      <tns:startingRow>0</tns:startingRow>
      <tns:rowCount>25</tns:rowCount>
    </tns:GetAuthoredDocuments>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all authored documents (equivalent to calling [GetAuthoredDocuments](GetAuthoredDocuments.md)).
- Results are returned in ascending order by document name.
- The `totalcount` attribute on the root element reflects the total number of matching documents, regardless of paging parameters.
