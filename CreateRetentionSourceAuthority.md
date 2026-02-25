# CreateRetentionSourceAuthority API

Creates a new retention source authority in the system. Retention source authorities specify the governing body or regulation that mandates retention requirements for records and documents.

## Endpoint

```
/srv.asmx/CreateRetentionSourceAuthority
```

## Methods

- **GET** `/srv.asmx/CreateRetentionSourceAuthority?authenticationTicket=...&authorityName=...`
- **POST** `/srv.asmx/CreateRetentionSourceAuthority` (form data)
- **SOAP** Action: `http://tempuri.org/CreateRetentionSourceAuthority`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `authorityName` | string | Yes | Name of the retention source authority to create (e.g., "SEC - Securities and Exchange Commission") |

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

- User must be authenticated (anonymous users cannot perform this action)
- User must have administrative rights to manage retention settings
- Typically requires Records Management or System Administrator role

## Authority Naming Guidelines

- **Use Descriptive Names**: Include both acronym and full name (e.g., "HIPAA - Health Insurance Portability and Accountability Act")
- **Avoid Duplicates**: Authority names must be unique
- **Character Limit**: Maximum length typically 255 characters
- **No Special Characters**: Avoid leading/trailing whitespace
- **Standardize Format**: Follow organizational naming conventions

## Example

### Request (GET)

```
GET /srv.asmx/CreateRetentionSourceAuthority?authenticationTicket=abc123-def456&authorityName=GDPR%20-%20General%20Data%20Protection%20Regulation HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/CreateRetentionSourceAuthority HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&authorityName=GDPR - General Data Protection Regulation
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/CreateRetentionSourceAuthority"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateRetentionSourceAuthority xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <authorityName>GDPR - General Data Protection Regulation</authorityName>
    </CreateRetentionSourceAuthority>
  </soap:Body>
</soap:Envelope>
```

