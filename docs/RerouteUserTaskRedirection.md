# RerouteUserTaskRedirection API

Changes the target user of an existing task redirection without modifying the start and end dates. Use this when a user's tasks are already being redirected and you want to point them to a different person.

To create a new redirection from scratch, use [SetUserTaskRedirection](SetUserTaskRedirection.md). To remove a redirection entirely, use [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md).

## Endpoint

```
/srv.asmx/RerouteUserTaskRedirection
```

## Methods

- **GET** `/srv.asmx/RerouteUserTaskRedirection?authenticationTicket=...&userName=...&redirectTasksToUser=...`
- **POST** `/srv.asmx/RerouteUserTaskRedirection` (form data)
- **SOAP** Action: `http://tempuri.org/RerouteUserTaskRedirection`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Login name of the user whose task redirection target should be changed. |
| `redirectTasksToUser` | string | Yes | Login name of the new user to redirect tasks to. |

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
- The **user themselves** (self-service -" rerouting their own redirection), or
- A **User Manager**, or
- A **Library Manager**.

Anonymous access is not permitted.

## Preconditions

The user specified by `userName` must **already have an active task redirection** configured. If no redirection exists, the call returns an error. Use [SetUserTaskRedirection](SetUserTaskRedirection.md) to create a new redirection.

## What Happens on Success

The existing task redirection for `userName` is updated so that tasks are forwarded to `redirectTasksToUser` instead of the previous target. The start date and end date from the existing redirection are preserved (the start date may be adjusted to the current time if the original start date is already in the past).

## Example

### GET Request

```
GET /srv.asmx/RerouteUserTaskRedirection
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &userName=john.smith
    &redirectTasksToUser=alice.jones
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/RerouteUserTaskRedirection HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&userName=john.smith&redirectTasksToUser=alice.jones
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

Points an existing redirection at a different user, keeping its dates.

```javascript
await call('RerouteUserTaskRedirection', {
  authenticationTicket: ticket,
  userName: 'jsmith',
  redirectTasksToUser: 'bpatel'
});
```

Calling it for a user who has nothing redirected answers `success="false"` `errorCode="4000"` with
an **empty** `error`, so check `GetUserTaskRedirectionTo` first if you need to tell the two apart.

## Notes

- This API only changes the redirection **target**. The date window is inherited from the existing record.
- If you need to change both the target and the date window, remove the existing redirection with [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md) and create a new one with [SetUserTaskRedirection](SetUserTaskRedirection.md).
- To verify the updated redirection, use [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md).

## Related APIs

- [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md) -" Get the current redirection target for a user.
- [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) -" Get all users who are redirecting their tasks to a specified user.
- [SetUserTaskRedirection](SetUserTaskRedirection.md) -" Set or update a task redirection with a specific date window.
- [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md) -" Remove a user's task redirection.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | `userName` or `redirectTasksToUser` is not a user |
| `4000` | the two names are the same, or that user has no redirection - the latter with no message |
| `4030` | there is no ticket at all |
