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
<response success="true" />
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

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid authentication ticket |
| `[499] ...` | `itemPaths` or `recipients` is empty |
| `[933] ...` | The Send Email feature is disabled in system settings |
| `[2301] ...: address` | One of the recipient addresses is not a valid email address |
| Path not found error | A path in `itemPaths` could not be resolved to a document or folder |

## Notes

- Recipients may be separated by commas or semicolons; both are accepted and normalised before sending.
- The email sender address is determined by system settings: either the system email address or the authenticated user's own email address (if *Send Emails From User's Email* is enabled).

## Related APIs

- `DistributeDocument` — Send a distribution notification to all OnChange subscribers of a document
- `GetEmailAndNotificationSettings` — Read current email feature flags
