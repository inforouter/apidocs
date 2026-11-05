# SetCustomMenus API

Replaces every custom menu the document list draws, and their entries, in the order given. A menu named after a built-in one (`FILE`, `EDIT`, `TOOLS`, `ADVANCED`, `VIEW`, `POPMENU`) adds its items to that menu; `POPMENU` is the right-click menu. Any other name becomes a new heading on the menu bar. [GetCustomMenus](GetCustomMenus.md) answers the new set at once.

## Endpoint

```
/srv.asmx/SetCustomMenus
```

## Methods

- **GET** `/srv.asmx/SetCustomMenus?authenticationTicket=...&customMenusXml=...`
- **POST** `/srv.asmx/SetCustomMenus` (form data)
- **SOAP** Action: `http://tempuri.org/SetCustomMenus`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `customMenusXml` | string | Yes | The whole new set, see below. An empty `<CustomMenus />` removes every custom menu. |

## The set

The shape [GetCustomMenus](GetCustomMenus.md) answers. Its `builtIn`, `popup` and `ignoredEntries` attributes are answers, not input, and are ignored, so a whole GetCustomMenus answer can be sent back as it is.

```xml
<CustomMenus>
  <Menu name="TOOLS">
    <MenuItem name="mnuFax" caption="Fax" tipText="Fax to a number" action="faxto.aspx" target="_faxto" />
  </Menu>
  <Menu name="SAPIntegration" caption="SAP Integration">
    <MenuItem name="mnuSubmit" caption="Submit for payment" action="https://sap.example/submit" target="_sap" />
  </Menu>
</CustomMenus>
```

| Element / attribute | Rule |
|---|---|
| `Menu/@name` | Required, at most 64 characters, unique (case-insensitive) |
| `Menu/@caption` | Required on a menu that is not built in, at most 128 characters; that is its heading. Ignored on a built-in menu, which keeps its own translated caption |
| `MenuItem/@name` | Required, at most 64 characters, unique across **all** menus (case-insensitive): the document list uses it as the entry's element id |
| `MenuItem/@caption` | Required, at most 128 characters |
| `MenuItem/@tipText` | Optional, at most 255 characters |
| `MenuItem/@action` | Required, at most 1000 characters. A relative path (`page.aspx`, `/help/x.htm`) or an `http`/`https` URL. Anything else - `javascript:`, `data:`, `vbscript:`, `file:` - is refused, and so is any control character |
| `MenuItem/@target` | Optional, at most 64 characters: the window the page opens in |

The order of the elements is the order the menus and entries are drawn. The set is checked as a whole before anything is written: the first problem is named in a `4000` refusal and nothing changes.

## Response

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[4000] Menu 'Reports', item 'mnuOne': the action must be a relative path or an http or https URL." errorCode="4000" />
```

| errorCode | When |
|-----------|------|
| `4000` | Malformed XML, an empty parameter, or a menu or entry that breaks a rule above |
| `4010` | No valid ticket (an anonymous session) |
| `4030` | The caller does not have the right described below |

## Required Permissions

The `UpdateApplicationSettingsAndPolicies` administrative right: the `sysadmin` account and members of `[Administrators]`. Anyone else is refused and nothing changes.

## Example

### Request (POST)

```
POST /srv.asmx/SetCustomMenus HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&customMenusXml=%3CCustomMenus%3E%3CMenu%20name%3D%22TOOLS%22%3E%3CMenuItem%20name%3D%22mnuFax%22%20caption%3D%22Fax%22%20action%3D%22faxto.aspx%22%20%2F%3E%3C%2FMenu%3E%3C%2FCustomMenus%3E
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetCustomMenus>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:customMenusXml>&lt;CustomMenus&gt;&lt;Menu name="TOOLS"&gt;&lt;MenuItem name="mnuFax" caption="Fax" action="faxto.aspx" /&gt;&lt;/Menu&gt;&lt;/CustomMenus&gt;</tns:customMenusXml>
    </tns:SetCustomMenus>
  </soap:Body>
</soap:Envelope>
```

## JavaScript

```javascript
// Read, add an entry to the right-click menu, write the whole set back.
const current = await call('GetCustomMenus', { authenticationTicket: ticket });
const set = current.querySelector('CustomMenus');

let popup = [...set.querySelectorAll('Menu')].find(m => m.getAttribute('name') === 'POPMENU');
if (!popup) {
  popup = set.ownerDocument.createElement('Menu');
  popup.setAttribute('name', 'POPMENU');
  set.appendChild(popup);
}
const item = set.ownerDocument.createElement('MenuItem');
item.setAttribute('name', 'mnuArchive');
item.setAttribute('caption', 'Send to archive');
item.setAttribute('action', 'https://archive.example/send');
popup.appendChild(item);

await call('SetCustomMenus', {
  authenticationTicket: ticket,
  customMenusXml: new XMLSerializer().serializeToString(set)
});
```

## Notes

- **Storage:** from 9.0 the menus are the `CUSTOMMENUS` and `CUSTOMMENUITEMS` tables. Until then they were the file `config\CustomMenus.xml`, edited by hand and read at start-up. The 9.0 upgrade copies the file into the tables and deletes it; an entry the file had without a name, with a duplicate name or without an action is skipped and reported. An action that is not a safe link is moved as it was but reported, and this API refuses the set until it is changed.
- **When the change shows:** at once on the server that took the call; on the other servers of a farm within 15 minutes.
- **Captions are not translated:** they are shown as given.

## Related APIs

- [GetCustomMenus](GetCustomMenus.md) - Get the custom menus
