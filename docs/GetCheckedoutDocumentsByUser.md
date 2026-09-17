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

Documents come back as the full `<document>` element. Since 9.0 it also carries `AIEnhanced` and
`AIExtractConfidence`. The first says which of the document's attributes infoRouter Connect
produced, as a set of bits - `0` when none did; the second how sure it was about the weakest value
it put in a property set, as a percentage. See [AIEnhanced](GetDocument.md#aienhanced) and
[AIExtractConfidence](GetDocument.md#aiextractconfidence).

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

Lists the documents one named user has checked out, a page at a time.

```javascript
const root = await call('GetCheckedoutDocumentsByUser', {
  authenticationTicket: ticket,
  userName: 'jsmith',
  startingRow: 0,
  rowCount: 100
});

console.log(root.getAttribute('recordCount'), 'checked out in total');
```

`rowCount=0` means **every row**, not none, and the answer then reports `rowCount` as the total rather
than the zero that was sent - so a loop that trusts the value it sent will not terminate. The root
carries `recordCount`, the total ignoring the paging, alongside the `startingRow` and `rowCount` that
were applied.

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all checked out documents.
- Results are returned in ascending order by document name.
- The `totalcount` attribute on the root element reflects the total number of checked out documents for the user, regardless of paging parameters.
- To retrieve checked out documents for the currently authenticated user, use [GetCheckedoutDocuments](GetCheckedoutDocuments.md).
- Each `<document>` element includes a `UserViewStatus` integer attribute: `0` = never viewed, `1` = viewed but the published version has since changed, `2` = viewed the current published version. See `GetDocument` for the full attribute reference.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

