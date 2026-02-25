# GetAllFolderColumns API

Returns all available folder column definitions that can be used for configuring folder display views. Each column definition includes a programmatic name and a localized display text. There are 34 available columns covering document metadata, workflow, retention, and classification fields.

## Endpoint

```
/srv.asmx/GetAllFolderColumns
```

## Methods

- **GET** `/srv.asmx/GetAllFolderColumns?authenticationTicket=...`
- **POST** `/srv.asmx/GetAllFolderColumns` (form data)
- **SOAP** Action: `http://tempuri.org/GetAllFolderColumns`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true">
  <FolderColumns>
    <FolderColumnDef>
      <ColumnName>ItemName</ColumnName>
      <ColumnText>Name</ColumnText>
    </FolderColumnDef>
    <FolderColumnDef>
      <ColumnName>DocumentSize</ColumnName>
      <ColumnText>Size</ColumnText>
    </FolderColumnDef>
    <FolderColumnDef>
      <ColumnName>DocumentFormat</ColumnName>
      <ColumnText>Format</ColumnText>
    </FolderColumnDef>
    <FolderColumnDef>
      <ColumnName>ModificationDate</ColumnName>
      <ColumnText>Modified</ColumnText>
    </FolderColumnDef>
    <!-- ... additional columns ... -->
  </FolderColumns>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## FolderColumnDef Properties

| Property | Type | Description |
|----------|------|-------------|
| `ColumnName` | string | Programmatic column identifier used in `SetDefaultFolderColumns` |
| `ColumnText` | string | Localized display text for the column header |

## Available Columns (34 total)

| ColumnName | Description |
|------------|-------------|
| `ItemName` | Document or folder name |
| `ItemId` | Document or folder ID |
| `DocumentSize` | File size |
| `DocumentFormat` | File format/extension |
| `ModificationDate` | Last modification date |
| `ApprovalStatus` | Workflow approval status |
| `ParentFolderName` | Parent folder name |
| `LastVersionNumber` | Latest version number |
| `PercentComplete` | Completion percentage |
| `CreationDate` | Creation date |
| `ModifiedByName` | Last modified by user |
| `OwnerName` | Document owner |
| `FlowName` | Workflow name |
| `CheckedOutByName` | Checked out by user |
| `StepNumber` | Workflow step number |
| `StepName` | Workflow step name |
| `CompletionDate` | Completion date |
| `Importance` | Importance level |
| `RetentionDefId` | Retention definition ID |
| `ClassificationLevel` | Security classification |
| `DeclassifyOn` | Declassification date |
| `DowngradeOn` | Downgrade date |
| `DispositionDate` | Disposition date |
| `LastIsoReview` | Last ISO review date |
| `NextIsoReview` | Next ISO review date |
| `DocTypeName` | Document type name |
| `DocumentSource` | Document source |
| `DocumentLanguage` | Document language |
| `DocumentAuthor` | Document author |
| `ExpirationDate` | Expiration date |
| `ReleasedVersion` | Released version number |
| `RegisterDate` | Registration date |
| `CutOffDate` | Cut-off date |
| `RetainUntil` | Retain until date |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- No specific administrative permissions required

## Use Cases

1. **UI Configuration**
   - Populate column selection dropdowns
   - Build folder view customization dialogs

2. **Settings Management**
   - Retrieve available columns before calling `SetDefaultFolderColumns`
   - Validate column names in client-side logic

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetAllFolderColumns?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetAllFolderColumns HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetAllFolderColumns"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetAllFolderColumns xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetAllFolderColumns>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getAllFolderColumns() {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetAllFolderColumns?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const columns = [];
        xmlDoc.querySelectorAll("FolderColumnDef").forEach(col => {
            columns.push({
                columnName: col.querySelector("ColumnName").textContent,
                columnText: col.querySelector("ColumnText").textContent
            });
        });
        return columns;
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function buildColumnSelector() {
    try {
        const columns = await getAllFolderColumns();
        columns.forEach(col => {
            console.log(`${col.columnName}: ${col.columnText}`);
        });
    } catch (error) {
        console.error("Failed to get folder columns:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetAllFolderColumnsAsync(authTicket);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            var columns = root.Descendants("FolderColumnDef")
                .Select(col => new
                {
                    ColumnName = col.Element("ColumnName")?.Value ?? "",
                    ColumnText = col.Element("ColumnText")?.Value ?? ""
                })
                .ToList();

            foreach (var col in columns)
            {
                Console.WriteLine($"{col.ColumnName}: {col.ColumnText}");
            }
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

- Column display text (`ColumnText`) is localized based on the authenticated user's language setting.
- The column list is hardcoded and does not change between requests; only the localized text varies.
- Use the `ColumnName` values (not `ColumnText`) when calling `SetDefaultFolderColumns`.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |

## Related APIs

- `GetDefaultFolderColumns` - Get the current system default folder columns
- `SetDefaultFolderColumns` - Set the system default folder columns
- `GetGeneralAppSettings` - Get general application settings

## Version History

- **New in current version**: Provides programmatic access to folder column definitions
- Returns localized column text based on user language
