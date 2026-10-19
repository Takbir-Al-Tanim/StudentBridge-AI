# StudentBridge AI V11.1 — navigation fix

V11 shipped with an old V10 `init()` function which still attempted to attach listeners to elements removed from the new Compare Payment Routes page, such as `#university`, `#add-quote`, `#fetch-rate`, and `#build-plan`. It also never called the new `initProfile()` and `initRouteCompareSimple()` routines.

V11.1 wires navigation before asynchronous data loading, calls all V11 feature initializers, avoids deleted fields, updates the Journey Studio handoff to the new comparison form, and increments the JS/CSS cache keys. Use a hard refresh after replacing your application files.

No database migration is needed. V11 authentication is demonstration-only and beneficiaries are kept in an application memory session; it is not a real secure banking login or persistent encrypted beneficiary database. No real-money transfer or unconfigured card checkout is enabled.
