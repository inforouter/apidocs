# RemoveTagFromDocument API



Removes a specific applied tag from a document. Because a document may have the same tag applied multiple times (e.g. by different users or at different times), the API requires an exact match on **all** identifying fields -" tag text, version number, date applied, and the user who applied it. Use this API to remove a tag that was applied via a workflow step or via `SetTagToDocument` when it is no longer appropriate.



## Endpoint



```

/srv.asmx/RemoveTagFromDocument

```



## Methods



- **GET** `/srv.asmx/RemoveTagFromDocument?authenticationTicket=...&path=...&tagText=...&tagDate=...&taggedBy=...&versionNumber=...`

- **POST** `/srv.asmx/RemoveTagFromDocument` (form data)

- **SOAP** Action: `http://tempuri.org/RemoveTagFromDocument`



## Parameters



| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `tagText` | string | Yes | Exact text of the tag to remove. Must be case-sensitive and match the stored value exactly. Obtain the exact tag text from the document's applied tag list or from `GetTagDefintions`. |
| `tagDate` | DateTime | Yes | The exact date and time the tag was applied, as returned by the document's applied tag list (ISO 8601 including milliseconds, e.g. `2026-05-04T07:23:42.093Z`). Pass that value back unchanged rather than re-typing it to the second, or nothing will match. UTC values are automatically converted to server local time before matching. Must match the stored `TAGDATE` value exactly. |
| `taggedBy` | int | Yes | Internal user ID of the user who applied the tag. Must match the stored `TAGGEDBYID` value exactly. Obtain via `GetUser` or `GetAllUsers`. |
| `versionNumber` | int | Yes | Internal version number of the document version the tag was applied to. This is the raw internal version number (e.g. `1000000` for Version 1, `2000000` for Version 2). Must match the stored `VERSIONNUMBER` value exactly. |



---



## Response



### Success Response



```xml

<response success="true" error="" errorCode="0" />

```



> **Note:** A `success="true"` response means a tag row was actually removed. If nothing matched, the call returns `success="false"` with a not-found error.



### Error Response



```xml

<response success="false" error="Insufficient rights." />

```



---



## Required Permissions



The calling user must have the **`DocumentPropertyChange`** permission on the document. This is typically granted to document owners, domain managers, and users with Edit access. Read-only users cannot remove tags.



---



## Example



### GET Request



```

GET /srv.asmx/RemoveTagFromDocument

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &path=/Finance/Reports/Q1-2024-Report.pdf

  &tagText=Approved

  &tagDate=2024-06-15T14:30:00.123Z

  &taggedBy=12

  &versionNumber=1000000

HTTP/1.1

```



### POST Request



```

POST /srv.asmx/RemoveTagFromDocument HTTP/1.1

Content-Type: application/x-www-form-urlencoded



authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&path=/Finance/Reports/Q1-2024-Report.pdf

&tagText=Approved

&tagDate=2024-06-15T14:30:00.123Z

&taggedBy=12

&versionNumber=1000000

```



### SOAP Request



```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:RemoveTagFromDocument>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>

      <tns:tagText>Approved</tns:tagText>

      <tns:tagDate>2024-06-15T14:30:00.123Z</tns:tagDate>

      <tns:taggedBy>12</tns:taggedBy>

      <tns:versionNumber>1000000</tns:versionNumber>

    </tns:RemoveTagFromDocument>

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

Removes one applied tag. All four identifying values have to match the row exactly - the text alone
does not identify it, since the same text can be applied more than once.

```javascript
const tags = await call('GetAppliedTags', {
  authenticationTicket: ticket, path: '/Finance/Invoices/inv-1001.pdf'
});
const applied = tags.querySelector('AppliedTag');

await call('RemoveTagFromDocument', {
  authenticationTicket: ticket,
  path: '/Finance/Invoices/inv-1001.pdf',
  tagText: applied.getAttribute('TagText'),
  tagDate: applied.getAttribute('TagDate'),           // exactly as it was read, to the millisecond
  taggedBy: applied.getAttribute('TaggedById'),
  versionNumber: applied.getAttribute('VersionNumber')
});
```

Get any one of the four wrong and nothing is removed: the answer is `4041` "tagged version not
found" rather than a complaint about which field was wrong. Reading the row first, as the sample
does, is the way to be sure.

## Notes



- **Exact Match Required**: The deletion targets the `APPLIEDTAGS` database table using an exact match on `DOCUMENTID + VERSIONNUMBER + TAGTEXT + TAGDATE + TAGGEDBYID` -" these five columns are the table's primary key. If any value differs by even one character, millisecond, or digit, no rows are deleted and the call reports not found. Always obtain the tag values programmatically rather than constructing them manually.

- **No-Match Is Reported**: If the specified tag record does not exist (e.g. it was already removed, or the values do not match), the API returns `success="false"` with a not-found error. A `success="true"` response therefore means a row was genuinely removed.

- **Date Precision Differs By Database**: `TAGDATE` is stored in a `DATETIME` column on SQL Server and MySQL and a `DATE` column on Oracle. SQL Server keeps milliseconds; MySQL and Oracle keep whole seconds. Passing back the value the server gave you always matches, on every database; constructing your own value may not.

- **tagDate UTC Conversion**: If `tagDate` is passed as a UTC value (with `Kind = Utc`), it is automatically converted to server local time before the database comparison. If passed as an unspecified or local time, it is used as-is.

- **versionNumber is Internal**: The `versionNumber` parameter uses the raw internal version number stored in the database -" e.g. `1000000` for Version 1, `2000000` for Version 2. This is also the value stored when `SetTagToDocument` applies a tag (it stores the document's current published version number).

- **Obtaining Tag Metadata**: To get the correct `tagDate`, `taggedBy`, and `versionNumber` values needed to remove a specific tag, retrieve the document's applied tags from the document properties (e.g. via `GetDocument` or `GetDocuments`).

- **Cannot Remove Tags on Shortcuts**: Tags cannot be applied to shortcut documents. If a tag was set via `SetTagToDocument` on a shortcut, this is also not possible.



---



## Related APIs



- [SetTagToDocument](SetTagToDocument.md) - Apply a tag to the latest version of a document

- [GetTagDefintions](GetTagDefintions.md) - Get the list of all configured tag definitions

- [GetDocument](GetDocument.md) - Get document properties including applied tags



---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path, or no applied tag matching all four values |
| `4030` | the caller may not change that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
