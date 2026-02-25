# SetDefaultFolderColumns API

Sets the system default folder columns using a comma-separated list of column names. The columns define which metadata fields are displayed by default in folder list views. All column names are validated against the list of available columns before being saved.

## Endpoint

```
/srv.asmx/SetDefaultFolderColumns
```

## Methods

- **GET** `/srv.asmx/SetDefaultFolderColumns?authenticationTicket=...&columnNames=...`
- **POST** `/srv.asmx/SetDefaultFolderColumns` (form data)
- **SOAP** Action: `http://tempuri.org/SetDefaultFolderColumns`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `columnNames` | string | Yes | Comma-separated list of column names (e.g., `ItemName,DocumentSize,ModificationDate,OwnerName`) |

## Response Structure

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- User must be authenticated (anonymous users cannot perform this action)

## Column Name Validation

All column names in the `columnNames` parameter are validated against the 34 available columns (see `GetAllFolderColumns`). Validation is case-insensitive. If any invalid column name is provided, the entire operation fails and returns an error listing both the invalid names and all valid column names.

### Valid Column Names

`ItemName`, `ItemId`, `DocumentSize`, `DocumentFormat`, `ModificationDate`, `ApprovalStatus`, `ParentFolderName`, `LastVersionNumber`, `PercentComplete`, `CreationDate`, `ModifiedByName`, `OwnerName`, `FlowName`, `CheckedOutByName`, `StepNumber`, `StepName`, `CompletionDate`, `Importance`, `RetentionDefId`, `ClassificationLevel`, `DeclassifyOn`, `DowngradeOn`, `DispositionDate`, `LastIsoReview`, `NextIsoReview`, `DocTypeName`, `DocumentSource`, `DocumentLanguage`, `DocumentAuthor`, `ExpirationDate`, `ReleasedVersion`, `RegisterDate`, `CutOffDate`, `RetainUntil`

## Use Cases

1. **Administration**
   - Configure the default folder view for all users
   - Customize which metadata fields are visible system-wide

2. **Deployment Automation**
   - Set default columns programmatically during system setup
   - Standardize column configuration across environments

## Example Requests

### Request (GET)

```
GET /srv.asmx/SetDefaultFolderColumns?authenticationTicket=abc123-def456&columnNames=ItemName,DocumentSize,ModificationDate,OwnerName,CreationDate HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/SetDefaultFolderColumns HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&columnNames=ItemName,DocumentSize,ModificationDate,OwnerName,CreationDate
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/SetDefaultFolderColumns"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetDefaultFolderColumns xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <columnNames>ItemName,DocumentSize,ModificationDate,OwnerName,CreationDate</columnNames>
    </SetDefaultFolderColumns>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function setDefaultFolderColumns(columnNames) {
    const ticket = getUserAuthTicket();

    const response = await fetch("/srv.asmx/SetDefaultFolderColumns", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `authenticationTicket=${encodeURIComponent(ticket)}&columnNames=${encodeURIComponent(columnNames)}`
    });

    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        console.log("Default folder columns updated successfully.");
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
setDefaultFolderColumns("ItemName,DocumentSize,DocumentFormat,ModificationDate,OwnerName,CreationDate");
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var columnNames = "ItemName,DocumentSize,DocumentFormat,ModificationDate,OwnerName,CreationDate";
        var response = await client.SetDefaultFolderColumnsAsync(authTicket, columnNames);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            Console.WriteLine("Default folder columns updated successfully.");
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

## Notes

- Column name validation is case-insensitive (e.g., `itemname` matches `ItemName`).
- At least one column name must be provided. An empty or whitespace-only string will return an error.
- Leading and trailing whitespace around column names is trimmed automatically.
- The settings are stored in the `USERFOLDSET` database table with `FolderId=0` and `PlayerId=0`.
- Changes take effect immediately for all users who do not have custom folder column settings.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |
| `Invalid column name(s): ...` | One or more column names are not recognized. The error message lists invalid and valid names. |
| `Column names cannot be empty...` | The columnNames parameter is empty |

## Related APIs

- `GetAllFolderColumns` - Get all available folder column definitions
- `GetDefaultFolderColumns` - Get the current system default folder columns
- `GetGeneralAppSettings` - Get general application settings

## Version History

- **New in current version**: Provides programmatic access to configure default folder columns
- Validates all column names before saving
