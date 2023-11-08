
/*
    This is a specification file for the verification of delegation features.
    This file was adapted from AaveTokenV3.sol smart contract to STK-3.0 smart contract.
    This file is run by the command line: 
          certoraRun --send_only certora/conf/token-v3-delegate.conf
    It uses the harness file: certora/harness/StakedAaveV3Harness.sol
*/

import "base.spec";
import "base-HL.spec";

methods {
    function _.mul_div_munged(uint256 x, uint256 denominator) external =>
        mul_div(x,denominator) expect uint256 ALL;
    function _.mul_div_munged(uint256 x, uint256 denominator) internal =>
        mul_div(x,denominator) expect uint256 ALL;
    function getExchangeRate() external returns (uint216) envfree;
}

ghost mul_div(mathint , mathint) returns uint256 {
    axiom
        (forall mathint den. mul_div(0,den)==0)
        &&
        (forall mathint a. forall mathint b. forall mathint deno.
         (mul_div(a+b,deno) + 0 == mul_div(a,deno) + mul_div(b,deno)) ||
         (mul_div(a+b,deno) + 0 == mul_div(a,deno) + mul_div(b,deno)+1) ||
         (mul_div(a+b,deno) + 0 == mul_div(a,deno) + mul_div(b,deno)-1)
        );
}



definition is_voting_delegate(address a) returns bool =
    mirror_delegationMode[a]==FULL_POWER_DELEGATED() || mirror_delegationMode[a]==VOTING_DELEGATED();

definition is_proposition_delegate(address a) returns bool =
    mirror_delegationMode[a]==FULL_POWER_DELEGATED() || mirror_delegationMode[a]==PROPOSITION_DELEGATED();





invariant mirror_votingDelegatee_correct()
    forall address a.mirror_votingDelegatee[a] == getVotingDelegatee(a);

invariant mirror_propositionDelegatee_correct()
    forall address a.mirror_propositionDelegatee[a] == getPropositionDelegatee(a);

invariant mirror_delegationMode_correct()
    forall address a.mirror_delegationMode[a] == getDelegationMode(a);

invariant mirror_balance_correct()
    forall address a.mirror_balance[a] == getBalance(a);



invariant inv_voting_power_correct(address a)
    a != 0 =>
    (
     to_mathint(getPowerCurrent(a, VOTING_POWER()))
     ==
     mul_div(sum_all_voting_delegated_power[a] + (is_voting_delegate(a) ? 0 : mirror_balance[a]),
             mirror_currentExchangeRate
            )+0
    )
{
    preserved with (env e) {
        requireInvariant user_cant_voting_delegate_to_himself();
        requireInvariant sum_all_voting_delegated_power_EQ_DelegatingVotingBal(a);
    }
}


invariant inv_proposition_power_correct(address a)
    a != 0 =>
    (
     to_mathint(getPowerCurrent(a, PROPOSITION_POWER()))
     ==
     mul_div(sum_all_proposition_delegated_power[a] + (is_proposition_delegate(a) ? 0 : mirror_balance[a]),
             mirror_currentExchangeRate
            )+0
    )
{
    preserved with (env e) {
        requireInvariant user_cant_proposition_delegate_to_himself();
        requireInvariant sum_all_proposition_delegated_power_EQ_DelegatingPropositionBal(a);
    }
}



invariant sum_all_voting_delegated_power_EQ_DelegatingVotingBal(address a)
    a != 0 =>
    (
     sum_all_voting_delegated_power[a] == getDelegatedVotingBalance(a) * FACTOR()
    )
{
    preserved with (env e) {
        requireInvariant user_cant_voting_delegate_to_himself();
    }
}

invariant sum_all_proposition_delegated_power_EQ_DelegatingPropositionBal(address a)
    a != 0 =>
    (
     sum_all_proposition_delegated_power[a] == getDelegatedPropositionBalance(a) * FACTOR()
    )
{
    preserved with (env e) {
        requireInvariant user_cant_proposition_delegate_to_himself();
    }
}


rule no_function_changes_both_balance_and_delegation_state(method f, address bob) {
    env e;
    calldataarg args;

    require (bob != 0);

    uint256 bob_balance_before = balanceOf(bob);
    bool is_bob_delegating_voting_before = getDelegatingVoting(bob);
    address bob_delegatee_before = mirror_votingDelegatee[bob];
    mathint exchange_rate_before = mirror_currentExchangeRate;

    f(e,args);

    uint256 bob_balance_after = balanceOf(bob);
    bool is_bob_delegating_voting_after = getDelegatingVoting(bob);
    address bob_delegatee_after = mirror_votingDelegatee[bob];
    mathint exchange_rate_after = mirror_currentExchangeRate;

    assert (bob_balance_before != bob_balance_after =>
            (is_bob_delegating_voting_before==is_bob_delegating_voting_after &&
             bob_delegatee_before == bob_delegatee_after &&
             exchange_rate_before == exchange_rate_after
            )
           );

    assert (bob_delegatee_before != bob_delegatee_after =>
            bob_balance_before == bob_balance_after
           );

    assert (is_bob_delegating_voting_before!=is_bob_delegating_voting_after =>
            bob_balance_before == bob_balance_after            
            );

    assert (exchange_rate_before != exchange_rate_after =>
            bob_balance_before == bob_balance_after            
           );
}



