# GetMyDocumentsAndFolders API

Returns all documents and folders owned by the currently authenticated user, across all locations in the infoRouter system. Optional flags control the level of detail included for each item.

## Endpoint

```
/srv.asmx/GetMyDocumentsAndFolders
```

## Methods

- **GET** `/srv.asmx/GetMyDocumentsAndFolders?authenticationTicket=...&withrules=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetMyDocumentsAndFolders` (form data)
- **SOAP** Action: `http://tempuri.org/GetMyDocumentsAndFolders`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `withrules` | bool | Yes | If `true`, includes folder rules (allowed file types, checkout/checkin policies, etc.) for each returned folder. |
| `withpropertysets` | bool | Yes | If `true`, includes applied custom property set values for each item. |
| `withsecurity` | bool | Yes | If `true`, includes the access control list (ACL) for each item. |
| `withOwner` | bool | Yes | If `true`, includes owner user information for each item. |
| `withVersions` | bool | Yes | If `true`, includes full version history for each returned document. |

---

## Response

### Success Response

```xml
<response success="true">
  <folder id="456" name="My Project" description="Project files" parentid="100"
          createdate="2023-01-15T09:00:00" modifydate="2024-03-20T14:30:00">
    <!-- Included only when withrules=true -->
    <Rules>...</Rules>
    <!-- Included only when withpropertysets=true -->
    <propertysets>...</propertysets>
    <!-- Included only when withsecurity=true -->
    <security>...</security>
  </folder>
  <document id="1001" name="Proposal.docx" versionid="1000045"
            createdate="2023-06-01T10:00:00" modifydate="2024-01-10T08:00:00">
    <!-- Included only when withVersions=true -->
    <versions>
      <version id="1000045" number="1" createdate="2023-06-01T10:00:00" />
    </versions>
    <!-- Included only when withpropertysets=true -->
    <propertysets>...</propertysets>
  </document>
</response>
```

Documents come back as the full `<document>` element. Since 9.0 it also carries `AIEnhanced` and
`AIExtractConfidence`. The first says which of the document's attributes infoRouter Connect
produced, as a set of bits - `0` when none did; the second how sure it was about the weakest value
it put in a property set, as a percentage. See [AIEnhanced](GetDocument.md#aienhanced) and
[AIExtractConfidence](GetDocument.md#aiextractconfidence).

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

The calling user must be authenticated. Only items owned by the current user are returned -" no special permissions are required beyond being logged in.

---

## Example

### GET Request (items only, no extra details)

```
GET /srv.asmx/GetMyDocumentsAndFolders
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withrules=false
  &withpropertysets=false
  &withsecurity=false
  &withOwner=false
  &withVersions=false
HTTP/1.1
```

### GET Request (with version history and property sets)

```
GET /srv.asmx/GetMyDocumentsAndFolders
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withrules=false
  &withpropertysets=true
  &withsecurity=false
  &withOwner=false
  &withVersions=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetMyDocumentsAndFolders HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&withrules=false
&withpropertysets=false
&withsecurity=false
&withOwner=false
&withVersions=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetMyDocumentsAndFolders>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:withrules>false</tns:withrules>
      <tns:withpropertysets>false</tns:withpropertysets>
      <tns:withsecurity>false</tns:withsecurity>
      <tns:withOwner>false</tns:withOwner>
      <tns:withVersions>false</tns:withVersions>
    </tns:GetMyDocumentsAndFolders>
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

Lists what the calling user owns, in the same full `<folder>` and `<document>` shape as
`GetFoldersAndDocuments` and with the same five flags. There is no `Path`: the answer is about who
the caller is, not where they are looking.

```javascript
const root = await call('GetMyDocumentsAndFolders', {
  authenticationTicket: ticket,
  withrules: false,
  withpropertysets: false,
  withsecurity: false,
  withOwner: false,
  withVersions: false
});

console.log(root.querySelectorAll(':scope > document').length, 'documents owned');
```

A caller with no ticket at all is the anonymous user, and the anonymous user owns nothing, so this is
one of the operations that refuses an unticketed call outright rather than answering for anonymous.

## Notes

- Returns items across all locations in infoRouter where the authenticated user is the owner.
- "Ownership" is determined by the document/folder owner field, not merely by having access.
- Setting all flags to `false` gives the fastest response (metadata only).
- Setting `withVersions=true` on large document sets may significantly increase response size and processing time.
- For a user's favorite items, use `GetFavorites`. For checked-out documents, use `GetCheckedoutDocuments`.
- Each `<document>` element includes a `UserViewStatus` integer attribute: `0` = never viewed, `1` = viewed but the published version has since changed, `2` = viewed the current published version. See `GetDocument` for the full attribute reference.

---

## Related APIs

- [GetFavorites](GetFavorites.md) - Get the current user's favorite items
- [GetCheckedoutDocuments](GetCheckedoutDocuments.md) - Get documents checked out by the current user
- [GetRecentDocuments](GetRecentDocuments.md) - Get recently accessed documents

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - unlike the folder listings, this operation does not answer for the anonymous user |


| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---