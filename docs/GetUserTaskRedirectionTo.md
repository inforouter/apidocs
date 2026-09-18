# GetUserTaskRedirectionTo API

Returns the task redirection that is currently configured for a user -" i.e., the user to whom all new tasks assigned to the specified user are being forwarded.

If no redirection is active, the response contains no `<TaskRedirection>` element.

## Endpoint

```
/srv.asmx/GetUserTaskRedirectionTo
```

## Methods

- **GET** `/srv.asmx/GetUserTaskRedirectionTo?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetUserTaskRedirectionTo` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserTaskRedirectionTo`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Login name of the user whose redirection to retrieve. |

## Response

### Success Response -" redirection active

```xml
<response success="true">
  <TaskRedirection>
    <UserId>15</UserId>
    <UserName>alice.jones</UserName>
    <FullName>Alice Jones</FullName>
    <Email>alice.jones@example.com</Email>
    <StartDate>2024-03-01</StartDate>
    <EndDate>2024-03-31</EndDate>
  </TaskRedirection>
</response>
```

### Success Response -" no redirection configured

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
```

## Response Field Reference

The `<TaskRedirection>` element describes the **destination** user (the person tasks are being redirected *to*):

| Element | Description |
|---------|-------------|
| `UserId` | Numeric user ID of the redirect target. |
| `UserName` | Login name of the redirect target. |
| `FullName` | Full display name of the redirect target. |
| `Email` | Email address of the redirect target. |
| `StartDate` | Date from which the redirection is active. Empty string if open-ended. |
| `EndDate` | Date on which the redirection expires. Empty string if open-ended. |

## Required Permissions

Any authenticated user may call this API.

## Example

### GET Request

```
GET /srv.asmx/GetUserTaskRedirectionTo
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &userName=john.smith
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetUserTaskRedirectionTo HTTP/1.1
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

Reports where a user's tasks are going.

```javascript
const root = await call('GetUserTaskRedirectionTo', { authenticationTicket: ticket, userName: 'jsmith' });

const redirection = root.querySelector('TaskRedirection');
if (redirection) {
  console.log(redirection.querySelector('UserName').textContent,
              redirection.querySelector('StartDate').textContent,
              redirection.querySelector('EndDate').textContent);
}
```

With nothing redirected the answer carries **no child element at all** - not an empty wrapper - so
test for `<TaskRedirection>` before reading it. A call with no ticket is the anonymous user rather
than an error, and it discloses nothing.

## Notes

- A task redirection causes all new tasks assigned to `userName` to be forwarded to another user for the duration of the active date range.
- If the redirection's `StartDate` and `EndDate` window has passed or has not yet started, the redirection may exist in the database but not be actively applied. The API returns the stored redirection record regardless.
- To check which users are redirecting tasks *to* a given user, use [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md).
- To configure a redirection, use [SetUserTaskRedirection](SetUserTaskRedirection.md).
- To remove a redirection, use [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md).

## Related APIs

- [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) -" List all users who are redirecting their tasks to a given user.
- [SetUserTaskRedirection](SetUserTaskRedirection.md) -" Set or update a task redirection for a user.
- [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md) -" Remove a user's task redirection.
- [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md) -" Change the target of an existing task redirection.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no user by that name |
