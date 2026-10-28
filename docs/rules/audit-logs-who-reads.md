# Which logs exist, and who reads each

infoRouter keeps several logs. They are not one thing with one reader: some follow the item, some follow the
user, some are the server's own. This page says who reads which.

## The rule

A log **about an item** is read by whoever holds the matching right on the item, and by the item's library
managers; **Audit Managers** read it without the right. A log **about a user** (what they viewed, subscribed,
favourited) is read by the user, by User Managers and by the user's library managers. The **server's** logs
and status are read by administrators and Audit Managers. Date-range logs across the system are Audit Managers'.

## Logs about items

| Log | Operation | Reads it |
|---|---|---|
| SOX log | GetSoxLogs | `DocumentReadSoxLog` on the document, library managers, Audit Managers |
| ISO log | GetISOLogs | `DocumentReadIsoLog` on the document, library managers, Audit Managers |
| Classification log | GetClassificationLogs | The library policy `DocumentReadClassificationLog` (owner, library managers, Full Control by default), then Audit Managers |
| Access list history of an item | GetAccessListHistory | `ReadSecurityAccessList` on the item, or Audit Managers and the item's library managers without it |
| Security changes under a path | GetSecurityChangeLog | Library managers for their library (the root included), Audit Managers |
| Who read a document | GetDocumentReadLogHistory | `DocumentReadViewLog` on the document |

These load the item first, and the item lookup has no role bypass: an Audit Manager reads an item's log only in
a library they can reach as a member (open decision 48 of the role review: by design, as for R&D Managers, or
a bypass for the role).

## Logs about users

| Log | Operation | Reads it |
|---|---|---|
| What a user viewed | GetUserViewLog, GetUserViewLog1, GetUserViewLogLite | The user, User Managers, the user's library managers (`ListingAuditLogOfUser`) |
| A user's subscriptions, favourites, download queue, and the search criteria that list them | GetSubscribedDocumentsByUser, GetFavoriteDocumentsOfUser, Search with SUBSCRIPTIONSOF / FAVORITESOF / DOWNLOADQUEOF / VIEWCRITERIA+USERNAME | The same |

Audit Managers are not among the readers of a user's view log (open decision 49). Who holds a document
checked out is shown on the document to anyone who can read it, and the CHECKEDOUTBYUSER criterion follows that.

## Date-range logs and the server's own

| Log | Operations | Reads it |
|---|---|---|
| Checkouts, check-ins, deletes, moves, renames, creates and the rest, over a period, optionally filtered by a library path | GetCheckoutLog, GetCheckInLog and the other date-range logs | Audit Managers; a library filter is resolved by name whether or not the caller is a member |
| Server logs and statistics | GetLogs, GetLogStatistics, GetLogStatistics1 | Administrators and Audit Managers |
| Licence, server status, warehouse status | GetLicenseInfo, GetServerStatus and kin | Administrators and Audit Managers |

## What the server answers

`4030` for a caller none of the readers; `4041` for an item or library the caller cannot reach; an unknown
library name in a date-range filter is `4041` for an Audit Manager and `4030` for anyone else, so the filter
does not tell a non-reader what exists.

## For developers

- The rule: `LogOperations` (`IsLogAccessAllowed`, `GetAccessListHistoryAsync`, `GetClassificationLogsAsync`),
  `DocumentExtensions.GetSoxLogsAsync` and kin, `ServerLogs`.
- Tests: `AuditLogBatchApiTests`, `ServerAndLicenseBatchApiTests`, `SearchBatchApiTests`.
- Role page: [Audit Managers](../AuditManagersRole.md).
- Two refusals still answer `4000` instead of `4030` (GetSoxLogs without the right, GetUserGroupMembers on a
  hidden group): treat them as refusals (open item 40).

## Since

- **9.0 (October 2026, the role review):** server logs opened to Audit Managers; the library root's security
  log to its managers; access list history to Audit Managers without the item right; the classification log
  follows the library policy; date-range filters resolve a library the Audit Manager is not a member of; the
  user-activity search criteria ask the same right as the dedicated calls.
