# Move API

Moves a document or folder from the source path to the destination path. Both documents and folders can be moved in a single call. The destination path must specify the target location including the new name.

## Endpoint

```
/srv.asmx/Move
```

## Methods

- **GET** `/srv.asmx/Move?authenticationTicket=...&SourcePath=...&DestinationPath=...`
- **POST** `/srv.asmx/Move` (form data)
- **SOAP** Action: `http://tempuri.org/Move`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `SourcePath` | string | Yes | Full infoRouter path to the document or folder to move (e.g. `/Finance/Reports/Q1.pdf`). |
| `DestinationPath` | string | Yes | The full path the item should have afterwards, **including its name** - e.g. `/Finance/Archive/Q1.pdf`, not `/Finance/Archive`. Its parent folder must already exist. See the warning below about what the last segment is and is not used for. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Access denied." />
```

---

## Required Permissions

The calling user must have:
- **Read** permission on the source item.
- **Delete** permission on the source item (to remove it from the source location).
- **Write** permission on the destination folder (to place the item there).

---

## Example

### GET Request (move a document)

```
GET /srv.asmx/Move
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &SourcePath=/Finance/Reports/Q1-2024.pdf
  &DestinationPath=/Finance/Archive/Q1-2024.pdf
HTTP/1.1
```

### GET Request (move a folder)

```
GET /srv.asmx/Move
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &SourcePath=/Finance/Reports
  &DestinationPath=/Finance/Archive/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/Move HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&SourcePath=/Finance/Reports/Q1-2024.pdf
&DestinationPath=/Finance/Archive/Q1-2024.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:Move>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:SourcePath>/Finance/Reports/Q1-2024.pdf</tns:SourcePath>
      <tns:DestinationPath>/Finance/Archive/Q1-2024.pdf</tns:DestinationPath>
    </tns:Move>
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

Moves a folder or a document. The same call does both: the source path is looked up as a document
first and as a folder second.

**`DestinationPath` is the full new path of the item, not the folder to put it in.** Moving
`/Finance/Q1.pdf` into `/Finance/Archive` means `DestinationPath=/Finance/Archive/Q1.pdf`. Passing
`/Finance/Archive` asks for something else entirely - move `Q1.pdf` so that it *becomes* `Archive` -
and is answered `4090` when a folder of that name is already there.

```javascript
// into another folder: repeat the name at the end
await call('Move', {
  authenticationTicket: ticket,
  SourcePath: '/Finance/Reports/Q1.pdf',
  DestinationPath: '/Finance/Archive/Q1.pdf'
});

// rename in place: same parent, different last segment
await call('Move', {
  authenticationTicket: ticket,
  SourcePath: '/Finance/Reports',
  DestinationPath: '/Finance/Quarterly Reports'
});
```

A folder moves with everything under it. When the parent is unchanged the call is a rename, and asking
for the path it already has is answered `4000`, "source and target folder are the same". A library
cannot be moved: its parent is the root, and that is `4000`.

**Always repeat the source's own name at the end when the parent changes.** The last segment is used
for the duplicate-name check and then discarded - the item is moved under the name it already had. So
a mismatched last segment does not rename anything, and if the source's own name is already taken at
the destination the check passes on the name you wrote while the move collides on the name it used.
That collision reaches the unique index on the folder table and comes back as `5000` carrying raw SQL,
where it should have been a `4090`. Nothing is moved when that happens.

## Notes

- The destination folder must already exist before calling this API.
- The item name at the destination is determined by the last component of `DestinationPath`. You can effectively rename an item during the move by using a different name in the destination path.
- Moving a folder moves all its contents (subfolders and documents) as well.
- Checked-out documents within the folder may prevent the move operation.
- This API works for both documents and folders in a single call.

---

## Related APIs

- [Copy](Copy.md) - Copy a document or folder to a new location
- [CreateFolder](CreateFolder.md) - Create a target folder before moving
- [DeleteFolder](DeleteFolder.md) - Delete a folder
- [DeleteDocument](DeleteDocument.md) - Delete a document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is told "Anonymous users cannot perform this action" |
| `4041` | nothing at `SourcePath`, or no folder at the parent of `DestinationPath` |
| `4090` | something of that name is already at the destination |
| `4000` | `DestinationPath` is where the item already is, or `SourcePath` is a library |
| `4030` | the caller may not take the item out of where it is, or put it where it is going |
| `4090` | an item of that name is already at the destination |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Source not found | The source path does not resolve to an existing document or folder. |
| Destination folder not found | The destination folder does not exist. |
| Access denied | The user does not have the required permissions. |
| `SystemError:...` | An unexpected server-side error occurred. |

---