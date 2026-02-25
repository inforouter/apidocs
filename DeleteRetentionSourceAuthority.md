# DeleteRetentionSourceAuthority API

Deletes a retention source authority from the system. The authority must not be in use by any retention and disposition schedules.

## Endpoint

```
/srv.asmx/DeleteRetentionSourceAuthority
```

## Methods

- **GET** `/srv.asmx/DeleteRetentionSourceAuthority?authenticationTicket=...&authorityName=...`
- **POST** `/srv.asmx/DeleteRetentionSourceAuthority` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteRetentionSourceAuthority`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `authorityName` | string | Yes | Exact name of the retention source authority to delete |

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

## Deletion Restrictions

The API will prevent deletion if:

- **Authority is in use**: Referenced by one or more R&D schedules
- **Authority not found**: No authority with the specified name exists
- **Empty name**: Authority name is empty or whitespace-only

## Example

### Request (GET)

```
GET /srv.asmx/DeleteRetentionSourceAuthority?authenticationTicket=abc123-def456&authorityName=GDPR%20-%20General%20Data%20Protection%20Regulation HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/DeleteRetentionSourceAuthority HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&authorityName=GDPR - General Data Protection Regulation
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/DeleteRetentionSourceAuthority"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DeleteRetentionSourceAuthority xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <authorityName>GDPR - General Data Protection Regulation</authorityName>
    </DeleteRetentionSourceAuthority>
  </soap:Body>
</soap:Envelope>
```

### Success Response

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true" />
```

### Error Response Examples

**Authority Not Found:**
```xml
<root success="false" error="Retention source authority not found" />
```

**Authority In Use:**
```xml
<root success="false" error="Cannot delete authority because it is referenced by one or more R&D schedules" />
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
- `CreateRetentionSourceAuthority` - Create a new retention source authority
- `UpdateRetentionSourceAuthority` - Update an existing authority (if available)

### Retention & Disposition Schedule Management
- `GetRandDSchedules` - Get all R&D schedules (to verify authority usage)
- `GetRandDScheduleInfo` - Get detailed schedule information
- `UpdateRandDSchedule` - Update schedule to remove authority reference
- `DeleteRandDSchedule` - Delete R&D schedule before deleting authority

## Use Cases

1. **Cleanup Obsolete Authorities**
   - Remove authorities that are no longer applicable
   - Consolidate duplicate or redundant authorities

2. **System Maintenance**
   - Remove test authorities created during setup
   - Clean up authorities added in error

3. **Compliance Updates**
   - Remove authorities for superseded regulations
   - Update authority list when regulations change

4. **Organization Restructuring**
   - Remove authorities specific to divested business units
   - Clean up after mergers or acquisitions

## Pre-Deletion Checklist

Before deleting a retention source authority:

1. **Check Usage**
   - Call `GetRandDSchedules` to get all R&D schedules
   - Verify no schedules reference the authority to be deleted

2. **Update or Delete Dependent Schedules**
   - Use `UpdateRandDSchedule` to change authority reference
   - Or use `DeleteRandDSchedule` to remove unused schedules

3. **Document Reason**
   - Maintain audit trail of why authority was removed
   - Document replacement authority if applicable

4. **Communicate Changes**
   - Notify compliance team of authority removal
   - Update retention policy documentation

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |
| `Authority name cannot be empty` | No authority name provided or only whitespace |
| `Retention source authority not found` | No authority with the specified name exists |
| `Cannot delete authority because it is referenced by one or more R&D schedules` | Authority is in use |
| `Access denied` | User does not have permission to delete authorities |

## Notes

- Authority names are case-sensitive when matching for deletion
- Whitespace is trimmed from the beginning and end of authority names
- The deletion is permanent and cannot be undone
- Authority deletion is logged in the system audit trail
- Consider exporting authority list before making bulk deletions
- Deleting an authority does not affect historical records that referenced it

## Workflow for Safe Deletion

1. **Verify Authority Exists**
   ```
   Call GetRetentionSourceAuthorities to confirm the authority name
   ```

2. **Check for Dependencies**
   ```
   Call GetRandDSchedules and review which schedules use this authority
   ```

3. **Remove Dependencies** (if any)
   ```
   For each R&D schedule using this authority:
     - Call UpdateRandDSchedule to change the authority reference
     - Or call DeleteRandDSchedule if the schedule is obsolete
   ```

4. **Delete Authority**
   ```
   Call DeleteRetentionSourceAuthority
   ```

5. **Verify Deletion**
   ```
   Call GetRetentionSourceAuthorities to confirm removal
   ```

## Best Practices

1. **Verify Before Delete**: Always check if authority is in use before attempting deletion
2. **Backup First**: Export authority list before making changes
3. **Update Dependencies**: Remove or update R&D schedules referencing the authority
4. **Document Changes**: Maintain audit trail of deletions
5. **Test in Staging**: Test deletion in non-production environment first
6. **Communicate**: Notify stakeholders before removing authorities
7. **Gradual Approach**: Delete authorities one at a time, not in bulk
8. **Verify Impact**: Check historical reports that may reference deleted authorities

## Security Considerations

- Authority deletion requires administrative privileges
- All deletion attempts are logged in the audit trail
- Authority names are sanitized to prevent injection attacks
- Consider implementing approval workflows for authority deletion
- Implement backup and recovery procedures

## Integration Example

### JavaScript/Client-Side

```javascript
async function deleteAuthority(authorityName) {
    // First, check if authority is in use
    const inUse = await isAuthorityInUse(authorityName);
    if (inUse) {
        alert('Cannot delete authority: it is currently in use by R&D schedules');
        return false;
    }
    
    // Confirm deletion
    if (!confirm(`Are you sure you want to delete authority: ${authorityName}?`)) {
        return false;
    }
    
    const ticket = getUserAuthTicket();
    const formData = new FormData();
    formData.append('authenticationTicket', ticket);
    formData.append('authorityName', authorityName);
    
    const response = await fetch('/srv.asmx/DeleteRetentionSourceAuthority', {
        method: 'POST',
        body: formData
    });
    
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");
    
    const success = xmlDoc.querySelector("root").getAttribute("success");
    if (success === "true") {
        console.log("Authority deleted successfully");
        return true;
    } else {
        const error = xmlDoc.querySelector("root").getAttribute("error");
        console.error("Failed to delete authority:", error);
        alert(error);
        return false;
    }
}

