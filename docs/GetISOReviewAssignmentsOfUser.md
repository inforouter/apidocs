# GetISOReviewAssignmentsOfUser API

Returns a paged list of documents assigned to the specified user for ISO review.

## Endpoint

```
/srv.asmx/GetISOReviewAssignmentsOfUser
```

## Methods

- **GET** `/srv.asmx/GetISOReviewAssignmentsOfUser?authenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetISOReviewAssignmentsOfUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetISOReviewAssignmentsOfUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `userName` | string | Yes | The username whose ISO review assignments are to be retrieved |
| `startingRow` | int | Yes | Zero-based row offset for paging. Pass `0` to start from the first result |
| `rowCount` | int | Yes | Number of rows to return (page size). Pass `0` to return all results |

## Required Permissions

- No additional permissions are required when querying the authenticated user's own ISO review assignments.
- To query another user's assignments, the caller must have the **ListingAuditLogOfUser** admin permission for the target user.

## Response

### Success Response

```xml
<root success="true" totalcount="12">
  <document id="510" name="QualityPolicy.docx" path="/ISO/QualityPolicy.docx" ... />
  <document id="622" name="ProcedureManual.pdf" path="/ISO/ProcedureManual.pdf" ... />
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or invalid ticket" />
```

## Example

### Request (GET)

```
GET /srv.asmx/GetISOReviewAssignmentsOfUser?authenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### Request (POST)

```
POST /srv.asmx/GetISOReviewAssignmentsOfUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### SOAP 1.1 Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetISOReviewAssignmentsOfUser>
      <tns:authenticationTicket>abc-123</tns:authenticationTicket>
      <tns:userName>jsmith</tns:userName>
      <tns:startingRow>0</tns:startingRow>
      <tns:rowCount>25</tns:rowCount>
    </tns:GetISOReviewAssignmentsOfUser>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all ISO review assignments.
- Results are returned in ascending order by document name.
- The `totalcount` attribute on the root element reflects the total number of ISO review assignments for the user, regardless of paging parameters.
- This API was formerly named `GetISOReviewAssignments`. Callers using the old name must update to `GetISOReviewAssignmentsOfUser` and add the `startingRow` and `rowCount` parameters.
