# GetUserTaskRedirectionsFrom API

Returns the list of users who are currently redirecting their tasks **to** the specified user. Each entry represents a different user whose tasks will be forwarded to the named user during the configured date range.

This is the reverse view of [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md).

## Endpoint

```
/srv.asmx/GetUserTaskRedirectionsFrom
```

## Methods

- **GET** `/srv.asmx/GetUserTaskRedirectionsFrom?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetUserTaskRedirectionsFrom` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserTaskRedirectionsFrom`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Login name of the user who is receiving redirected tasks. |

## Response

### Success Response

```xml
<root success="true">
  <TaskRedirections>
    <TaskRedirection>
      <UserId>7</UserId>
      <UserName>john.smith</UserName>
      <FullName>John Smith</FullName>
      <Email>john.smith@example.com</Email>
      <StartDate>2024-03-01</StartDate>
      <EndDate>2024-03-31</EndDate>
    </TaskRedirection>
    <TaskRedirection>
      <UserId>9</UserId>
      <UserName>bob.jones</UserName>
      <FullName>Bob Jones</FullName>
      <Email>bob.jones@example.com</Email>
      <StartDate>2024-03-10</StartDate>
      <EndDate></EndDate>
    </TaskRedirection>
  </TaskRedirections>
</root>
```

### Success Response — no inbound redirections

```xml
<root success="true">
  <TaskRedirections />
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## Response Field Reference

The `<TaskRedirections>` element contains zero or more `<TaskRedirection>` entries. Each entry describes the **source** user (the person whose tasks are being redirected *from*):

| Element | Description |
|---------|-------------|
| `UserId` | Numeric user ID of the source user (the one redirecting tasks away). |
| `UserName` | Login name of the source user. |
| `FullName` | Full display name of the source user. |
| `Email` | Email address of the source user. |
| `StartDate` | Date from which the redirection is active. Empty string if open-ended. |
| `EndDate` | Date on which the redirection expires. Empty string if open-ended. |

## Required Permissions

Any authenticated user may call this API.

## Example

### GET Request

```
GET /srv.asmx/GetUserTaskRedirectionsFrom
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &userName=alice.jones
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetUserTaskRedirectionsFrom HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&userName=alice.jones
```

## Notes

- Each entry represents a user who has configured `userName` as their redirection target.
- The entries are stored redirection records and may include redirections whose date window has already expired or not yet started.
- To see where a user's own tasks are being redirected *to*, use [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md).
- To configure a redirection, use [SetUserTaskRedirection](SetUserTaskRedirection.md).
- To remove a redirection, use [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md).

## Related APIs

- [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md) – Get the user that a given user's tasks are being forwarded to.
- [SetUserTaskRedirection](SetUserTaskRedirection.md) – Set or update a task redirection for a user.
- [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md) – Remove a user's task redirection.
- [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md) – Change the target of an existing task redirection.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| User not found | The specified `userName` does not exist. |
