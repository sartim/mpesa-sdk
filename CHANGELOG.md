# CHANGELOG

<!-- version list -->

## v2.0.0 (2026-10-11)

### Bug Fixes

- Pass optional Daraja request fields
  ([`1c1c85e`](https://github.com/sartim/mpesa-sdk/commit/1c1c85e37db1308a2c45b97efcc525a82cd1008a))

### Chores

- Configure weekly dependency updates ([#41](https://github.com/sartim/mpesa-sdk/pull/41),
  [`c175df1`](https://github.com/sartim/mpesa-sdk/commit/c175df19040279fad09733b3dc33ff619f4b7760))

- Keep package version assertion current ([#41](https://github.com/sartim/mpesa-sdk/pull/41),
  [`c175df1`](https://github.com/sartim/mpesa-sdk/commit/c175df19040279fad09733b3dc33ff619f4b7760))

- Update workflow actions and pytest range ([#47](https://github.com/sartim/mpesa-sdk/pull/47),
  [`a028937`](https://github.com/sartim/mpesa-sdk/commit/a028937f284331134726781c348ff91aeceda806))

### Features

- Update B2C wrapper to Daraja v3
  ([`15c0f68`](https://github.com/sartim/mpesa-sdk/commit/15c0f683f049c86532620775ed957ce434281bf4))

### Breaking Changes

- B2C requests now use the v3 endpoint and require OriginatorConversationID. The callback occasion
  field is sent as Occassion; the former Occasion spelling remains accepted as an input alias.


## v1.2.0 (2026-10-08)

### Features

- Add manual sandbox OAuth smoke check
  ([`ebf2d43`](https://github.com/sartim/mpesa-sdk/commit/ebf2d435507c693d753d0d8e03a5bee9c5a90a97))

### Testing

- Cover all wrapped Daraja endpoints
  ([`7d1a98e`](https://github.com/sartim/mpesa-sdk/commit/7d1a98e9ea4a13da98595fa06b2647285eba74e1))


## v1.1.0 (2026-10-08)

### Build System

- Automate PyPI releases with semantic release
  ([`9117c77`](https://github.com/sartim/mpesa-sdk/commit/9117c775e055949817c4f774d2ca4be76bcabeb1))

### Features

- **daraja**: Modernize client naming and safety
  ([`8f25c25`](https://github.com/sartim/mpesa-sdk/commit/8f25c2508456aff5dcfd7b1547c776f0b1dce04f))


## v1.0.7 (2020-07-22)


## v1.0.6 (2020-06-17)


## v1.0.5 (2020-06-16)


## v1.0.2 (2020-04-05)


## v1.0.0 (2020-03-16)

- Initial Release
