
/*
    This is a specification file for the verification of delegation features.
    This file was adapted from AaveTokenV3.sol smart contract to STK-3.0 smart contract.
    This file is run by the command line: 
          certoraRun --send_only certora/conf/token-v3-delegate.conf
    It uses the harness file: certora/harness/StakedAaveV3Harness.sol
*/

import "base.spec";


methods {
    function _.mul_div_munged(uint256 x, uint256 denominator) external =>
        mul_div(x,denominator) expect uint256 ALL;
    function _.mul_div_munged(uint256 x, uint256 denominator) internal =>
        mul_div(x,denominator) expect uint256 ALL;
    function getExchangeRate() external returns (uint216) envfree;// => ALWAYS(2000000000000000000);
}
//getReserveNormalizedIncome(address) returns (uint256) => ALWAYS(1000000000000000000000000000)
//1000000000000000000
//1234567890123456789

/*
ghost mul_div(mathint , mathint) returns uint256 {
    axiom
        (forall mathint den. mul_div(0,den)==0)
        &&
        (forall mathint a. forall mathint b. forall mathint deno.
         (mul_div(a+b,deno) + 0 == mul_div(a,deno) + mul_div(b,deno))
          &&
         (mul_div(0-a,deno) + 0 == 0 - mul_div(a,deno))
         // || (mul_div(a+b,deno) + 0 == mul_div(a,deno) + mul_div(b,deno)+1)
         // || (mul_div(a+b,deno) + 0 == mul_div(a,deno) + mul_div(b,deno)-1)
        );
}
*/


ghost mul_div(mathint , mathint) returns uint256 {
    axiom
        (forall mathint a. forall mathint deno.
         (mul_div(a,deno)+0 == 2*a) 
        );
        }


/*
ghost mul_div(mathint , mathint) returns uint256 {
    axiom
        (forall mathint a. forall mathint deno.
         (mul_div(a,deno)+0 == (a * 10^18) / deno) 
        );
        }*/



function normalizeNew(uint256 amount) returns mathint {
    return mul_div(amount / DELEGATED_POWER_DIVIDER() * DELEGATED_POWER_DIVIDER(),getExchangeRate());
}

definition NN(mathint bal) returns mathint =  mul_div(bal/(10^10)*(10^10),mirror_currentExchangeRate) ;



definition is_stake_redeem_method(method f) returns bool =
    f.selector == sig:stakeWithPermit(uint256,uint256,uint8,bytes32,bytes32).selector ||
    f.selector == sig:redeem(address,uint256).selector ||
    f.selector == sig:claimRewardsAndStake(address,uint256).selector ||
    f.selector == sig:claimRewardsAndRedeemOnBehalf(address,address,uint256,uint256).selector ||
    f.selector == sig:claimRewardsAndRedeem(address,uint256,uint256).selector ||
    f.selector == sig:claimRewardsAndStakeOnBehalf(address,address,uint256).selector ||
    f.selector == sig:redeemOnBehalf(address,address,uint256).selector ||
    f.selector == sig:stake(address,uint256).selector
    ;


ghost uint216 mirror_currentExchangeRate {
    init_state axiom mirror_currentExchangeRate==0;
}
hook Sstore _currentExchangeRate uint216 newVal (uint216 oldVal) STORAGE {
    mirror_currentExchangeRate = newVal;
}
hook Sload uint216 val _currentExchangeRate STORAGE {
    require(mirror_currentExchangeRate == val);
}




ghost mapping(address => mathint) sum_all_voting_delegated_power {
    init_state axiom forall address delegatee. sum_all_voting_delegated_power[delegatee] == 0;
}
ghost mapping(address => mathint) sum_all_proposition_delegated_power {
    init_state axiom forall address delegatee. sum_all_proposition_delegated_power[delegatee] == 0;
}

