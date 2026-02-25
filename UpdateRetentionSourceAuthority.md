# UpdateRetentionSourceAuthority API

Updates (renames) a retention source authority in the system. The new authority name must be unique and not already exist.

## Endpoint

```
/srv.asmx/UpdateRetentionSourceAuthority
```

## Methods

- **GET** `/srv.asmx/UpdateRetentionSourceAuthority?authenticationTicket=...&currentAuthorityName=...&newAuthorityName=...`
- **POST** `/srv.asmx/UpdateRetentionSourceAuthority` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateRetentionSourceAuthority`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `currentAuthorityName` | string | Yes | Current name of the retention source authority to update |
| `newAuthorityName` | string | Yes | New name for the retention source authority |

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

## Update Rules

The API enforces the following rules:

- **Current Authority Must Exist**: The current authority name must exist in the system
- **Unique New Name**: The new authority name must not already exist
- **Non-Empty Names**: Both current and new names cannot be empty or whitespace-only
- **Length Limit**: New authority name must not exceed 64 characters
- **No Case Change Only**: Changing only the case is not allowed if it results in a duplicate

## Example

### Request (GET)

```
GET /srv.asmx/UpdateRetentionSourceAuthority?authenticationTicket=abc123-def456&currentAuthorityName=SEC&newAuthorityName=SEC%20-%20Securities%20and%20Exchange%20Commission HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/UpdateRetentionSourceAuthority HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&currentAuthorityName=SEC&newAuthorityName=SEC - Securities and Exchange Commission
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/UpdateRetentionSourceAuthority"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <UpdateRetentionSourceAuthority xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <currentAuthorityName>SEC</currentAuthorityName>
      <newAuthorityName>SEC - Securities and Exchange Commission</newAuthorityName>
    </UpdateRetentionSourceAuthority>
  </soap:Body>
</soap:Envelope>
```

### Success Response

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true" />
```

### Error Response Examples

**Current Authority Not Found:**
```xml
<root success="false" error="Current authority not found." />
```

**New Name Already Exists:**
```xml
<root success="false" error="There is already a Retention Source Authority with same name." />
```

**Empty Current Name:**
```xml
<root success="false" error="Current authority name cannot be empty" />
```

**Empty New Name:**
```xml
<root success="false" error="New authority name cannot be empty" />
```

**Name Too Long:**
```xml
<root success="false" error="Character length of the Authority Source Name cannot be greater than 64 character. Please enter shorter name." />
```

## Related APIs

### Retention Source Authority Management
- `GetRetentionSourceAuthorities` - List all retention source authorities
- `CreateRetentionSourceAuthority` - Create a new retention source authority
- `DeleteRetentionSourceAuthority` - Delete a retention source authority

### Retention & Disposition Schedule Management
- `GetRandDSchedules` - Get all R&D schedules that may reference the authority
- `GetRandDScheduleInfo` - Get detailed schedule information
- `UpdateRandDSchedule` - Update R&D schedule (note: authority references are stored)

## Use Cases

1. **Standardize Naming**
   - Update authorities to follow consistent naming conventions
   - Add missing full names or acronyms to authority names

2. **Correct Typos**
   - Fix spelling errors in authority names
   - Correct formatting issues

3. **Expand Abbreviations**
   - Change "SEC" to "SEC - Securities and Exchange Commission"
   - Make authority names more descriptive

4. **Consolidate Authorities**
   - Rename an authority before migrating R&D schedules
   - Update to match organizational naming standards

## Update Workflow

Recommended workflow for updating a retention source authority:

1. **Verify Current Authority**
   ```
   Call GetRetentionSourceAuthorities to confirm current name
   ```

2. **Check New Name Availability**
   ```
   Call GetRetentionSourceAuthorities to ensure new name doesn't exist
   ```

3. **Check R&D Schedule Impact**
   ```
   Call GetRandDSchedules to review which schedules reference this authority
   Note: R&D schedules store authority name as text, not as a reference
   ```

4. **Perform Update**
   ```
   Call UpdateRetentionSourceAuthority with current and new names
   ```

5. **Verify Update**
   ```
   Call GetRetentionSourceAuthorities to confirm the change
   ```

6. **Update R&D Schedules** (if necessary)
   ```
   If R&D schedules store authority name (not ID), they may need updating
   Call UpdateRandDSchedule for each affected schedule
   ```

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |
| `Current authority name cannot be empty` | No current authority name provided |
| `New authority name cannot be empty` | No new authority name provided |
| `Current authority not found.` | The specified current authority does not exist |
| `There is already a Retention Source Authority with same name.` | The new name duplicates an existing authority |
| `Character length of the Authority Source Name cannot be greater than 64 character.` | New name exceeds maximum length |
| `Access denied` | User does not have permission to update authorities |

## Notes

- Authority names are case-sensitive during matching
- Whitespace is trimmed from both current and new authority names
- The update is atomic - either succeeds completely or fails with no changes
- Update is logged in the system audit trail
- Authority update does not automatically update R&D schedules that reference the old name
- Consider the impact on R&D schedules before renaming widely-used authorities

## Impact on R&D Schedules

Important considerations:

- **Check Storage Method**: Determine if R&D schedules store authority by name or by reference
- **Update Schedules**: If stored by name, all schedules using the old name need updating
- **Historical Records**: Historical compliance records may still reference the old name
- **Reports**: Existing reports may need to be updated to use the new authority name

## Best Practices

1. **Verify Before Update**: Always check that current authority exists
2. **Check Uniqueness**: Ensure new name doesn't already exist
3. **Document Changes**: Maintain audit trail of authority name changes
4. **Communicate**: Notify stakeholders before renaming widely-used authorities
5. **Update Schedules**: If necessary, update R&D schedules that reference the old name
6. **Test First**: Test rename in staging environment before production
7. **Backup**: Export authority list before making changes
8. **Consistent Format**: Follow organizational naming conventions

