# How WebDAV maps onto documents

Word, Explorer and other WebDAV clients see infoRouter as a drive. Behind the drive are documents with
versions, checkouts and access lists, and each WebDAV verb is translated into one of those. This page says
what each verb does to the document, and what a client's save sequence ends up doing.

## The rule

A WebDAV **lock is a checkout** by the user who sent it, a **PUT onto an existing name is a new version**, and
a **MOVE or COPY onto an existing name is also a new version** of the document already there. A document is
never replaced by another document and never deleted by a save; it keeps its id, its versions, its property sets,
its access list and its subscriptions, whatever the client does. DELETE sends it to the recycle bin.

## Addresses

`/dav/<library>/<folder>/.../<document>`, for example `/dav/accounting/invoices/123.pdf`. Only libraries,
folders and documents are served; there are no other files on the drive.

## What each verb does

| Verb | On a document | Answers |
|---|---|---|
| LOCK | Checks the document out to the caller. Already checked out by the caller: the same lock again. Checked out by somebody else: refused. The advertised timeout is 900 seconds, but the checkout does not expire; it lasts until UNLOCK or a check-in. | `200`; `423` when another user holds it |
| UNLOCK | Checks the document in without making a version (the version was made by PUT). By a user who does not hold the checkout: refused. | `204`; `412` for another user |
| PUT, new name | Creates the document. The first version may be empty (Explorer creates a file empty and then writes it). A name infoRouter does not allow is the client's mistake. | `201`; `400` for a bad name |
| PUT, existing name | A new version with the uploaded file. The same bytes again store nothing. An empty file is refused: only the first version may be empty. Checked out by somebody else: refused. A checkout PUT makes for itself is released afterwards; one the caller holds (a LOCK) stays. | `200` with the new ETag; `200` and nothing stored for the same bytes; `415` empty; `403` held by another |
| GET | The published version's content, tagged with its ETag, `Cache-Control: private, no-store`. `?Version=` asks for another version. | `200`; `404` |
| HEAD, PROPFIND | The document's properties; the ETag is the published version's, the same tag GET sends. | `200`, `207` |
| MOVE, free name | Renames or moves the document. | `201` |
| MOVE, onto an existing document | The document already there takes the moved file as its next version and keeps everything else; the source, usually the client's temporary file, goes to the recycle bin. With `Overwrite: F` nothing happens. While the target is checked out to the caller (a LOCK), it goes through; held by somebody else, refused. | `204`; `412` with Overwrite F; `423` held by another |
| MOVE, a rename that only changes case | Refused by infoRouter's own move, as before WebDAV. | `409` |
| COPY, onto an existing document | As MOVE, but the source stays. Onto itself: refused. | `204`; `403` onto itself |
| MOVE or COPY, folder onto an existing folder | The folder there goes to the recycle bin and the moved or copied one takes its place. | `204`; `412` with Overwrite F |
| DELETE | Document or folder to the caller's recycle bin, as the UI's delete does; refused when the recycle is (held by somebody else, under retention). | `204`; `423` |

## What Office does when it saves

Word and Excel save with a sequence, not a single PUT: LOCK the document, PUT the new content under a
temporary name beside it, MOVE the temporary file over the document, UNLOCK, and DELETE what is left. On
infoRouter that is: checkout, a throwaway document, a new version of the original from the temporary file with
the throwaway recycled, check-in. The result is the same document with one version more, which is what a save
should be. Explorer saves with a plain PUT.

## ETags

One tag per version, `<document id>:<version number>`, the same from GET, HEAD and PROPFIND; a new version is
a new tag. A client compares the tag it downloaded with the one in a listing to know whether its copy is current,
so the three must agree.

## Lock tokens

The token is `opaquelocktoken:infoRouterDocument-<id>`, the same for every lock of a document. It is not
checked on later requests: infoRouter keeps no lock tokens, and the identity that matters is the user who holds
the checkout. A LOCK by another user is refused whatever token the request carries. (The token is sent without the
angle brackets RFC 4918 asks for, as 8.7 sent it; the clients in use accept it.)

## Caching

Every document download, WebDAV or not, is `Cache-Control: private`: a document is what one user may see, and
the address may carry that user's session ticket, so no shared cache may keep it for the next user. WebDAV GET
adds `no-store`.

## For developers

- Server: `DAVCoreMiddleware` (one file per verb; `DestinationMethod` for MOVE and COPY onto an existing
  name, `PutMethod.PublishNewVersionAsync` for the new-version path they share with PUT).
- Tests: `TestProjects/DAVCoreMiddlewareTests`, one class per verb; `MoveTests` plays Office's save sequence.
- The middleware is kept wire-compatible with infoRouter 8.7's DAVHandler, and deviates only where 8.7 was
  wrong; each deviation is noted in the code.

## Since

- **9.0.200 (2026-10-28):** a MOVE or COPY onto an existing document makes a new version of it. From 9.0 until
  then the document there was recycled and the source put in its place, a new document with no history; 8.7
  refused the MOVE with `409`. The same release made GET's ETag agree with PROPFIND's (it used to say `id:0`),
  made downloads private (they were `public`, as in 8.7), and stopped a new version of a form-made document
  from being rendered again from its template (see [Documents made from forms and templates](documents-from-forms.md)).
