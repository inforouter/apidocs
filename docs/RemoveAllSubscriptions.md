# RemoveAllSubscriptions API

Removes all folder and document subscriptions for the specified user. This is a bulk operation that clears all subscription entries at once.

## Endpoint

```
/srv.asmx/RemoveAllSubscriptions
```

## Methods

- **GET** `/srv.asmx/RemoveAllSubscriptions?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/RemoveAllSubscriptions` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveAllSubscriptions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | The username whose subscriptions to remove |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

Access is granted if any of the following conditions are met:
- The caller is the same user as the specified `userName`
- The caller is a system administrator
- The caller is a domain manager of the domain the specified user belongs to

If none of these conditions are met, an access denied error is returned.

## Example

### Request (GET)

```
GET /srv.asmx/RemoveAllSubscriptions?authenticationTicket=abc123-def456&userName=jsmith HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/RemoveAllSubscriptions HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/RemoveAllSubscriptions"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RemoveAllSubscriptions xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
    </RemoveAllSubscriptions>
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

Removes every subscription one user has, to documents and folders alike.

```javascript
await call('RemoveAllSubscriptions', { authenticationTicket: ticket, userName: 'jsmith' });
```

There is no undo and no report of what was removed. Read
[GetSubscribedDocumentsByUser](GetSubscribedDocumentsByUser.md) and
[GetSubscribedFoldersByUser](GetSubscribedFoldersByUser.md) first if the list is worth keeping.

## Notes

- This operation removes both document subscriptions and folder subscriptions for the user
- This action is irreversible; all subscriptions are permanently deleted
- See also: `RemoveUserFromFolderSubscribers` to remove a user from a single folder's subscription list
- See also: `RemoveUserFromDocumentSubscribers` to remove a user from a single document's subscription list
- See also: `GetSubscriptionsByUser` to retrieve the current subscriptions before removing them

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

On success this operation answers `<response success="true" error=""/>` with **no** `errorCode`
attribute at all, where most operations answer `errorCode="0"`. Branch on `success`.
