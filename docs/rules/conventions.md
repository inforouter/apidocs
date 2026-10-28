# Conventions: how an answer is read

Every call answers XML with HTTP 200, success or not, so the attributes are what to read. This page says what
the codes mean, what a partial success looks like, and a few things that surprise first-time callers.

## The rule

`success="true"` or `"false"`; on a refusal `errorCode` says why in a number and `error` says it in the
caller's language. The code is the HTTP status the refusal corresponds to, times ten, so a client that knows
HTTP knows the bands. The text is for people and changes with the language; branch on the code.

## The bands

| `errorCode` | Meaning | Typical cause |
|---:|---|---|
| `4000` | Bad request | A parameter the server could not accept: a name with a character it does not allow, a value out of range, a state the action does not fit (not checked out, not active, frozen) |
| `4010` | Not authenticated | The ticket is expired or unknown |
| `4030` | Access denied | The caller lacks the right, the role or the ownership the action needs |
| `4041` | Not found | No document, folder, library, user or group of that name or id reachable by the caller |
| `4080` | Request timeout | An upload past the allowed time |
| `4090` | Already exists | A name already taken where names must be unique |
| `4170` | Expectation failed | A value of the wrong shape, such as `~L` followed by something that is not an id |
| `4200` | Unclassified | A refusal the server could not place in a band; rare, and each site is being classified |
| `4230` | Locked | Checked out by somebody else, frozen, offline, in a workflow: the caller may get it later |
| `5000` | Server error | Something went wrong on the server; the text names it |
| `5030` | Service unavailable | A service the server depends on is down: Connect, search, mail |
| `6000` | Licence | The licence does not allow it: library count, user count |
| `2070` | MultiStatus | Part of the work was done and part refused; see below |

## MultiStatus

An operation that walks a tree and acts on each item - SetOwner, the folder forms of DisposeItem,
TransferToExternalAgency, SetFolderCutoffDate, CreateDomainFromTemplate - does not stop at the first refusal. It
logs the item and goes on, and answers `success="false"` with `errorCode="2070"` and one `<log>` entry per refused
item, each with `<item>` and `<error>`. Everything not in the log was done. A caller that wants all or nothing
must undo it; the operation's page says how.

## Things that surprise

- **No ticket at all is not `4010`.** A call with no ticket runs as the anonymous user, and is refused the
  right, `4030`, or finds nothing, `4041`. `4010` is a ticket that is expired or unknown.
- **A missing required string is not an XML answer.** A REST call that leaves out a required string parameter is
  refused by model binding with HTTP 400 and no `<response>` element at all. Optional strings may be left out.
- **Not found can mean not reachable.** A library the caller cannot reach answers `4041`, the same as one that
  does not exist, on purpose: a refusal would tell the caller what exists. The same for users and groups behind
  the administrator-account guard.
- **Libraries are domains.** The operations say Domain, the messages say library, the element is `<domain>`,
  and its flags are the words `TRUE` and `FALSE`. A library can be named by `~L` and its id wherever a library
  name is taken.
- **A name with a special character is refused**, `4000`, for libraries, folders, documents and groups; the
  message names the character. Folder names were cleaned up silently once; they are not any more.
- **Reads before rights are gone.** Where a call used to look something up and only then ask the right, it asks
  the right first since the role review, so a caller without it sees `4030` and learns nothing.

## For developers

- The bands: `enum_IR.IrErrorNumbers` (`IRBase/IRBaseEnum.cs`). `Result<T>` and `ActionResult` carry the
  code from the operation to the answer; `ApiHelper.WebServiceError` writes it.
- MultiStatus: `ApiHelper.LogResultMultiStatus` and `ResponseLogger`.
