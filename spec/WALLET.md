# Wallet and Custody Profile

The wallet profile covers deposits, withdrawals, internal transfers, subaccounts, custody, and compliance metadata.

## Assets and Networks

Each asset MAY exist on multiple networks.

Example:

```json
{
  "asset_id": "USDT",
  "networks": [
    {
      "network_id": "TRON",
      "deposit_enabled": true,
      "withdrawal_enabled": true,
      "min_confirmations": 20,
      "withdrawal_fee": "1.000000"
    }
  ]
}
```

## Deposits

Deposit statuses:

- `address_created`;
- `pending`;
- `confirming`;
- `credited`;
- `rejected`;
- `returned`;
- `failed`.

Deposit records MUST include:

- `wallet_transaction_id`;
- `asset_id`;
- `network_id`;
- `amount`;
- `address`;
- `tx_hash`, if available;
- `confirmations`;
- `status`;
- `created_at`;
- `updated_at`.

## Withdrawals

Withdrawal statuses:

- `created`;
- `compliance_review`;
- `approved`;
- `broadcasting`;
- `broadcasted`;
- `confirming`;
- `completed`;
- `cancelled`;
- `rejected`;
- `failed`.

Withdrawal creation MUST support idempotency.

## Address Book

Regulated venues SHOULD support a withdrawal address book with:

- ownership metadata;
- network;
- memo/tag;
- allowlist status;
- travel rule metadata, if applicable.

## Internal Transfers

Transfer types:

- account to subaccount;
- subaccount to account;
- subaccount to subaccount;
- spot to derivatives wallet;
- derivatives to spot wallet;
- custody to trading wallet.

Transfer statuses:

- `created`;
- `completed`;
- `rejected`;
- `failed`.

## Travel Rule Metadata

When legally required, wallet operations SHOULD include structured metadata:

- originator;
- beneficiary;
- VASP information;
- transfer purpose;
- screening status.

The standard does not mandate a specific legal interpretation. It reserves a structured field so compliance systems can interoperate.

## Russian Law-Aware Guardrails

Wallet and custody flows used in the Russian legal context SHOULD make the compliance boundary visible:

- withdrawal and transfer responses SHOULD expose structured compliance statuses instead of free-form text;
- `compliance_review` MUST NOT imply that a transfer is approved;
- digital currency movements MUST NOT be described as a generally permitted domestic payment use outside the applicable legal regime;
- personal data, AML/KYC attributes, address ownership data, and screening details MUST be scoped to private APIs and protected by the implementation;
- sandbox wallet operations MUST be clearly separated from production permissions.
