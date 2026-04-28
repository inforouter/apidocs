# UploadZipWithHandler API

Imports a ZIP archive as a folder and document structure into the specified folder. The ZIP file is supplied as a pre-uploaded chunked upload handler GUID rather than raw bytes, making this the recommended approach for large ZIP archives.

## Endpoint

```
/srv.asmx/UploadZipWithHandler
```

## Methods

- **GET** `/srv.asmx/UploadZipWithHandler?authenticationTicket=...&folderPath=...&uploadHandler=...&changedOnly=...&checkOutCheckIn=...&sendEmail=...`
- **POST** `/srv.asmx/UploadZipWithHandler` (form data)
- **SOAP** Action: `http://tempuri.org/UploadZipWithHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `folderPath` | string | Yes | Full infoRouter path of the destination folder (e.g. `/Domain/Folder`). The folder must exist |
| `uploadHandler` | string (GUID) | Yes | Upload handler GUID returned by `CreateUploadHandler` after all chunks have been sent via `UploadFileChunk` |
| `changedOnly` | bool | Yes | When `true`, existing documents are updated only if the uploaded content differs from the current version. When `false`, all matching documents are updated regardless |
| `checkOutCheckIn` | bool | Yes | When `true`, existing documents are checked out before update and checked back in afterwards. Automatically applied when `changedOnly` is `true` |
| `sendEmail` | bool | Yes | When `true`, email notifications are sent to folder subscribers |

## Chunked Upload Workflow

```
1. CreateUploadHandler   — negotiate chunk size, receive handler GUID
2. UploadFileChunk       — send ZIP file chunks sequentially with per-chunk CRC32
3. UploadZipWithHandler  — trigger the import using the completed handler
4. DeleteUploadHandler   — release the server-side temp file (optional but recommended)
```

Each chunk must include a CRC32 hex checksum of that chunk's bytes (`ChunkHEXCRC`). On the last chunk the server returns the accumulated `filehexcrc` of the entire file — compare it against your locally computed file CRC to verify a clean transfer. If they differ, abort and retry the upload from step 1.

The server may respond with `tryagain="true"` on a transient failure for a single chunk — retry that same chunk without advancing the offset.

---

### JavaScript Sample

The sample below uses the browser `File` API and `fetch`. It covers all four steps, computes CRC32 in-browser, handles `tryagain` retries, verifies the final file checksum, and explicitly deletes the upload handler after a successful import.

{% raw %}
```javascript
/**
 * Upload a ZIP archive to infoRouter using the chunked upload API.
 *
 * @param {string}  baseUrl               Server root, e.g. "https://your-server"
 * @param {string}  authenticationTicket  Ticket from AuthenticateUser
 * @param {File}    file                  ZIP file object from <input type="file">
 * @param {string}  folderPath            Destination folder, e.g. "/Domain/Imports"
 * @param {boolean} changedOnly           Update existing docs only when content differs
 * @param {boolean} checkOutCheckIn       Use checkout/checkin flow for existing docs
 * @param {boolean} sendEmail             Send email notifications to subscribers
 * @returns {% raw %}{{ success: boolean, logs: Array<{ item: string, error: string }> }}{% endraw %}
 */
async function uploadZipWithChunks(baseUrl, authenticationTicket, file, folderPath, changedOnly, checkOutCheckIn, sendEmail) {
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

  // ── Step 4: Trigger the ZIP import ───────────────────────────────────────
  const finalXml = await post("UploadZipWithHandler", {
    authenticationTicket,
    folderPath,
    uploadHandler,
    changedOnly:     String(changedOnly),
    checkOutCheckIn: String(checkOutCheckIn),
    sendEmail:       String(sendEmail)
  });

  if (finalXml.getAttribute("success") !== "true")
    throw new Error("UploadZipWithHandler failed");

  // ── Step 5: DeleteUploadHandler ───────────────────────────────────────────
  // Release the server-side temp file immediately. The server would eventually
  // clean it up on its own, but calling this right after a successful import
  // frees the storage without waiting for the background cleanup interval.
  await post("DeleteUploadHandler", { authenticationTicket, uploadHandler });

  // Collect log entries from the response
  const logs = [...finalXml.querySelectorAll("logs > log")].map(log => ({
    item:  log.querySelector("item")?.textContent  ?? "",
    error: log.querySelector("error")?.textContent ?? ""
  }));

  return { success: true, logs };
}
```
{% endraw %}

#### Usage

```javascript
document.getElementById("uploadBtn").addEventListener("click", async () => {
  const file = document.getElementById("fileInput").files[0];

  try {
    const { logs } = await uploadZipWithChunks(
      "https://your-inforouter-server",
      "your-auth-ticket",
      file,
      "/MyDomain/Imports",
      true,   // changedOnly
      true,   // checkOutCheckIn
      false   // sendEmail
    );
    console.log("Import complete. Log entries:", logs);
  } catch (err) {
    console.error("Upload failed:", err.message);
  }
});
```

---

## Response

### Success

```xml
<root success="true">
  <logs />
</root>
```

The `<logs>` element is empty on a fully successful import. Log entries are only written for items that could not be processed.

### Failure

```xml
<root success="false">
  <logs>
    <log><item>upload.zip</item><error>Unzip operation failed: invalid ZIP format</error></log>
  </logs>
</root>
```

### Error (authentication, folder, or handler)

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

- User must be authenticated.
- Caller must have document creation permission on the destination folder.
- If the folder rule `DisallowNewDocument` is set, the import will be rejected.

## Example Requests

### Request (POST)

```
POST /srv.asmx/UploadZipWithHandler HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&folderPath=/MyDomain/Imports&uploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890&changedOnly=true&checkOutCheckIn=true&sendEmail=false
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/UploadZipWithHandler"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <UploadZipWithHandler xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <folderPath>/MyDomain/Imports</folderPath>
      <uploadHandler>a1b2c3d4-e5f6-7890-abcd-ef1234567890</uploadHandler>
      <changedOnly>true</changedOnly>
      <checkOutCheckIn>true</checkOutCheckIn>
      <sendEmail>false</sendEmail>
    </UploadZipWithHandler>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Folder not found | The specified `folderPath` does not exist |
| Invalid upload handler | The `uploadHandler` GUID is not a valid GUID format |
| Handler not found / expired | The handler GUID is valid but the server-side temp file no longer exists |
| Access denied | Caller lacks document creation permission on the destination folder |
| Unzip operation failed | The uploaded bytes are not a valid ZIP archive |

## Notes

- The ZIP archive's internal folder structure is recreated under the destination folder.
- `changedOnly=true` implicitly enables `checkOutCheckIn` behaviour.
- Classification level, importance, and retention schedule are always applied with system defaults.
- The `<logs>` response children are always emitted and describe each item processed during import.
- For small ZIP files where chunked upload is not required, use `UploadZip` instead.

## Related APIs

- `CreateUploadHandler` — Create an upload handler and negotiate chunk size
- `UploadFileChunk` — Upload a single binary chunk to the handler
- `DeleteUploadHandler` — Release the server-side temp file after a successful import
- `UploadZip` — Import a ZIP archive supplied as raw bytes (no chunking)
- `GetFoldersAndDocuments` — Browse folder contents to find the destination folder path