### Success Response

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true" />
```

### Error Response Examples

**Duplicate Authority:**
```xml
<root success="false" error="Authority with this name already exists" />
```

**Empty Name:**
```xml
<root success="false" error="Authority name cannot be empty" />
```

**Invalid Ticket:**
```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
```

## Related APIs

### Retention Source Authority Management
- `GetRetentionSourceAuthorities` - List all retention source authorities
- `DeleteRetentionSourceAuthority` - Delete a retention source authority
- `UpdateRetentionSourceAuthority` - Update an existing authority (if available)

### Retention & Disposition Schedule Management
- `GetRandDSchedules` - Get all R&D schedules
- `CreateRandDSchedule` - Create a new R&D schedule (references source authority)
- `UpdateRandDSchedule` - Update an existing R&D schedule
- `DeleteRandDSchedule` - Delete an R&D schedule

## Use Cases

1. **Initial System Setup**
   - Configure retention authorities during system implementation
   - Set up authorities for organization's compliance requirements

2. **New Regulation Compliance**
   - Add new regulatory authorities as laws are enacted
   - Respond to changing compliance landscape

3. **Multi-Jurisdiction Organizations**
   - Add authorities for different geographical regions
   - Support international compliance requirements

4. **Industry Standards**
   - Add industry-specific retention standards
   - Support vertical-specific regulations

## Common Authority Examples

### Financial Services
```
SEC - Securities and Exchange Commission
FINRA - Financial Industry Regulatory Authority
SOX - Sarbanes-Oxley Act
GLBA - Gramm-Leach-Bliley Act
```

### Healthcare
```
HIPAA - Health Insurance Portability and Accountability Act
FDA - Food and Drug Administration
HITECH - Health Information Technology for Economic and Clinical Health Act
```

### International
```
GDPR - General Data Protection Regulation
ISO 15489 - Records Management Standard
ISO 27001 - Information Security Management
```

### Government
```
NARA - National Archives and Records Administration
FOIA - Freedom of Information Act
DoD 5015.2 - Department of Defense Records Management
```

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |
| `Authority name cannot be empty` | No authority name provided or only whitespace |
| `Authority with this name already exists` | An authority with the same name is already defined |
| `Invalid authority name` | Authority name contains invalid characters or exceeds length limit |
| `Access denied` | User does not have permission to create authorities |

## Notes

- Authority names are case-sensitive
- Whitespace is trimmed from the beginning and end of authority names
- The authority name is sanitized to prevent injection attacks
- Once created, the authority can be immediately used in R&D schedule definitions
- Authorities cannot be renamed - they must be deleted and recreated
- Deleting an authority that is in use by R&D schedules may be prevented
- Authority creation is logged in the system audit trail

## Workflow Integration

After creating a retention source authority:

1. **Verify Creation**
   - Call `GetRetentionSourceAuthorities` to confirm the authority was added

2. **Create R&D Schedules**
   - Use the new authority in `CreateRandDSchedule` to define retention policies

3. **Apply to Documents**
   - Apply R&D schedules (which reference the authority) to documents and folders

4. **Monitor Compliance**
   - Generate reports showing retention requirements by authority

## Best Practices

1. **Use Standard Names**: Follow industry-standard authority naming conventions
2. **Document Purpose**: Maintain documentation of what each authority governs
3. **Avoid Duplicates**: Check existing authorities before creating new ones
4. **Consistent Format**: Use a standard format like "CODE - Full Name"
5. **Version Control**: Include version numbers for authorities that change over time (e.g., "ISO 15489:2016")
6. **Localization**: Consider multi-language support for international organizations
7. **Review Process**: Implement approval workflow for adding new authorities
8. **Regular Audit**: Periodically review authority list for obsolete entries

## Security Considerations

- Authority creation requires administrative privileges
- Authority names are HTML-encoded to prevent XSS attacks
- Audit logs track who created each authority and when
- Changes to authorities may require compliance review
- Consider implementing approval workflows for sensitive industries

## Validation Rules

The API performs the following validations:

- **Non-Empty**: Authority name must not be empty or whitespace-only
- **Uniqueness**: Authority name must not duplicate an existing authority
- **Length**: Authority name must not exceed maximum length (typically 255 characters)
- **Characters**: Authority name must not contain certain special characters
- **Authentication**: User must have valid authentication ticket
- **Authorization**: User must have administrative permissions

## Integration Example

### JavaScript/Client-Side

```javascript
async function createAuthority(authorityName) {
    const ticket = getUserAuthTicket();
    const formData = new FormData();
    formData.append('authenticationTicket', ticket);
    formData.append('authorityName', authorityName);
    
    const response = await fetch('/srv.asmx/CreateRetentionSourceAuthority', {
        method: 'POST',
        body: formData
    });
    
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");
    
    const success = xmlDoc.querySelector("root").getAttribute("success");
    if (success === "true") {
        console.log("Authority created successfully");
        return true;
    } else {
        const error = xmlDoc.querySelector("root").getAttribute("error");
        console.error("Failed to create authority:", error);
        return false;
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.CreateRetentionSourceAuthorityAsync(
            authTicket, 
            "CCPA - California Consumer Privacy Act"
        );
        
        var root = response.Root;
        if (root.Attribute("success")?.Value == "true")
        {
            Console.WriteLine("Authority created successfully");
        }
        else
        {
            var error = root.Attribute("error")?.Value;
            Console.WriteLine($"Error: {error}");
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Exception: {ex.Message}");
    }
}
```

## Version History

- Compatible with infoRouter 8.7 and later
- Supports both synchronous SOAP and REST access patterns
- Authority management features may require Records Management license
- Validation and error handling enhanced in version 8.7.152

## See Also

- [GetRetentionSourceAuthorities](./GetRetentionSourceAuthorities.md) - List all authorities
- [CreateRandDSchedule](./CreateRandDSchedule.md) - Create retention schedule
- Control Panel UI: `RetentionSourceAuthority.aspx` - Authority creation form
