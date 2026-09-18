# SetUserTaskRedirection API

Sets or replaces a task redirection for a user. During the configured date window, incoming tasks assigned to `userName` are automatically forwarded to `redirectTasksToUser` instead.

If the user already has a task redirection configured, it is atomically replaced by the new one.

## Endpoint

```
/srv.asmx/SetUserTaskRedirection
```

## Methods

- **GET** `/srv.asmx/SetUserTaskRedirection?authenticationTicket=...&userName=...&redirectTasksToUser=...&startOn=...&endOn=...`
- **POST** `/srv.asmx/SetUserTaskRedirection` (form data)
- **SOAP** Action: `http://tempuri.org/SetUserTaskRedirection`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Login name of the user whose tasks should be redirected. |
| `redirectTasksToUser` | string | Yes | Login name of the user to redirect tasks to. Cannot be the same as `userName`. |
| `startOn` | DateTime | Yes | Start date of the redirection window. If in the past, it is automatically adjusted to the current time. Recommended format: `yyyy-MM-ddTHH:mm:ss`. |
| `endOn` | DateTime | Yes | End date of the redirection window. Must be a future date and must be greater than `startOn`. Recommended format: `yyyy-MM-ddTHH:mm:ss`. Genuinely required: until 9.0 the REST action declared it optional while the operation insisted on it, so an empty value travelled all the way to a refusal. A redirection with no end cannot be expressed - use [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md) to end one. |

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Task redirection end date cannot be in the past." />
```

## Required Permissions

The calling user must be one of:
- The **user themselves** (self-service -" setting their own redirection), or
- A **User Manager**, or
- A **Library Manager**.

Anonymous access is not permitted.

## Validation Rules

| Rule | Description |
|------|-------------|
| `endOn` must be a future date | Returns an error if `endOn` is in the past. |
| `endOn` must be after `startOn` | Returns an error if `endOn` is not greater than `startOn`. |
| Cannot redirect to yourself | `redirectTasksToUser` cannot be the same user as `userName`. |
| Target user must be active | Returns an error if `redirectTasksToUser` is a disabled user. |
| No overlapping inbound redirections | The specified date window must not overlap with any redirection already pointing to `userName`. |
| Target not already redirecting | The `redirectTasksToUser` user must not already have an active redirection during the same period. |

## Example

### GET Request

```
GET /srv.asmx/SetUserTaskRedirection
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &userName=john.smith
    &redirectTasksToUser=alice.jones
    &startOn=2024-04-01T00:00:00
    &endOn=2024-04-30T23:59:59
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetUserTaskRedirection HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&userName=john.smith&redirectTasksToUser=alice.jones&startOn=2024-04-01T00%3A00%3A00&endOn=2024-04-30T23%3A59%3A59
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

Sends one user's new tasks to another for a period - a holiday cover. The two users have to be
different.

```javascript
await call('SetUserTaskRedirection', {
  authenticationTicket: ticket,
  userName: 'jsmith',
  redirectTasksToUser: 'ajones',
  startOn: '2026-07-01',
  endOn: '2026-07-31'
});
```

`endOn` is declared optional, but the operation insists on a date after `startOn`: a redirection
with no end is not something this API can express.

## Notes

- If the user already has a redirection configured, it is replaced (not stacked). There can only be one active redirection per user at a time.
- If `startOn` is in the past, the system silently adjusts it to the current time instead of returning an error.
- This API cannot create an open-ended (no end date) redirection. Both start and end dates are required.
- To only change the target user without changing dates, use [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md).
- To remove the redirection, use [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md).

## Related APIs

- [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md) -" Get the current redirection target for a user.
- [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) -" Get all users redirecting tasks to a specified user.
- [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md) -" Change the redirection target while keeping the existing dates.
- [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md) -" Remove a user's task redirection.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | `userName` or `redirectTasksToUser` is not a user |
| `4000` | the two names are the same, or `endOn` is empty or not after `startOn` |
| `4030` | there is no ticket at all |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