// =========================================================================
//   mirror_votingDelegatee
// =========================================================================
ghost mapping(address => address) mirror_votingDelegatee { 
    init_state axiom forall address a. mirror_votingDelegatee[a] == 0;
}
hook Sstore _votingDelegatee[KEY address delegator] address new_delegatee (address old_delegatee) STORAGE {
    mirror_votingDelegatee[delegator] = new_delegatee;
    if ((mirror_delegationMode[delegator]==FULL_POWER_DELEGATED() ||
         mirror_delegationMode[delegator]==VOTING_DELEGATED()) &&
        new_delegatee != old_delegatee) { // if a delegator changes his delegatee
        sum_all_voting_delegated_power[new_delegatee] =
            sum_all_voting_delegated_power[new_delegatee] + NN(mirror_balance[delegator]);
        //            mul_div(mirror_balance[delegator]/(10^10)*(10^10),2) ;
        sum_all_voting_delegated_power[old_delegatee] = 
            sum_all_voting_delegated_power[old_delegatee] - NN(mirror_balance[delegator]);
        //            mul_div(mirror_balance[delegator]/(10^10)*(10^10),2);
    }
}
hook Sload address val _votingDelegatee[KEY address delegator] STORAGE {
    require(mirror_votingDelegatee[delegator] == val);
}
invariant mirror_votingDelegatee_correct()
    forall address a.mirror_votingDelegatee[a] == getVotingDelegatee(a);

// =========================================================================
//   mirror_propositionDelegatee
// =========================================================================
ghost mapping(address => address) mirror_propositionDelegatee { 
    init_state axiom forall address a. mirror_propositionDelegatee[a] == 0;
}
hook Sstore _propositionDelegatee[KEY address delegator] address new_delegatee (address old_delegatee) STORAGE {
    mirror_propositionDelegatee[delegator] = new_delegatee;
    if ((mirror_delegationMode[delegator]==FULL_POWER_DELEGATED() ||
         mirror_delegationMode[delegator]==PROPOSITION_DELEGATED()) &&
        new_delegatee != old_delegatee) { // if a delegator changes his delegatee
        sum_all_proposition_delegated_power[new_delegatee] =
            sum_all_proposition_delegated_power[new_delegatee] + NN(mirror_balance[delegator]);
        sum_all_proposition_delegated_power[old_delegatee] = 
            sum_all_proposition_delegated_power[old_delegatee] - NN(mirror_balance[delegator]);
    }
}
hook Sload address val _propositionDelegatee[KEY address delegator] STORAGE {
    require(mirror_propositionDelegatee[delegator] == val);
}
invariant mirror_propositionDelegatee_correct()
    forall address a.mirror_propositionDelegatee[a] == getPropositionDelegatee(a);


// =========================================================================
//   mirror_delegationMode
// =========================================================================
ghost mapping(address => StakedAaveV3Harness.DelegationMode) mirror_delegationMode { 
    init_state axiom forall address a. mirror_delegationMode[a] ==
        StakedAaveV3Harness.DelegationMode.NO_DELEGATION;
}
hook Sstore _balances[KEY address a].delegationMode StakedAaveV3Harness.DelegationMode newVal (StakedAaveV3Harness.DelegationMode oldVal) STORAGE {
    mirror_delegationMode[a] = newVal;

    if ( (newVal==VOTING_DELEGATED() || newVal==FULL_POWER_DELEGATED())
         &&
         (oldVal!=VOTING_DELEGATED() && oldVal!=FULL_POWER_DELEGATED())
       ) { // if we start to delegate VOTING now
        sum_all_voting_delegated_power[mirror_votingDelegatee[a]] =
            sum_all_voting_delegated_power[mirror_votingDelegatee[a]] + NN(mirror_balance[a]);
    }

    if ( (newVal==PROPOSITION_DELEGATED() || newVal==FULL_POWER_DELEGATED())
         &&
         (oldVal!=PROPOSITION_DELEGATED() && oldVal!=FULL_POWER_DELEGATED())
       ) { // if we start to delegate PROPOSITION now
        sum_all_proposition_delegated_power[mirror_propositionDelegatee[a]] =
            sum_all_proposition_delegated_power[mirror_propositionDelegatee[a]] +NN(mirror_balance[a]);
    }
}
hook Sload StakedAaveV3Harness.DelegationMode val _balances[KEY address a].delegationMode STORAGE {
    require(mirror_delegationMode[a] == val);
}
invariant mirror_delegationMode_correct()
    forall address a.mirror_delegationMode[a] == getDelegationMode(a);



