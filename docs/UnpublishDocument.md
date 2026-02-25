# UnpublishDocument API

Sets the document at the specified path to an unpublished state. An unpublished document is not visible to regular users who only have read access — it behaves as if no version has been officially released. This is the reverse of `PublishDocument`. Use this API to retract a previously published document while keeping all versions, metadata, and history intact.

## Endpoint

```
/srv.asmx/UnpublishDocument
```

## Methods

- **GET** `/srv.asmx/UnpublishDocument?authenticationTicket=...&documentPath=...`
- **POST** `/srv.asmx/UnpublishDocument` (form data)
- **SOAP** Action: `http://tempuri.org/UnpublishDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

## Required Permissions

The calling user must have **publish** permission on the document or its containing folder.

---

## Example

### GET Request

```
GET /srv.asmx/UnpublishDocument
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &documentPath=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UnpublishDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&documentPath=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UnpublishDocument>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:documentPath>/Finance/Reports/Q1-2024-Report.pdf</tns:documentPath>
    </tns:UnpublishDocument>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API sets the publishing rule to `UNPUBLISHED`, hiding the document from read-only users.
- All document versions, metadata, and history are preserved — unpublishing does not delete any data.
- If the document is already in an unpublished state, this call returns success without making any changes.
- To re-publish the document, use `PublishDocument`.

---

## Related APIs

- [PublishDocument](PublishDocument.md) - Set the published version of a document
- [GetDocument](GetDocument.md) - Get document properties including the current publishing status

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Access denied | The user does not have publish permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UnpublishDocument*
