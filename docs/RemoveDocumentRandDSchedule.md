# RemoveDocumentRandDSchedule API

Removes (unassigns) the Retention and Disposition (R&D) schedule from a document identified by path. After this call the document has no R&D schedule.

## Endpoint

```
/srv.asmx/RemoveDocumentRandDSchedule
```

## Methods

- **GET** `/srv.asmx/RemoveDocumentRandDSchedule?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/RemoveDocumentRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveDocumentRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1.pdf`). |

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
GET /srv.asmx/RemoveDocumentRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Finance/Reports/Q1-2024.pdf
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/RemoveDocumentRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Finance/Reports/Q1-2024.pdf
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

Takes the schedule off a document. It is `SetDocumentRandDSchedule` with `RDDefId="0"`, and it is
safe to repeat - a document that has no schedule is a success.

```javascript
await call('RemoveDocumentRandDSchedule', {
  authenticationTicket: ticket,
  Path: '/Finance/Invoices/inv-1001.pdf'
});
```

## Notes

- If the document has no schedule assigned, the call succeeds without error (no-op).
- Removing a schedule clears the computed retention and disposition dates from the document.
- This operation is required before deleting the schedule definition via [DeleteRandDSchedule](DeleteRandDSchedule.md) if the schedule is assigned to documents.
- To assign a schedule, use [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md).
- To remove a schedule from a folder hierarchy, use [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md).

## Related APIs

- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) -" Assign an R&D schedule to a document.
- [GetDocumentRandDSchedule](GetDocumentRandDSchedule.md) -" Get the R&D schedule currently assigned to a document.
- [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md) -" Remove the R&D schedule from a folder hierarchy.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete an R&D schedule definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path |
| `4030` | the caller may not change that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
