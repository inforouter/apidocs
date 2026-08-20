# UpdateDocumentTypeDef1 API

Updates an existing document type definition. Allows renaming the document type, changing its required property set, and setting or clearing its default retention and disposition schedule.

## Endpoint

```
/srv.asmx/UpdateDocumentTypeDef1
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentTypeDef1?authenticationTicket=...&DocumentTypeId=...&NewDocumentTypeName=...&NewRequiredPropertySetName=...&RandDScheduleName=...&Description=...`
- **POST** `/srv.asmx/UpdateDocumentTypeDef1` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentTypeDef1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentTypeId` | int | Yes | The numeric ID of the document type definition to update. Use `GetDocumentTypes` to retrieve IDs. |
| `NewDocumentTypeName` | string | Yes | New name for the document type. Must be unique system-wide. |
| `NewRequiredPropertySetName` | string | **Yes** | Name of the property set to require for documents of this type. **Whatever you send is written**: send the current name to keep it, an empty string to remove it. Omitting it removes it, so send it every time. Use [UpdateDocumentTypeDef](UpdateDocumentTypeDef.md) when you want the property set left alone. |
| `RandDScheduleName` | string | No | Name of an existing retention and disposition schedule to set as the default for this type. Pass an empty string to remove the current schedule. Omit (pass `null`) to leave the existing schedule unchanged. |
| `Description` | string | **Yes** | What the document type means, in a sentence. Maximum 255 characters, single line. **Whatever you send is written**: send the current description to keep it, an empty string to clear it. Omitting it clears the description, so send it every time. Use [UpdateDocumentTypeDef](UpdateDocumentTypeDef.md) when you want the description left alone. |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

The calling user must be an **authenticated user**. Anonymous users are not permitted.

---

## Example

### GET Request — rename and set schedule

```
GET /srv.asmx/UpdateDocumentTypeDef1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentTypeId=5
  &NewDocumentTypeName=Financial+Report
  &NewRequiredPropertySetName=FinanceProperties
  &RandDScheduleName=Finance+Records+-+7+Years
  &Description=A+statement+of+account+activity+for+a+reporting+period
HTTP/1.1
```

### GET Request — clear the schedule

```
GET /srv.asmx/UpdateDocumentTypeDef1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentTypeId=5
  &NewDocumentTypeName=Financial+Report
  &NewRequiredPropertySetName=FinanceProperties
  &RandDScheduleName=
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDocumentTypeDef1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentTypeId=5
&NewDocumentTypeName=Financial+Report
&NewRequiredPropertySetName=FinanceProperties
&RandDScheduleName=Finance+Records+-+7+Years
&Description=A+statement+of+account+activity+for+a+reporting+period
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDocumentTypeDef1>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DocumentTypeId>5</tns:DocumentTypeId>
      <tns:NewDocumentTypeName>Financial Report</tns:NewDocumentTypeName>
      <tns:NewRequiredPropertySetName>FinanceProperties</tns:NewRequiredPropertySetName>
      <tns:RandDScheduleName>Finance Records - 7 Years</tns:RandDScheduleName>
      <tns:Description>A statement of account activity for a reporting period</tns:Description>
    </tns:UpdateDocumentTypeDef1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Renaming a document type affects all documents currently assigned to that type — they will reflect the new name immediately.
- Changing or removing the required property set may affect metadata validation for documents already assigned to this type.
- `RandDScheduleName` behavior:
  - **Omitted / null** — the existing schedule is preserved unchanged.
  - **Empty string** — the current default schedule is removed (sets `DefaultRDDefID` to 0).
  - **A schedule name** — the named schedule becomes the new default. The schedule must already exist.
- `Description` behavior:
  - **Omitted / null** — the existing description is preserved unchanged.
  - **Empty string** — the current description is cleared.
  - **A sentence** — becomes the new description. Maximum 255 characters, single line.
- `Description` is what infoRouter tells infoRouter Connect the type is, and Connect recognises a described type in a document noticeably better than one identified by its name alone. It is returned by `GetDocumentTypes`.
- Changes to the default retention schedule only affect documents assigned this type **after** the update. Existing documents are not retroactively updated.
- Use `GetDocumentTypes` to retrieve document type IDs and current configuration.

---

## Related APIs

- [UpdateDocumentTypeDef](UpdateDocumentTypeDef.md) - Update a document type definition without changing its retention schedule
- [CreateDocumentTypeDef1](CreateDocumentTypeDef1.md) - Create a document type with an optional retention schedule
- [GetDocumentTypes](GetDocumentTypes.md) - Retrieve all defined document type definitions
- [UpdateDocumentType](UpdateDocumentType.md) - Assign a document type to a specific document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Insufficient rights | Anonymous users cannot perform this action. |
| `Document type not found` | The specified `DocumentTypeId` does not exist. |
| `A document type with this name already exists.` | The new name conflicts with an existing document type. |
| `Specified custom propertyset not applicable to the documents.` | The named property set is not configured to apply to documents. |
| `Specified custom propertyset is not a public property set.` | The named property set is not a global property set. |
| `The selected retention and disposition schedule cannot be found.` | The value in `RandDScheduleName` does not match any existing schedule. |
| `Maximum allowable character length exceeded` | `Description` is longer than 255 characters. |
| `SystemError:...` | An unexpected server-side error occurred. |
