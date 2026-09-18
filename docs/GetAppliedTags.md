# GetAppliedTags API

Returns all tags applied to a document. Each tag entry includes the tag text, the date it was applied, the user who applied it, the document version it belongs to, and workflow context when the tag was applied via a workflow step.

## Endpoint

```
/srv.asmx/GetAppliedTags
```

## Methods

- **GET** `/srv.asmx/GetAppliedTags?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/GetAppliedTags` (form data)
- **SOAP** Action: `http://tempuri.org/GetAppliedTags`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/MyLibrary/Reports/Report.pdf`). |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing an `<AppliedTags>` element with zero or more `<AppliedTag>` child elements. Results are ordered by `TagDate` ascending.

```xml
<response success="true" error="">
  <AppliedTags>
    <AppliedTag
      TagText="Approved"
      TagDate="2024-01-15T10:30:00Z"
      VersionNumber="2"
      VersionNumberMultiPart="2.0"
      TaggedById="42"
      TaggedByName="John Doe"
      WorkFlowId="7"
      WorkFlowName="Document Approval"
      WorkFlowStepNumber="3" />
    <AppliedTag
      TagText="Final"
      TagDate="2024-02-01T09:00:00Z"
      VersionNumber="3"
      VersionNumberMultiPart="3.0"
      TaggedById="15"
      TaggedByName="Jane Smith"
      WorkFlowId="0"
      WorkFlowName=""
      WorkFlowStepNumber="0" />
  </AppliedTags>
</response>
```

### No Tags Applied Response

When no tags have been applied to the document:

```xml
<response success="true" error="">
  <AppliedTags />
</response>
```

### Error Response

```xml
<response success="false" error="[900] Authentication failed." />
```

---

## Response Attributes

Each `<AppliedTag>` element carries the following attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `TagText` | string | The tag label text, exactly as defined in the tag definitions. |
| `TagDate` | datetime | UTC date and time when the tag was applied. |
| `VersionNumber` | integer | The version number of the document to which the tag was applied. |
| `VersionNumberMultiPart` | string | Human-readable version number (e.g. `2.0`). |
| `TaggedById` | integer | User ID of the user who applied the tag. |
| `TaggedByName` | string | Full name of the user who applied the tag. |
| `WorkFlowId` | integer | ID of the workflow that applied the tag, or `0` if applied manually. |
| `WorkFlowName` | string | Name of the workflow that applied the tag, or empty string if applied manually. |
| `WorkFlowStepNumber` | integer | Step number within the workflow that applied the tag, or `0` if applied manually. |

---

## Required Permissions

The caller must be authenticated and must have **view (read) access** to the document. If the document does not exist or the caller lacks access, the API returns `success="false"`.

---

## Example

### GET Request

```
GET /srv.asmx/GetAppliedTags
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/TestDomain/TestFolder/report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAppliedTags HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&path=/TestDomain/TestFolder/report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAppliedTags>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/TestDomain/TestFolder/report.pdf</tns:path>
    </tns:GetAppliedTags>
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

Lists the tags on a document, with who applied each one, when, and to which version.

```javascript
const root = await call('GetAppliedTags', {
  authenticationTicket: ticket, path: '/Finance/Invoices/inv-1001.pdf'
});

for (const applied of root.querySelectorAll('AppliedTag')) {
  console.log(applied.getAttribute('TagText'),
              applied.getAttribute('VersionNumberMultiPart'),   // "1.0.0"
              applied.getAttribute('TaggedByName'),
              applied.getAttribute('TagDate'));
}
```

The four attributes `TagText`, `TagDate`, `TaggedById` and `VersionNumber` are what
[RemoveTagFromDocument](RemoveTagFromDocument.md) takes, so a row read here can be handed straight
back to it.

`WorkFlowId`, `WorkFlowName` and `WorkFlowStepNumber` name the workflow step that applied the tag; a
tag applied by hand carries zeroes and an empty name.

## Notes

- Tags are returned across **all versions** of the document, ordered by `TagDate` ascending.
- `TagText` is case-sensitive and must match values returned by `GetTagDefinitions` exactly when used in calls to `SetTagToDocument` or `RemoveTagFromDocument`.
- When `WorkFlowId` is `0`, the tag was applied manually via `SetTagToDocument`.
- Use `VersionNumber` or `VersionNumberMultiPart` to determine which document version carries each tag.

---

## Related APIs

- [GetTagDefinitions](GetTagDefinitions.md) - Get the list of configured tag definition labels
- [SetTagToDocument](SetTagToDocument.md) - Apply a tag to the latest version of a document
- [RemoveTagFromDocument](RemoveTagFromDocument.md) - Remove a specific tag from a document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path |
| `4030` | the caller may not see that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
