

certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-delegate.conf 

certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-delegate-HL-rules.conf  --rule vp_change_in_balance_affect_power_DELEGATEE
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-delegate-HL-rules.conf  --rule vp_change_of_balance_affect_power_NON_DELEGATEE
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-delegate-HL-rules.conf  --rule pp_change_in_balance_affect_power_DELEGATEE
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-delegate-HL-rules.conf  --rule pp_change_of_balance_affect_power_NON_DELEGATEE
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-delegate-HL-rules.conf  --rule mirror_votingDelegatee_correct mirror_propositionDelegatee_correct mirror_delegationMode_correct mirror_balance_correct inv_voting_power_correct inv_proposition_power_correct user_cant_voting_delegate_to_himself user_cant_proposition_delegate_to_himself no_function_changes_both_balance_and_delegation_state


certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf  --rule integrityOfSlashing --rule integrityOfStaking --rule previewStakeEquivalentStake --rule noStakingPostSlashingPeriod --rule noSlashingMoreThanMax --rule noRedeemOutOfUnstakeWindow --rule noEntryUntilSlashingSettled --rule integrityOfRedeem --rule cooldownCorrectness --rule airdropNotMutualized --rule integrityOfReturnFunds --rule slashAndReturnFundsOfZeroDoesntChangeExchangeRate

certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf --rule rewardsIncreaseForNonClaimFunctions
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf --rule rewardsMonotonicallyIncrease
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf --rule rewardsGetterEquivalentClaim
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf --rule indexesMonotonicallyIncrease
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf --rule exchangeRateNeverZero
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf --rule totalSupplyDoesNotDropToZero
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf --rule slashingIncreaseExchangeRate
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/allProps.conf --rule returnFundsDecreaseExchangeRate

certoraRun --send_only --disable_auto_cache_key_gen certora/conf/propertiesWithSummarization.conf  
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/invariants.conf  

certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-general.conf  --rule delegateCorrectness
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-general.conf  --rule sumOfVBalancesCorrectness
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-general.conf  --rule sumOfPBalancesCorrectness
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-general.conf  --rule transferDoesntChangeDelegationMode

certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-erc20.conf 
certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-community.conf 



