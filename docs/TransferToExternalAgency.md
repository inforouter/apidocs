# TransferToExternalAgency API

Records that a document or folder has been transferred to the external agency its Retention and Disposition (R&D) schedule names. The path type is auto-detected: a document path records the transfer of that one document; a folder path records the folder's own transfer and, when asked, walks the subfolders and documents below it.

## Why this operation exists

An R&D schedule can end in one of two ways: final disposition, or transfer to an external agency. For the first, [DisposeItem](DisposeItem.md) carries out the disposal. For the second, the system records that the transfer happened, and that record is what everything else waits on:

- **The daily disposition job creates a task for every document that falls due** under a transfer-type schedule with *CreateTask* on. The task carries the *Transfer* requirement and is assigned to an R&D Manager.
- **That task cannot be completed until the document's disposition status carries a transfer submission date.** `UpdateTaskStatus` refuses it with "This task cannot be completed. The document has not been transferred."
- **DisposeItem refuses such a document** with "The document's disposition type is 'transfer to external agency'", so it is not a way around.

Until version 9.0 nothing in the web service API could write that submission date; only the retired ASP.NET page could. Every Transfer task created by the job therefore stayed open for good, and the *Transfer to external agency* administrative action existed as a rule nobody could reach. This operation is the missing call: it writes the transfer record, which lets the task be completed and gives the role something to govern.

## Endpoint

```
/srv.asmx/TransferToExternalAgency
```

## Methods

- **GET** `/srv.asmx/TransferToExternalAgency?authenticationTicket=...&path=...&transferAgency=...&agencyNotes=...&dateTransferSubmitted=...&dateTransferApproved=...&includeSubFolders=...&includeDocuments=...`
- **POST** `/srv.asmx/TransferToExternalAgency` (form data)
- **SOAP** Action: `http://tempuri.org/TransferToExternalAgency`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `path` | string | Yes | Full path of the document or folder |
| `transferAgency` | string | No | Name of the receiving agency. Maximum 64 characters; a longer value is refused with `4000`. When omitted or empty, the agency name the schedule put on the disposition status is kept. |
| `agencyNotes` | string | No | Notes about the transfer. Maximum 255 characters; a longer value is refused with `4000`. An empty value clears the notes. |
| `dateTransferSubmitted` | DateTime | No | Date the transfer was submitted to the agency. Defaults to the current date and time. Recommended format: `yyyy-MM-ddTHH:mm:ss`. |
| `dateTransferApproved` | DateTime | No | Date the agency approved the transfer. Omit if not yet approved; it is stored as none. |
| `includeSubFolders` | bool | No | Folder paths only. `true` also walks the subfolders. Default `false`. |
| `includeDocuments` | bool | No | Folder paths only. `true` also records the transfer of the documents inside. Default `false`. |

## Response

### Success Response (document, or folder with no per-item errors)

```xml
<root success="true" />
```

### Multi-status Response (folder with per-item failures)

The folder form walks the tree and logs one entry per item it could not transfer. When there is at least one, the answer is `success="false"` with `errorCode="2070"`, and the log says what was refused. The other items were still transferred.

```xml
<root success="false" errorCode="2070" error="MultiStatus">
  <log><item>/Library/Records/2019/contract.pdf</item><error>Transfer cannot be completed. The document's retention schedule has been frozen.</error></log>
  <log><item>/Library/Records/2019</item><error>Transfer cannot be completed. The folder's disposition status has not yet been created.</error></log>
</root>
```

### Error Response

```xml
<root success="false" error="Error message" errorCode="4030" />
```

## Required Permissions

The caller must be in the Retention & Disposition Managers role, or be a system administrator. The role is asked first, before the path is looked up, so a caller without it learns nothing about what is at the path. The caller also needs the `RetentionPeriodChange` right on the item (the library policy right that also governs applying and freezing schedules).

## What the item must look like

The transfer is only recorded when all of the following hold. Each refusal is `4000` with the message shown; for a folder the message goes into the `<log>` instead.

| Condition | Document message | Folder message |
|---|---|---|
| The item carries an R&D schedule | The document has no retention schedule. | The folder's retention schedule is different. |
| The schedule is not frozen | The document's retention schedule has been frozen. | The folder's retention schedule has been frozen. |
| A disposition date has been calculated | The document's disposition date has not been calculated yet. | The folder's disposition date has not yet been calculated. |
| The disposition date has arrived | The document's disposition date is in the future. | The folder's disposition date is in the future. |
| The daily job has created the disposition status row | The document's disposition status has not yet been created. | The folder's disposition status has not yet been created. |
| The schedule's disposition type is *transfer to external agency* | The document's disposition type is not 'transfer to external agency'. | The folder's R&D schedule does not call for a "transfer to the external agency." |

