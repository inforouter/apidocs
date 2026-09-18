# RemoveUsergroupFromDocumentSubscribers API

Removes a specified user group from the subscription list of a document. After removal, members of that group will no longer receive email notifications via the group subscription for any events on that document. Use this API to clean up group subscriptions when a group no longer needs to track a document.

> **These two do not remove a group subscription.** `FolderServices.RemoveSubscriberAsync`
> resolves the group's id and then unsubscribes a *user* with it. The document form finds no such
> user, changes nothing, and answers `success="true"`; the folder form answers "user not found"
> about a group that exists. Either way the group stays subscribed, and there is no way through
> the API to remove it.

## Endpoint

```

/srv.asmx/RemoveUsergroupFromDocumentSubscribers

```

## Methods

- **GET** `/srv.asmx/RemoveUsergroupFromDocumentSubscribers?authenticationTicket=...&documentPath=...&groupName=...`

- **POST** `/srv.asmx/RemoveUsergroupFromDocumentSubscribers` (form data)

- **SOAP** Action: `http://tempuri.org/RemoveUsergroupFromDocumentSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`). Supports short document ID paths (`~D{id}` or `~D{id}.ext`). |
| `groupName` | string | Yes | Name of the user group. Must be a **global** group. A group that belongs to a library is never found - the lookup is done with no library name - and the call is refused as though no such group existed. Removing it does not work in any case - see the warning at the top of this page. |

---

## Response

### Success Response

```xml

<response success="true" error="" />

```

### Error Response

```xml

<response success="false" error="User group not found." />

```

---

## Required Permissions

The calling user must be authenticated. To remove a user group from the subscription list, the calling user must have **write access** or **manage access** to the document.

---

## Example

### GET Request

```

GET /srv.asmx/RemoveUsergroupFromDocumentSubscribers

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &documentPath=/Finance/Reports/Q1-2024-Report.pdf

  &groupName=Finance-Managers

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/RemoveUsergroupFromDocumentSubscribers HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&documentPath=/Finance/Reports/Q1-2024-Report.pdf

&groupName=Finance-Managers

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:RemoveUsergroupFromDocumentSubscribers>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:DocumentPath>/Finance/Reports/Q1-2024-Report.pdf</tns:DocumentPath>

      <tns:groupName>Finance-Managers</tns:groupName>

    </tns:RemoveUsergroupFromDocumentSubscribers>

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

Intended to unsubscribe a group from a document. It does not - see the warning above.

```javascript
// Reports success and leaves the group subscribed. Read GetSubscribers afterwards rather than
// trusting the answer.
await call('RemoveUsergroupFromDocumentSubscribers', {
  authenticationTicket: ticket,
  DocumentPath: '/Public/Reports/q3.pdf',
  groupName: 'Auditors',
});
```

## Notes

- **Not Subscribed**: If the specified group is not currently subscribed to the document, the API returns `success="true"` -" it does not treat this as an error.

- **Group Must Exist**: The `groupName` must match an existing infoRouter user group. If the group is not found, an error is returned.

- **Individual User Subscriptions Unaffected**: This API only removes the group-level subscription. Individual users who happen to be members of this group and have their own personal subscriptions will continue to receive notifications. Use `RemoveUserFromDocumentSubscribers` to remove individual user subscriptions.

- **Short Path Support**: The `documentPath` parameter supports short document ID notation: `~D123` or `~D123.pdf`.

- **Folder Group Subscriptions**: This API operates on document subscriptions only. To remove a group from a folder subscription, use `RemoveUsergroupFromFolderSubscribers`.

---

## Related APIs

- [AddUsergroupToDocumentSubscribers](AddUsergroupToDocumentSubscribers.md) - Add a user group to a document's subscription list

- [RemoveUserFromDocumentSubscribers](RemoveUserFromDocumentSubscribers.md) - Remove an individual user from a document's subscription list

- [RemoveUsergroupFromFolderSubscribers](RemoveUsergroupFromFolderSubscribers.md) - Remove a user group from a folder's subscription list

- [GetSubscribers](GetSubscribers.md) - Get the full subscriber list of a document or folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path, including one the caller may not see |
| `4041` | no global user group by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
