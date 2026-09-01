# GetCustomMenus API

Returns the custom menus this infoRouter installation adds to the document list, as defined in `appdir\config\CustomMenus.xml`. These are the entries an administrator wires up to reach pages or external systems of their own — the document list menu bar and the right-click menu are extended with them.

The definitions are installation-wide: every signed-in user sees the same set, and the response does not vary by folder, domain, or permissions.

## Endpoint

```
/srv.asmx/GetCustomMenus
```

## Methods

- **GET** `/srv.asmx/GetCustomMenus?authenticationTicket=...`
- **POST** `/srv.asmx/GetCustomMenus` (form data)
- **SOAP** Action: `http://tempuri.org/GetCustomMenus`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response Structure

### Success Response

```xml
<response success="true" error="">
  <CustomMenus ignoredEntries="0">
    <Menu name="FILE" caption="" builtIn="true" popup="false">
      <MenuItem name="mnuUploadRarFile" caption="Upload RAR File" tipText="Uploads rar file and Expand it on the server." action="UploadRar.aspx" target="_rarupload" />
      <MenuItem name="mnuCreateImage" caption="Create an Image" tipText="Create an Image Document using server side image editor." action="CreateImage.aspx" target="_createImage" />
    </Menu>
    <Menu name="Help" caption="Help" builtIn="false" popup="false">
      <MenuItem name="mnuHelpCreateDocument" caption="How to create a document" tipText="Explains the options of how to create a documents" action="/help/en/HowtoCreateDocument.htm" target="_help" />
    </Menu>
    <Menu name="POPMENU" caption="" builtIn="true" popup="true">
      <MenuItem name="mnuPopForward" caption="Forward to " tipText="forward the selected document to X Department" action="http://127.0.0.1:81/forward/x.aspx" target="_forward" />
    </Menu>
  </CustomMenus>
</response>
```

An installation with no `CustomMenus.xml` returns an empty `<CustomMenus ignoredEntries="0" />`.

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## CustomMenus Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `ignoredEntries` | int | How many menus or items were dropped because they carried no `name`. Non-zero means `CustomMenus.xml` has something wrong with it. |

## Menu Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | string | The menu's name. For a built-in menu this is the menu it extends; otherwise it is the id of the new menu. |
| `caption` | string | Heading text for a menu that is not built in. Ignored for a built-in menu, which keeps its own localized caption. |
| `builtIn` | bool | `true` when the items are appended to a menu infoRouter already draws: `FILE`, `EDIT`, `TOOLS`, `ADVANCED`, `VIEW`, `POPMENU`. `false` means a new heading of its own on the menu bar. |
| `popup` | bool | `true` for `POPMENU`, the right-click menu over a listed item rather than the menu bar. |

## MenuItem Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | string | Element id for the entry. Items without one are not returned and are counted in `ignoredEntries`. |
| `caption` | string | Text to show. Not localized — it is whatever the configuration file says. |
| `tipText` | string | Tooltip text, empty where the file gives none. |
| `action` | string | Page the entry opens: a path relative to the application root, or a full URL. |
| `target` | string | Window name the page opens in. |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- No administrative permissions required

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetCustomMenus?authenticationTicket=abc123-def456 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetCustomMenus HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetCustomMenus"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCustomMenus xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
    </GetCustomMenus>
  </soap:Body>
</soap:Envelope>
```

## Integration Example

```javascript
async function getCustomMenus() {
    const ticket = getUserAuthTicket();
    const url = `/srv.asmx/GetCustomMenus?authenticationTicket=${encodeURIComponent(ticket)}`;

    const response = await fetch(url);
    const xmlDoc = new DOMParser().parseFromString(await response.text(), "text/xml");

    const root = xmlDoc.querySelector("response");
    if (root.getAttribute("success") !== "true") {
        throw new Error(root.getAttribute("error"));
    }

    return Array.from(xmlDoc.querySelectorAll("Menu")).map(menu => ({
        name: menu.getAttribute("name"),
        caption: menu.getAttribute("caption"),
        builtIn: menu.getAttribute("builtIn") === "true",
        popup: menu.getAttribute("popup") === "true",
        items: Array.from(menu.querySelectorAll("MenuItem")).map(item => ({
            name: item.getAttribute("name"),
            caption: item.getAttribute("caption"),
            tipText: item.getAttribute("tipText"),
            action: item.getAttribute("action"),
            target: item.getAttribute("target")
        }))
    }));
}
```

## Notes

- Menus and items are returned in the order the configuration file lists them.
- A menu with no items is still returned. The old document list drew such a menu's heading but no drop-down; a caller is free to skip it.
- Captions and tooltips come from the configuration file verbatim and are not run through infoRouter's resource files, so an installation serving several languages has to write them in whichever language it chooses.
- The file is read when application settings are loaded. Editing `CustomMenus.xml` takes effect after the application cache is flushed (`FlushApplicationCache`) or the application restarts.
- A `CustomMenus.xml` that is not well-formed XML makes this call fail rather than returning an empty set.

## Error Codes

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |

## Related APIs

- `FlushApplicationCache` - Reload application settings, including `CustomMenus.xml`
- `getApplicationParameters` - Other installation-wide settings
