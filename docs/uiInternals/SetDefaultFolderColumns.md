---
search:
  exclude: true
---

# SetDefaultFolderColumns API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Sets the system default folder columns using a comma-separated list of column names. The columns define which metadata fields are displayed by default in folder list views. All column names are validated against the list of available columns before being saved.

## Endpoint

```
/api/UIInternals/SetDefaultFolderColumns
```

## Methods

- **GET** `/api/UIInternals/SetDefaultFolderColumns?authenticationTicket=...&columnNames=...`
- **POST** `/api/UIInternals/SetDefaultFolderColumns` (form data)

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

- An **administrator** or a member of **[Policy Managers]**, as for the other application-wide settings. Up to 8.7 only administrators could, and others were refused with `4000`.
- The permission is checked before the column list, so a caller without it gets `4030` whatever it sent.

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
GET /api/UIInternals/SetDefaultFolderColumns?authenticationTicket=abc123-def456&columnNames=ItemName,DocumentSize,ModificationDate,OwnerName,CreationDate HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /api/UIInternals/SetDefaultFolderColumns HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&columnNames=ItemName,DocumentSize,ModificationDate,OwnerName,CreationDate
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function setDefaultFolderColumns(columnNames) {
    const ticket = getUserAuthTicket();

    const response = await fetch("/api/UIInternals/SetDefaultFolderColumns", {
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

## Notes

- A column named more than once in `columnNames` is kept once.
- Column name validation is case-insensitive (e.g., `itemname` matches `ItemName`).
- At least one column name must be provided. An empty or whitespace-only string will return an error.
- Leading and trailing whitespace around column names is trimmed automatically.
- The settings are stored in the `USERFOLDSET` database table with `FolderId=0` and `PlayerId=0`.
- Changes take effect immediately for all users who do not have custom folder column settings.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | a caller with no ticket, or one who is neither an administrator nor a Policy Manager |


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