Every message starts with "Transfer cannot be completed."

The disposition status row is written by the daily disposition job when the item's disposition date arrives, not by the schedule assignment. So a document whose date has just passed cannot be transferred until the job has run; once it has, the Transfer task exists and this call completes it.

## Folder walk

With `includeSubFolders` every subfolder is walked first, and with `includeDocuments` every document in each folder is transferred. A document is only transferred when it carries the same schedule as the folder the call was made on; a document under a different schedule is logged with "The document's retention schedule is different." and left alone. The folder itself is checked last, after its contents. Both flags default to `false`, so a bare folder call records the transfer of the folder only.

## Example

### Record the transfer of a document (GET)

```
GET /srv.asmx/TransferToExternalAgency?authenticationTicket=abc123-def456&path=/Library/Records/2019/contract.pdf&agencyNotes=Box+17 HTTP/1.1
```

### Record the transfer of a folder and its documents (POST)

```
POST /srv.asmx/TransferToExternalAgency HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&path=/Library/Records/2019&transferAgency=National+Archives&agencyNotes=Accession+2019-07&dateTransferSubmitted=2026-10-01T00:00:00&dateTransferApproved=2026-10-20T00:00:00&includeSubFolders=true&includeDocuments=true
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/TransferToExternalAgency"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <TransferToExternalAgency xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <path>/Library/Records/2019/contract.pdf</path>
      <transferAgency>National Archives</transferAgency>
      <agencyNotes>Accession 2019-07</agencyNotes>
      <dateTransferSubmitted>2026-10-01T00:00:00</dateTransferSubmitted>
      <includeSubFolders>false</includeSubFolders>
      <includeDocuments>false</includeDocuments>
    </TransferToExternalAgency>
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

Records the transfer and then completes the Transfer task the daily job created for the document.

```javascript
await call('TransferToExternalAgency', {
  authenticationTicket: ticket,
  path: '/Finance/Invoices/inv-1001.pdf',
  agencyNotes: 'Accession 2019-07'
});

// Transfer tasks are listed with GetTasks1; complete the one for this document.
await call('UpdateTaskStatus', {
  authenticationTicket: ticket,
  taskId: transferTaskId,
  taskStatus: 30,
  finishDate: '0001-01-01T00:00:00',
  comments: 'Transferred to the National Archives'
});
```

**The folder form answers MultiStatus when it could not do all of it.** With `errorCode="2070"` read the `<log>` entries: each names the item and why it was refused. Items not in the log were transferred.

## Notes

- Recording a transfer does not move, delete or hide the item. It writes the submission date, approval date, agency name and notes onto the item's disposition status, which is what the Transfer task reads.
- Calling it again on the same item overwrites the dates and notes. An empty `transferAgency` keeps the name already on record; an empty `agencyNotes` clears the notes.
- `dateTransferSubmitted` is never stored empty: it is the mark of a transfer, and a call without it records the current date and time.
- The folder itself gets a disposition status row from the daily job like a document does, but no task; only documents get Transfer tasks.

Who may change retention at all, and the role's reach: [Who may change retention and disposition](rules/retention-who-may.md).

## Related APIs

- [`DisposeItem`](DisposeItem.md) — Dispose a document or folder under a final-disposition schedule
- [`SetDocumentRandDSchedule`](SetDocumentRandDSchedule.md) — Assign an R&D schedule to a document
- [`SetFolderRandDSchedule`](SetFolderRandDSchedule.md) — Assign an R&D schedule to a folder
- [`UpdateTaskStatus`](UpdateTaskStatus.md) — Complete the Transfer task once the transfer is recorded
- [`RDManagersRole`](RDManagersRole.md) — What R&D Managers can and cannot do

## Error Codes

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller is not an R&D Manager or administrator (asked before the path), or lacks `RetentionPeriodChange` on the item |
| `4000` | `transferAgency` is longer than 64 or `agencyNotes` longer than 255 characters, or the item fails one of the conditions above |
| `4041` | no document and no folder at that path |
| `2070` | the folder form refused at least one item; read the `<log>` entries |
| `HTTP 400` | `path` was empty; refused by model binding, so there is no error document |
