# AddISOComment API

Adds an ISO compliance review comment to the latest version of the specified document. The comment is recorded as an ISO log entry and the document's last ISO review date is updated. The calling user must have an active ISO Review Task assigned to them for the target document.

## Endpoint

```
/srv.asmx/AddISOComment
```

## Methods

- **GET** `/srv.asmx/AddISOComment?authenticationTicket=...&DocumentPath=...&CommentText=...`
- **POST** `/srv.asmx/AddISOComment` (form data)
- **SOAP** Action: `http://tempuri.org/AddISOComment`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path of the document to comment on (e.g. `/Finance/Reports/Q1Report.pdf`). |
| `CommentText` | string | Yes | The ISO review comment text to record. Leading/trailing whitespace is normalized before saving. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

- The caller must be an **authenticated user** with a valid ticket.
- The caller must have an **active ISO Review Task assigned to them** for the specified document. Users without an assigned ISO Review Task will receive an error even if they have other permissions on the document.
- The document must not be in an **Offline (archived)** state.

---

## Example

### GET Request

```
GET /srv.asmx/AddISOComment?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&DocumentPath=/Finance/Reports/Q1Report.pdf&CommentText=Reviewed+and+approved+per+ISO+9001+requirements HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AddISOComment HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentPath=/Finance/Reports/Q1Report.pdf
&CommentText=Reviewed and approved per ISO 9001 requirements
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AddISOComment>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DocumentPath>/Finance/Reports/Q1Report.pdf</tns:DocumentPath>
      <tns:CommentText>Reviewed and approved per ISO 9001 requirements</tns:CommentText>
    </tns:AddISOComment>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The comment is always applied to the **latest version** of the document (`LastVersionNumber`). There is no way to add an ISO comment to a specific older version via this API.
- The document's **Last ISO Review Date** field is automatically updated to the current server date and time when the comment is successfully added.
- Comment text is sanitized (whitespace normalized) before being stored.
- If the document is in an **Offline** state (archived to secondary storage), the API returns an error. The document must be online to accept ISO comments.
- An ISO Review Task is created as part of a Workflow process that includes an ISO review step. If no such workflow task exists for the calling user on this document, this API call will fail.

---

## Related APIs

- [AddSOXComment](AddSOXComment.md) - Add an SOX compliance comment to a document
- [GetISOLogs](GetISOLogs.md) - Retrieve the ISO comment history for a document
- [GetISOReviewAssignments](GetISOReviewAssignments.md) - Get documents assigned to the current user for ISO review
- [Search](Search.md) - Search for documents, e.g. by next ISO review date

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified `DocumentPath` does not exist or the user does not have access to it. |
| There is no ISO Review Task assigned to you | The calling user does not have an active ISO Review Task for this document. |
| Document is offline | The document is archived (offline state) and cannot accept ISO comments. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/AddISOComment*
