# StudentBridge AI V11

## Main improvements

### 1. Send Money redesigned
- Multi-step flow instead of one long form
- Session-based sign-in
- Saved beneficiaries
- Separate bank transfer vs Visa/Mastercard path
- Server-generated transfer review

### 2. My Profile added
- Demo login/session view
- Shows profile information
- Shows saved beneficiaries

### 3. Compare Payment Routes simplified
- Only key fields: origin, destination, payable amount, deadline, optional invoice upload
- Cleaner comparison cards
- Server-side route comparison endpoint

## Notes
- No MySQL schema change was required.
- Beneficiaries are stored in the active demo session, not in a new database table.
- Real live transfers are still not enabled.
