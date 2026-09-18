# SetDocumentRandDSchedule API

Assigns a Retention and Disposition (R&D) schedule to a document identified by path. The schedule controls how long the document must be retained and what happens when the retention period expires.

## Endpoint

```
/srv.asmx/SetDocumentRandDSchedule
```

## Methods

- **GET** `/srv.asmx/SetDocumentRandDSchedule?authenticationTicket=...&Path=...&RDDefId=...`
- **POST** `/srv.asmx/SetDocumentRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/SetDocumentRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1.pdf`). |
| `RDDefId` | integer | Yes | ID of the R&D schedule definition to assign. Must be > 0. Use [GetRandDSchedules](GetRandDSchedules.md) to find valid IDs. |

## Response

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must have write access to the document.

## Example

### GET Request

```
GET /srv.asmx/SetDocumentRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Finance/Reports/Q1-2024.pdf
    &RDDefId=47
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetDocumentRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Finance/Reports/Q1-2024.pdf&RDDefId=47
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

Puts a schedule on a document, replacing whatever was there.

```javascript
await call('SetDocumentRandDSchedule', {
  authenticationTicket: ticket,
  Path: '/Finance/Invoices/inv-1001.pdf',
  RDDefId: 18706
});
```

`RDDefId="0"` takes the schedule off, which is exactly what
[RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) sends internally. Any other id that no
schedule has is refused `4041`.

The retention and disposition dates are computed from the schedule when it is applied. A schedule
triggered on create dates from the document's creation date; one triggered on cut off computes
nothing until the item has a cut-off date.

## Notes

- Assigning a schedule triggers the calculation of the document's retention end date and disposition date based on the schedule settings and the document's creation date or cutoff date.
- If the document already has a schedule assigned, it is replaced with the new one.
- To remove a schedule from a document without replacing it, use [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md).
- To assign a schedule to an entire folder hierarchy, use [SetFolderRandDSchedule](SetFolderRandDSchedule.md).

## Related APIs

- [GetDocumentRandDSchedule](GetDocumentRandDSchedule.md) -" Get the R&D schedule currently assigned to a document.
- [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) -" Remove the R&D schedule from a document.
- [SetFolderRandDSchedule](SetFolderRandDSchedule.md) -" Assign a schedule to a folder hierarchy.
- [GetRandDSchedules](GetRandDSchedules.md) -" List all R&D schedule definitions with their IDs.
- [CreateRandDSchedule](CreateRandDSchedule.md) -" Create a new R&D schedule definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path, or no schedule by that id |
| `4030` | the caller may not change that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
