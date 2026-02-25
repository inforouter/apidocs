# SetGeneralAppSettings API

Updates the global *General Application Settings* by sending a serialized `GeneralSettings` object. Use this API when you need to modify upload limits, recycle bin policies, workdays/holidays, or other platform-wide configuration options in a single atomic operation.

## Endpoint

```
/srv.asmx/SetGeneralAppSettings
```

## Methods

- **GET** `/srv.asmx/SetGeneralAppSettings?authenticationTicket=...&settingsXml=...`
- **POST** `/srv.asmx/SetGeneralAppSettings` (form data)
- **SOAP** Action: `http://tempuri.org/SetGeneralAppSettings`

> The `settingsXml` value must contain the `GeneralSettings` XML. Always URL-encode the XML when calling the GET endpoint.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Ticket returned by `AuthenticateUser`. The caller must have permission to update application settings. |
| `settingsXml` | string | Yes | XML representation of the `GeneralSettings` object. Obtain the current structure via `GetGeneralAppSettings`, update the desired values, then submit the modified XML here. |

## Response

### Success

```xml
<root success="true" />
```

### Error

```xml
<root success="false" error="[2730]Insufficient rights. Anonymous users cannot perform this action" />
```

Typical errors:
- `[2730]` when the user is not authenticated or lacks admin rights
- `Invalid settings XML format` when the payload cannot be deserialized
- The message returned by `UpdateGeneralApplicationSettings` (for validation failures)

## Required Permissions

- `UpdateApplicationSettingsAndPolicies` admin permission (can be verified in Control Panel ? System Administration ? Security Policies)
- Only authenticated administrators can invoke this method

## Example (REST POST)

```
POST /srv.asmx/SetGeneralAppSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=6F9C2A...&
settingsXml=%3CGeneralSettings%3E...%3C%2FGeneralSettings%3E
```

### SOAP Request

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/SetGeneralAppSettings"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetGeneralAppSettings xmlns="http://tempuri.org/">
      <authenticationTicket>6F9C2A...</authenticationTicket>
      <settingsXml><![CDATA[
        <GeneralSettings>
          <UploadSettings>
            <DocumentMaxSize>524288000</DocumentMaxSize>
            <FileUploadTimeOut>900</FileUploadTimeOut>
            <DefaultUploadFileChunkSize>8388608</DefaultUploadFileChunkSize>
          </UploadSettings>
          <AllowOwnershipTransfer>true</AllowOwnershipTransfer>
          <WebDav>false</WebDav>
          <DisplayAddIns>true</DisplayAddIns>
          <SearchPageSize>50</SearchPageSize>
          <SystemRecycleBinAutoPurgeOption>6</SystemRecycleBinAutoPurgeOption>
          <MoveUsersRecycleBinToSystemRecycleBinIn>3</MoveUsersRecycleBinToSystemRecycleBinIn>
          <RerouteRedirections>false</RerouteRedirections>
          <MinYearInDateControls>1950</MinYearInDateControls>
          <SendDiagnosticsAndStatistics>true</SendDiagnosticsAndStatistics>
          <Workdays>
            <Monday>true</Monday>
            <Tuesday>true</Tuesday>
            <Wednesday>true</Wednesday>
            <Thursday>true</Thursday>
            <Friday>true</Friday>
            <Saturday>false</Saturday>
            <Sunday>false</Sunday>
            <StartHour>8</StartHour>
            <StartMinute>0</StartMinute>
            <EndHour>18</EndHour>
            <EndMinute>0</EndMinute>
          </Workdays>
          <HolidayList>
            <Holiday>
              <HolidayDate>2025-01-01T00:00:00</HolidayDate>
              <Description>New Year</Description>
            </Holiday>
            <Holiday>
              <HolidayDate>2025-07-04T00:00:00</HolidayDate>
              <Description>Independence Day</Description>
            </Holiday>
          </HolidayList>
          <ZipDownloadSetting>
            <Enabled>true</Enabled>
            <MaxTotalSize>209715200</MaxTotalSize>
            <MaxTotalCount>500</MaxTotalCount>
          </ZipDownloadSetting>
        </GeneralSettings>
      ]]></settingsXml>
    </SetGeneralAppSettings>
  </soap:Body>
</soap:Envelope>
```

## Sample `settingsXml` Payload

```xml
<GeneralSettings>
  <UploadSettings>
    <DocumentMaxSize>524288000</DocumentMaxSize>
    <FileUploadTimeOut>900</FileUploadTimeOut>
    <DefaultUploadFileChunkSize>8388608</DefaultUploadFileChunkSize>
  </UploadSettings>
  <AllowOwnershipTransfer>true</AllowOwnershipTransfer>
  <WebDav>false</WebDav>
  <DisplayAddIns>true</DisplayAddIns>
  <SearchPageSize>20</SearchPageSize>
  <SystemRecycleBinAutoPurgeOption>6</SystemRecycleBinAutoPurgeOption>
  <MoveUsersRecycleBinToSystemRecycleBinIn>3</MoveUsersRecycleBinToSystemRecycleBinIn>
  <RerouteRedirections>false</RerouteRedirections>
  <MinYearInDateControls>1950</MinYearInDateControls>
  <SendDiagnosticsAndStatistics>true</SendDiagnosticsAndStatistics>
  <Workdays>
    <Monday>true</Monday>
    <Tuesday>true</Tuesday>
    <Wednesday>true</Wednesday>
    <Thursday>true</Thursday>
    <Friday>true</Friday>
    <Saturday>false</Saturday>
    <Sunday>false</Sunday>
    <StartHour>8</StartHour>
    <StartMinute>0</StartMinute>
    <EndHour>18</EndHour>
    <EndMinute>0</EndMinute>
  </Workdays>
  <HolidayList>
    <Holiday>
      <HolidayDate>2025-01-01T00:00:00</HolidayDate>
      <Description>New Year</Description>
    </Holiday>
  </HolidayList>
  <ZipDownloadSetting>
    <Enabled>true</Enabled>
    <MaxTotalSize>209715200</MaxTotalSize>
    <MaxTotalCount>1000</MaxTotalCount>
  </ZipDownloadSetting>
</GeneralSettings>
```

> **Important:** The `HolidayList` element is required if you want to persist holidays. If you omit it, existing holiday definitions will be cleared.

## Usage Guidelines

1. Call `GetGeneralAppSettings` to retrieve the current settings.
2. Modify only the values you need to change; keep the structure intact.
3. Validate business rules (e.g., recycle bin values between `0-36`, document max size ? `1 GB`).
4. Submit the updated XML via `SetGeneralAppSettings`.
5. On success, settings are refreshed in memory automatically and take effect immediately.

## Notes

- All numeric values are expressed in *bytes* unless the property name indicates minutes/hours.
- Upload limits must stay within the server's IIS `maxRequestLength` and execution timeout settings.
- Holidays are serialized through `HolidayList` (dictionary values are not serialized directly).
- Failure responses always include a localized message in the `error` attribute.
- Because this API overwrites the entire `GeneralSettings` object, avoid sending partial XML documents.
- Audit and change tracking should be handled at the application level by storing copies of previous XML payloads.