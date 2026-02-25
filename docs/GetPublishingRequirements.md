# GetPublishingRequirements API

Returns the publishing requirements configured for the specified domain/library. Publishing requirements define what conditions must be met before a document in the domain can be published. Use this API to determine whether any pre-publishing checks (such as requiring a document type to be assigned) must be satisfied before calling `PublishDocument`.

## Endpoint

```
/srv.asmx/GetPublishingRequirements
```

## Methods

- **GET** `/srv.asmx/GetPublishingRequirements?AuthenticationTicket=...&domainname=...`
- **POST** `/srv.asmx/GetPublishingRequirements` (form data)
- **SOAP** Action: `http://tempuri.org/GetPublishingRequirements`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainname` | string | Yes | Name of the domain/library whose publishing requirements to retrieve (e.g. `Finance`). |

---

## Response

### Success Response

Returns a `<root>` element containing a `<PublishingRequirements>` child element. Each active requirement appears as a `<PublishingRequirement>` child of that element. If no requirements are configured, `<PublishingRequirements>` is present but empty.

**With a requirement configured:**

```xml
<root success="true">
  <PublishingRequirements>
    <PublishingRequirement>Doctype</PublishingRequirement>
  </PublishingRequirements>
</root>
```

**No requirements configured:**

```xml
<root success="true">
  <PublishingRequirements />
</root>
```

### Publishing Requirement Values

| Value | Description |
|-------|-------------|
| `Doctype` | A document type must be assigned to the document before it can be published. Documents without an assigned document type will be rejected when `PublishDocument` is called. |

> Currently `Doctype` is the only publishing requirement supported. Additional requirements may be added in future versions.

### Error Response

```xml
<root success="false" error="Domain not found." />
```

---

## Required Permissions

Any authenticated user may call this API. No special domain permissions are required to read publishing requirements.

---

## Example

### GET Request

```
GET /srv.asmx/GetPublishingRequirements
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &domainname=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetPublishingRequirements HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&domainname=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetPublishingRequirements>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:domainname>Finance</tns:domainname>
    </tns:GetPublishingRequirements>
  </soap:Body>
</soap:Envelope>
```

### Checking before publishing

```
1. GET /srv.asmx/GetPublishingRequirements?...&domainname=Finance
   -' <PublishingRequirement>Doctype</PublishingRequirement> present

2. Ensure the document has a document type assigned (check GetDocument/@DocTypeID != "0")

3. GET /srv.asmx/PublishDocument?...&Path=/Finance/Reports/Q1-Report.pdf&VersionNumber=2000000
```

---

## Notes

- The `<PublishingRequirements>` element is always present in a success response, even when empty. Test for the presence of `<PublishingRequirement>` child elements rather than the parent element itself.
- The `Doctype` requirement means that `GetDocument/@DocTypeID` must not be `0` before the document can be published. Assign a document type using `UpdateDocumentType` if needed.
- Publishing requirements are configured at the domain/library level and apply to all documents within that domain.
- The `domainname` parameter is the plain name of the domain (e.g. `Finance`), not a full path.

---

## Related APIs

- [PublishDocument](PublishDocument.md) - Publish a specific version of a document
- [UnpublishDocument](UnpublishDocument.md) - Set a document as unpublished
- [GetDocument](GetDocument.md) - Get document properties including `DocTypeID` and `PublishingRule`
- [UpdateDocumentType](UpdateDocumentType.md) - Assign a document type to a document
- [GetDomainPolicies](GetDomainPolicies.md) - Get the full set of policies for a domain/library

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Domain not found | The specified `domainname` does not resolve to an existing domain/library. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
