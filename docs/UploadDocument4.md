# UploadDocument4 API

Uploads a new document or creates a new version of an existing document at the specified path using a raw byte array, with extended options supplied through an XML parameters string. This is the most flexible direct-upload variant and supports all upload options including version comment, checkout, publish option, keywords, text-only content, custom dates, and more.

## Endpoint

```
/srv.asmx/UploadDocument4
```

## Methods

- **POST** `/srv.asmx/UploadDocument4` (form data — recommended for binary content)
- **SOAP** Action: `http://tempuri.org/UploadDocument4`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `fileContent` | byte[] | Yes | The raw binary content of the file, encoded as Base64 when sent over HTTP. |
| `xmlParameters` | string | Yes | XML string containing additional upload options. See the XML Parameters section below. Pass an empty string `""` for default behavior. |

---

## XML Parameters Format

The `xmlParameters` value is an XML string. The root element is `<xmlparameters>` and each option is an `<item>` element with `NAME` and `VALUE` attributes:

```xml
<xmlparameters>
  <item NAME="TEXTONLYCONTENT" VALUE="lorem dolor sit amet.."/>
  <item NAME="DESCRIPTION" VALUE="this is the sample description of this document"/>
  <item NAME="VERSIONCOMMENT" VALUE="sample version comment from the author."/>
  <item NAME="CHECKOUT" VALUE="TRUE"/>
  <item NAME="MPVERSIONMAJOR" VALUE="1"/>
  <item NAME="MPVERSIONMINOR" VALUE="0"/>
  <item NAME="MPVERSIONREVISION" VALUE="0"/>
  <item NAME="PUBLISHOPTION" VALUE="Publish"/>
  <item NAME="KEYWORDS" VALUE="finance quarterly 2024"/>
  <item NAME="SENDEMAILS" VALUE="true"/>
  <item NAME="CREATIONDATE" VALUE="2024-01-15"/>
  <item NAME="MODIFICATIONDATE" VALUE="2024-03-31"/>
</xmlparameters>
```

All `NAME` values are case-insensitive. If `VALUE` is omitted the element's inner text is used instead.

### Supported XML Parameter Keys

| Key | Type | Description |
|-----|------|-------------|
| `TEXTONLYCONTENT` | string | Plain-text content for full-text indexing (useful for image-only documents). |
| `DESCRIPTION` | string | Document description. |
| `KEYWORDS` | string | Comma-separated keywords. A keyword may be a phrase ("acceptance letter"); spaces do not separate keywords. |
| `VERSIONCOMMENT` | string | Version comment recorded in version history. |
| `CHECKOUT` | bool (`true`/`false`) | Lock document immediately after upload. |
| `PUBLISHOPTION` | enum | Publishing behavior: `ServerDefault`, `Publish`, `DontPublish`. |
| `SENDEMAILS` | bool (`true`/`false`) | Whether to send notification emails on upload. Default: `true`. |
| `CREATIONDATE` | DateTime | Override the document creation date (e.g. `2024-01-15`). |
| `MODIFICATIONDATE` | DateTime | Override the document modification date (e.g. `2024-03-31`). |
| `MPVERSIONMAJOR` | short | Major component of the manual version number (e.g. `2` for v2.0.1). Range: 1–2400. |
| `MPVERSIONMINOR` | short | Minor component of the manual version number (e.g. `0` for v2.0.1). Range: 0–999. |
| `MPVERSIONREVISION` | short | Revision component of the manual version number (e.g. `1` for v2.0.1). Range: 0–999. |

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000004" />
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

The calling user must have **write** (upload) permission on the destination folder.

---

## Example

### POST Request

```
POST /srv.asmx/UploadDocument4 HTTP/1.1
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="authenticationTicket"

3f2504e0-4f89-11d3-9a0c-0305e82c3301
------FormBoundary
Content-Disposition: form-data; name="path"

/Finance/Reports/Q1-2024-Report.pdf
------FormBoundary
Content-Disposition: form-data; name="fileContent"; filename="Q1-2024-Report.pdf"
Content-Type: application/octet-stream

[binary file content]
------FormBoundary
Content-Disposition: form-data; name="xmlParameters"

<xmlparameters><item NAME="VERSIONCOMMENT" VALUE="Revised Q1 figures"/><item NAME="KEYWORDS" VALUE="finance quarterly 2024"/><item NAME="PUBLISHOPTION" VALUE="Publish"/></xmlparameters>
------FormBoundary--
```

