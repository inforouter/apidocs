# DeleteDocument API

Moves a document to the recycle bin. The document is not permanently removed -" it can be restored using `RestoreRecycleBinItem` or permanently purged using `PurgeRecycleBinItem`.

## Endpoint

```

/srv.asmx/DeleteDocument

```

## Methods

- **GET** `/srv.asmx/DeleteDocument?authenticationTicket=...&Path=...`

- **POST** `/srv.asmx/DeleteDocument` (form data)

- **SOAP** Action: `http://tempuri.org/DeleteDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path of the document to delete (e.g. `/MyLibrary/Reports/OldReport.pdf`). |

## Response

### Success Response

```xml

<root success="true" />

```

### Error Response

```xml

<root success="false" error="Error message" />

```

---

## Required Permissions

The authenticated user must be the **document owner**, a **domain manager** of the containing library, or have **Delete** permission on the document or its parent folder.

---

## Example

### GET Request

```

GET /srv.asmx/DeleteDocument

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/MyLibrary/Reports/OldReport.pdf

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/DeleteDocument HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/MyLibrary/Reports/OldReport.pdf

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:DeleteDocument>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:Path>/MyLibrary/Reports/OldReport.pdf</tns:Path>

    </tns:DeleteDocument>

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

Deletes a document. Deleting one that is already gone is a `4041` failure, so a delete that runs twice
reports the second attempt rather than passing silently.

```javascript
await call('DeleteDocument', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf'
});
```

It will not take a folder: a folder path is answered `4041`, "document not found". Use
[DeleteFolder](DeleteFolder.md) for those.

A caller with no ticket is refused, but the message is `4041` "User not found" rather than the `4010`
the other writes use - the same wording as [DeleteFolder](DeleteFolder.md). Do not read that `4041` as
a missing document.

## Notes

- This API moves the document to the **recycle bin**. The document is not permanently deleted and its content and metadata remain intact until explicitly purged.

- To restore a deleted document, use `RestoreRecycleBinItem`.

- To permanently remove a document from the recycle bin, use `PurgeRecycleBinItem`.

- To empty the entire recycle bin at once, use `EmptyRecycleBin`.

- A document that is currently **checked out** may still be deleted; the checkout state is cleared when it is moved to the recycle bin.

- Deleting a document shortcut (`.lnk` file) removes only the shortcut -" the original target document is unaffected.

---

## Related APIs

- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a document from the recycle bin

- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a document from the recycle bin

- [EmptyRecycleBin](EmptyRecycleBin.md) - Permanently delete all items in the current user's recycle bin

- [GetRecycleBinContent](GetRecycleBinContent.md) - List documents currently in the recycle bin

- [DeleteFolder](DeleteFolder.md) - Move a folder to the recycle bin

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is refused |
| `4041` | no document at that path - including a folder path, one the caller may not see, and a call with no ticket at all, which is worded "User not found" |
| `4030` | the caller may not delete here, or folder rules disallow document deletes |
| `4230` | the document is checked out or locked |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found` | The `Path` does not refer to an existing document. |

---

