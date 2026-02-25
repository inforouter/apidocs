# GetRetentionSourceAuthorities API

Returns a list of all retention source authorities defined in the system. Retention source authorities are used to specify the governing body or regulation that mandates retention requirements for records and documents.

## Endpoint

```
/srv.asmx/GetRetentionSourceAuthorities
```

## Methods

- **GET** `/srv.asmx/GetRetentionSourceAuthorities?authenticationTicket=...`
- **POST** `/srv.asmx/GetRetentionSourceAuthorities` (form data)
- **SOAP** Action: `http://tempuri.org/GetRetentionSourceAuthorities`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response

### Success Response

```xml
<root success="true">
  <RetentionSourceAuthorities>
    <Authority Name="SEC - Securities and Exchange Commission" />
    <Authority Name="HIPAA - Health Insurance Portability and Accountability Act" />
    <Authority Name="SOX - Sarbanes-Oxley Act" />
    <Authority Name="GDPR - General Data Protection Regulation" />
  </RetentionSourceAuthorities>
</root>
```

### Response Structure

| Element | Description |
|---------|-------------|
| `RetentionSourceAuthorities` | Container element for all authorities |
| `Authority` | Individual authority entry with Name attribute |

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- User must be authenticated (anonymous users cannot access this API)
- No specific administrative permissions required - all authenticated users can view retention source authorities

## Use Cases

1. **R&D Schedule Configuration**
   - When creating or editing retention and disposition schedules
   - Select appropriate source authority that mandates the retention requirements

2. **Compliance Documentation**
   - Document which regulations govern record retention
   - Maintain audit trail of compliance requirements

3. **Dropdown Population**
   - Populate UI dropdowns for source authority selection
   - Standardize authority references across the system

4. **Reporting and Analytics**
   - Generate compliance reports showing retention requirements by authority
   - Analyze retention policies grouped by governing regulation

## Example

### Request (GET)

```
GET /srv.asmx/GetRetentionSourceAuthorities?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetRetentionSourceAuthorities HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetRetentionSourceAuthorities"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetRetentionSourceAuthorities xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetRetentionSourceAuthorities>
  </soap:Body>
</soap:Envelope>
```

### Success Response Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true">
  <RetentionSourceAuthorities>
    <Authority Name="FDA - Food and Drug Administration" />
    <Authority Name="IRS - Internal Revenue Service" />
    <Authority Name="OSHA - Occupational Safety and Health Administration" />
    <Authority Name="ISO 15489 - Records Management Standard" />
    <Authority Name="DoD 5015.2 - Department of Defense Records Management" />
  </RetentionSourceAuthorities>
</root>
```

### Empty List Response

If no retention source authorities are defined:

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true">
  <RetentionSourceAuthorities />
</root>
```

## Related APIs

### Retention & Disposition Schedule Management
- `GetRandDSchedules` - Get all R&D schedules
- `GetRandDScheduleInfo` - Get detailed info for a specific schedule
- `CreateRandDSchedule` - Create a new R&D schedule
- `UpdateRandDSchedule` - Update an existing R&D schedule
- `DeleteRandDSchedule` - Delete an R&D schedule

### Document Retention
- `GetDocumentRandDSchedule` - Get R&D schedule applied to a document
- `SetDocumentRandDSchedule` - Apply R&D schedule to a document
- `RemoveDocumentRandDSchedule` - Remove R&D schedule from document

### Folder Retention
- `GetFolderRandDSchedule` - Get R&D schedule applied to a folder
- `SetFolderRandDSchedule` - Apply R&D schedule to a folder
- `RemoveFolderRandDSchedule` - Remove R&D schedule from folder

## Notes

- Source authorities are system-wide settings managed by administrators
- Authority names are free-form text and can be customized per organization
- The list is typically small (5-20 entries) representing key regulations
- Source authorities are referenced when creating R&D schedules
- This API is read-only - authorities are managed through the Control Panel UI or separate administrative APIs
- Authority names should follow a consistent naming convention (e.g., "Acronym - Full Name")
- Common authorities include: SEC, HIPAA, SOX, GDPR, FDA, IRS, OSHA, ISO standards, DoD regulations

## Common Source Authorities

Organizations typically define authorities based on their industry and jurisdiction:

**Financial Services:**
- SEC (Securities and Exchange Commission)
- SOX (Sarbanes-Oxley Act)
- FINRA (Financial Industry Regulatory Authority)
- GLBA (Gramm-Leach-Bliley Act)

**Healthcare:**
- HIPAA (Health Insurance Portability and Accountability Act)
- FDA (Food and Drug Administration)
- HITECH (Health Information Technology for Economic and Clinical Health Act)

**Government:**
- FOIA (Freedom of Information Act)
- NARA (National Archives and Records Administration)
- DoD 5015.2 (Department of Defense Records Management)

**International:**
- GDPR (General Data Protection Regulation - EU)
- ISO 15489 (International Records Management Standard)

**General Business:**
- IRS (Internal Revenue Service)
- OSHA (Occupational Safety and Health Administration)
- State-specific regulations

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |
| `System error accessing retention settings` | Database or configuration access error |

## Integration Example

### JavaScript/Client-Side Usage

```javascript
async function loadRetentionAuthorities() {
    const ticket = getUserAuthTicket();
    const response = await fetch(
        `/srv.asmx/GetRetentionSourceAuthorities?authenticationTicket=${ticket}`
    );
    
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");
    
    const authorities = xmlDoc.querySelectorAll("Authority");
    const dropdown = document.getElementById("authoritySelect");
    
    authorities.forEach(auth => {
        const option = document.createElement("option");
        option.value = auth.getAttribute("Name");
        option.text = auth.getAttribute("Name");
        dropdown.appendChild(option);
    });
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    var response = await client.GetRetentionSourceAuthoritiesAsync(authTicket);
    var authorities = response.Descendants("Authority")
        .Select(a => a.Attribute("Name")?.Value)
        .Where(n => n != null)
        .ToList();
    
    // Populate dropdown or process authorities
    authorityDropDown.DataSource = authorities;
}
```

## Best Practices

1. **Cache Results**: Authority lists change infrequently - cache for improved performance
2. **Display Format**: Present full authority names in UI for clarity
3. **Validation**: Validate selected authority against current list before saving
4. **Documentation**: Maintain documentation of what each authority represents
5. **Naming Convention**: Use consistent format (e.g., "CODE - Full Name")
6. **Regular Review**: Periodically review and update authority list as regulations change

## Version History

- Compatible with infoRouter 8.7 and later
- Supports both synchronous SOAP and REST access patterns
- Authority management features may require Records Management license