// =========================================================================
//   mirror_balance
// =========================================================================
ghost mapping(address => uint104) mirror_balance { 
    init_state axiom forall address a. mirror_balance[a] == 0;
}
hook Sstore _balances[KEY address a].balance uint104 balance (uint104 old_balance) STORAGE {
    mirror_balance[a] = balance;
    //sum_all_voting_delegated_power[a] = sum_all_voting_delegated_power[a] + balance - old_balance;
    // The code should be:
    // if a delegates to b, sum_all_voting_delegated_power[b] += the diff of balances of a
    if (a!=0 &&
        (mirror_delegationMode[a]==FULL_POWER_DELEGATED() ||
         mirror_delegationMode[a]==VOTING_DELEGATED() )
        )
        sum_all_voting_delegated_power[mirror_votingDelegatee[a]] =
            sum_all_voting_delegated_power[mirror_votingDelegatee[a]] +
            NN(balance) - NN(old_balance);
    //(balance/ (10^10) * (10^10)) - (old_balance/ (10^10) * (10^10)) ;

    if (a!=0 &&
        (mirror_delegationMode[a]==FULL_POWER_DELEGATED() ||
         mirror_delegationMode[a]==PROPOSITION_DELEGATED() )
        )
        sum_all_proposition_delegated_power[mirror_propositionDelegatee[a]] =
            sum_all_proposition_delegated_power[mirror_propositionDelegatee[a]] +
            NN(balance) - NN(old_balance);
    //            (balance/ (10^10) * (10^10)) - (old_balance/ (10^10) * (10^10)) ;
}
hook Sload uint104 bal _balances[KEY address a].balance STORAGE {
    require(mirror_balance[a] == bal);
}
invariant mirror_balance_correct()
    forall address a.mirror_balance[a] == getBalance(a);


invariant inv_voting_power_correct(address user)
    user != 0 =>
    (
     to_mathint(getPowerCurrent(user, VOTING_POWER()))
     ==
     sum_all_voting_delegated_power[user] +
     ( (mirror_delegationMode[user]==FULL_POWER_DELEGATED() ||
        mirror_delegationMode[user]==VOTING_DELEGATED()) ?
       0 : mul_div(mirror_balance[user],mirror_currentExchangeRate))
    )
//    filtered {f -> !is_stake_redeem_method(f)}
{
    preserved with (env e) {
        requireInvariant user_cant_voting_delegate_to_himself();
    }
}


invariant inv_proposition_power_correct(address user)
    user != 0 =>
    (
     to_mathint(getPowerCurrent(user, PROPOSITION_POWER()))
     ==
     sum_all_proposition_delegated_power[user] +
     ( (mirror_delegationMode[user]==FULL_POWER_DELEGATED() ||
        mirror_delegationMode[user]==PROPOSITION_DELEGATED()) ?
       0 : mul_div(mirror_balance[user],mirror_currentExchangeRate))
    )
