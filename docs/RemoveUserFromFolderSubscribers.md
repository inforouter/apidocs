# RemoveUserFromFolderSubscribers API

Removes the specified user from the subscription list of a folder. Optionally removes the user from all sub-folders and documents within the folder.

## Endpoint

```
/srv.asmx/RemoveUserFromFolderSubscribers
```

## Methods

- **GET** `/srv.asmx/RemoveUserFromFolderSubscribers?AuthenticationTicket=...&FolderPath=...&UserName=...&IncludeSubObjects=...`
- **POST** `/srv.asmx/RemoveUserFromFolderSubscribers` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveUserFromFolderSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `FolderPath` | string | Yes | Full path of the folder (e.g., `/MyLibrary/Projects`) |
| `UserName` | string | Yes | Username of the user to remove from the subscription list |
| `IncludeSubObjects` | bool | Yes | When `true`, also removes the user from all sub-folders and documents within the folder. When `false`, only removes from the specified folder. |

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

The caller must have sufficient rights to modify the subscription list of the specified folder (typically requires the **AddRemoveSubscription** policy right on the domain).

## Example

### Request (GET)

```
GET /srv.asmx/RemoveUserFromFolderSubscribers?AuthenticationTicket=abc123-def456&FolderPath=/MyLibrary/Projects&UserName=jsmith&IncludeSubObjects=true HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/RemoveUserFromFolderSubscribers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&FolderPath=/MyLibrary/Projects&UserName=jsmith&IncludeSubObjects=true
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/RemoveUserFromFolderSubscribers"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RemoveUserFromFolderSubscribers xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <FolderPath>/MyLibrary/Projects</FolderPath>
      <UserName>jsmith</UserName>
      <IncludeSubObjects>true</IncludeSubObjects>
    </RemoveUserFromFolderSubscribers>
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

Unsubscribes one user from a folder, and optionally from everything inside it.

```javascript
await call('RemoveUserFromFolderSubscribers', {
  authenticationTicket: ticket,
  FolderPath: '/Public/Reports',
  UserName: 'jsmith',
  IncludeSubObjects: true,   // clears the whole tree, matching the add
});
```

## Notes

- The `FolderPath` must point to an existing folder; an error is returned if the path is not found
- The specified `UserName` must be a valid user in the system
- Setting `IncludeSubObjects` to `true` recursively removes the user from all nested folders and documents
- See also: `RemoveUserFromDocumentSubscribers` for removing a user from a single document's subscription list
- See also: `RemoveUsergroupFromFolderSubscribers` for removing a user group instead of an individual user

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at that path, including one the caller may not see |
| `4041` | no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
