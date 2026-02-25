# GetMimeTypes API

Returns the list of all defined MIME types in the system. Each entry includes the file extension, a human-readable description, and the MIME type string. The list is sorted alphabetically by extension type.

## Endpoint

```
/srv.asmx/GetMimeTypes
```

## Methods

- **GET** `/srv.asmx/GetMimeTypes?authenticationTicket=...`
- **POST** `/srv.asmx/GetMimeTypes` (form data)
- **SOAP** Action: `http://tempuri.org/GetMimeTypes`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true">
  <MimeTypes>
    <MimeType>
      <ExtensionType>.csv</ExtensionType>
      <Description>Comma Separated Values</Description>
      <MimeTypeString>text/csv</MimeTypeString>
    </MimeType>
    <MimeType>
      <ExtensionType>.doc</ExtensionType>
      <Description>Microsoft Word Document</Description>
      <MimeTypeString>application/msword</MimeTypeString>
    </MimeType>
    <MimeType>
      <ExtensionType>.docx</ExtensionType>
      <Description>Microsoft Word Open XML Document</Description>
      <MimeTypeString>application/vnd.openxmlformats-officedocument.wordprocessingml.document</MimeTypeString>
    </MimeType>
    <MimeType>
      <ExtensionType>.pdf</ExtensionType>
      <Description>Portable Document Format</Description>
      <MimeTypeString>application/pdf</MimeTypeString>
    </MimeType>
    <MimeType>
      <ExtensionType>.xlsx</ExtensionType>
      <Description>Microsoft Excel Open XML Spreadsheet</Description>
      <MimeTypeString>application/vnd.openxmlformats-officedocument.spreadsheetml.sheet</MimeTypeString>
    </MimeType>
    <!-- ... additional MIME types ... -->
  </MimeTypes>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## MimeType Properties

| Property | Type | Description |
|----------|------|-------------|
| `ExtensionType` | string | File extension including the leading dot (e.g., `.pdf`, `.docx`) |
| `Description` | string | Human-readable description of the file type |
| `MimeTypeString` | string | Standard MIME type string (e.g., `application/pdf`) |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- No specific administrative permissions required

## Use Cases

1. **File Upload Validation**
   - Retrieve supported file types before upload
   - Validate file extensions against known MIME types

2. **UI Configuration**
   - Populate file type filter dropdowns
   - Display file type icons based on MIME type

3. **Content Type Resolution**
   - Map file extensions to MIME types for HTTP responses
   - Determine appropriate viewers based on MIME type

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetMimeTypes?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetMimeTypes HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetMimeTypes"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetMimeTypes xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetMimeTypes>
  </soap:Body>
</soap:Envelope>
```

## Integration Examples

### JavaScript/Client-Side

```javascript
async function getMimeTypes() {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetMimeTypes?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") === "true") {
        const mimeTypes = [];
        xmlDoc.querySelectorAll("MimeType").forEach(mt => {
            mimeTypes.push({
                extensionType: mt.querySelector("ExtensionType").textContent,
                description: mt.querySelector("Description").textContent,
                mimeTypeString: mt.querySelector("MimeTypeString").textContent
            });
        });
        return mimeTypes;
    } else {
        const error = root.getAttribute("error");
        throw new Error(error);
    }
}

// Usage example
async function buildFileTypeFilter() {
    try {
        const mimeTypes = await getMimeTypes();

        // Build a lookup map
        const mimeMap = {};
        mimeTypes.forEach(mt => {
            mimeMap[mt.extensionType.toLowerCase()] = mt.mimeTypeString;
        });

        console.log(`Supported file types: ${mimeTypes.length}`);
        console.log(`MIME type for .pdf: ${mimeMap[".pdf"]}`);
        console.log(`MIME type for .docx: ${mimeMap[".docx"]}`);
    } catch (error) {
        console.error("Failed to get MIME types:", error);
    }
}
```

### C# Client Usage

```csharp
using (var client = new SrvSoapClient())
{
    try
    {
        var response = await client.GetMimeTypesAsync(authTicket);
        var root = XElement.Parse(response.ToString());

        if (root.Attribute("success")?.Value == "true")
        {
            var mimeTypes = root.Descendants("MimeType")
                .Select(mt => new
                {
                    ExtensionType = mt.Element("ExtensionType")?.Value ?? "",
                    Description = mt.Element("Description")?.Value ?? "",
                    MimeTypeString = mt.Element("MimeTypeString")?.Value ?? ""
                })
                .ToList();

            foreach (var mt in mimeTypes)
            {
                Console.WriteLine($"{mt.ExtensionType}: {mt.Description} ({mt.MimeTypeString})");
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

- The MIME type list is loaded from the application settings and is system-wide.
- The list is sorted alphabetically by `ExtensionType`.
- The `ExtensionType` includes the leading dot (e.g., `.pdf` not `pdf`).
- This API returns all MIME types defined in the system, not just those for documents currently stored.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |

## Related APIs

- `GetAllFolderColumns` - Get available folder column definitions
- `GetGeneralAppSettings` - Get general application settings
- `getApplicationParameters` - Get application parameters
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New in current version**: Provides programmatic access to the MIME type registry
- Available to all authenticated users
