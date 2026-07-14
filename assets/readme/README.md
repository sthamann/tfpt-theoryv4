# README illustrations

Still frames used by the top-level [`README.md`](../../README.md). They are **rendered from the
Remotion intro film** in [`video/`](../../video) (the same source that produces
`website/public/intro/tfpt-intro.mp4`), so they stay on-brand and never drift from the film.

| File | Scene | Master frame |
|---|---|---|
| `01_outputs.png` | What comes out (the cascade) | 1630 |
| `02_inputs.png` | The two inputs `c₃ = 1/(8π)`, `g_car = 5` | 2210 |
| `03_e8.png` | E₈ — the proof layer | 3320 |
| `04_fixedpoint.png` | The fixed point | 4680 |
| `05_nullmodel.png` | Frozen predictions vs the null model | 7180 |

## Regenerate

```bash
cd video
npx remotion still TfptIntro ../assets/readme/01_outputs.png    --frame=1630
npx remotion still TfptIntro ../assets/readme/02_inputs.png     --frame=2210
npx remotion still TfptIntro ../assets/readme/03_e8.png         --frame=3320
npx remotion still TfptIntro ../assets/readme/04_fixedpoint.png --frame=4680
npx remotion still TfptIntro ../assets/readme/05_nullmodel.png  --frame=7180
```
