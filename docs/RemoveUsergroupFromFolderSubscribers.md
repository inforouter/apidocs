# RemoveUsergroupFromFolderSubscribers API

Removes the specified user group from the subscription list of a folder. After removal, members of that group will no longer receive email notifications via the group subscription for any events on that folder. Optionally removes the group from all sub-folders and documents within the folder as well.

> **These two do not remove a group subscription.** `FolderServices.RemoveSubscriberAsync`
> resolves the group's id and then unsubscribes a *user* with it. The document form finds no such
> user, changes nothing, and answers `success="true"`; the folder form answers "user not found"
> about a group that exists. Either way the group stays subscribed, and there is no way through
> the API to remove it.

## Endpoint

```

/srv.asmx/RemoveUsergroupFromFolderSubscribers

```

## Methods

- **GET** `/srv.asmx/RemoveUsergroupFromFolderSubscribers?AuthenticationTicket=...&FolderPath=...&groupName=...&IncludeSubObjects=...`

- **POST** `/srv.asmx/RemoveUsergroupFromFolderSubscribers` (form data)

- **SOAP** Action: `http://tempuri.org/RemoveUsergroupFromFolderSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). The folder must already exist. |
| `groupName` | string | Yes | Name of the user group. Must be a **global** group. A group that belongs to a library is never found - the lookup is done with no library name - and the call is refused as though no such group existed. Removing it does not work in any case - see the warning at the top of this page. |
| `IncludeSubObjects` | bool | Yes | When `true`, also removes the group subscription from all sub-folders and documents nested within the specified folder. When `false`, only the subscription on the specified folder itself is removed. |

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

The calling user must be authenticated. To remove a user group from a folder's subscription list, the calling user must have **write access** or **manage access** to the folder.

---

## Example

### GET Request

```

GET /srv.asmx/RemoveUsergroupFromFolderSubscribers

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &FolderPath=/Finance/Reports

  &groupName=Finance-Managers

  &IncludeSubObjects=true

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/RemoveUsergroupFromFolderSubscribers HTTP/1.1

Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&FolderPath=/Finance/Reports

&groupName=Finance-Managers

&IncludeSubObjects=true

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:RemoveUsergroupFromFolderSubscribers>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:FolderPath>/Finance/Reports</tns:FolderPath>

      <tns:groupName>Finance-Managers</tns:groupName>

      <tns:IncludeSubObjects>true</tns:IncludeSubObjects>

    </tns:RemoveUsergroupFromFolderSubscribers>

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

Intended to unsubscribe a group from a folder. It does not - see the warning above.

```javascript
// Answers "user not found" about the group, and leaves the subscription in place.
await call('RemoveUsergroupFromFolderSubscribers', {
  authenticationTicket: ticket,
  FolderPath: '/Public/Reports',
  groupName: 'Auditors',
  IncludeSubObjects: true,
});
```

## Notes

- **Not subscribed**: the call fails whether the group is subscribed or not, because the group's id is handed to the unsubscribe as a user id and no user has it.

- **Group Must Exist**: The `groupName` must match an existing infoRouter user group (local or global). If the group is not found, an error is returned.

- **IncludeSubObjects**: intended to apply the removal to every sub-folder and document. Nothing is removed at any level, so the flag makes no difference today.

- **Individual User Subscriptions Unaffected**: This API only removes the group-level subscription. Individual users who are members of the group and have their own personal subscriptions will continue to receive notifications. Use `RemoveUserFromFolderSubscribers` to remove individual user subscriptions.

- **Global groups only**, and even a global group is not removed. See the warning at the top of this page.

- **Document Group Subscriptions**: This API operates on folder subscriptions only. To remove a group from a document subscription, use `RemoveUsergroupFromDocumentSubscribers`.

---

## Related APIs

- [AddUsergroupToFolderSubscribers](AddUsergroupToFolderSubscribers.md) - Add a user group to a folder's subscription list

- [RemoveUserFromFolderSubscribers](RemoveUserFromFolderSubscribers.md) - Remove an individual user from a folder's subscription list

- [RemoveUsergroupFromDocumentSubscribers](RemoveUsergroupFromDocumentSubscribers.md) - Remove a user group from a document's subscription list

- [GetSubscribers](GetSubscribers.md) - Get the full subscriber list of a document or folder

- [GetSubscriptions](GetSubscriptions.md) - Get all subscriptions for the current user

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at that path, including one the caller may not see |
| `4041` | no global user group by that name, and also what a group that does exist is reported as |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
