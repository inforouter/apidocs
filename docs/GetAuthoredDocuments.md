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

Lists the documents one user wrote, a page at a time, in the full `<document>` shape
[GetDocument](GetDocument.md) uses.

```javascript
let startingRow = 0;
const rowCount = 100;

for (;;) {
  const root = await call('GetAuthoredDocuments', {
    authenticationTicket: ticket, userName: 'jsmith', startingRow, rowCount
  });

  for (const document of root.querySelectorAll(':scope > document')) {
    console.log(document.getAttribute('Path'));
  }

  startingRow += rowCount;
  if (startingRow >= Number(root.getAttribute('recordCount'))) break;
}
```

`rowCount=0` means **every row**, not none, and the answer then reports `rowCount` as the total rather
than the zero that was sent - so a loop that trusts the value it sent will not terminate. The root
carries `recordCount`, the total ignoring the paging, alongside the `startingRow` and `rowCount` that
were applied.

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all authored documents (equivalent to calling [GetAuthoredDocuments](GetAuthoredDocuments.md)).
- Results are returned in ascending order by document name.
- The `totalcount` attribute on the root element reflects the total number of matching documents, regardless of paging parameters.
- Each `<document>` element includes a `UserViewStatus` integer attribute: `0` = never viewed, `1` = viewed but the published version has since changed, `2` = viewed the current published version. See `GetDocument` for the full attribute reference.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no user by that name |
| `4010` | there is no ticket at all; the list is about the signed-in user and there is not one |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

