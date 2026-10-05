# Test evidence

Everything in this folder is captured pytest output. The explanatory text at the top of each file was written around it; the output itself was not edited.

## Files

| File | What it shows | How strong is it |
| --- | --- | --- |
| `br3_red.txt` | The original RED for BR3, as first captured | Weak - dies at import |
| `br4_red.txt` | The original RED for BR4, as first captured | Weak - dies at import |
| `test_results.txt` | The earliest capture, before T3 and T4 existed: 6 collected, 2 collection errors | Weak - dies at import |
| `br3_rule_verification_red.txt` | The BR3 tests re-run with the BR3 guard removed | Strong - fails on behaviour |
| `br4_rule_verification_red.txt` | The BR4 tests re-run with the BR4 guard removed | Strong - fails on behaviour |
| `test_results_green.txt` | The full suite in its final state: 28 passed | Final result |

## Why there are two kinds of RED here

The weak files are the honest original TDD history, and they are kept as they were. They record `ModuleNotFoundError`, which proves only that a module did not exist yet. No assertion about BR3 or BR4 behaviour ever ran, so on their own they do not show that any test actually expressed the rule. A RED that dies during import has not yet said anything about the business rule.

That is a real weakness in the evidence, so the two `*_rule_verification_red.txt` files were added. On 2026-10-05 each guard was temporarily removed from the finished code and its tests re-run:

- **BR3** - delete the already-reserved check in `Show.reserve_seat()`.
- **BR4** - disable the four-seat limit in `ReservationEligibilityService.check_eligibility()`.

Each run failed exactly one test, with `DID NOT RAISE`, and each guard was restored straight afterwards. In the BR4 run the other six tests still passed, which is the useful part: they isolate the seat-count rule specifically, so the single failure points straight at the guard that was removed.

These are verification runs against completed code. They are not a claim about how the code was originally written, and both files say so in their header. They answer a different question from the original REDs: not "did this test fail first?" but "does this test notice when the rule is gone?"

## Reproducing any of it

```bash
pip install -r requirements.txt

pytest -v                                  # the final green run
pytest tests/test_t3_br3_show_seat_allocation.py -v
pytest tests/test_t4_br4_reservation_eligibility.py -v
python scripts/check_dependencies.py       # no import points out of its layer
```

Each `*_rule_verification_red.txt` file ends with step-by-step instructions for reproducing its own RED.