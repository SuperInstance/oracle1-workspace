# License Batch 4 — S-Z Repos

**Date:** 2026-07-12  
**Scope:** SuperInstance repos starting with letters S through Z  
**Status:** ✅ COMPLETE  

## Summary

- **Total s-z repos scanned:** 700
- **Repos already with valid license:** 183
- **Repos needing license fix:** 517 + 1 (`ternary-svm` fixed separately)
- **Repos fixed:** 518
- **Failures:** 0
- **Rate limit at end:** 3980

## What Was Done

1. Scanned all 4,099 repos in the SuperInstance org via GitHub API (paginated, alphabetical sort)
2. Identified 700 repos in the s-z range (pages 35-41 of 100/page)
3. Checked each repo's license status via `gh api repos/SuperInstance/REPO/license`
4. For repos with `NONE`, `NOASSERTION`, or unrecognized license (including AGPL-3.0), replaced/added standard MIT LICENSE file
5. All operations succeeded with zero failures

## Categories Fixed

- **NOASSERTION (359 repos):** Had a LICENSE file but GitHub couldn't identify it (e.g., dual-license, custom text)
- **NONE (152 repos):** Had no LICENSE file at all
- **AGPL-3.0 → MIT (4 repos):** `Studylog-AI`, `superinstance-ai-pages`, `warp`, `whisper-sync`
- **Empty/unrecognized (2 repos):** `wasserstein-narrative`, `ws-status-indicator`

## Notable Repos Fixed

- All `superinstance-*` repos (~35 repos)
- All `ternary-*` repos (~280+ repos)
- `symplectic-*`, `symmetry-*`, `swarm-*`, `tropical-*` families
- `zeroclaw-*`, `zhc-*`, `vessel-*`, `warp-*` repos
- `ternary-svm` (fixed separately — had dual MIT/Apache license that GitHub couldn't parse)

## License Applied

Standard MIT License:

```
MIT License

Copyright (c) 2024 SuperInstance

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Rate Limit

Started at ~5000, ended at 3980. Never dropped below 400 threshold.
