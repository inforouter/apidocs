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
| `endOn` | DateTime | Yes | End date of the redirection window. Must be a future date and must be greater than `startOn`. Recommended format: `yyyy-MM-ddTHH:mm:ss`. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Task redirection end date cannot be in the past." />
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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| User not found | The specified `userName` or `redirectTasksToUser` does not exist. |
| Access Denied | Calling user is not the target user, a User Manager, or a Library Manager. |
| End date in the past | `endOn` is before the current date and time. |
| Invalid date range | `endOn` is not after `startOn`. |
| Self-redirect | `redirectTasksToUser` is the same as `userName`. |
| Target user disabled | The specified `redirectTasksToUser` account is disabled. |
| Overlapping period | The date window overlaps with an existing inbound redirection to `userName`. |
| Target already redirecting | The `redirectTasksToUser` user has their own active redirection during the specified period. |