invariant user_cant_voting_delegate_to_himself()
    forall address a. a!=0 => mirror_votingDelegatee[a] != a;

invariant user_cant_proposition_delegate_to_himself()
    forall address a. a!=0 => mirror_propositionDelegatee[a] != a;



//===================================================================================
//===================================================================================
// High-level rules that verify that a change in the balance (generated by any function)
// results in a correct change in the power.
//===================================================================================
//===================================================================================



/*
    @Rule

    @Description:
        Verify correct voting power after any change in (any user) balance.
        We consider the following case:
        - No user is delegating to bob.
        - bob may be delegating and may not.
        - We assume that the function that was call doesn't change the delegation state of bob,
          and the value of _currentExchangeRate.

        We emphasize that we assume that each function that alters the balance of a user (Bob),
        doesn't alter its delegation state (including the delegatee), 
        nor the _currentExchangeRate. We indeed check this property in the rule 
        no_function_changes_both_balance_and_delegation_state().
        
    @Note:

    @Link:
*/
rule vp_change_of_balance_affect_power_NON_DELEGATEE(method f, address bob)
{
    env e;
    calldataarg args;
    require bob != 0;
    
    uint256 bob_bal_before = balanceOf(bob);
    mathint bob_power_before = getPowerCurrent(bob, VOTING_POWER());
    bool is_bob_delegating_before = getDelegatingVoting(bob);
    mathint exchange_rate_before = mirror_currentExchangeRate;

    // The following says the no one delegates to bob
    require forall address a. 
        (mirror_votingDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=VOTING_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );

    requireInvariant user_cant_voting_delegate_to_himself();
    requireInvariant inv_voting_power_correct(bob);
    requireInvariant sum_all_voting_delegated_power_EQ_DelegatingVotingBal(bob);

    f(e,args);
    
    require forall address a. 
        (mirror_votingDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=VOTING_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );

    uint256 bob_bal_after = balanceOf(bob);
    mathint bob_power_after = getPowerCurrent(bob, VOTING_POWER());
    bool is_bob_delegating_after = getDelegatingVoting(bob);
    mathint bob_diff = bob_bal_after - bob_bal_before;
    mathint exchange_rate_after = mirror_currentExchangeRate;

    require (is_bob_delegating_before == is_bob_delegating_after);
    require (exchange_rate_before == exchange_rate_after);
    
    assert !is_bob_delegating_after =>
        upto_1(bob_power_after, bob_power_before + mul_div(bob_diff,mirror_currentExchangeRate));
    assert is_bob_delegating_after => bob_power_after==bob_power_before;
}




    
/*
    @Rule

    @Description:
        Verify correct proposition power after any change in (any user) balance.
        We consider the following case:
        - No user is delegating to bob.
        - bob may be delegating and may not.
        - We assume that the function that was call doesn't change the delegation state of bob,
          and the value of _currentExchangeRate.

        We emphasize that we assume that each function that alters the balance of a user (Bob),
        doesn't alter its delegation state (including the delegatee), 
        nor the _currentExchangeRate. We indeed check this property in the rule 
        no_function_changes_both_balance_and_delegation_state().
        
    @Note:

    @Link:
*/

rule pp_change_of_balance_affect_power_NON_DELEGATEE(method f, address bob)
{
    env e;
    calldataarg args;
    require bob != 0;
    
    uint256 bob_bal_before = balanceOf(bob);
    mathint bob_power_before = getPowerCurrent(bob, PROPOSITION_POWER());
    bool is_bob_delegating_before = getDelegatingProposition(bob);
    mathint exchange_rate_before = mirror_currentExchangeRate;

    // The following says the no one delegates to bob
    require forall address a. 
        (mirror_propositionDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=PROPOSITION_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );

    requireInvariant user_cant_proposition_delegate_to_himself();
    requireInvariant inv_proposition_power_correct(bob);
    requireInvariant sum_all_proposition_delegated_power_EQ_DelegatingPropositionBal(bob);

    f(e,args);
    
    require forall address a. 
        (mirror_propositionDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=PROPOSITION_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );

    uint256 bob_bal_after = balanceOf(bob);
    mathint bob_power_after = getPowerCurrent(bob, PROPOSITION_POWER());
    bool is_bob_delegating_after = getDelegatingProposition(bob);
    mathint bob_diff = bob_bal_after - bob_bal_before;
    mathint exchange_rate_after = mirror_currentExchangeRate;

    require (is_bob_delegating_before == is_bob_delegating_after);
    require exchange_rate_before==exchange_rate_after;
    
    assert !is_bob_delegating_after =>
        upto_1(bob_power_after,bob_power_before + mul_div(bob_diff,mirror_currentExchangeRate));
    assert is_bob_delegating_after => bob_power_after==bob_power_before;
}



