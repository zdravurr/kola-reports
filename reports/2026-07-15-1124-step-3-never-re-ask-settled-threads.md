# Step 3 never re-ask settled threads

_2026-07-15 11:24 UTC_

---

## STEP 3 — STOP RE-ASKING SETTLED THREADS — CLOSED

The morning "unclassified thread" alarm for Michelle :: La-Z-Boy S. Sofa is fixed at the root, not patched over.

### Root cause (two layers)
1. Michelle · La-Z-Boy was NOT in the permanent Boss-ruling list. It sat as a code comment "awaiting Boss confirmation", so it was never actually ruled. Only I. (Beelink) and Robert (Async) were.
2. The FB inbox sweep's classifier never received the sender's NAME and never consulted the Boss-ruling function at all. So "La-Z-Boy S. Sofa" hit the generic "sofa" category → verdict `uncertain` → dumped into the "unidentified threads" digest → the Boss got asked AGAIN. And because rulings lived only as hardcoded Python, every new ruling required a code edit — easy to forget, which is exactly what happened.

### Fix — a ruling is now written down once and checked before ever asking again
- New persistent store `.kola_state/boss_rulings.json` + `record_boss_ruling(name, listing, kind)`. A Boss ruling is written to disk and SURVIVES any code redeploy. New rulings no longer need a code change.
- `boss_not_ours()` now checks BOTH sources: the hardcoded list (survives a git restore) and the disk store (survives without a code edit). Michelle is in BOTH now — belt and suspenders.
- `classify(text, name=)` checks the Boss ruling as its FIRST step — a settled thread can never become `uncertain` again.
- The sweep now passes the name into classification, and `escalate_unclassified` has a final safety-net: even if a ruled thread somehow reaches the digest, it is silently dropped, never asked.

### Proven live (real code paths, patched alarm so nothing reached the Boss)
- Michelle/La-Z-Boy → foreign (procurement). Irena/Beelink → foreign. Robert/Async → foreign.
- Michelle/Giant Mountain Bike → still `ours` (she is the buyer of our bike — distinguished purely by listing, as required).
- Forced all three ruled threads into the unknown list → escalation dropped all three and asked ONLY about a genuinely-unknown decoy ("Some R. Kayak"). Zero re-asks for settled threads.
- Syntax-checked both modules; committed as botuser (107ac6a). Durable memory updated.

### How future rulings work
Any new Boss decision about a thread (ours / not ours / a buy) → one call `ir.record_boss_ruling(name, listing, kind)`. Written to disk, checked before any future question. No code edit, no re-ask.
