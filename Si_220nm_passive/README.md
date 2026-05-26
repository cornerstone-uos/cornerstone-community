# SOI220nm_1550nm_TM_STRIP_focusing_GC_apodised

SOI220nm_1550nm_TM_STRIP_focusing_GC_apodised — grating-coupler on SOI 220 nm Passive.

---

Prepared via CORNERSTONE PDK Monitor v1.0.0 on 2026-05-26T19:04:37.749Z.

**Author identity:** https://github.com/AEmreKaplan/
**BB type:** grating-coupler
**Category:** passive
**Platform:** SOI 220 nm Passive
**Status:** progress
**Updating:** existing community PDK folder

## Layout

```
Si_220nm_passive/
  layout/                 ← raw GDS / OASIS / SVG layout uploads
  components/             ← auto-generated YAML descriptor (next to a community-PDK .gds reference)
  sparams/                ← S-matrix tab
  tests/                  ← Tests tab
  fab/                    ← Fabrication tab
  scripts/                ← Scripts tab
  eda/                    ← EDA tab (links as eda_links.json)
  documents/              ← non-YAML docs (PDFs, datasheets)
  variants/               ← recursive variant sub-folders
```

## Notes

- Folder layout matches [cornerstone-community](https://github.com/cornerstone-uos/cornerstone-community).
- Re-running *Prepare for community PDK* is idempotent — only new / changed files are uploaded.
- An admin can cherry-pick this folder straight into the main PDK repo.
