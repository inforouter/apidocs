# GetConnectSettings API

Returns what this infoRouter instance can ask the **infoRouter Connect** AI service for: the capabilities the service offers, whether each one is usable right now, and the rules infoRouter applies to them.

Written for a caller building a UI — deciding which AI actions to offer, and what to say about the ones it cannot. Read it **once** when the UI loads rather than per document: it asks the Connect service a question of its own.

## Endpoint

```
/srv.asmx/GetConnectSettings
```

## Methods

- **GET** `/srv.asmx/GetConnectSettings?AuthenticationTicket=...`
- **POST** `/srv.asmx/GetConnectSettings` (form data)
- **SOAP** Action: `http://tempuri.org/GetConnectSettings`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

## Response

```xml
<response success="true" error="">
  <ConnectSettings configured="true" reachable="true" provisioned="true" scrubPii="true"
                   maxKeywordCount="10" storeOcrText="true"
>
    <SupportedExtensions>pdf,docx,xlsx,pptx,html,htm,txt,md,csv</SupportedExtensions>
    <Service aiReady="true" scrubbingReady="true" ocrAvailable="true"
             documentTypeReady="true" documentTypes="3" typesVersion="393781196">
      <TranslateLanguages>
        <Language code="en" name="English" />
        <Language code="tr" name="Turkish" />
      </TranslateLanguages>
    </Service>
    <Capabilities>
      <Capability key="summarize" usable="true" enabledOnService="true"
                  ready="true" operation="Analyze" />
      <Capability key="translate" usable="true" enabledOnService="true"
                  ready="true" />
    </Capabilities>
  </ConnectSettings>
</response>
```

### `<ConnectSettings>`

| Attribute | Description |
|-----------|-------------|
| `configured` | False when this instance has no Connect service configured at all. Everything below is then empty. |
| `reachable` | Whether the service answered. False leaves `<Capabilities>` empty and puts the reason in `error`. |
| `provisioned` | False when the service answers but has not been set up yet. |
| `scrubPii` | Whether documents are scrubbed of personal data on the way out by default. |
| `maxKeywordCount` | How many keywords are asked for when a request does not say. |
| `storeOcrText` | Whether text read out of a scan is kept on the document. |

> **Both confidence thresholds were removed in 9.0.** infoRouter no longer keeps a threshold of
> its own for either document type matching or extracted field values.
>
> The service decides how sure a document type match must be, in its own control panel, and
> reports the number it is using as `documentTypeThreshold` on the `<Service>` element below.
> infoRouter used to keep a second threshold beside it, which could silently override that panel.
>
> Extracted field values have no threshold at all now: whatever Connect finds is written, however
> unsure it was, because a value a person is going to review is worth more than the blank it would
> otherwise leave. How sure it was is reported per document as
> [AIExtractConfidence](GetDocument.md#aiextractconfidence).

`<SupportedExtensions>` is the comma separated list of file types the service is expected to be able to read here. A document of any other type is refused before a call is made — except OCR, which exists for exactly the file types this list leaves out.

### `<Service>`

What the service reports about itself. All of it can change without anybody touching a setting.

| Attribute | Description |
|-----------|-------------|
| `aiReady` | The AI side reports itself ready. |
| `scrubbingReady` | PII scrubbing can run. A request that needs scrubbing fails without it. |
| `ocrAvailable` | The scanned document OCR fallback is usable. |
| `documentTypeReady` | A document type list has been pushed and stored. |
| `documentTypes` | How many types the service holds. |
| `typesVersion` | The version of that list, as the service reports it. |
| `documentTypeThreshold` | How sure the service must be before it returns a document type match, as it reports it. `0` where the service did not answer. Reported, not set here - it is configured in the service's own control panel. |

`<TranslateLanguages>` lists what the service can translate between, each with the `code` a request sends. Absent when translation is not offered.

### `<Capability>`

One row per thing the service knows how to do. **Read `usable` to decide whether to offer it**; the other three say which of the three separate things is missing, which is what an administrator needs to fix it.

| Attribute | Description |
|-----------|-------------|
| `key` | The service's own name: `summarize`, `document_type`, `keywords`, `profile`, `extract_data`, `translate`, `extract_text`, `redaction`. |
| `usable` | True only when both of the below are true. |
| `enabledOnService` | An administrator has left it switched on at the Connect service. |
| `ready` | The service has a usable model behind it. True for capabilities that call no model. |
| `operation` | The operation infoRouter queues for it. Absent where infoRouter has none. |

**Label it yourself.** The row carries no display name on purpose: what to call a capability in front of a user is infoRouter's business, in infoRouter's languages, and a service's English label cannot be translated for you.

Two keys map to the same operation. Asking infoRouter which type a document is runs a **profile** call, which carries the match — so `document_type` and `profile` both report `operation="Profile"` and rise and fall together.

`translate` and `redaction` carry no `operation`: they are the service's own endpoints and nothing in infoRouter asks for them yet. They still report whether the service offers them, so a UI can know what is coming.

## Behavior

1. **Anonymous callers are refused.** Nothing secret is in the report, but what an instance is configured to do is not for a caller who has not signed in.
2. **A service that does not answer still produces a report.** `reachable="false"`, `error` says why, and everything this instance decides for itself is still there. A caller can tell "the service says no" from "the service said nothing".
3. **Nothing secret is included** — not the service token, not the address Connect answers on.
4. **It is a read.** Nothing is queued, and no AI call is made or paid for.

## Required Permissions

Any signed-in user. Anonymous access is refused.

## Example

### Request (GET)

```
GET /srv.asmx/GetConnectSettings?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301 HTTP/1.1
```

### Request (SOAP)

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetConnectSettings>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetConnectSettings>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Cache it. The report changes when an administrator changes something, not between two documents.
- A capability being `usable` is not a promise that a particular document can be processed: the file still has to be one the service can read. See `<SupportedExtensions>`.
- Ask for the work itself with [GetConnectProfile](GetConnectProfile.md), which reports per answer what became of the request.

## Error Codes

| Error | `errorcode` | Description |
|-------|-------------|-------------|
| `[900] Authentication failed` | `4010` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | `4010` | The ticket has expired or does not exist. |
| Insufficient rights. Anonymous users cannot perform this action. | `4010` | The caller has not signed in. |

## Related APIs

- [GetConnectProfile](GetConnectProfile.md) - Ask the service to produce content for a document
- [SetFolderAIPreferences](SetFolderAIPreferences.md) - Have content produced automatically on upload
- [GetLogs](GetLogs.md) - Read the daily record of the calls made to the service
