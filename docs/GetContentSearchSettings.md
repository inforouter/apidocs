# GetContentSearchSettings API

**Available in:** infoRouter 9.0 and later

Returns the content search settings in effect: whether content search is on, where it goes (a catalog on the infoRouter Search Service, or Windows Search), the search service's API key, and whether the service is told which documents changed. Administrators only; [SetContentSearchSettings](SetContentSearchSettings.md) changes them.

## Endpoint

```
/srv.asmx/GetContentSearchSettings
```

## Methods

- **GET** `/srv.asmx/GetContentSearchSettings?authenticationTicket=...`
- **POST** `/srv.asmx/GetContentSearchSettings` (form data)
- **SOAP** Action: `http://tempuri.org/GetContentSearchSettings`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response

### Success Response
```xml
<response success="true" error="">
  <ContentSearchSettings>
    <IndexSrv>true</IndexSrv>
    <IndexCatalog>http://search01:5000/corp/</IndexCatalog>
    <RemoteSearchApiKey>3f9c0d...</RemoteSearchApiKey>
    <RemoteSearchIndexNotify>true</RemoteSearchIndexNotify>
    <CheckSecurityOnSearch>false</CheckSecurityOnSearch>
    <MaxContentSearchResult>100000</MaxContentSearchResult>
  </ContentSearchSettings>
</response>
```

| Element | Type | Description |
|---------|------|-------------|
| `IndexSrv` | bool | `true`: content search is on. `false`: off; a search with keywords answers that there is no content search service. |
| `IndexCatalog` | string | The catalog's address on the infoRouter Search Service, `http://server:port/catalog-name/`, or `SYSTEMINDEX` for Windows Search. Empty when none is set. |
| `RemoteSearchApiKey` | string | The catalog's API key, sent to the search service with every request. Empty: no key is sent. |
| `RemoteSearchIndexNotify` | bool | `true`: infoRouter tells the search service which documents changed, so they are searchable within seconds. `false`: the service's nightly rescan finds the changes. |
| `CheckSecurityOnSearch` | bool | `true`: while search result pages are built, each hit's permission is checked again (for hits the search could not already mark as allowed). Applies to every search, not only content search. Default `false`. |
| `MaxContentSearchResult` | int | The most hits a content search takes from the search engine, 1 to 1,000,000. Default `100000`. |
| `SettingsProblem` | string | Present only when the settings file could not be read (see Notes). Says what is wrong with it; content search is off until it is corrected or the settings are saved. |

### Error Response
```xml
<response success="false" error="[ErrorCode] Error message" errorCode="4030" />
```

| errorCode | When |
|-----------|------|
| 4010 | No authentication ticket, or an invalid or expired one |
| 4030 | The user is not allowed to change application settings |

## Required Permissions

The `UpdateApplicationSettingsAndPolicies` administrative right (system administrators), the same as the other application settings APIs.

Whether content search is on is public: [GetApplicationParameters](getApplicationParameters.md) returns it to everyone as `INDEXSRV`.

## Example

### Request (POST)
```
POST /srv.asmx/GetContentSearchSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

## Notes

- The settings are kept in their own file, `config\content-search-setting.json` in infoRouter's application folder, not in `appsettings.json`. Without that file content search is off (`IndexSrv` `false`, the other values empty or default).
- The answer is what infoRouter is using now: the file as it was last read (at start or by [FlushApplicationCache](FlushApplicationCache.md)), or as SetContentSearchSettings last saved it. A change made to the file by hand is used after FlushApplicationCache or a restart.
- A catalog infoRouter cannot use here, written in the file by hand (`SYSTEMINDEX` on an infoRouter that does not run on Windows, for instance), does not stop infoRouter from starting: it is returned as it is, the problem is written to the error log, and keyword searches fail, saying why, until it is corrected.
- infoRouter 8.7 kept `INDEXSRV` and `INDEXCATALOG` in `web.config`; the upgrade to 9.0 moves them to this file.