## Security Considerations

- Authority updates require administrative privileges
- All update attempts are logged in the audit trail
- Authority names are sanitized to prevent injection attacks
- Consider implementing approval workflows for sensitive changes
- Maintain backup of authority list before updates

## Validation Rules

The API performs the following validations:

- **Non-Empty Current**: Current authority name must not be empty or whitespace-only
- **Non-Empty New**: New authority name must not be empty or whitespace-only
- **Existence Check**: Current authority must exist in the system
- **Uniqueness**: New authority name must not duplicate an existing authority
- **Length**: New authority name must not exceed 64 characters
- **Authentication**: User must have valid authentication ticket
- **Authorization**: User must have administrative permissions

## Integration Example

### JavaScript/Client-Side

```javascript
async function updateAuthority(currentName, newName) {
    // Validate new name
    if (!newName || newName.trim().length === 0) {
        alert('New authority name cannot be empty');
        return false;
    }
    
    if (newName.length > 64) {
        alert('Authority name cannot exceed 64 characters');
        return false;
    }
    
    // Check if new name already exists
    const authorities = await getRetentionSourceAuthorities();
    if (authorities.includes(newName)) {
        alert('An authority with the new name already exists');
        return false;
    }
    
    // Confirm update
    if (!confirm(`Rename "${currentName}" to "${newName}"?`)) {
        return false;
    }
    
    const ticket = getUserAuthTicket();
    const formData = new FormData();
    formData.append('authenticationTicket', ticket);
    formData.append('currentAuthorityName', currentName);
    formData.append('newAuthorityName', newName);
    
    const response = await fetch('/srv.asmx/UpdateRetentionSourceAuthority', {
        method: 'POST',
        body: formData
    });
    
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");
    
    const success = xmlDoc.querySelector("root").getAttribute("success");
    if (success === "true") {
        console.log("Authority updated successfully");
        return true;
    } else {
        const error = xmlDoc.querySelector("root").getAttribute("error");
        console.error("Failed to update authority:", error);
        alert(error);
        return false;
    }
}

async function getRetentionSourceAuthorities() {
    const ticket = getUserAuthTicket();
    const response = await fetch(
        `/srv.asmx/GetRetentionSourceAuthorities?authenticationTicket=${ticket}`
    );
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");
    
    const authorities = [];
    xmlDoc.querySelectorAll("Authority").forEach(auth => {
        authorities.push(auth.getAttribute("Name"));
    });
    return authorities;
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        string currentName = "SEC";
        string newName = "SEC - Securities and Exchange Commission";
        
        // Validate inputs
        if (string.IsNullOrWhiteSpace(newName))
        {
            Console.WriteLine("New authority name cannot be empty");
            return;
        }
        
        if (newName.Length > 64)
        {
            Console.WriteLine("Authority name cannot exceed 64 characters");
            return;
        }
        
        // Check if new name already exists
        var authoritiesResponse = await client.GetRetentionSourceAuthoritiesAsync(authTicket);
        var authorities = authoritiesResponse.Descendants("Authority")
            .Select(a => a.Attribute("Name")?.Value)
            .ToList();
        
        if (authorities.Contains(newName))
        {
            Console.WriteLine("An authority with the new name already exists");
            return;
        }
        
        // Confirm update
        Console.WriteLine($"Rename '{currentName}' to '{newName}'? (y/n)");
        var confirm = Console.ReadLine();
        if (confirm?.ToLower() != "y")
        {
            Console.WriteLine("Update cancelled");
            return;
        }
        
        // Perform update
        var response = await client.UpdateRetentionSourceAuthorityAsync(
            authTicket,
            currentName,
            newName
        );
        
        var root = response.Root;
        if (root.Attribute("success")?.Value == "true")
        {
            Console.WriteLine("Authority updated successfully");
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

## Common Scenarios

### Scenario 1: Expand Abbreviation

```
Current: "HIPAA"
New: "HIPAA - Health Insurance Portability and Accountability Act"

1. Call UpdateRetentionSourceAuthority("HIPAA", "HIPAA - Health Insurance...")
2. Verify update with GetRetentionSourceAuthorities
3. Update any R&D schedules that store the authority name
```

### Scenario 2: Fix Typo

```
Current: "GDPR - General Data Protction Regulation" (typo: "Protction")
New: "GDPR - General Data Protection Regulation"

1. Call UpdateRetentionSourceAuthority with corrected spelling
2. Verify correction
```

### Scenario 3: Standardize Format

```
Multiple authorities with inconsistent formats:
- "SEC"
- "FINRA - Financial Industry Regulatory Authority"
- "Sarbanes-Oxley Act"

Standardize to "CODE - Full Name" format:
1. Update "SEC" → "SEC - Securities and Exchange Commission"
2. Keep "FINRA - Financial Industry Regulatory Authority" (already correct)
3. Update "Sarbanes-Oxley Act" → "SOX - Sarbanes-Oxley Act"
```

## Version History

- Compatible with infoRouter 8.7 and later
- Supports both synchronous SOAP and REST access patterns
- Authority management features may require Records Management license
- Update validation enhanced in latest version

## See Also

- [GetRetentionSourceAuthorities](./GetRetentionSourceAuthorities.md) - List all authorities
- [CreateRetentionSourceAuthority](./CreateRetentionSourceAuthority.md) - Create new authority
- [DeleteRetentionSourceAuthority](./DeleteRetentionSourceAuthority.md) - Delete authority
- [GetRandDSchedules](./GetRandDSchedules.md) - Get R&D schedules