async function isAuthorityInUse(authorityName) {
    // Check if any R&D schedules reference this authority
    const ticket = getUserAuthTicket();
    const response = await fetch(
        `/srv.asmx/GetRandDSchedules?authenticationTicket=${ticket}`
    );
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");
    
    // Parse schedules and check for authority reference
    // (Actual implementation would need to check schedule details)
    return false; // Simplified for example
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        // First check if authority exists
        var authoritiesResponse = await client.GetRetentionSourceAuthoritiesAsync(authTicket);
        var authorities = authoritiesResponse.Descendants("Authority")
            .Select(a => a.Attribute("Name")?.Value)
            .ToList();
        
        if (!authorities.Contains(authorityToDelete))
        {
            Console.WriteLine("Authority not found");
            return;
        }
        
        // Check if in use (simplified - would need to check R&D schedules)
        var schedulesResponse = await client.GetRandDSchedulesAsync(authTicket);
        // ... check if any schedules reference the authority ...
        
        // Confirm deletion
        Console.WriteLine($"Are you sure you want to delete '{authorityToDelete}'? (y/n)");
        var confirm = Console.ReadLine();
        if (confirm?.ToLower() != "y")
        {
            Console.WriteLine("Deletion cancelled");
            return;
        }
        
        // Perform deletion
        var response = await client.DeleteRetentionSourceAuthorityAsync(
            authTicket, 
            authorityToDelete
        );
        
        var root = response.Root;
        if (root.Attribute("success")?.Value == "true")
        {
            Console.WriteLine("Authority deleted successfully");
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

### Scenario 1: Clean Up Test Authorities

```
1. Get list of all authorities
2. Identify test authorities (e.g., names starting with "TEST_")
3. For each test authority:
   - Verify it's not in use
   - Delete the authority
4. Verify cleanup complete
```

### Scenario 2: Consolidate Duplicate Authorities

```
1. Identify duplicate authorities (e.g., "SEC" and "SEC - Securities and Exchange Commission")
2. Choose the authority name to keep
3. Update all R&D schedules to use the kept authority
4. Delete the duplicate authorities
5. Verify all schedules still function correctly
```

### Scenario 3: Remove Superseded Regulation

```
1. Identify the superseded authority (e.g., old regulation)
2. Create new authority for replacement regulation
3. Update all R&D schedules to reference new authority
4. Delete the old authority
5. Document the change in compliance records
```

## Version History

- Compatible with infoRouter 8.7 and later
- Supports both synchronous SOAP and REST access patterns
- Authority management features may require Records Management license
- Deletion validation enhanced in version 8.7.152

## See Also

- [GetRetentionSourceAuthorities](./GetRetentionSourceAuthorities.md) - List all authorities
- [CreateRetentionSourceAuthority](./CreateRetentionSourceAuthority.md) - Create new authority
- [GetRandDSchedules](./GetRandDSchedules.md) - Get R&D schedules to check dependencies
- Control Panel UI: `RetentionSourceAuthority.aspx?method=delete` - Authority deletion form
