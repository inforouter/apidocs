# Values Connect extracted, and whether somebody reviewed them

infoRouter Connect fills property set rows from a document's content. A person is expected to look at what it
wrote. This page says how the server records that, and how a listing finds the documents still to review.

## The rule

A property set row Connect wrote carries **Connect's confidence** in it, a percentage from 1 to 100, the
weakest of the fields it filled. Every row also carries who saved it last. The two together are the row's
**review state**: a row with a confidence whose last saver is still the system account (`infoRouter Connect`)
is **not reviewed**; a row with a confidence saved since by a person is **reviewed**; a row with no confidence
was never Connect's work. **A person saving the row is the review**, through
[UpdatePropertySetRow](../UpdatePropertySetRow.md) or the UI, changed or not; the confidence is left as Connect
wrote it and never says whether the reviewer agreed.

## What a row says

| `ReviewState` | `AIConfidence` | Last saver | Meaning |
|---|---|---|---|
| `NotExtracted` | none | anyone | Typed by a person, or applied or inherited from a folder |
| `NotReviewed` | present | the system account | Connect wrote it; nobody has saved it since |
| `Reviewed` | present | a person | Connect wrote it; that person saved it on that date |

Connect filling the row again (a new version, a re-run) puts the system account back as saver, so the row is to
be reviewed again. A folder apply that overwrites the row takes the confidence with it. There is no
confidence threshold: whatever Connect found is written, however unsure, on the reasoning that a value a
person will review is worth more than a blank; a row reporting `12` is the one to send somebody to.

## Finding the documents still to review

Each document carries one summary bit, `ExtractedDataReviewPending` (bit 30 of `AIEnhanced`,
`1073741824`): set while any row of any of its property sets is not reviewed, recomputed from the rows on every
row write or removal. [Search](../Search.md) finds them with
`<criteria NAME="AIENHANCED" VALUE="EXTRACTEDDATAREVIEWPENDING" />`. The words `ANY`, `ALL` and `NONE` do not
include this bit: it is a state of the rows, not something Connect produced, and `ALL` would otherwise stop
matching a document once its rows were reviewed.

## For developers

- Operations: [GetPropertySets](../GetPropertySets.md) (the `AIConfidence` and `ReviewState` attributes on
  each row's `<Log>`), [UpdatePropertySetRow](../UpdatePropertySetRow.md), [GetDocument](../GetDocument.md),
  [Search](../Search.md).
- The rule: `PropertySetDataRow.ReviewState` (derived), `PropertySetOperations` (the confidence is carried
  across a person's save and the bit recomputed in `RecomputeExtractedDataReviewPendingAsync`); the
  `CPSETAICONFIDENCE` column on every property set table.
- Tests: `PropertySetRowReviewApiTests`.

## Since

- **9.0.200 (2026-10-27):** the confidence lives on the row and is never reset. Until then the document carried
  a single `AIExtractConfidence`, the lowest across all of its sets, reset to 0 by any property set save, which
  said nothing about who had looked at what.
