# GetCheckedoutDocumentsByUser API

Returns a paged list of documents currently checked out by the specified user.

## Endpoint

```
/srv.asmx/GetCheckedoutDocumentsByUser
```

## Methods

- **GET** `/srv.asmx/GetCheckedoutDocumentsByUser?AuthenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetCheckedoutDocumentsByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetCheckedoutDocumentsByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `userName` | string | Yes | The username whose checked out documents are to be retrieved |
| `startingRow` | int | Yes | Zero-based row offset for paging. Pass `0` to start from the first result |
| `rowCount` | int | Yes | Number of rows to return (page size). Pass `0` to return all results |

## Required Permissions

- No additional permissions are required when querying the authenticated user's own checked out documents.
- To query another user's checked out documents, the caller must have the **ListingAuditLogOfUser** admin permission for the target user.

## Response

### Success Response

```xml
<root success="true" totalcount="5">
  <document id="301" name="Contract.docx" path="/Legal/Contract.docx" checkedoutby="jsmith" ... />
  <document id="402" name="Proposal.pdf" path="/Sales/Proposal.pdf" checkedoutby="jsmith" ... />
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or invalid ticket" />
```

## Example

### Request (GET)

```
GET /srv.asmx/GetCheckedoutDocumentsByUser?AuthenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### Request (POST)

```
POST /srv.asmx/GetCheckedoutDocumentsByUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### SOAP 1.1 Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetCheckedoutDocumentsByUser>
      <tns:authenticationTicket>abc-123</tns:authenticationTicket>
      <tns:userName>jsmith</tns:userName>
      <tns:startingRow>0</tns:startingRow>
      <tns:rowCount>25</tns:rowCount>
    </tns:GetCheckedoutDocumentsByUser>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all checked out documents.
- Results are returned in ascending order by document name.
- The `totalcount` attribute on the root element reflects the total number of checked out documents for the user, regardless of paging parameters.
- To retrieve checked out documents for the currently authenticated user, use [GetCheckedoutDocuments](GetCheckedoutDocuments.md).
