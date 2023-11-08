
certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule vp_change_in_balance_affect_power_DELEGATEE_all_others

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule vp_change_in_balance_affect_power_DELEGATEE_transfer_M

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule vp_change_in_balance_affect_power_DELEGATEE_stake_M

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule vp_change_in_balance_affect_power_DELEGATEE_redeem_M

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule vp_change_in_balance_affect_power_DELEGATEE_delegate_M



certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule pp_change_in_balance_affect_power_DELEGATEE_all_others

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule pp_change_in_balance_affect_power_DELEGATEE_transfer_M

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule pp_change_in_balance_affect_power_DELEGATEE_stake_M

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule pp_change_in_balance_affect_power_DELEGATEE_redeem_M

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL-under-approx.conf \
           --rule pp_change_in_balance_affect_power_DELEGATEE_delegate_M

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL.conf \
           --rule vp_change_of_balance_affect_power_NON_DELEGATEE

certoraRun --send_only --disable_auto_cache_key_gen \
           certora/conf/token-v3-delegate-HL.conf \
           --rule pp_change_of_balance_affect_power_NON_DELEGATEE

certoraRun --send_only --disable_auto_cache_key_gen certora/conf/token-v3-delegate-HL.conf \
           --rule \
           mirror_votingDelegatee_correct \
           mirror_propositionDelegatee_correct \
           mirror_delegationMode_correct \
           mirror_balance_correct \
           inv_voting_power_correct \
           inv_proposition_power_correct \
           user_cant_voting_delegate_to_himself \
           user_cant_proposition_delegate_to_himself \
           no_function_changes_both_balance_and_delegation_state \
           sum_all_voting_delegated_power_EQ_DelegatingVotingBal \
           sum_all_proposition_delegated_power_EQ_DelegatingPropositionBal

