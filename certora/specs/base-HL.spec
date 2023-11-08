

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
            sum_all_voting_delegated_power[new_delegatee] +
            //NN(mirror_balance[delegator]);
            norm(mirror_balance[delegator]);
        sum_all_voting_delegated_power[old_delegatee] = 
            sum_all_voting_delegated_power[old_delegatee] -
            //NN(mirror_balance[delegator]);
            norm(mirror_balance[delegator]);
    }
}
hook Sload address val _votingDelegatee[KEY address delegator] STORAGE {
    require(mirror_votingDelegatee[delegator] == val);
}

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
            sum_all_proposition_delegated_power[new_delegatee] +
            //NN(mirror_balance[delegator]);
            norm(mirror_balance[delegator]);
        sum_all_proposition_delegated_power[old_delegatee] = 
            sum_all_proposition_delegated_power[old_delegatee] -
            //NN(mirror_balance[delegator]);
            norm(mirror_balance[delegator]);

    }
}
hook Sload address val _propositionDelegatee[KEY address delegator] STORAGE {
    require(mirror_propositionDelegatee[delegator] == val);
}

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
            sum_all_voting_delegated_power[mirror_votingDelegatee[a]] +
            //NN(mirror_balance[a]);
            norm(mirror_balance[a]);
    }

    if ( (newVal==PROPOSITION_DELEGATED() || newVal==FULL_POWER_DELEGATED())
         &&
         (oldVal!=PROPOSITION_DELEGATED() && oldVal!=FULL_POWER_DELEGATED())
       ) { // if we start to delegate PROPOSITION now
        sum_all_proposition_delegated_power[mirror_propositionDelegatee[a]] =
            sum_all_proposition_delegated_power[mirror_propositionDelegatee[a]] +
            //NN(mirror_balance[a]);
            norm(mirror_balance[a]);
    }
}
hook Sload StakedAaveV3Harness.DelegationMode val _balances[KEY address a].delegationMode STORAGE {
    require(mirror_delegationMode[a] == val);
}


// =========================================================================
//   mirror_balance
// =========================================================================
ghost mapping(address => uint104) mirror_balance { 
    init_state axiom forall address a. mirror_balance[a] == 0;
}
hook Sstore _balances[KEY address a].balance uint104 balance (uint104 old_balance) STORAGE {
    mirror_balance[a] = balance;

    if (a!=0 &&
        (mirror_delegationMode[a]==FULL_POWER_DELEGATED() ||
         mirror_delegationMode[a]==VOTING_DELEGATED() )
        )
        sum_all_voting_delegated_power[mirror_votingDelegatee[a]] =
            sum_all_voting_delegated_power[mirror_votingDelegatee[a]] + 
            norm(balance) - norm(old_balance);

    if (a!=0 &&
        (mirror_delegationMode[a]==FULL_POWER_DELEGATED() ||
         mirror_delegationMode[a]==PROPOSITION_DELEGATED() )
        )
        sum_all_proposition_delegated_power[mirror_propositionDelegatee[a]] =
            sum_all_proposition_delegated_power[mirror_propositionDelegatee[a]] +
            norm(balance) - norm(old_balance);
}
hook Sload uint104 bal _balances[KEY address a].balance STORAGE {
    require(mirror_balance[a] == bal);
}
