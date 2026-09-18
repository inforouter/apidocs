# SendEmail API

Sends one or more infoRouter documents and/or folders to a list of recipients by email. Each item is included as a clickable library link in the email body.

## Endpoint

```
/srv.asmx/SendEmail
```

## Methods

- **GET** `/srv.asmx/SendEmail?authenticationTicket=...&recipients=...&subject=...&body=...&itemPaths=...`
- **POST** `/srv.asmx/SendEmail` (form data)
- **SOAP** Action: `http://tempuri.org/SendEmail`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `recipients` | string | Yes | Comma- or semicolon-separated list of recipient email addresses |
| `subject` | string | Yes | Email subject line |
| `body` | string | No | Email body text |
| `itemPaths` | string | Yes | Pipe-delimited list of infoRouter paths. Paths ending with `/` or `\` are resolved as folders; all others are resolved as documents. See [itemPaths format](#itempaths-format) below. |

## itemPaths Format

Pass one or more infoRouter paths separated by `|`. The server determines whether each path is a document or folder by its trailing character:

| Path | Resolved as |
|------|-------------|
| `/Accounting/report.pdf` | Document (no trailing slash) |
| `/Accounting/Invoices/` | Folder (trailing `/`) |
| `/Accounting/Invoices\` | Folder (trailing `\`) |

**Example:**
```
/Accounting/Q1-report.pdf|/HR/Policies/handbook.docx|/Projects/Alpha/
```

If any path cannot be found, the request fails immediately and returns an error identifying the missing path.

## Delivery

Items are always delivered as **library links** embedded in the email body. The recipient receives a clickable link for each document or folder that opens the item directly in infoRouter.

Long paths are automatically shortened using infoRouter short-path format (`~D{id}` for documents, `~F{id}` for folders) when the full URL would exceed 260 characters.

## Response

### Success

```xml
<response success="true" error="" errorCode="0" />
```

### Error

```xml
<response success="false" error="Error message here" />
```

## Required Permissions

- User must be authenticated
- The **Send Email** feature must be enabled in *Control Panel → Email and Notification Settings*

## Example Requests

### Request (GET)

```
GET /srv.asmx/SendEmail
  ?authenticationTicket=abc123
  &recipients=alice@example.com,bob@example.com
  &subject=Q1%20Report
  &body=Please%20find%20the%20links%20below.
  &itemPaths=%2FAccounting%2FQ1-report.pdf%7C%2FAccounting%2FInvoices%2F
HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/SendEmail HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&
recipients=alice@example.com;bob@example.com&
subject=Project+Files&
body=Links+to+the+project+materials.&
itemPaths=/Projects/Alpha/spec.docx|/Projects/Alpha/Drawings/
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/SendEmail"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SendEmail xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <recipients>alice@example.com;bob@example.com</recipients>
      <subject>Shared Documents</subject>
      <body>Please review the materials linked below.</body>
      <itemPaths>/Projects/Alpha/spec.docx|/Projects/Alpha/Drawings/</itemPaths>
    </SendEmail>
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

Sends a message with one or more infoRouter documents attached.

```javascript
await call('SendEmail', {
  authenticationTicket: ticket,
  recipients: 'alice@example.com,bob@example.com',   // a comma or a semicolon both separate
  subject: 'The procedure you asked for',
  body: 'Attached.',
  itemPaths: '/Quality/Procedures/qp-001.pdf'        // comma separated
});
```

**`recipients` and `subject` are required; `body` and `itemPaths` are not.** An empty `itemPaths`
is a plain message with nothing attached, and an empty `body` is an empty mail. Until 9.0 all four
were non-nullable strings, so an empty one was refused by model binding with HTTP 400 and there was
no way to send a message this operation did not attach a document to.

`itemPaths` is a list of **documents**. A folder path among them is not resolved as a folder; the
whole call is refused `4041`, and the message does not say which entry was the problem. An address
that is not one is refused `4000` and the message names it.

## Notes

- Recipients may be separated by commas or semicolons; both are accepted and normalised before sending.
- The email sender address is determined by system settings: either the system email address or the authenticated user's own email address (if *Send Emails From User's Email* is enabled).

## Related APIs

- `DistributeDocument` — Send a distribution notification to all OnChange subscribers of a document
- `GetEmailAndNotificationSettings` — Read current email feature flags

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | one of the `itemPaths` is not a document the caller can see |
| `4000` | one of the `recipients` is not an email address; the message names it |
| `5030` | the mail service is not reachable |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
