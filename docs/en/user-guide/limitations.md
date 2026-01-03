# Limitations

Current limitations based on the implementation:

- `JalaliDataFrameAccessor` requires at least one column of `jdatetime`
  objects and raises if none are present.
- `JalaliResampler` expects a `pd.DatetimeIndex` as index; otherwise it raises.
- `jalali_date_range` requires at least two of `start`, `end`, `periods`;
  if all three are provided, `freq` is required.
- `to_jalali_datetime` parses a fixed set of formats unless `format` is
  provided explicitly.
- `JalaliDatetimeArray` stores values in an object array, which can be slower
  than native `datetime64` operations for large datasets.

If you hit a limitation, open an issue with a minimal reproduction case.