---

## JavaScript

```javascript
// Anything carrying bytes is POST-only: a byte[] cannot be bound from a query string, and a GET is
// answered HTTP 415 before the operation runs.
async function post(action, fields) {
  const response = await fetch(`/srv.asmx/${action}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ authenticationTicket: ticket, ...fields })
  });

  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}

const base64 = bytes => btoa(String.fromCharCode(...bytes));
```

```javascript
await post('UploadDocument4', {
  Path: '/Finance/Reports/Q1.pdf',
  FileContent: base64(bytes),
  xmlParameters:
    '<parameters>' +
      '<parameter Name="DESCRIPTION" Value="Q1 figures" />' +
      '<parameter Name="KEYWORDS" Value="quarterly,finance" />' +
      '<parameter Name="VERSIONCOMMENT" Value="Corrected after review" />' +
      '<parameter Name="CHECKOUT" Value="YES" />' +
    '</parameters>'
});
```

The parameter document is the same one [CreateHtmlDocument](CreateHtmlDocument.md) takes, with the
same two traps: **it is required even when empty** - send `<parameters />` - and a **malformed one is
answered HTTP 500 with no error document at all**, because the parse runs before the operation is
entered and outside any handler. Boolean values take English words only (`ON`, `TRUE`, `T`, `YES`,
`Y`, `1` and their negatives), whatever language the refusal message arrives in.

### The upload family

Two ways in. Either the bytes travel with the call, or they are staged first and the call names the
handler that holds them.

| Bytes with the call | Staged, by handler | Adds |
|---|---|---|
| [UploadDocument](UploadDocument.md) | [UploadDocumentWithHandler](UploadDocumentWithHandler.md) | nothing |
| [UploadDocument1](UploadDocument1.md) | [UploadDocumentWithHandler1](UploadDocumentWithHandler1.md) | a version comment |
| [UploadDocument2](UploadDocument2.md) | | the `Checkout` flag |
| [UploadDocument3](UploadDocument3.md) | [UploadDocumentWithHandler2](UploadDocumentWithHandler2.md) | a comment, and a checkout flag or a version number |
| [UploadDocument4](UploadDocument4.md) | [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) | a parameter document |
| | [UploadNewDocumentWidthHandler](UploadNewDocumentWidthHandler.md) | a folder and a name instead of one path |

**Uploading over a document that already exists is a new version, and only whoever holds the checkout
may make one.** Without a checkout the answer is `4000` "this document is not checked out". The
`Checkout` flag means *check it out for me if it is not already*: the operation then checks out,
uploads and checks back in, leaving the document free. It does not mean "leave it checked out".

## Notes

- Passing an empty string `""` for `xmlParameters` uses server defaults for all options.
- `PUBLISHOPTION` values: `ServerDefault` (use the domain's publishing setting), `Publish` (publish immediately), `DontPublish` (do not publish).
- Manual version numbers (`MPVERSIONMAJOR`, `MPVERSIONMINOR`, `MPVERSIONREVISION`) set the human-readable version label (e.g. `2.0.1`) independently of the internal version ID.
- For large files, use the chunked handler approach with `UploadDocumentWithHandler3` which accepts the same XML parameters format.

---

## Related APIs

- [UploadDocument](UploadDocument.md) - Basic upload
- [UploadDocument3](UploadDocument3.md) - Upload with version comment and checkout (no XML)
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) - Chunked upload with XML parameters
- [CreateUploadHandler](CreateUploadHandler.md) - Create a handler for chunked large file uploads

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | a document is already at that path and is not checked out by the caller |
| `4041` | no folder at the parent of the path |
| `4030` | the caller may not add documents there, or the folder rules forbid the file type |
| `4000` | a boolean parameter carried a value that is not one of the English words |
| `HTTP 415` | the call was a GET; the content can only be posted |
| `HTTP 400` | `xmlParameters` was empty; it is required, so send `<parameters />` |
| `HTTP 500` | `xmlParameters` was not well-formed XML; the exception escapes and there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The destination folder in the path does not exist. |
| Invalid parameter value | An XML parameter key has an invalid value (e.g. bad enum or non-boolean for `CHECKOUT`). |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
