# GetDefaultFolderColumns API

Returns the system default folder column configuration. These columns define which metadata fields are displayed by default in folder list views when no user-specific or folder-specific column settings are applied.

## Endpoint

```
/srv.asmx/GetDefaultFolderColumns
```

## Methods

- **GET** `/srv.asmx/GetDefaultFolderColumns?authenticationTicket=...`
- **POST** `/srv.asmx/GetDefaultFolderColumns` (form data)
- **SOAP** Action: `http://tempuri.org/GetDefaultFolderColumns`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true">
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
  <FolderColumnDef>
    <ColumnName>OwnerName</ColumnName>
    <ColumnText>Owner</ColumnText>
  </FolderColumnDef>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## FolderColumnDef Properties

| Property | Type | Description |
|----------|------|-------------|
| `ColumnName` | string | Programmatic column identifier |
| `ColumnText` | string | Localized display text for the column header |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- No specific administrative permissions required

## Use Cases

1. **UI Initialization**
   - Load the default column layout when rendering folder views
   - Determine which columns to display when no custom settings exist

2. **Settings Display**
   - Pre-populate the default columns in an administration form
   - Compare current defaults with the full column list from `GetAllFolderColumns`

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetDefaultFolderColumns?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetDefaultFolderColumns HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetDefaultFolderColumns"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetDefaultFolderColumns xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetDefaultFolderColumns>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getDefaultFolderColumns() {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetDefaultFolderColumns?authenticationTicket=${encodeURIComponent(ticket)}`;

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
async function initFolderView() {
    try {
        const defaultColumns = await getDefaultFolderColumns();
        console.log("Default columns:", defaultColumns.map(c => c.columnName).join(", "));
    } catch (error) {
        console.error("Failed to get default folder columns:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetDefaultFolderColumnsAsync(authTicket);
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

- The default columns are stored in the `USERFOLDSET` database table with `FolderId=0` and `PlayerId=0`.
- If no system defaults have been configured, a hardcoded set of columns is returned: `ItemName`, `DocumentSize`, `DocumentFormat`, `ModificationDate`, `OwnerName`.
- Column text is localized based on the authenticated user's language setting.
- To change the default columns, use the `SetDefaultFolderColumns` API.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |

## Related APIs

- `GetAllFolderColumns` - Get all available folder column definitions
- `SetDefaultFolderColumns` - Set the system default folder columns
- `GetGeneralAppSettings` - Get general application settings

## Version History

- **New in current version**: Provides programmatic access to default folder column settings
- Returns localized column text based on user language