//filtered {f -> !is_stake_redeem_method(f)}
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

    f(e,args);

    uint256 bob_balance_after = balanceOf(bob);
    bool is_bob_delegating_voting_after = getDelegatingVoting(bob);
    address bob_delegatee_after = mirror_votingDelegatee[bob];

    assert (bob_balance_before != bob_balance_after =>
            (is_bob_delegating_voting_before==is_bob_delegating_voting_after &&
             bob_delegatee_before == bob_delegatee_after)
           );

    assert (bob_delegatee_before != bob_delegatee_after =>
            bob_balance_before == bob_balance_after
           );

    assert (is_bob_delegating_voting_before!=is_bob_delegating_voting_after =>
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
        - bob is the delegatee of alice1, and possibly of alice2. No other user delegates
        to bob.
        - bob may be delegating and may not.
        - We assume that the function that was call doesn't change the delegation state of neither
          bob, alice1 or alice2.

        We emphasize that we assume that no function alters both the balance of a user (Bob),
        and its delegation state (including the delegatee). We indeed check this property in the
        rule no_function_changes_both_balance_and_delegation_state().
        
    @Note:

    @Link:
*/
rule vp_change_in_balance_affect_power_DELEGATEE(method f,address bob,address alice1,address alice2)
//filtered {f -> !is_stake_redeem_method(f)}
{
    env e;
    calldataarg args;
    require bob != 0; require alice1 != 0; require alice2 != 0;
    require (bob != alice1 && bob != alice2 && alice1 != alice2);

    uint256 bob_bal_before = balanceOf(bob);
    mathint bob_power_before = getPowerCurrent(bob, VOTING_POWER());
    bool is_bob_delegating_before = getDelegatingVoting(bob);

    uint256 alice1_bal_before = balanceOf(alice1);
    bool is_alice1_delegating_before = getDelegatingVoting(alice1);
    address alice1D_before = getVotingDelegatee(alice1); // alice1D == alice1_delegatee
    uint256 alice2_bal_before = balanceOf(alice2);
    bool is_alice2_delegating_before = getDelegatingVoting(alice2);
    address alice2D_before = getVotingDelegatee(alice2); // alice2D == alice2_delegatee

    // The following says that alice1 is delegating to bob, alice2 may do so, and no other
    // user may do so.
    require (is_alice1_delegating_before && alice1D_before == bob);
    require forall address a. (a!=alice1 && a!=alice2) =>
        (mirror_votingDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=VOTING_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );

    requireInvariant user_cant_voting_delegate_to_himself();
    requireInvariant inv_voting_power_correct(alice1);
    requireInvariant inv_voting_power_correct(alice2);
    requireInvariant inv_voting_power_correct(bob);

    f(e,args);
    
    uint256 alice1_bal_after = balanceOf(alice1);
    mathint alice1_power_after = getPowerCurrent(alice1,VOTING_POWER());
    bool is_alice1_delegating_after = getDelegatingVoting(alice1);
    address alice1D_after = getVotingDelegatee(alice1); // alice1D == alice1_delegatee
    uint256 alice2_bal_after = balanceOf(alice2);
    mathint alice2_power_after = getPowerCurrent(alice2,VOTING_POWER());
    bool is_alice2_delegating_after = getDelegatingVoting(alice2);
    address alice2D_after = getVotingDelegatee(alice2); // alice2D == alice2_delegatee

    require (is_alice1_delegating_after && alice1D_after == bob);
    require forall address a. (a!=alice1 && a!=alice2) =>
        (mirror_votingDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=VOTING_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );
    // No change in the delegation state of alice2
    require (is_alice2_delegating_before==is_alice2_delegating_after &&
             alice2D_before == alice2D_after);

    uint256 bob_bal_after = balanceOf(bob);
    mathint bob_power_after = getPowerCurrent(bob, VOTING_POWER());
    bool is_bob_delegating_after = getDelegatingVoting(bob);

    // No change in the delegation state of bob
    require (is_bob_delegating_before == is_bob_delegating_after);

    mathint alice1_diff = 
        (is_alice1_delegating_after && alice1D_after==bob) ?
        NN(alice1_bal_after) - NN(alice1_bal_before) : 0;


    mathint alice2_diff = 
        (is_alice2_delegating_after && alice2D_after==bob) ?
        NN(alice2_bal_after) - NN(alice2_bal_before) : 0;


    
    mathint bob_diff = mul_div(bob_bal_after - bob_bal_before, mirror_currentExchangeRate);
    
    assert
        !is_bob_delegating_after =>
        bob_power_after == bob_power_before + alice1_diff + alice2_diff + bob_diff;

    assert
        is_bob_delegating_after =>
        bob_power_after == bob_power_before + alice1_diff + alice2_diff;
}



/*
    @Rule

    @Description:
        Verify correct voting power after any change in (any user) balance.
        We consider the following case:
        - No user is delegating to bob.
        - bob may be delegating and may not.
        - We assume that the function that was call doesn't change the delegation state of bob.

        We emphasize that we assume that no function alters both the balance of a user (Bob),
        and its delegation state (including the delegatee). We indeed check this property in the
        rule no_function_changes_both_balance_and_delegation_state().
        
    @Note:

    @Link:
*/
rule vp_change_of_balance_affect_power_NON_DELEGATEE(method f, address bob)
//    filtered {f -> !is_stake_redeem_method(f)}
{
    env e;
    calldataarg args;
    require bob != 0;
    
    uint256 bob_bal_before = balanceOf(bob);
    mathint bob_power_before = getPowerCurrent(bob, VOTING_POWER());
    bool is_bob_delegating_before = getDelegatingVoting(bob);

    // The following says the no one delegates to bob
    require forall address a. 
        (mirror_votingDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=VOTING_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );

    requireInvariant user_cant_voting_delegate_to_himself();
    requireInvariant inv_voting_power_correct(bob);

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

    require (is_bob_delegating_before == is_bob_delegating_after);
    
    assert !is_bob_delegating_after =>
        bob_power_after==bob_power_before + mul_div(bob_diff,mirror_currentExchangeRate);
    assert is_bob_delegating_after => bob_power_after==bob_power_before;
}




/*
    @Rule

    @Description:
        Verify correct proposition power after any change in (any user) balance.
        We consider the following case:
        - bob is the delegatee of alice1, and possibly of alice2. No other user delegates
        to bob.
        - bob may be delegating and may not.
        - We assume that the function that was call doesn't change the delegation state of neither
          bob, alice1 or alice2.

        We emphasize that we assume that no function alters both the balance of a user (Bob),
        and its delegation state (including the delegatee). We indeed check this property in the
        rule no_function_changes_both_balance_and_delegation_state().
        
    @Note:

    @Link:
*/
rule pp_change_in_balance_affect_power_DELEGATEE(method f,address bob,address alice1,address alice2)
//    filtered {f -> !is_stake_redeem_method(f)}
{
    env e;
    calldataarg args;
    require bob != 0; require alice1 != 0; require alice2 != 0;
    require (bob != alice1 && bob != alice2 && alice1 != alice2);

    uint256 bob_bal_before = balanceOf(bob);
    mathint bob_power_before = getPowerCurrent(bob, PROPOSITION_POWER());
    bool is_bob_delegating_before = getDelegatingProposition(bob);

    uint256 alice1_bal_before = balanceOf(alice1);
    bool is_alice1_delegating_before = getDelegatingProposition(alice1);
    address alice1D_before = getPropositionDelegatee(alice1); // alice1D == alice1_delegatee
    uint256 alice2_bal_before = balanceOf(alice2);
    bool is_alice2_delegating_before = getDelegatingProposition(alice2);
    address alice2D_before = getPropositionDelegatee(alice2); // alice2D == alice2_delegatee

    // The following says that alice1 is delegating to bob, alice2 may do so, and no other
    // user may do so.
    require (is_alice1_delegating_before && alice1D_before == bob);
    require forall address a. (a!=alice1 && a!=alice2) =>
        (mirror_propositionDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=PROPOSITION_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );

    requireInvariant user_cant_proposition_delegate_to_himself();
    requireInvariant inv_proposition_power_correct(alice1);
    requireInvariant inv_proposition_power_correct(alice2);
    requireInvariant inv_proposition_power_correct(bob);

    f(e,args);
    
    uint256 alice1_bal_after = balanceOf(alice1);
    mathint alice1_power_after = getPowerCurrent(alice1,PROPOSITION_POWER());
    bool is_alice1_delegating_after = getDelegatingProposition(alice1);
    address alice1D_after = getPropositionDelegatee(alice1); // alice1D == alice1_delegatee
    uint256 alice2_bal_after = balanceOf(alice2);
    mathint alice2_power_after = getPowerCurrent(alice2,PROPOSITION_POWER());
    bool is_alice2_delegating_after = getDelegatingProposition(alice2);
    address alice2D_after = getPropositionDelegatee(alice2); // alice2D == alice2_delegatee

    require (is_alice1_delegating_after && alice1D_after == bob);
    require forall address a. (a!=alice1 && a!=alice2) =>
        (mirror_propositionDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=PROPOSITION_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );
    // No change in the delegation state of alice2
    require (is_alice2_delegating_before==is_alice2_delegating_after &&
             alice2D_before == alice2D_after);

    uint256 bob_bal_after = balanceOf(bob);
    mathint bob_power_after = getPowerCurrent(bob, PROPOSITION_POWER());
    bool is_bob_delegating_after = getDelegatingProposition(bob);

    // No change in the delegation state of bob
    require (is_bob_delegating_before == is_bob_delegating_after);

    mathint alice1_diff = 
        (is_alice1_delegating_after && alice1D_after==bob) ?
        NN(alice1_bal_after)-NN(alice1_bal_before) : 0;
        //        normalize(alice1_bal_after) - normalize(alice1_bal_before) : 0;

    mathint alice2_diff = 
        (is_alice2_delegating_after && alice2D_after==bob) ?
        NN(alice2_bal_after)-NN(alice2_bal_before) : 0;
    //        mul_div(normalize(alice2_bal_after),mirror_currentExchangeRate) -
    //   mul_div(normalize(alice2_bal_before) : 0;

    mathint bob_diff = mul_div(bob_bal_after - bob_bal_before, mirror_currentExchangeRate);
    
    assert
        !is_bob_delegating_after =>
        bob_power_after == bob_power_before + alice1_diff + alice2_diff + bob_diff;

    assert
        is_bob_delegating_after =>
        bob_power_after == bob_power_before + alice1_diff + alice2_diff;
}



/*
    @Rule

    @Description:
        Verify correct proposition power after any change in (any user) balance.
        We consider the following case:
        - No user is delegating to bob.
        - bob may be delegating and may not.
        - We assume that the function that was call doesn't change the delegation state of bob.

        We emphasize that we assume that no function alters both the balance of a user (Bob),
        and its delegation state (including the delegatee). We indeed check this property in the
        rule no_function_changes_both_balance_and_delegation_state().
        
    @Note:

    @Link:
*/

rule pp_change_of_balance_affect_power_NON_DELEGATEE(method f, address bob)
//    filtered {f -> !is_stake_redeem_method(f)}
{
    env e;
    calldataarg args;
    require bob != 0;
    
    uint256 bob_bal_before = balanceOf(bob);
    mathint bob_power_before = getPowerCurrent(bob, PROPOSITION_POWER());
    bool is_bob_delegating_before = getDelegatingProposition(bob);

    // The following says the no one delegates to bob
    require forall address a. 
        (mirror_propositionDelegatee[a] != bob ||
         (mirror_delegationMode[a]!=PROPOSITION_DELEGATED() &&
          mirror_delegationMode[a]!=FULL_POWER_DELEGATED()
         )
        );

    requireInvariant user_cant_proposition_delegate_to_himself();
    requireInvariant inv_proposition_power_correct(bob);

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

    require (is_bob_delegating_before == is_bob_delegating_after);
    
    assert !is_bob_delegating_after =>
        bob_power_after==bob_power_before + mul_div(bob_diff,mirror_currentExchangeRate);
    assert is_bob_delegating_after => bob_power_after==bob_power_before;
}


