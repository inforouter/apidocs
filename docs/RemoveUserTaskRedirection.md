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
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Access Denied" />
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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| User not found | The specified `userName` does not exist. |
| Access Denied | Calling user is not the target user, a User Manager, or a Library Manager. |
