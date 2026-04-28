# UploadDocumentWithHandler3 API

Finalizes a chunked file upload and creates a new document or a new version of an existing document at the specified path, with extended options supplied through an XML parameters string. This is the most flexible handler-finalization method and supports all upload options including version comment, publish option, checkout, keywords, text-only content, manual version numbers, custom dates, and email notifications.

## Endpoint

```
/srv.asmx/UploadDocumentWithHandler3
```

## Methods

- **GET** `/srv.asmx/UploadDocumentWithHandler3?authenticationTicket=...&path=...&uploadHandler=...&xmlParameters=...`
- **POST** `/srv.asmx/UploadDocumentWithHandler3` (form data)
- **SOAP** Action: `http://tempuri.org/UploadDocumentWithHandler3`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `uploadHandler` | string (GUID) | Yes | The upload handler GUID returned by `CreateUploadHandler` after all chunks have been uploaded. |
| `xmlParameters` | string | Yes | XML string with additional upload options. Pass an empty string `""` for default behavior. See XML Parameters section below. |

---

## XML Parameters Format

The `xmlParameters` is an XML string with key-value pairs (same format as `UploadDocument4`):

```xml
<parameters>
  <parameter key="DESCRIPTION">Quarterly financial summary</parameter>
  <parameter key="KEYWORDS">finance quarterly 2024</parameter>
  <parameter key="VERSIONCOMMENT">Updated figures</parameter>
  <parameter key="CHECKOUT">true</parameter>
  <parameter key="PUBLISHOPTION">Publish</parameter>
  <parameter key="SENDEMAILS">true</parameter>
  <parameter key="TEXTONLYCONTENT">Plain text version of the document</parameter>
  <parameter key="CREATIONDATE">2024-01-15</parameter>
  <parameter key="MODIFICATIONDATE">2024-03-31</parameter>
  <parameter key="MPVERSIONMAJOR">2</parameter>
  <parameter key="MPVERSIONMINOR">0</parameter>
  <parameter key="MPVERSIONREVISION">1</parameter>
</parameters>
```

See `UploadDocument4` for the full list of supported XML parameter keys and their valid values.

---

## Chunked Upload Workflow

```
1. CreateUploadHandler        — negotiate chunk size, receive handler GUID
2. UploadFileChunk            — send chunks sequentially; include CRC32 per chunk
3. UploadDocumentWithHandler3 — finalize: set path, metadata, and XML parameters
4. DeleteUploadHandler        — release the server-side temp file immediately after success
```

Each chunk must include a CRC32 hex checksum of that chunk's bytes (`ChunkHEXCRC`). On the last chunk the server returns the accumulated `filehexcrc` of the entire file — compare it against your locally computed file CRC to verify a clean transfer. If they differ, abort and retry the upload from step 1.

The server may respond with `tryagain="true"` on a transient failure for a single chunk — retry that same chunk without advancing the offset.

---

### JavaScript Sample

The sample below uses the browser `File` API and `fetch`. It covers all four steps, computes CRC32 in-browser, handles `tryagain` retries, verifies the final file checksum, and explicitly deletes the upload handler after a successful finalization.

