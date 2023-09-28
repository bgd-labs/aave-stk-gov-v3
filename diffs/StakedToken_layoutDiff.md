```diff
diff --git a/diffs/currentStakedToken.md b/diffs/nextStakedToken.md
index 6edc627..9f525e5 100644
--- a/diffs/currentStakedToken.md
+++ b/diffs/nextStakedToken.md
@@ -1,28 +1,24 @@
 | Name                                | Type                                                                                   | Slot | Offset | Bytes |
 |-------------------------------------|----------------------------------------------------------------------------------------|------|--------|-------|
-| _balances                           | mapping(address => uint256)                                                            | 0    | 0      | 32    |
+| _balances                           | mapping(address => struct BaseAaveToken.DelegationAwareBalance)                        | 0    | 0      | 32    |
 | _allowances                         | mapping(address => mapping(address => uint256))                                        | 1    | 0      | 32    |
 | _totalSupply                        | uint256                                                                                | 2    | 0      | 32    |
 | _name                               | string                                                                                 | 3    | 0      | 32    |
 | _symbol                             | string                                                                                 | 4    | 0      | 32    |
-| _decimals                           | uint8                                                                                  | 5    | 0      | 1     |
-| _votingSnapshots                    | mapping(address => mapping(uint256 => struct GovernancePowerDelegationERC20.Snapshot)) | 6    | 0      | 32    |
-| _votingSnapshotsCounts              | mapping(address => uint256)                                                            | 7    | 0      | 32    |
-| _aaveGovernance                     | contract ITransferHook                                                                 | 8    | 0      | 20    |
+| ______DEPRECATED_OLD_ERC20_DECIMALS | uint8                                                                                  | 5    | 0      | 1     |
+| __________DEPRECATED_GOV_V2_PART    | uint256[3]                                                                             | 6    | 0      | 96    |
 | lastInitializedRevision             | uint256                                                                                | 9    | 0      | 32    |
 | ______gap                           | uint256[50]                                                                            | 10   | 0      | 1600  |
 | assets                              | mapping(address => struct AaveDistributionManager.AssetData)                           | 60   | 0      | 32    |
 | stakerRewardsToClaim                | mapping(address => uint256)                                                            | 61   | 0      | 32    |
 | stakersCooldowns                    | mapping(address => struct IStakedTokenV2.CooldownSnapshot)                             | 62   | 0      | 32    |
-| _votingDelegates                    | mapping(address => address)                                                            | 63   | 0      | 32    |
-| _propositionPowerSnapshots          | mapping(address => mapping(uint256 => struct GovernancePowerDelegationERC20.Snapshot)) | 64   | 0      | 32    |
-| _propositionPowerSnapshotsCounts    | mapping(address => uint256)                                                            | 65   | 0      | 32    |
-| _propositionPowerDelegates          | mapping(address => address)                                                            | 66   | 0      | 32    |
-| DOMAIN_SEPARATOR                    | bytes32                                                                                | 67   | 0      | 32    |
+| ______DEPRECATED_FROM_STK_AAVE_V2   | uint256[5]                                                                             | 63   | 0      | 160   |
 | _nonces                             | mapping(address => uint256)                                                            | 68   | 0      | 32    |
 | _admins                             | mapping(uint256 => address)                                                            | 69   | 0      | 32    |
 | _pendingAdmins                      | mapping(uint256 => address)                                                            | 70   | 0      | 32    |
-| ______gap                           | uint256[8]                                                                             | 71   | 0      | 256   |
+| _votingDelegatee                    | mapping(address => address)                                                            | 71   | 0      | 32    |
+| _propositionDelegatee               | mapping(address => address)                                                            | 72   | 0      | 32    |
+| ______gap                           | uint256[6]                                                                             | 73   | 0      | 192   |
 | _cooldownSeconds                    | uint256                                                                                | 79   | 0      | 32    |
 | _maxSlashablePercentage             | uint256                                                                                | 80   | 0      | 32    |
 | _currentExchangeRate                | uint216                                                                                | 81   | 0      | 27    |
```
