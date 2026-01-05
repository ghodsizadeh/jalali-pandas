# Jalali Pandas North Star + Plan

## North Star (Definition of Done)
A first-class Jalali calendar experience in pandas that provides feature parity (as feasible) with the Gregorian time-series stack, so users can:
- parse/format Jalali datetimes, convert to/from Gregorian, and round-trip without loss
- generate Jalali-aware ranges, offsets, and indices
- perform time-series operations (indexing, slicing, resampling, rolling, grouping) in Jalali calendar terms
- use Jalali time with consistent, typed, and vectorized APIs

Scope decisions:
- Timezone: use pandas' existing tz infrastructure and support tz-aware Jalali datetimes where possible; aim for correctness with common zones (e.g., Asia/Tehran) via conversion to Gregorian for tz calculations, then map back to Jalali.
- Storage: align with pandas ExtensionArray/Dtype conventions for interoperability.

## Strategy (How We Get There)
Build a dedicated Jalali datetime dtype + array with a minimal but solid core, then incrementally integrate with pandas time-series APIs (date_range, offsets, resample, index ops). Prioritize correctness, vectorization, and typing. Leverage pandas' extension interfaces to avoid forking core pandas.

## Milestones (Ordered)

### 1) Specification + Architecture (North Star Refinement)
- Define Jalali datetime scalar semantics (date range limits, leap rules, week definitions).
- Decide canonical internal representation (e.g., store as Gregorian int64 ns + metadata vs. Jalali fields).
- Define tz strategy: convert between Jalali <-> Gregorian for tz operations, and document edge cases.
- Define API surface:
  - Series/Index accessors
  - dtype construction
  - conversion functions
  - frequency aliases and offset behavior

### 2) Core Jalali Dtype + Array
- Implement `JalaliDateTimeDtype` and `JalaliDateTimeArray` (pandas ExtensionArray).
- Add scalar type (if needed) with NA support.
- Implement conversions:
  - `to_jalali` / `to_gregorian`
  - parse/format methods
- Ensure vectorized operations for performance.

### 3) Index & Range Generation
- Implement `JalaliDatetimeIndex` (or equivalent Index wrapper) and `jalali_date_range`.
- Support indexing, slicing, and alignment.
- Support `freq`/offsets mapping to Jalali calendar boundaries.

### 4) Time-Series Feature Parity
- Resampling and asfreq with Jalali boundaries.
- Groupby by Jalali year/month/day/week/quarter.
- Rolling/expanding with Jalali-aware offsets.
- Integration with pandas `Grouper` and `DataFrame.resample`.

### 5) Timezone Integration
- Enable tz-aware Jalali datetimes where possible.
- Validate DST behavior using Gregorian conversions and map back to Jalali.
- Document limitations and unsupported zones if any.

### 6) Typing, Testing, and Performance
- Add typing for public APIs (py.typed, type hints, optional mypy/pyright config).
- Comprehensive test matrix:
  - conversions and round-trips
  - leap years and month boundaries
  - tz-aware cases and DST transitions
  - empty/NaT handling
  - index alignment, resample, and groupby
- Benchmarks for core operations.

## Success Criteria
- Users can perform end-to-end Jalali time-series workflows similar to Gregorian pandas.
- All core time-series operations are supported or explicitly documented as unsupported.
- Typed API, stable behavior across pandas versions in the support range.

## Risks / Open Questions
- pandas ExtensionArray limitations and what needs custom Index classes.
- Performance overhead of Jalali conversions at scale.
- Precise handling of tz/DST when mapping to/from Jalali.

## Immediate Next Steps (No Code Changes Yet)
- Confirm internal representation choice and minimum supported pandas versions.
- Define exact Jalali frequency rules (month length, week start, quarter definitions).
- Draft a feature parity checklist vs. pandas `DatetimeIndex`/`TimedeltaIndex` APIs.