{% raw %}
```javascript
/**
 * Upload a file to infoRouter using the chunked upload API.
 *
 * @param {string} baseUrl               Server root, e.g. "https://your-server"
 * @param {string} authenticationTicket  Ticket from AuthenticateUser
 * @param {File}   file                  File object from <input type="file">
 * @param {string} irPath                Destination path, e.g. "/Finance/Reports/Q1.pdf"
 * @param {string} xmlParameters         XML options string, or "" for server defaults
 * @returns {{ documentId: string, versionId: string }}
 */
async function uploadWithChunks(baseUrl, authenticationTicket, file, irPath, xmlParameters) {
  const endpoint = `${baseUrl}/srv.asmx`;

  // ── CRC32 lookup table (IEEE 802.3 polynomial) ────────────────────────────
  const crcTable = (() => {
    const t = new Uint32Array(256);
    for (let i = 0; i < 256; i++) {
      let c = i;
      for (let j = 0; j < 8; j++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[i] = c;
    }
    return t;
  })();

  function crc32(bytes) {
    let crc = 0xFFFFFFFF;
    for (let i = 0; i < bytes.length; i++)
      crc = crcTable[(crc ^ bytes[i]) & 0xFF] ^ (crc >>> 8);
    return (crc ^ 0xFFFFFFFF) >>> 0;  // unsigned 32-bit
  }

  function toHex(n) { return n.toString(16).toUpperCase(); }

  function parseXml(text) {
    return new DOMParser().parseFromString(text, "text/xml").documentElement;
  }

  // POST application/x-www-form-urlencoded fields
  async function post(action, fields) {
    const res = await fetch(`${endpoint}/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(fields).toString()
    });
    return parseXml(await res.text());
  }

  // POST a single binary chunk as multipart/form-data
  async function postChunk(uploadHandler, chunkBytes, chunkHexCrc, lastChunk) {
    const form = new FormData();
    form.append("authenticationTicket", authenticationTicket);
    form.append("uploadHandler", uploadHandler);
    form.append("FileChunk", new Blob([chunkBytes]));
    form.append("ChunkHEXCRC", chunkHexCrc);
    form.append("LastChunk", String(lastChunk));
    const res = await fetch(`${endpoint}/UploadFileChunk`, { method: "POST", body: form });
    return parseXml(await res.text());
  }

  // ── Step 1: CreateUploadHandler ───────────────────────────────────────────
  const handlerXml = await post("CreateUploadHandler", {
    authenticationTicket,
    ChunkSize: 512 * 1024     // suggest 512 KB; server may return a different size
  });

  if (handlerXml.getAttribute("success") !== "true")
    throw new Error("CreateUploadHandler failed: " + handlerXml.getAttribute("error"));

  const uploadHandler = handlerXml.getAttribute("UploadHandler");
  const chunkSize     = parseInt(handlerXml.getAttribute("ChunkSize"), 10);

  // ── Step 2: Read file bytes and compute full-file CRC32 ───────────────────
  const fileBytes = new Uint8Array(await file.arrayBuffer());
  const fileCrc   = crc32(fileBytes);

  // ── Step 3: Upload chunks ─────────────────────────────────────────────────
  let offset = 0;
  while (offset < fileBytes.length) {
    const chunk     = fileBytes.slice(offset, offset + chunkSize);
    const chunkCrc  = crc32(chunk);
    const lastChunk = (offset + chunk.length) >= fileBytes.length;

    let xml;
    // Inner retry loop: repeat the same chunk if server responds tryagain="true"
    while (true) {
      xml = await postChunk(uploadHandler, chunk, toHex(chunkCrc), lastChunk);

      if (xml.getAttribute("success") === "true") break;

      if (xml.getAttribute("tryagain") === "true") continue;   // transient — retry

      throw new Error("UploadFileChunk failed: " + xml.getAttribute("error"));
    }

    // After the last chunk, verify the server's accumulated file CRC
    if (lastChunk) {
      const serverCrc = parseInt(xml.getAttribute("filehexcrc"), 16);
      if (serverCrc !== fileCrc)
        throw new Error(
          `File CRC mismatch — local: ${toHex(fileCrc)}, server: ${xml.getAttribute("filehexcrc")}`
        );
    }

    offset += chunk.length;
  }

  // ── Step 4: Finalize ──────────────────────────────────────────────────────
  const finalXml = await post("UploadDocumentWithHandler3", {
    authenticationTicket,
    path: irPath,
    uploadHandler,
    xmlParameters
  });

  if (finalXml.getAttribute("success") !== "true")
    throw new Error("UploadDocumentWithHandler3 failed: " + finalXml.getAttribute("error"));

  // ── Step 5: DeleteUploadHandler ───────────────────────────────────────────
  // Release the server-side temp file immediately. The server would eventually
  // clean it up on its own, but calling this right after a successful finalize
  // frees the storage without waiting for the background cleanup interval.
  await post("DeleteUploadHandler", { authenticationTicket, uploadHandler });

  return {
    documentId: finalXml.getAttribute("DocumentId"),
    versionId:  finalXml.getAttribute("VersionId")
  };
}
```
{% endraw %}

#### Usage

```javascript
document.getElementById("uploadBtn").addEventListener("click", async () => {
  const file = document.getElementById("fileInput").files[0];

  const xmlParameters = [
    "<parameters>",
    '  <parameter key="VERSIONCOMMENT">Uploaded via JS</parameter>',
    '  <parameter key="PUBLISHOPTION">Publish</parameter>',
    '  <parameter key="SENDEMAILS">true</parameter>',
    "</parameters>"
  ].join("\n");

  try {
    const { documentId, versionId } = await uploadWithChunks(
      "https://your-inforouter-server",
      "your-auth-ticket",
      file,
      "/Finance/Reports/" + file.name,
      xmlParameters
    );
    console.log("Uploaded — DocumentId:", documentId, "VersionId:", versionId);
  } catch (err) {
    console.error("Upload failed:", err.message);
  }
});
```

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000004" />
```

### Error Response

```xml
<root success="false" error="Invalid upload handler." />
```

---

## Required Permissions

The calling user must have **write** (upload) permission on the destination folder.

---

## Example

### POST Request

```
POST /srv.asmx/UploadDocumentWithHandler3 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&uploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
&xmlParameters=<parameters><parameter key="VERSIONCOMMENT">Revised figures</parameter><parameter key="PUBLISHOPTION">Publish</parameter></parameters>
```

---

## Notes

- Passing an empty string for `xmlParameters` uses server defaults.
- This is the recommended approach for large file uploads requiring full metadata control.
- See `UploadDocument4` for the complete XML parameter reference.

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for chunked uploads
- [UploadFileChunk](UploadFileChunk.md) - Upload a single chunk
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Basic handler finalization
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1.md) - Finalize with version comment
- [UploadDocumentWithHandler2](UploadDocumentWithHandler2.md) - Finalize with manual version numbers
- [UploadDocument4](UploadDocument4.md) - Direct byte-array upload with the same XML parameters

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid upload handler.` | The GUID is not a valid or active upload handler. |
| Invalid parameter value | An XML parameter key has an invalid value. |
| Folder not found | The destination folder in the path does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---