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
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Access Denied" />
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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| User not found | The specified `userName` or `redirectTasksToUser` does not exist. |
| Access Denied | Calling user is not the target user, a User Manager, or a Library Manager. |
| No existing redirection | The user does not have a task redirection configured. Use SetUserTaskRedirection to create one. |
