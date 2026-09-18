# SendWelcomeEmailForUser API

Sends a welcome email to a specified user. For native-authenticated users the email includes a 48-hour password reset link. For externally-authenticated users it includes their authentication source name. Requires system administrator privileges.

## Endpoint

```
/srv.asmx/SendWelcomeEmailForUser
```

## Methods

- **GET** `/srv.asmx/SendWelcomeEmailForUser?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/SendWelcomeEmailForUser` (form data)
- **SOAP** Action: `http://tempuri.org/SendWelcomeEmailForUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `userName` | string | Yes | The username of the user to send the welcome email to |

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

Caller must be a **system administrator**.

## Email Content

The email sent depends on the user's authentication type:

| Authentication Type | Email Template | Password Reset Link |
|--------------------|----------------|---------------------|
| Native (infoRouter) | `WELCOMETOIR` | Yes — 48-hour expiry |
| External (LDAP, OAuth, etc.) | `WELCOMETOIREXTERNAL` | No — shows authentication source name |

The email is rendered in the **user's configured language preference**.

## Example

### Request (GET)
```
GET /srv.asmx/SendWelcomeEmailForUser?authenticationTicket=abc123&userName=jdoe HTTP/1.1
```

### Request (POST)
```
POST /srv.asmx/SendWelcomeEmailForUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&userName=jdoe
```

## Error Conditions

| Condition | Error Message |
|-----------|---------------|
| Caller is not a system administrator | Only the system administrator can perform this operation |
| User not found | User does not exist |
| User has no email address on file | User has no e-mail address on file |

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

Hands the welcome message for one user to the mail agent.

```javascript
await call('SendWelcomeEmailForUser', { authenticationTicket: ticket, userName: 'jsmith' });
```

There is no "already welcomed" state: calling it again sends it again. The answer says the message
was handed over, not that it was delivered - the address is whatever
[CreateUser](CreateUser.md) stored, which is not checked.

## Notes

- The password reset link embedded in native-account welcome emails expires after 48 hours.
- The SMTP server must be configured in `appsettings.json` for emails to be delivered.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4030` | there is no ticket at all |
| `4010` | the ticket is expired or unknown |
| `4000` | no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
