---
search:
  exclude: true
---

# SetContentSearchSettings API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Replaces the content search settings and applies them at once, without restarting infoRouter. Then asks the search service whether it answers with them and returns the answer. Administrators only; [GetContentSearchSettings](GetContentSearchSettings.md) reads them.

## Endpoint

```
/api/UIInternals/SetContentSearchSettings
```

## Methods

- **GET** `/api/UIInternals/SetContentSearchSettings?authenticationTicket=...&indexSrv=...&indexCatalog=...&remoteSearchApiKey=...&remoteSearchIndexNotify=...&checkSecurityOnSearch=...&maxContentSearchResult=...`
- **POST** `/api/UIInternals/SetContentSearchSettings` (form data)

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `indexSrv` | bool | Yes | `true` turns content search on, `false` turns it off |
| `indexCatalog` | string | When `indexSrv` is `true` | The catalog's address on the infoRouter Search Service, `http://server:port/catalog-name/` (http:// or https://), as the service's administration page shows it; or `SYSTEMINDEX` for Windows Search. May be empty while content search is off |
| `remoteSearchApiKey` | string | No | The catalog's API key, as the search service's administration page shows it. Empty: no key is sent |
| `remoteSearchIndexNotify` | bool | No | `true` (default): the search service is told which documents changed, so they are searchable within seconds. `false`: its nightly rescan finds the changes |
| `checkSecurityOnSearch` | bool | No | `true`: each search hit's permission is checked again while result pages are built (every search, not only content search). Left out: unchanged |
| `maxContentSearchResult` | int | No | The most hits a content search takes from the search engine, 1 to 1,000,000. Left out: unchanged |

The first four settings are replaced: to change one, send the others as GetContentSearchSettings returned them. `checkSecurityOnSearch` and `maxContentSearchResult` are optional; left out, they stay as they are. `indexCatalog` and `remoteSearchApiKey` are trimmed.

## Response

### Success Response
```xml
<response success="true" error="">
  <Connection>
    <Checked>true</Checked>
    <Connected>true</Connected>
    <ServiceVersion>2.2.317</ServiceVersion>
  </Connection>
</response>
```

The settings are saved and in use. `Connection` says whether the search service answers with them:

| Element | Type | Description |
|---------|------|-------------|
| `Checked` | bool | `false` when there was nothing to ask: content search off, or Windows Search |
| `Connected` | bool | `true`: the search service answered and accepted the API key |
| `ServiceVersion` | string | The search service's version; only when it answered |
| `Error` | string | Why the search service did not answer; only when it did not |

A search service that does not answer does not stop the save:

```xml
<response success="true" error="">
  <Connection>
    <Checked>true</Checked>
    <Connected>false</Connected>
    <Error>No connection could be made because the target machine actively refused it. (search01:5000)</Error>
  </Connection>
</response>
```

### Error Response
```xml
<response success="false" error="[ErrorCode] Error message" errorCode="4000" />
```

| errorCode | When |
|-----------|------|
| 4000 | `indexCatalog` is neither an http:// or https:// address nor `SYSTEMINDEX`, or it is empty while `indexSrv` is `true` |
| 4000 | `SYSTEMINDEX` with `indexSrv` `true` on an infoRouter that does not run on Windows |
| 4000 | `maxContentSearchResult` is not between 1 and 1,000,000 |
| 4010 | No authentication ticket, or an invalid or expired one |
| 4030 | The user is not allowed to change application settings |

Nothing is changed when the call fails.

## Required Permissions

The `UpdateApplicationSettingsAndPolicies` administrative right (system administrators), the same as the other application settings APIs.

## Example

### Request (POST)
```
POST /api/UIInternals/SetContentSearchSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&indexSrv=true&indexCatalog=http%3A%2F%2Fsearch01%3A5000%2Fcorp%2F&remoteSearchApiKey=3f9c0d...&remoteSearchIndexNotify=true
```

## Notes

- The settings are saved to `config\content-search-setting.json` in infoRouter's application folder, and searches started after the call use them; a search already running finishes with the settings it started with. Change notices switch at the same time, and those queued for the previous search service are still sent to it.
- [GetApplicationParameters](../getApplicationParameters.md) shows the new `INDEXSRV` at once.
- To change the file by hand instead, edit it and call [FlushApplicationCache](FlushApplicationCache.md); infoRouter reads it again without a restart. A catalog this call refuses (see Error Response) is accepted from the file but does not work: keyword searches fail, saying why.
- The catalog's address and key come from the infoRouter Search Service's administration page, under *Connection for infoRouter*. The address must name the catalog; the service's address alone is refused by the service.
- A search service that has no change notices (the infoRouter 8.7 dtSearch web service) answers them with "not found"; infoRouter then stops sending them until the settings are saved again or infoRouter restarts.
