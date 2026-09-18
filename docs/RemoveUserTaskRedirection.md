# RemoveUserTaskRedirection API

Removes the task redirection configured for the specified user. After this call, incoming tasks assigned to that user will no longer be automatically forwarded to another user.

If the user has no active task redirection, the call succeeds silently with no error.

## Endpoint

```
/srv.asmx/RemoveUserTaskRedirection
```

## Methods

- **GET** `/srv.asmx/RemoveUserTaskRedirection?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/RemoveUserTaskRedirection` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveUserTaskRedirection`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Login name of the user whose task redirection should be removed. |

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Access denied." errorCode="4030" />
```

## Required Permissions

The calling user must be one of:
- The **user themselves** (self-service -" removing their own redirection), or
- A **User Manager**, or
- A **Library Manager**.

Anonymous access is not permitted.

## Example

### GET Request

```
GET /srv.asmx/RemoveUserTaskRedirection
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &userName=john.smith
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/RemoveUserTaskRedirection HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&userName=john.smith
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

Cancels a user's redirection. Calling it when there is nothing to cancel is accepted, so it is safe
to run unconditionally.

```javascript
await call('RemoveUserTaskRedirection', { authenticationTicket: ticket, userName: 'jsmith' });
```

## Notes

- If the user currently has no task redirection configured, the call still returns `success="true"` (idempotent delete).
- Removing a redirection does not affect tasks that were already forwarded before the removal. Only future task assignments are affected.
- To view the current redirection for a user, use [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md).
- To set or update a redirection, use [SetUserTaskRedirection](SetUserTaskRedirection.md).
- To change the redirection target without removing and re-adding it, use [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md).

## Related APIs

- [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md) -" Get the user that a given user's tasks are being forwarded to.
- [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) -" Get the list of users redirecting tasks to a specified user.
- [SetUserTaskRedirection](SetUserTaskRedirection.md) -" Set or update a task redirection for a user.
- [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md) -" Change the target of an existing task redirection.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no user by that name |
| `4030` | there is no ticket at all |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
