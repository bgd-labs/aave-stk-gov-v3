```diff
diff --git a/src/etherscan/mainnet_0xe42f02713aec989132c1755117f768dbea523d2f/StakedTokenV2Rev3/Contract.sol b/src/flattened/StakedAaveV3Flattened.sol
index 83f9691..b4a600a 100644
--- a/src/etherscan/mainnet_0xe42f02713aec989132c1755117f768dbea523d2f/StakedTokenV2Rev3/Contract.sol
+++ b/src/flattened/StakedAaveV3Flattened.sol
@@ -1,124 +1,50 @@
-/**
- *Submitted for verification at Etherscan.io on 2020-12-10
- */
-
 // SPDX-License-Identifier: agpl-3.0
-pragma solidity 0.7.5;
-pragma experimental ABIEncoderV2;
+pragma solidity ^0.8.0;
 
-interface IGovernancePowerDelegationToken {
-  enum DelegationType {
-    VOTING_POWER,
-    PROPOSITION_POWER
-  }
+// most imports are only here to force import order for better (i.e smaller) diff on flattening
 
-  /**
-   * @dev emitted when a user delegates to another
-   * @param delegator the delegator
-   * @param delegatee the delegatee
-   * @param delegationType the type of delegation (VOTING_POWER, PROPOSITION_POWER)
-   **/
-  event DelegateChanged(
-    address indexed delegator,
-    address indexed delegatee,
-    DelegationType delegationType
-  );
-
-  /**
-   * @dev emitted when an action changes the delegated power of a user
-   * @param user the user which delegated power has changed
-   * @param amount the amount of delegated power for the user
-   * @param delegationType the type of delegation (VOTING_POWER, PROPOSITION_POWER)
-   **/
-  event DelegatedPowerChanged(
-    address indexed user,
-    uint256 amount,
-    DelegationType delegationType
-  );
-
-  /**
-   * @dev delegates the specific power to a delegatee
-   * @param delegatee the user which delegated power has changed
-   * @param delegationType the type of delegation (VOTING_POWER, PROPOSITION_POWER)
-   **/
-  function delegateByType(address delegatee, DelegationType delegationType)
-    external
-    virtual;
-
-  /**
-   * @dev delegates all the powers to a specific user
-   * @param delegatee the user to which the power will be delegated
-   **/
-  function delegate(address delegatee) external virtual;
-
-  /**
-   * @dev returns the delegatee of an user
-   * @param delegator the address of the delegator
-   **/
-  function getDelegateeByType(address delegator, DelegationType delegationType)
-    external
-    view
-    virtual
-    returns (address);
-
-  /**
-   * @dev returns the current delegated power of a user. The current power is the
-   * power delegated at the time of the last snapshot
-   * @param user the user
-   **/
-  function getPowerCurrent(address user, DelegationType delegationType)
-    external
-    view
-    virtual
-    returns (uint256);
-
-  /**
-   * @dev returns the delegated power of a user at a certain block
-   * @param user the user
-   **/
-  function getPowerAtBlock(
-    address user,
-    uint256 blockNumber,
-    DelegationType delegationType
-  ) external view virtual returns (uint256);
-
-  /**
-   * @dev returns the total supply at a certain block number
-   **/
-  function totalSupplyAt(uint256 blockNumber)
-    external
-    view
-    virtual
-    returns (uint256);
-}
+// OpenZeppelin Contracts v4.4.1 (utils/Context.sol)
 
 /**
- * @dev From https://github.com/OpenZeppelin/openzeppelin-contracts
- * Provides information about the current execution context, including the
+ * @dev Provides information about the current execution context, including the
  * sender of the transaction and its data. While these are generally available
  * via msg.sender and msg.data, they should not be accessed in such a direct
- * manner, since when dealing with GSN meta-transactions the account sending and
+ * manner, since when dealing with meta-transactions the account sending and
  * paying for execution may not be the actual sender (as far as an application
  * is concerned).
  *
  * This contract is only required for intermediate, library-like contracts.
  */
 abstract contract Context {
-  function _msgSender() internal view virtual returns (address payable) {
+  function _msgSender() internal view virtual returns (address) {
     return msg.sender;
   }
 
-  function _msgData() internal view virtual returns (bytes memory) {
-    this; // silence state mutability warning without generating bytecode - see https://github.com/ethereum/solidity/issues/2691
+  function _msgData() internal view virtual returns (bytes calldata) {
     return msg.data;
   }
 }
 
+// OpenZeppelin Contracts (last updated v4.6.0) (token/ERC20/IERC20.sol)
+
 /**
  * @dev Interface of the ERC20 standard as defined in the EIP.
- * From https://github.com/OpenZeppelin/openzeppelin-contracts
  */
 interface IERC20 {
+  /**
+   * @dev Emitted when `value` tokens are moved from one account (`from`) to
+   * another (`to`).
+   *
+   * Note that `value` may be zero.
+   */
+  event Transfer(address indexed from, address indexed to, uint256 value);
+
+  /**
+   * @dev Emitted when the allowance of a `spender` for an `owner` is set by
+   * a call to {approve}. `value` is the new allowance.
+   */
+  event Approval(address indexed owner, address indexed spender, uint256 value);
+
   /**
    * @dev Returns the amount of tokens in existence.
    */
@@ -130,13 +56,13 @@ interface IERC20 {
   function balanceOf(address account) external view returns (uint256);
 
   /**
-   * @dev Moves `amount` tokens from the caller's account to `recipient`.
+   * @dev Moves `amount` tokens from the caller's account to `to`.
    *
    * Returns a boolean value indicating whether the operation succeeded.
    *
    * Emits a {Transfer} event.
    */
-  function transfer(address recipient, uint256 amount) external returns (bool);
+  function transfer(address to, uint256 amount) external returns (bool);
 
   /**
    * @dev Returns the remaining number of tokens that `spender` will be
@@ -167,7 +93,7 @@ interface IERC20 {
   function approve(address spender, uint256 amount) external returns (bool);
 
   /**
-   * @dev Moves `amount` tokens from `sender` to `recipient` using the
+   * @dev Moves `amount` tokens from `from` to `to` using the
    * allowance mechanism. `amount` is then deducted from the caller's
    * allowance.
    *
@@ -176,249 +102,36 @@ interface IERC20 {
    * Emits a {Transfer} event.
    */
   function transferFrom(
-    address sender,
-    address recipient,
+    address from,
+    address to,
     uint256 amount
   ) external returns (bool);
+}
 
-  /**
-   * @dev Emitted when `value` tokens are moved from one account (`from`) to
-   * another (`to`).
-   *
-   * Note that `value` may be zero.
-   */
-  event Transfer(address indexed from, address indexed to, uint256 value);
+// OpenZeppelin Contracts (last updated v4.8.0) (token/ERC20/ERC20.sol)
 
-  /**
-   * @dev Emitted when the allowance of a `spender` for an `owner` is set by
-   * a call to {approve}. `value` is the new allowance.
-   */
-  event Approval(address indexed owner, address indexed spender, uint256 value);
-}
+// OpenZeppelin Contracts v4.4.1 (token/ERC20/extensions/IERC20Metadata.sol)
 
 /**
- * @dev From https://github.com/OpenZeppelin/openzeppelin-contracts
- * Wrappers over Solidity's arithmetic operations with added overflow
- * checks.
- *
- * Arithmetic operations in Solidity wrap on overflow. This can easily result
- * in bugs, because programmers usually assume that an overflow raises an
- * error, which is the standard behavior in high level programming languages.
- * `SafeMath` restores this intuition by reverting the transaction when an
- * operation overflows.
+ * @dev Interface for the optional metadata functions from the ERC20 standard.
  *
- * Using this library instead of the unchecked operations eliminates an entire
- * class of bugs, so it's recommended to use it always.
+ * _Available since v4.1._
  */
-library SafeMath {
+interface IERC20Metadata is IERC20 {
   /**
-   * @dev Returns the addition of two unsigned integers, reverting on
-   * overflow.
-   *
-   * Counterpart to Solidity's `+` operator.
-   *
-   * Requirements:
-   * - Addition cannot overflow.
+   * @dev Returns the name of the token.
    */
-  function add(uint256 a, uint256 b) internal pure returns (uint256) {
-    uint256 c = a + b;
-    require(c >= a, 'SafeMath: addition overflow');
-
-    return c;
-  }
+  function name() external view returns (string memory);
 
   /**
-   * @dev Returns the subtraction of two unsigned integers, reverting on
-   * overflow (when the result is negative).
-   *
-   * Counterpart to Solidity's `-` operator.
-   *
-   * Requirements:
-   * - Subtraction cannot overflow.
+   * @dev Returns the symbol of the token.
    */
-  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
-    return sub(a, b, 'SafeMath: subtraction overflow');
-  }
+  function symbol() external view returns (string memory);
 
   /**
-   * @dev Returns the subtraction of two unsigned integers, reverting with custom message on
-   * overflow (when the result is negative).
-   *
-   * Counterpart to Solidity's `-` operator.
-   *
-   * Requirements:
-   * - Subtraction cannot overflow.
+   * @dev Returns the decimals places of the token.
    */
-  function sub(
-    uint256 a,
-    uint256 b,
-    string memory errorMessage
-  ) internal pure returns (uint256) {
-    require(b <= a, errorMessage);
-    uint256 c = a - b;
-
-    return c;
-  }
-
-  /**
-   * @dev Returns the multiplication of two unsigned integers, reverting on
-   * overflow.
-   *
-   * Counterpart to Solidity's `*` operator.
-   *
-   * Requirements:
-   * - Multiplication cannot overflow.
-   */
-  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
-    // Gas optimization: this is cheaper than requiring 'a' not being zero, but the
-    // benefit is lost if 'b' is also tested.
-    // See: https://github.com/OpenZeppelin/openzeppelin-contracts/pull/522
-    if (a == 0) {
-      return 0;
-    }
-
-    uint256 c = a * b;
-    require(c / a == b, 'SafeMath: multiplication overflow');
-
-    return c;
-  }
-
-  /**
-   * @dev Returns the integer division of two unsigned integers. Reverts on
-   * division by zero. The result is rounded towards zero.
-   *
-   * Counterpart to Solidity's `/` operator. Note: this function uses a
-   * `revert` opcode (which leaves remaining gas untouched) while Solidity
-   * uses an invalid opcode to revert (consuming all remaining gas).
-   *
-   * Requirements:
-   * - The divisor cannot be zero.
-   */
-  function div(uint256 a, uint256 b) internal pure returns (uint256) {
-    return div(a, b, 'SafeMath: division by zero');
-  }
-
-  /**
-   * @dev Returns the integer division of two unsigned integers. Reverts with custom message on
-   * division by zero. The result is rounded towards zero.
-   *
-   * Counterpart to Solidity's `/` operator. Note: this function uses a
-   * `revert` opcode (which leaves remaining gas untouched) while Solidity
-   * uses an invalid opcode to revert (consuming all remaining gas).
-   *
-   * Requirements:
-   * - The divisor cannot be zero.
-   */
-  function div(
-    uint256 a,
-    uint256 b,
-    string memory errorMessage
-  ) internal pure returns (uint256) {
-    // Solidity only automatically asserts when dividing by 0
-    require(b > 0, errorMessage);
-    uint256 c = a / b;
-    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
-
-    return c;
-  }
-
-  /**
-   * @dev Returns the remainder of dividing two unsigned integers. (unsigned integer modulo),
-   * Reverts when dividing by zero.
-   *
-   * Counterpart to Solidity's `%` operator. This function uses a `revert`
-   * opcode (which leaves remaining gas untouched) while Solidity uses an
-   * invalid opcode to revert (consuming all remaining gas).
-   *
-   * Requirements:
-   * - The divisor cannot be zero.
-   */
-  function mod(uint256 a, uint256 b) internal pure returns (uint256) {
-    return mod(a, b, 'SafeMath: modulo by zero');
-  }
-
-  /**
-   * @dev Returns the remainder of dividing two unsigned integers. (unsigned integer modulo),
-   * Reverts with custom message when dividing by zero.
-   *
-   * Counterpart to Solidity's `%` operator. This function uses a `revert`
-   * opcode (which leaves remaining gas untouched) while Solidity uses an
-   * invalid opcode to revert (consuming all remaining gas).
-   *
-   * Requirements:
-   * - The divisor cannot be zero.
-   */
-  function mod(
-    uint256 a,
-    uint256 b,
-    string memory errorMessage
-  ) internal pure returns (uint256) {
-    require(b != 0, errorMessage);
-    return a % b;
-  }
-}
-
-/**
- * @dev Collection of functions related to the address type
- * From https://github.com/OpenZeppelin/openzeppelin-contracts
- */
-library Address {
-  /**
-   * @dev Returns true if `account` is a contract.
-   *
-   * [IMPORTANT]
-   * ====
-   * It is unsafe to assume that an address for which this function returns
-   * false is an externally-owned account (EOA) and not a contract.
-   *
-   * Among others, `isContract` will return false for the following
-   * types of addresses:
-   *
-   *  - an externally-owned account
-   *  - a contract in construction
-   *  - an address where a contract will be created
-   *  - an address where a contract lived, but was destroyed
-   * ====
-   */
-  function isContract(address account) internal view returns (bool) {
-    // According to EIP-1052, 0x0 is the value returned for not-yet created accounts
-    // and 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470 is returned
-    // for accounts without code, i.e. `keccak256('')`
-    bytes32 codehash;
-    bytes32 accountHash = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
-    // solhint-disable-next-line no-inline-assembly
-    assembly {
-      codehash := extcodehash(account)
-    }
-    return (codehash != accountHash && codehash != 0x0);
-  }
-
-  /**
-   * @dev Replacement for Solidity's `transfer`: sends `amount` wei to
-   * `recipient`, forwarding all available gas and reverting on errors.
-   *
-   * https://eips.ethereum.org/EIPS/eip-1884[EIP1884] increases the gas cost
-   * of certain opcodes, possibly making contracts go over the 2300 gas limit
-   * imposed by `transfer`, making them unable to receive funds via
-   * `transfer`. {sendValue} removes this limitation.
-   *
-   * https://diligence.consensys.net/posts/2019/09/stop-using-soliditys-transfer-now/[Learn more].
-   *
-   * IMPORTANT: because control is transferred to `recipient`, care must be
-   * taken to not create reentrancy vulnerabilities. Consider using
-   * {ReentrancyGuard} or the
-   * https://solidity.readthedocs.io/en/v0.5.11/security-considerations.html#use-the-checks-effects-interactions-pattern[checks-effects-interactions pattern].
-   */
-  function sendValue(address payable recipient, uint256 amount) internal {
-    require(address(this).balance >= amount, 'Address: insufficient balance');
-
-    // solhint-disable-next-line avoid-low-level-calls, avoid-call-value
-    (bool success, ) = recipient.call{value: amount}('');
-    require(
-      success,
-      'Address: unable to send value, recipient may have reverted'
-    );
-  }
+  function decimals() external view returns (uint8);
 }
 
 /**
@@ -429,12 +142,13 @@ library Address {
  * For a generic mechanism see {ERC20PresetMinterPauser}.
  *
  * TIP: For a detailed writeup see our guide
- * https://forum.zeppelin.solutions/t/how-to-implement-erc20-supply-mechanisms/226[How
+ * https://forum.openzeppelin.com/t/how-to-implement-erc20-supply-mechanisms/226[How
  * to implement supply mechanisms].
  *
- * We have followed general OpenZeppelin guidelines: functions revert instead
- * of returning `false` on failure. This behavior is nonetheless conventional
- * and does not conflict with the expectations of ERC20 applications.
+ * We have followed general OpenZeppelin Contracts guidelines: functions revert
+ * instead returning `false` on failure. This behavior is nonetheless
+ * conventional and does not conflict with the expectations of ERC20
+ * applications.
  *
  * Additionally, an {Approval} event is emitted on calls to {transferFrom}.
  * This allows applications to reconstruct the allowance for all accounts just
@@ -445,39 +159,32 @@ library Address {
  * functions have been added to mitigate the well-known issues around setting
  * allowances. See {IERC20-approve}.
  */
-contract ERC20 is Context, IERC20 {
-  using SafeMath for uint256;
-  using Address for address;
-
-  mapping(address => uint256) private _balances;
+contract ERC20 is Context, IERC20, IERC20Metadata {
+  mapping(address => uint256) internal _balances;
 
   mapping(address => mapping(address => uint256)) private _allowances;
 
-  uint256 private _totalSupply;
+  uint256 internal _totalSupply;
 
-  string internal _name;
-  string internal _symbol;
-  uint8 private _decimals;
+  string private _name;
+  string private _symbol;
+  uint8 private _decimals; // @deprecated
 
   /**
-   * @dev Sets the values for {name} and {symbol}, initializes {decimals} with
-   * a default value of 18.
+   * @dev Sets the values for {name} and {symbol}.
    *
-   * To select a different value for {decimals}, use {_setupDecimals}.
+   * The default value of {decimals} is 18. To select a different value for
+   * {decimals} you should overload it.
    *
-   * All three of these values are immutable: they can only be set once during
+   * All two of these values are immutable: they can only be set once during
    * construction.
    */
-  constructor(string memory name, string memory symbol) public {
-    _name = name;
-    _symbol = symbol;
-    _decimals = 18;
-  }
+  constructor() {}
 
   /**
    * @dev Returns the name of the token.
    */
-  function name() public view returns (string memory) {
+  function name() public view virtual override returns (string memory) {
     return _name;
   }
 
@@ -485,38 +192,44 @@ contract ERC20 is Context, IERC20 {
    * @dev Returns the symbol of the token, usually a shorter version of the
    * name.
    */
-  function symbol() public view returns (string memory) {
+  function symbol() public view virtual override returns (string memory) {
     return _symbol;
   }
 
   /**
    * @dev Returns the number of decimals used to get its user representation.
    * For example, if `decimals` equals `2`, a balance of `505` tokens should
-   * be displayed to a user as `5,05` (`505 / 10 ** 2`).
+   * be displayed to a user as `5.05` (`505 / 10 ** 2`).
    *
    * Tokens usually opt for a value of 18, imitating the relationship between
-   * Ether and Wei. This is the value {ERC20} uses, unless {_setupDecimals} is
-   * called.
+   * Ether and Wei. This is the value {ERC20} uses, unless this function is
+   * overridden;
    *
    * NOTE: This information is only used for _display_ purposes: it in
    * no way affects any of the arithmetic of the contract, including
    * {IERC20-balanceOf} and {IERC20-transfer}.
    */
-  function decimals() public view returns (uint8) {
-    return _decimals;
+  function decimals() public view virtual override returns (uint8) {
+    return 18;
   }
 
   /**
    * @dev See {IERC20-totalSupply}.
    */
-  function totalSupply() public view override returns (uint256) {
+  function totalSupply() public view virtual override returns (uint256) {
     return _totalSupply;
   }
 
   /**
    * @dev See {IERC20-balanceOf}.
    */
-  function balanceOf(address account) public view override returns (uint256) {
+  function balanceOf(address account)
+    public
+    view
+    virtual
+    override
+    returns (uint256)
+  {
     return _balances[account];
   }
 
@@ -525,16 +238,17 @@ contract ERC20 is Context, IERC20 {
    *
    * Requirements:
    *
-   * - `recipient` cannot be the zero address.
+   * - `to` cannot be the zero address.
    * - the caller must have a balance of at least `amount`.
    */
-  function transfer(address recipient, uint256 amount)
+  function transfer(address to, uint256 amount)
     public
     virtual
     override
     returns (bool)
   {
-    _transfer(_msgSender(), recipient, amount);
+    address owner = _msgSender();
+    _transfer(owner, to, amount);
     return true;
   }
 
@@ -554,6 +268,9 @@ contract ERC20 is Context, IERC20 {
   /**
    * @dev See {IERC20-approve}.
    *
+   * NOTE: If `amount` is the maximum `uint256`, the allowance is not updated on
+   * `transferFrom`. This is semantically equivalent to an infinite approval.
+   *
    * Requirements:
    *
    * - `spender` cannot be the zero address.
@@ -564,7 +281,8 @@ contract ERC20 is Context, IERC20 {
     override
     returns (bool)
   {
-    _approve(_msgSender(), spender, amount);
+    address owner = _msgSender();
+    _approve(owner, spender, amount);
     return true;
   }
 
@@ -572,28 +290,26 @@ contract ERC20 is Context, IERC20 {
    * @dev See {IERC20-transferFrom}.
    *
    * Emits an {Approval} event indicating the updated allowance. This is not
-   * required by the EIP. See the note at the beginning of {ERC20};
+   * required by the EIP. See the note at the beginning of {ERC20}.
+   *
+   * NOTE: Does not update the allowance if the current allowance
+   * is the maximum `uint256`.
    *
    * Requirements:
-   * - `sender` and `recipient` cannot be the zero address.
-   * - `sender` must have a balance of at least `amount`.
-   * - the caller must have allowance for ``sender``'s tokens of at least
+   *
+   * - `from` and `to` cannot be the zero address.
+   * - `from` must have a balance of at least `amount`.
+   * - the caller must have allowance for ``from``'s tokens of at least
    * `amount`.
    */
   function transferFrom(
-    address sender,
-    address recipient,
+    address from,
+    address to,
     uint256 amount
   ) public virtual override returns (bool) {
-    _transfer(sender, recipient, amount);
-    _approve(
-      sender,
-      _msgSender(),
-      _allowances[sender][_msgSender()].sub(
-        amount,
-        'ERC20: transfer amount exceeds allowance'
-      )
-    );
+    address spender = _msgSender();
+    _spendAllowance(from, spender, amount);
+    _transfer(from, to, amount);
     return true;
   }
 
@@ -614,11 +330,8 @@ contract ERC20 is Context, IERC20 {
     virtual
     returns (bool)
   {
-    _approve(
-      _msgSender(),
-      spender,
-      _allowances[_msgSender()][spender].add(addedValue)
-    );
+    address owner = _msgSender();
+    _approve(owner, spender, allowance(owner, spender) + addedValue);
     return true;
   }
 
@@ -641,47 +354,55 @@ contract ERC20 is Context, IERC20 {
     virtual
     returns (bool)
   {
-    _approve(
-      _msgSender(),
-      spender,
-      _allowances[_msgSender()][spender].sub(
-        subtractedValue,
-        'ERC20: decreased allowance below zero'
-      )
+    address owner = _msgSender();
+    uint256 currentAllowance = allowance(owner, spender);
+    require(
+      currentAllowance >= subtractedValue,
+      'ERC20: decreased allowance below zero'
     );
+    unchecked {
+      _approve(owner, spender, currentAllowance - subtractedValue);
+    }
+
     return true;
   }
 
   /**
-   * @dev Moves tokens `amount` from `sender` to `recipient`.
+   * @dev Moves `amount` of tokens from `from` to `to`.
    *
-   * This is internal function is equivalent to {transfer}, and can be used to
+   * This internal function is equivalent to {transfer}, and can be used to
    * e.g. implement automatic token fees, slashing mechanisms, etc.
    *
    * Emits a {Transfer} event.
    *
    * Requirements:
    *
-   * - `sender` cannot be the zero address.
-   * - `recipient` cannot be the zero address.
-   * - `sender` must have a balance of at least `amount`.
+   * - `from` cannot be the zero address.
+   * - `to` cannot be the zero address.
+   * - `from` must have a balance of at least `amount`.
    */
   function _transfer(
-    address sender,
-    address recipient,
+    address from,
+    address to,
     uint256 amount
   ) internal virtual {
-    require(sender != address(0), 'ERC20: transfer from the zero address');
-    require(recipient != address(0), 'ERC20: transfer to the zero address');
+    require(from != address(0), 'ERC20: transfer from the zero address');
+    require(to != address(0), 'ERC20: transfer to the zero address');
 
-    _beforeTokenTransfer(sender, recipient, amount);
+    _beforeTokenTransfer(from, to, amount);
 
-    _balances[sender] = _balances[sender].sub(
-      amount,
-      'ERC20: transfer amount exceeds balance'
-    );
-    _balances[recipient] = _balances[recipient].add(amount);
-    emit Transfer(sender, recipient, amount);
+    uint256 fromBalance = _balances[from];
+    require(fromBalance >= amount, 'ERC20: transfer amount exceeds balance');
+    unchecked {
+      _balances[from] = fromBalance - amount;
+      // Overflow not possible: the sum of all balances is capped by totalSupply, and the sum is preserved by
+      // decrementing then incrementing.
+      _balances[to] += amount;
+    }
+
+    emit Transfer(from, to, amount);
+
+    _afterTokenTransfer(from, to, amount);
   }
 
   /** @dev Creates `amount` tokens and assigns them to `account`, increasing
@@ -689,18 +410,23 @@ contract ERC20 is Context, IERC20 {
    *
    * Emits a {Transfer} event with `from` set to the zero address.
    *
-   * Requirements
+   * Requirements:
    *
-   * - `to` cannot be the zero address.
+   * - `account` cannot be the zero address.
    */
   function _mint(address account, uint256 amount) internal virtual {
     require(account != address(0), 'ERC20: mint to the zero address');
 
     _beforeTokenTransfer(address(0), account, amount);
 
-    _totalSupply = _totalSupply.add(amount);
-    _balances[account] = _balances[account].add(amount);
+    _totalSupply += amount;
+    unchecked {
+      // Overflow not possible: balance + amount is at most totalSupply + amount, which is checked above.
+      _balances[account] += amount;
+    }
     emit Transfer(address(0), account, amount);
+
+    _afterTokenTransfer(address(0), account, amount);
   }
 
   /**
@@ -709,7 +435,7 @@ contract ERC20 is Context, IERC20 {
    *
    * Emits a {Transfer} event with `to` set to the zero address.
    *
-   * Requirements
+   * Requirements:
    *
    * - `account` cannot be the zero address.
    * - `account` must have at least `amount` tokens.
@@ -719,18 +445,23 @@ contract ERC20 is Context, IERC20 {
 
     _beforeTokenTransfer(account, address(0), amount);
 
-    _balances[account] = _balances[account].sub(
-      amount,
-      'ERC20: burn amount exceeds balance'
-    );
-    _totalSupply = _totalSupply.sub(amount);
+    uint256 accountBalance = _balances[account];
+    require(accountBalance >= amount, 'ERC20: burn amount exceeds balance');
+    unchecked {
+      _balances[account] = accountBalance - amount;
+      // Overflow not possible: amount <= accountBalance <= totalSupply.
+      _totalSupply -= amount;
+    }
+
     emit Transfer(account, address(0), amount);
+
+    _afterTokenTransfer(account, address(0), amount);
   }
 
   /**
-   * @dev Sets `amount` as the allowance of `spender` over the `owner`s tokens.
+   * @dev Sets `amount` as the allowance of `spender` over the `owner` s tokens.
    *
-   * This is internal function is equivalent to `approve`, and can be used to
+   * This internal function is equivalent to `approve`, and can be used to
    * e.g. set automatic allowances for certain subsystems, etc.
    *
    * Emits an {Approval} event.
@@ -753,14 +484,25 @@ contract ERC20 is Context, IERC20 {
   }
 
   /**
-   * @dev Sets {decimals} to a value other than the default one of 18.
+   * @dev Updates `owner` s allowance for `spender` based on spent `amount`.
    *
-   * WARNING: This function should only be called from the constructor. Most
-   * applications that interact with token contracts will not expect
-   * {decimals} to ever change, and may work incorrectly if it does.
+   * Does not update the allowance amount in case of infinite allowance.
+   * Revert if not enough allowance is available.
+   *
+   * Might emit an {Approval} event.
    */
-  function _setupDecimals(uint8 decimals_) internal {
-    _decimals = decimals_;
+  function _spendAllowance(
+    address owner,
+    address spender,
+    uint256 amount
+  ) internal virtual {
+    uint256 currentAllowance = allowance(owner, spender);
+    if (currentAllowance != type(uint256).max) {
+      require(currentAllowance >= amount, 'ERC20: insufficient allowance');
+      unchecked {
+        _approve(owner, spender, currentAllowance - amount);
+      }
+    }
   }
 
   /**
@@ -770,7 +512,7 @@ contract ERC20 is Context, IERC20 {
    * Calling conditions:
    *
    * - when `from` and `to` are both non-zero, `amount` of ``from``'s tokens
-   * will be to transferred to `to`.
+   * will be transferred to `to`.
    * - when `from` is zero, `amount` tokens will be minted for `to`.
    * - when `to` is zero, `amount` of ``from``'s tokens will be burned.
    * - `from` and `to` are never both zero.
@@ -782,16 +524,26 @@ contract ERC20 is Context, IERC20 {
     address to,
     uint256 amount
   ) internal virtual {}
-}
 
-interface IStakedAave {
-  function stake(address to, uint256 amount) external;
-
-  function redeem(address to, uint256 amount) external;
-
-  function cooldown() external;
-
-  function claimRewards(address to, uint256 amount) external;
+  /**
+   * @dev Hook that is called after any transfer of tokens. This includes
+   * minting and burning.
+   *
+   * Calling conditions:
+   *
+   * - when `from` and `to` are both non-zero, `amount` of ``from``'s tokens
+   * has been transferred to `to`.
+   * - when `from` is zero, `amount` tokens have been minted for `to`.
+   * - when `to` is zero, `amount` of ``from``'s tokens have been burned.
+   * - `from` and `to` are never both zero.
+   *
+   * To learn more about hooks, head to xref:ROOT:extending-contracts.adoc#using-hooks[Using Hooks].
+   */
+  function _afterTokenTransfer(
+    address from,
+    address to,
+    uint256 amount
+  ) internal virtual {}
 }
 
 interface ITransferHook {
@@ -816,10 +568,288 @@ library DistributionTypes {
   }
 }
 
+// OpenZeppelin Contracts (last updated v4.8.0) (utils/Address.sol)
+
+/**
+ * @dev Collection of functions related to the address type
+ */
+library Address {
+  /**
+   * @dev Returns true if `account` is a contract.
+   *
+   * [IMPORTANT]
+   * ====
+   * It is unsafe to assume that an address for which this function returns
+   * false is an externally-owned account (EOA) and not a contract.
+   *
+   * Among others, `isContract` will return false for the following
+   * types of addresses:
+   *
+   *  - an externally-owned account
+   *  - a contract in construction
+   *  - an address where a contract will be created
+   *  - an address where a contract lived, but was destroyed
+   * ====
+   *
+   * [IMPORTANT]
+   * ====
+   * You shouldn't rely on `isContract` to protect against flash loan attacks!
+   *
+   * Preventing calls from contracts is highly discouraged. It breaks composability, breaks support for smart wallets
+   * like Gnosis Safe, and does not provide security since it can be circumvented by calling from a contract
+   * constructor.
+   * ====
+   */
+  function isContract(address account) internal view returns (bool) {
+    // This method relies on extcodesize/address.code.length, which returns 0
+    // for contracts in construction, since the code is only stored at the end
+    // of the constructor execution.
+
+    return account.code.length > 0;
+  }
+
+  /**
+   * @dev Replacement for Solidity's `transfer`: sends `amount` wei to
+   * `recipient`, forwarding all available gas and reverting on errors.
+   *
+   * https://eips.ethereum.org/EIPS/eip-1884[EIP1884] increases the gas cost
+   * of certain opcodes, possibly making contracts go over the 2300 gas limit
+   * imposed by `transfer`, making them unable to receive funds via
+   * `transfer`. {sendValue} removes this limitation.
+   *
+   * https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/[Learn more].
+   *
+   * IMPORTANT: because control is transferred to `recipient`, care must be
+   * taken to not create reentrancy vulnerabilities. Consider using
+   * {ReentrancyGuard} or the
+   * https://solidity.readthedocs.io/en/v0.5.11/security-considerations.html#use-the-checks-effects-interactions-pattern[checks-effects-interactions pattern].
+   */
+  function sendValue(address payable recipient, uint256 amount) internal {
+    require(address(this).balance >= amount, 'Address: insufficient balance');
+
+    (bool success, ) = recipient.call{value: amount}('');
+    require(
+      success,
+      'Address: unable to send value, recipient may have reverted'
+    );
+  }
+
+  /**
+   * @dev Performs a Solidity function call using a low level `call`. A
+   * plain `call` is an unsafe replacement for a function call: use this
+   * function instead.
+   *
+   * If `target` reverts with a revert reason, it is bubbled up by this
+   * function (like regular Solidity function calls).
+   *
+   * Returns the raw returned data. To convert to the expected return value,
+   * use https://solidity.readthedocs.io/en/latest/units-and-global-variables.html?highlight=abi.decode#abi-encoding-and-decoding-functions[`abi.decode`].
+   *
+   * Requirements:
+   *
+   * - `target` must be a contract.
+   * - calling `target` with `data` must not revert.
+   *
+   * _Available since v3.1._
+   */
+  function functionCall(address target, bytes memory data)
+    internal
+    returns (bytes memory)
+  {
+    return
+      functionCallWithValue(target, data, 0, 'Address: low-level call failed');
+  }
+
+  /**
+   * @dev Same as {xref-Address-functionCall-address-bytes-}[`functionCall`], but with
+   * `errorMessage` as a fallback revert reason when `target` reverts.
+   *
+   * _Available since v3.1._
+   */
+  function functionCall(
+    address target,
+    bytes memory data,
+    string memory errorMessage
+  ) internal returns (bytes memory) {
+    return functionCallWithValue(target, data, 0, errorMessage);
+  }
+
+  /**
+   * @dev Same as {xref-Address-functionCall-address-bytes-}[`functionCall`],
+   * but also transferring `value` wei to `target`.
+   *
+   * Requirements:
+   *
+   * - the calling contract must have an ETH balance of at least `value`.
+   * - the called Solidity function must be `payable`.
+   *
+   * _Available since v3.1._
+   */
+  function functionCallWithValue(
+    address target,
+    bytes memory data,
+    uint256 value
+  ) internal returns (bytes memory) {
+    return
+      functionCallWithValue(
+        target,
+        data,
+        value,
+        'Address: low-level call with value failed'
+      );
+  }
+
+  /**
+   * @dev Same as {xref-Address-functionCallWithValue-address-bytes-uint256-}[`functionCallWithValue`], but
+   * with `errorMessage` as a fallback revert reason when `target` reverts.
+   *
+   * _Available since v3.1._
+   */
+  function functionCallWithValue(
+    address target,
+    bytes memory data,
+    uint256 value,
+    string memory errorMessage
+  ) internal returns (bytes memory) {
+    require(
+      address(this).balance >= value,
+      'Address: insufficient balance for call'
+    );
+    (bool success, bytes memory returndata) = target.call{value: value}(data);
+    return
+      verifyCallResultFromTarget(target, success, returndata, errorMessage);
+  }
+
+  /**
+   * @dev Same as {xref-Address-functionCall-address-bytes-}[`functionCall`],
+   * but performing a static call.
+   *
+   * _Available since v3.3._
+   */
+  function functionStaticCall(address target, bytes memory data)
+    internal
+    view
+    returns (bytes memory)
+  {
+    return
+      functionStaticCall(target, data, 'Address: low-level static call failed');
+  }
+
+  /**
+   * @dev Same as {xref-Address-functionCall-address-bytes-string-}[`functionCall`],
+   * but performing a static call.
+   *
+   * _Available since v3.3._
+   */
+  function functionStaticCall(
+    address target,
+    bytes memory data,
+    string memory errorMessage
+  ) internal view returns (bytes memory) {
+    (bool success, bytes memory returndata) = target.staticcall(data);
+    return
+      verifyCallResultFromTarget(target, success, returndata, errorMessage);
+  }
+
+  /**
+   * @dev Same as {xref-Address-functionCall-address-bytes-}[`functionCall`],
+   * but performing a delegate call.
+   *
+   * _Available since v3.4._
+   */
+  function functionDelegateCall(address target, bytes memory data)
+    internal
+    returns (bytes memory)
+  {
+    return
+      functionDelegateCall(
+        target,
+        data,
+        'Address: low-level delegate call failed'
+      );
+  }
+
+  /**
+   * @dev Same as {xref-Address-functionCall-address-bytes-string-}[`functionCall`],
+   * but performing a delegate call.
+   *
+   * _Available since v3.4._
+   */
+  function functionDelegateCall(
+    address target,
+    bytes memory data,
+    string memory errorMessage
+  ) internal returns (bytes memory) {
+    (bool success, bytes memory returndata) = target.delegatecall(data);
+    return
+      verifyCallResultFromTarget(target, success, returndata, errorMessage);
+  }
+
+  /**
+   * @dev Tool to verify that a low level call to smart-contract was successful, and revert (either by bubbling
+   * the revert reason or using the provided one) in case of unsuccessful call or if target was not a contract.
+   *
+   * _Available since v4.8._
+   */
+  function verifyCallResultFromTarget(
+    address target,
+    bool success,
+    bytes memory returndata,
+    string memory errorMessage
+  ) internal view returns (bytes memory) {
+    if (success) {
+      if (returndata.length == 0) {
+        // only check isContract if the call was successful and the return data is empty
+        // otherwise we already know that it was a contract
+        require(isContract(target), 'Address: call to non-contract');
+      }
+      return returndata;
+    } else {
+      _revert(returndata, errorMessage);
+    }
+  }
+
+  /**
+   * @dev Tool to verify that a low level call was successful, and revert if it wasn't, either by bubbling the
+   * revert reason or using the provided one.
+   *
+   * _Available since v4.3._
+   */
+  function verifyCallResult(
+    bool success,
+    bytes memory returndata,
+    string memory errorMessage
+  ) internal pure returns (bytes memory) {
+    if (success) {
+      return returndata;
+    } else {
+      _revert(returndata, errorMessage);
+    }
+  }
+
+  function _revert(bytes memory returndata, string memory errorMessage)
+    private
+    pure
+  {
+    // Look for revert reason and bubble it up if present
+    if (returndata.length > 0) {
+      // The easiest way to bubble the revert reason is using memory via assembly
+      /// @solidity memory-safe-assembly
+      assembly {
+        let returndata_size := mload(returndata)
+        revert(add(32, returndata), returndata_size)
+      }
+    } else {
+      revert(errorMessage);
+    }
+  }
+}
+
+// OpenZeppelin Contracts v4.4.1 (token/ERC20/utils/SafeERC20.sol)
+
 /**
  * @title SafeERC20
- * @dev From https://github.com/OpenZeppelin/openzeppelin-contracts
- * Wrappers around ERC20 operations that throw on failure (when the token
+ * @dev Wrappers around ERC20 operations that throw on failure (when the token
  * contract returns false). Tokens that return no value (and instead revert or
  * throw on failure) are also supported, non-reverting calls are assumed to be
  * successful.
@@ -827,7 +857,6 @@ library DistributionTypes {
  * which allows you to call the safe operations as `token.safeTransfer(...)`, etc.
  */
 library SafeERC20 {
-  using SafeMath for uint256;
   using Address for address;
 
   function safeTransfer(
@@ -835,7 +864,7 @@ library SafeERC20 {
     address to,
     uint256 value
   ) internal {
-    callOptionalReturn(
+    _callOptionalReturn(
       token,
       abi.encodeWithSelector(token.transfer.selector, to, value)
     );
@@ -847,37 +876,85 @@ library SafeERC20 {
     address to,
     uint256 value
   ) internal {
-    callOptionalReturn(
+    _callOptionalReturn(
       token,
       abi.encodeWithSelector(token.transferFrom.selector, from, to, value)
     );
   }
 
+  /**
+   * @dev Deprecated. This function has issues similar to the ones found in
+   * {IERC20-approve}, and its usage is discouraged.
+   *
+   * Whenever possible, use {safeIncreaseAllowance} and
+   * {safeDecreaseAllowance} instead.
+   */
   function safeApprove(
     IERC20 token,
     address spender,
     uint256 value
   ) internal {
+    // safeApprove should only be called when setting an initial allowance,
+    // or when resetting it to zero. To increase and decrease it, use
+    // 'safeIncreaseAllowance' and 'safeDecreaseAllowance'
     require(
       (value == 0) || (token.allowance(address(this), spender) == 0),
       'SafeERC20: approve from non-zero to non-zero allowance'
     );
-    callOptionalReturn(
+    _callOptionalReturn(
       token,
       abi.encodeWithSelector(token.approve.selector, spender, value)
     );
   }
 
-  function callOptionalReturn(IERC20 token, bytes memory data) private {
-    require(address(token).isContract(), 'SafeERC20: call to non-contract');
+  function safeIncreaseAllowance(
+    IERC20 token,
+    address spender,
+    uint256 value
+  ) internal {
+    uint256 newAllowance = token.allowance(address(this), spender) + value;
+    _callOptionalReturn(
+      token,
+      abi.encodeWithSelector(token.approve.selector, spender, newAllowance)
+    );
+  }
 
-    // solhint-disable-next-line avoid-low-level-calls
-    (bool success, bytes memory returndata) = address(token).call(data);
-    require(success, 'SafeERC20: low-level call failed');
+  function safeDecreaseAllowance(
+    IERC20 token,
+    address spender,
+    uint256 value
+  ) internal {
+    unchecked {
+      uint256 oldAllowance = token.allowance(address(this), spender);
+      require(
+        oldAllowance >= value,
+        'SafeERC20: decreased allowance below zero'
+      );
+      uint256 newAllowance = oldAllowance - value;
+      _callOptionalReturn(
+        token,
+        abi.encodeWithSelector(token.approve.selector, spender, newAllowance)
+      );
+    }
+  }
 
+  /**
+   * @dev Imitates a Solidity high-level call (i.e. a regular function call to a contract), relaxing the requirement
+   * on the return value: the return value is optional (but if data is returned, it must not be false).
+   * @param token The token targeted by the call.
+   * @param data The call data (encoded using abi.encode or one of its variants).
+   */
+  function _callOptionalReturn(IERC20 token, bytes memory data) private {
+    // We need to perform a low level call here, to bypass Solidity's return data size checking mechanism, since
+    // we're implementing it ourselves. We use {Address.functionCall} to perform this call, which verifies that
+    // the target address contains contract code and also asserts for success in the low-level call.
+
+    bytes memory returndata = address(token).functionCall(
+      data,
+      'SafeERC20: low-level call failed'
+    );
     if (returndata.length > 0) {
       // Return data is optional
-      // solhint-disable-next-line max-line-length
       require(
         abi.decode(returndata, (bool)),
         'SafeERC20: ERC20 operation did not succeed'
@@ -941,8 +1018,6 @@ interface IAaveDistributionManager {
  * @author Aave
  **/
 contract AaveDistributionManager is IAaveDistributionManager {
-  using SafeMath for uint256;
-
   struct AssetData {
     uint128 emissionPerSecond;
     uint128 lastUpdateTimestamp;
@@ -966,8 +1041,8 @@ contract AaveDistributionManager is IAaveDistributionManager {
     uint256 index
   );
 
-  constructor(address emissionManager, uint256 distributionDuration) public {
-    DISTRIBUTION_END = block.timestamp.add(distributionDuration);
+  constructor(address emissionManager, uint256 distributionDuration) {
+    DISTRIBUTION_END = block.timestamp + distributionDuration;
     EMISSION_MANAGER = emissionManager;
   }
 
@@ -1081,14 +1156,14 @@ contract AaveDistributionManager is IAaveDistributionManager {
     uint256 accruedRewards = 0;
 
     for (uint256 i = 0; i < stakes.length; i++) {
-      accruedRewards = accruedRewards.add(
+      accruedRewards =
+        accruedRewards +
         _updateUserAssetInternal(
           user,
           stakes[i].underlyingAsset,
           stakes[i].stakedByUser,
           stakes[i].totalStaked
-        )
-      );
+        );
     }
 
     return accruedRewards;
@@ -1115,9 +1190,13 @@ contract AaveDistributionManager is IAaveDistributionManager {
         stakes[i].totalStaked
       );
 
-      accruedRewards = accruedRewards.add(
-        _getRewards(stakes[i].stakedByUser, assetIndex, assetConfig.users[user])
-      );
+      accruedRewards =
+        accruedRewards +
+        _getRewards(
+          stakes[i].stakedByUser,
+          assetIndex,
+          assetConfig.users[user]
+        );
     }
     return accruedRewards;
   }
@@ -1135,9 +1214,8 @@ contract AaveDistributionManager is IAaveDistributionManager {
     uint256 userIndex
   ) internal pure returns (uint256) {
     return
-      principalUserBalance.mul(reserveIndex.sub(userIndex)).div(
-        10**uint256(PRECISION)
-      );
+      (principalUserBalance * (reserveIndex - userIndex)) /
+      (10**uint256(PRECISION));
   }
 
   /**
@@ -1166,13 +1244,10 @@ contract AaveDistributionManager is IAaveDistributionManager {
     uint256 currentTimestamp = block.timestamp > DISTRIBUTION_END
       ? DISTRIBUTION_END
       : block.timestamp;
-    uint256 timeDelta = currentTimestamp.sub(lastUpdateTimestamp);
+    uint256 timeDelta = currentTimestamp - lastUpdateTimestamp;
     return
-      emissionPerSecond
-        .mul(timeDelta)
-        .mul(10**uint256(PRECISION))
-        .div(totalBalance)
-        .add(currentIndex);
+      ((emissionPerSecond * timeDelta * (10**uint256(PRECISION))) /
+        totalBalance) + currentIndex;
   }
 
   /**
@@ -1190,6 +1265,85 @@ contract AaveDistributionManager is IAaveDistributionManager {
   }
 }
 
+interface IGovernancePowerDelegationToken {
+  enum DelegationType {
+    VOTING_POWER,
+    PROPOSITION_POWER
+  }
+
+  /**
+   * @dev emitted when a user delegates to another
+   * @param delegator the delegator
+   * @param delegatee the delegatee
+   * @param delegationType the type of delegation (VOTING_POWER, PROPOSITION_POWER)
+   **/
+  event DelegateChanged(
+    address indexed delegator,
+    address indexed delegatee,
+    DelegationType delegationType
+  );
+
+  /**
+   * @dev emitted when an action changes the delegated power of a user
+   * @param user the user which delegated power has changed
+   * @param amount the amount of delegated power for the user
+   * @param delegationType the type of delegation (VOTING_POWER, PROPOSITION_POWER)
+   **/
+  event DelegatedPowerChanged(
+    address indexed user,
+    uint256 amount,
+    DelegationType delegationType
+  );
+
+  /**
+   * @dev delegates the specific power to a delegatee
+   * @param delegatee the user which delegated power has changed
+   * @param delegationType the type of delegation (VOTING_POWER, PROPOSITION_POWER)
+   **/
+  function delegateByType(address delegatee, DelegationType delegationType)
+    external;
+
+  /**
+   * @dev delegates all the powers to a specific user
+   * @param delegatee the user to which the power will be delegated
+   **/
+  function delegate(address delegatee) external;
+
+  /**
+   * @dev returns the delegatee of an user
+   * @param delegator the address of the delegator
+   **/
+  function getDelegateeByType(address delegator, DelegationType delegationType)
+    external
+    view
+    returns (address);
+
+  /**
+   * @dev returns the current delegated power of a user. The current power is the
+   * power delegated at the time of the last snapshot
+   * @param user the user
+   **/
+  function getPowerCurrent(address user, DelegationType delegationType)
+    external
+    view
+    returns (uint256);
+
+  /**
+   * @dev returns the delegated power of a user at a certain block
+   * @param user the user
+   **/
+  function getPowerAtBlock(
+    address user,
+    uint256 blockNumber,
+    DelegationType delegationType
+  ) external view returns (uint256);
+
+  /**
+   * @dev returns the total supply at a certain block number
+   **/
+  function totalSupplyAt(uint256 blockNumber) external view returns (uint256);
+}
+
 /**
  * @notice implementation of the AAVE token contract
  * @author Aave
@@ -1198,7 +1352,6 @@ abstract contract GovernancePowerDelegationERC20 is
   ERC20,
   IGovernancePowerDelegationToken
 {
-  using SafeMath for uint256;
   /// @notice The EIP-712 typehash for the delegation struct used by the contract
   bytes32 public constant DELEGATE_BY_TYPE_TYPEHASH =
     keccak256(
@@ -1298,12 +1451,7 @@ abstract contract GovernancePowerDelegationERC20 is
    * In this initial implementation with no AAVE minting, simply returns the current supply
    * A snapshots mapping will need to be added in case a mint function is added to the AAVE token in the future
    **/
-  function totalSupplyAt(uint256 blockNumber)
-    external
-    view
-    override
-    returns (uint256)
-  {
+  function totalSupplyAt(uint256) external view override returns (uint256) {
     return super.totalSupply();
   }
 
@@ -1378,10 +1526,10 @@ abstract contract GovernancePowerDelegationERC20 is
         snapshotsCounts,
         from,
         uint128(previous),
-        uint128(previous.sub(amount))
+        uint128(previous - amount)
       );
 
-      emit DelegatedPowerChanged(from, previous.sub(amount), delegationType);
+      emit DelegatedPowerChanged(from, previous - amount, delegationType);
     }
     if (to != address(0)) {
       uint256 previous = 0;
@@ -1397,10 +1545,10 @@ abstract contract GovernancePowerDelegationERC20 is
         snapshotsCounts,
         to,
         uint128(previous),
-        uint128(previous.add(amount))
+        uint128(previous + amount)
       );
 
-      emit DelegatedPowerChanged(to, previous.add(amount), delegationType);
+      emit DelegatedPowerChanged(to, previous + amount, delegationType);
     }
   }
 
@@ -1416,7 +1564,7 @@ abstract contract GovernancePowerDelegationERC20 is
     mapping(address => uint256) storage snapshotsCounts,
     address user,
     uint256 blockNumber
-  ) internal view returns (uint256) {
+  ) internal view virtual returns (uint256) {
     require(blockNumber <= block.number, 'INVALID_BLOCK_NUMBER');
 
     uint256 snapshotsCount = snapshotsCounts[user];
@@ -1425,21 +1573,29 @@ abstract contract GovernancePowerDelegationERC20 is
       return balanceOf(user);
     }
 
-    // First check most recent balance
-    if (snapshots[user][snapshotsCount - 1].blockNumber <= blockNumber) {
-      return snapshots[user][snapshotsCount - 1].value;
-    }
-
-    // Next check implicit zero balance
+    // Check implicit zero balance
     if (snapshots[user][0].blockNumber > blockNumber) {
       return 0;
     }
 
+    return _binarySearch(snapshots[user], snapshotsCount, blockNumber);
+  }
+
+  function _binarySearch(
+    mapping(uint256 => Snapshot) storage snapshots,
+    uint256 snapshotsCount,
+    uint256 blockNumber
+  ) internal view returns (uint256) {
+    // First check most recent balance
+    if (snapshots[snapshotsCount - 1].blockNumber <= blockNumber) {
+      return snapshots[snapshotsCount - 1].value;
+    }
+
     uint256 lower = 0;
     uint256 upper = snapshotsCount - 1;
     while (upper > lower) {
       uint256 center = upper - (upper - lower) / 2; // ceil, avoiding overflow
-      Snapshot memory snapshot = snapshots[user][center];
+      Snapshot memory snapshot = snapshots[center];
       if (snapshot.blockNumber == blockNumber) {
         return snapshot.value;
       } else if (snapshot.blockNumber < blockNumber) {
@@ -1448,7 +1604,7 @@ abstract contract GovernancePowerDelegationERC20 is
         upper = center - 1;
       }
     }
-    return snapshots[user][lower].value;
+    return snapshots[lower].value;
   }
 
   /**
@@ -1526,8 +1682,6 @@ abstract contract GovernancePowerDelegationERC20 is
 abstract contract GovernancePowerWithSnapshot is
   GovernancePowerDelegationERC20
 {
-  using SafeMath for uint256;
-
   /**
    * @dev The following storage layout points to the prior StakedToken.sol implementation:
    * _snapshots => _votingSnapshots
@@ -1540,11 +1694,68 @@ abstract contract GovernancePowerWithSnapshot is
   /// @dev reference to the Aave governance contract to call (if initialized) on _beforeTokenTransfer
   /// !!! IMPORTANT The Aave governance is considered a trustable contract, being its responsibility
   /// to control all potential reentrancies by calling back the this contract
+  /// @dev DEPRECATED
   ITransferHook public _aaveGovernance;
+}
 
-  function _setAaveGovernance(ITransferHook aaveGovernance) internal virtual {
-    _aaveGovernance = aaveGovernance;
-  }
+// most imports are only here to force import order for better (i.e smaller) diff on flattening
+
+interface IERC20WithPermit is IERC20 {
+  function permit(
+    address owner,
+    address spender,
+    uint256 value,
+    uint256 deadline,
+    uint8 v,
+    bytes32 r,
+    bytes32 s
+  ) external;
+}
+
+interface IStakedTokenV2 {
+  /**
+   * @dev Allows staking a specified amount of STAKED_TOKEN
+   * @param to The address to receiving the shares
+   * @param amount The amount of assets to be staked
+   **/
+  function stake(address to, uint256 amount) external;
+
+  /**
+   * @dev Redeems shares, and stop earning rewards
+   * @param to Address to redeem to
+   * @param amount Amount of shares to redeem
+   **/
+  function redeem(address to, uint256 amount) external;
+
+  function cooldown() external;
+
+  /**
+   * @dev Claims an `amount` of `REWARD_TOKEN` to the address `to`
+   * @param to Address to send the claimed rewards
+   * @param amount Amount to stake
+   **/
+  function claimRewards(address to, uint256 amount) external;
+
+  /**
+   * @dev Calculates the how is gonna be a new cooldown timestamp depending on the sender/receiver situation
+   *  - If the timestamp of the sender is "better" or the timestamp of the recipient is 0, we take the one of the recipient
+   *  - Weighted average of from/to cooldown timestamps if:
+   *    # The sender doesn't have the cooldown activated (timestamp 0).
+   *    # The sender timestamp is expired
+   *    # The sender has a "worse" timestamp
+   *  - If the receiver's cooldown timestamp expired (too old), the next is 0
+   * @param fromCooldownTimestamp Cooldown timestamp of the sender
+   * @param amountToReceive Amount
+   * @param toAddress Address of the recipient
+   * @param toBalance Current balance of the receiver
+   * @return The new cooldown timestamp
+   **/
+  function getNextCooldownTimestamp(
+    uint256 fromCooldownTimestamp,
+    uint256 amountToReceive,
+    address toAddress,
+    uint256 toBalance
+  ) external view returns (uint256);
 }
 
 /**
@@ -1552,21 +1763,20 @@ abstract contract GovernancePowerWithSnapshot is
  * @notice Contract to stake Aave token, tokenize the position and get rewards, inheriting from a distribution manager contract
  * @author Aave
  **/
-contract StakedTokenV2Rev3 is
-  IStakedAave,
+abstract contract StakedTokenV2 is
+  IStakedTokenV2,
   GovernancePowerWithSnapshot,
   VersionedInitializable,
   AaveDistributionManager
 {
-  using SafeMath for uint256;
   using SafeERC20 for IERC20;
 
-  /// @dev Start of Storage layout from StakedToken v1
-  uint256 public constant REVISION = 3;
+  function REVISION() public pure virtual returns (uint256) {
+    return 2;
+  }
 
   IERC20 public immutable STAKED_TOKEN;
   IERC20 public immutable REWARD_TOKEN;
-  uint256 public immutable COOLDOWN_SECONDS;
 
   /// @notice Seconds available to redeem once the cooldown period is fullfilled
   uint256 public immutable UNSTAKE_WINDOW;
@@ -1620,121 +1830,22 @@ contract StakedTokenV2Rev3 is
   constructor(
     IERC20 stakedToken,
     IERC20 rewardToken,
-    uint256 cooldownSeconds,
     uint256 unstakeWindow,
     address rewardsVault,
     address emissionManager,
-    uint128 distributionDuration,
-    string memory name,
-    string memory symbol,
-    uint8 decimals,
-    address governance
-  )
-    public
-    ERC20(name, symbol)
-    AaveDistributionManager(emissionManager, distributionDuration)
-  {
+    uint128 distributionDuration
+  ) ERC20() AaveDistributionManager(emissionManager, distributionDuration) {
     STAKED_TOKEN = stakedToken;
     REWARD_TOKEN = rewardToken;
-    COOLDOWN_SECONDS = cooldownSeconds;
     UNSTAKE_WINDOW = unstakeWindow;
     REWARDS_VAULT = rewardsVault;
-    _aaveGovernance = ITransferHook(governance);
-    ERC20._setupDecimals(decimals);
   }
 
-  /**
-   * @dev Called by the proxy contract
-   **/
-  function initialize() external initializer {
-    uint256 chainId;
+  /// @inheritdoc IStakedTokenV2
+  function stake(address onBehalfOf, uint256 amount) external virtual override;
 
-    //solium-disable-next-line
-    assembly {
-      chainId := chainid()
-    }
-
-    DOMAIN_SEPARATOR = keccak256(
-      abi.encode(
-        EIP712_DOMAIN,
-        keccak256(bytes(name())),
-        keccak256(EIP712_REVISION),
-        chainId,
-        address(this)
-      )
-    );
-
-    // Update lastUpdateTimestamp of stkAave to reward users since the end of the prior staking period
-    AssetData storage assetData = assets[address(this)];
-    assetData.lastUpdateTimestamp = 1620594720;
-  }
-
-  function stake(address onBehalfOf, uint256 amount) external override {
-    require(amount != 0, 'INVALID_ZERO_AMOUNT');
-    uint256 balanceOfUser = balanceOf(onBehalfOf);
-
-    uint256 accruedRewards = _updateUserAssetInternal(
-      onBehalfOf,
-      address(this),
-      balanceOfUser,
-      totalSupply()
-    );
-    if (accruedRewards != 0) {
-      emit RewardsAccrued(onBehalfOf, accruedRewards);
-      stakerRewardsToClaim[onBehalfOf] = stakerRewardsToClaim[onBehalfOf].add(
-        accruedRewards
-      );
-    }
-
-    stakersCooldowns[onBehalfOf] = getNextCooldownTimestamp(
-      0,
-      amount,
-      onBehalfOf,
-      balanceOfUser
-    );
-
-    _mint(onBehalfOf, amount);
-    IERC20(STAKED_TOKEN).safeTransferFrom(msg.sender, address(this), amount);
-
-    emit Staked(msg.sender, onBehalfOf, amount);
-  }
-
-  /**
-   * @dev Redeems staked tokens, and stop earning rewards
-   * @param to Address to redeem to
-   * @param amount Amount to redeem
-   **/
-  function redeem(address to, uint256 amount) external override {
-    require(amount != 0, 'INVALID_ZERO_AMOUNT');
-    //solium-disable-next-line
-    uint256 cooldownStartTimestamp = stakersCooldowns[msg.sender];
-    require(
-      block.timestamp > cooldownStartTimestamp.add(COOLDOWN_SECONDS),
-      'INSUFFICIENT_COOLDOWN'
-    );
-    require(
-      block.timestamp.sub(cooldownStartTimestamp.add(COOLDOWN_SECONDS)) <=
-        UNSTAKE_WINDOW,
-      'UNSTAKE_WINDOW_FINISHED'
-    );
-    uint256 balanceOfMessageSender = balanceOf(msg.sender);
-
-    uint256 amountToRedeem = (amount > balanceOfMessageSender)
-      ? balanceOfMessageSender
-      : amount;
-
-    _updateCurrentUnclaimedRewards(msg.sender, balanceOfMessageSender, true);
-
-    _burn(msg.sender, amountToRedeem);
-
-    if (balanceOfMessageSender.sub(amountToRedeem) == 0) {
-      stakersCooldowns[msg.sender] = 0;
-    }
-
-    IERC20(STAKED_TOKEN).safeTransfer(to, amountToRedeem);
-
-    emit Redeem(msg.sender, to, amountToRedeem);
-  }
+  /// @inheritdoc IStakedTokenV2
+  function redeem(address to, uint256 amount) external virtual override;
 
   /**
    * @dev Activates the cooldown period to unstake
@@ -1748,30 +1859,8 @@ contract StakedTokenV2Rev3 is
     emit Cooldown(msg.sender);
   }
 
-  /**
-   * @dev Claims an `amount` of `REWARD_TOKEN` to the address `to`
-   * @param to Address to stake for
-   * @param amount Amount to stake
-   **/
-  function claimRewards(address to, uint256 amount) external override {
-    uint256 newTotalRewards = _updateCurrentUnclaimedRewards(
-      msg.sender,
-      balanceOf(msg.sender),
-      false
-    );
-    uint256 amountToClaim = (amount == type(uint256).max)
-      ? newTotalRewards
-      : amount;
-
-    stakerRewardsToClaim[msg.sender] = newTotalRewards.sub(
-      amountToClaim,
-      'INVALID_AMOUNT'
-    );
-
-    REWARD_TOKEN.safeTransferFrom(REWARDS_VAULT, to, amountToClaim);
-
-    emit RewardsClaimed(msg.sender, to, amountToClaim);
-  }
+  /// @inheritdoc IStakedTokenV2
+  function claimRewards(address to, uint256 amount) external virtual override;
 
   /**
    * @dev Internal ERC20 _transfer of the tokenized staked tokens
@@ -1827,7 +1916,7 @@ contract StakedTokenV2Rev3 is
       userBalance,
       totalSupply()
     );
-    uint256 unclaimedRewards = stakerRewardsToClaim[user].add(accruedRewards);
+    uint256 unclaimedRewards = stakerRewardsToClaim[user] + accruedRewards;
 
     if (accruedRewards != 0) {
       if (updateStorage) {
@@ -1839,56 +1928,13 @@ contract StakedTokenV2Rev3 is
     return unclaimedRewards;
   }
 
-  /**
-   * @dev Calculates the how is gonna be a new cooldown timestamp depending on the sender/receiver situation
-   *  - If the timestamp of the sender is "better" or the timestamp of the recipient is 0, we take the one of the recipient
-   *  - Weighted average of from/to cooldown timestamps if:
-   *    # The sender doesn't have the cooldown activated (timestamp 0).
-   *    # The sender timestamp is expired
-   *    # The sender has a "worse" timestamp
-   *  - If the receiver's cooldown timestamp expired (too old), the next is 0
-   * @param fromCooldownTimestamp Cooldown timestamp of the sender
-   * @param amountToReceive Amount
-   * @param toAddress Address of the recipient
-   * @param toBalance Current balance of the receiver
-   * @return The new cooldown timestamp
-   **/
+  /// @inheritdoc IStakedTokenV2
   function getNextCooldownTimestamp(
     uint256 fromCooldownTimestamp,
     uint256 amountToReceive,
     address toAddress,
     uint256 toBalance
-  ) public view returns (uint256) {
-    uint256 toCooldownTimestamp = stakersCooldowns[toAddress];
-    if (toCooldownTimestamp == 0) {
-      return 0;
-    }
-
-    uint256 minimalValidCooldownTimestamp = block
-      .timestamp
-      .sub(COOLDOWN_SECONDS)
-      .sub(UNSTAKE_WINDOW);
-
-    if (minimalValidCooldownTimestamp > toCooldownTimestamp) {
-      toCooldownTimestamp = 0;
-    } else {
-      uint256 fromCooldownTimestamp = (minimalValidCooldownTimestamp >
-        fromCooldownTimestamp)
-        ? block.timestamp
-        : fromCooldownTimestamp;
-
-      if (fromCooldownTimestamp < toCooldownTimestamp) {
-        return toCooldownTimestamp;
-      } else {
-        toCooldownTimestamp = (
-          amountToReceive.mul(fromCooldownTimestamp).add(
-            toBalance.mul(toCooldownTimestamp)
-          )
-        ).div(amountToReceive.add(toBalance));
-      }
-    }
-    return toCooldownTimestamp;
-  }
+  ) public view virtual returns (uint256);
 
   /**
    * @dev Return the total rewards pending to claim by an staker
@@ -1908,17 +1954,16 @@ contract StakedTokenV2Rev3 is
       totalStaked: totalSupply()
     });
     return
-      stakerRewardsToClaim[staker].add(
-        _getUnclaimedRewards(staker, userStakeInputs)
-      );
+      stakerRewardsToClaim[staker] +
+      _getUnclaimedRewards(staker, userStakeInputs);
   }
 
   /**
    * @dev returns the revision of the implementation contract
    * @return The revision
    */
-  function getRevision() internal pure override returns (uint256) {
-    return REVISION;
+  function getRevision() internal pure virtual override returns (uint256) {
+    return REVISION();
   }
 
   /**
@@ -1963,7 +2008,7 @@ contract StakedTokenV2Rev3 is
     );
 
     require(owner == ecrecover(digest, v, r, s), 'INVALID_SIGNATURE');
-    _nonces[owner] = currentValidNonce.add(1);
+    _nonces[owner] = currentValidNonce + 1;
     _approve(owner, spender, value);
   }
 
@@ -1980,7 +2025,7 @@ contract StakedTokenV2Rev3 is
     address from,
     address to,
     uint256 amount
-  ) internal override {
+  ) internal virtual override {
     address votingFromDelegatee = _votingDelegates[from];
     address votingToDelegatee = _votingDelegates[to];
 
@@ -2014,12 +2059,6 @@ contract StakedTokenV2Rev3 is
       amount,
       DelegationType.PROPOSITION_POWER
     );
-
-    // caching the aave governance address to avoid multiple state loads
-    ITransferHook aaveGovernance = _aaveGovernance;
-    if (aaveGovernance != ITransferHook(0)) {
-      aaveGovernance.onTransfer(from, to, amount);
-    }
   }
 
   function _getDelegationDataByType(DelegationType delegationType)
@@ -2112,3 +2151,932 @@ contract StakedTokenV2Rev3 is
     _delegateByType(signatory, delegatee, DelegationType.PROPOSITION_POWER);
   }
 }
+
+interface IStakedTokenV3 is IStakedTokenV2 {
+  event Staked(
+    address indexed from,
+    address indexed to,
+    uint256 assets,
+    uint256 shares
+  );
+  event Redeem(
+    address indexed from,
+    address indexed to,
+    uint256 assets,
+    uint256 shares
+  );
+  event MaxSlashablePercentageChanged(uint256 newPercentage);
+  event Slashed(address indexed destination, uint256 amount);
+  event SlashingExitWindowDurationChanged(uint256 windowSeconds);
+  event CooldownSecondsChanged(uint256 cooldownSeconds);
+  event ExchangeRateChanged(uint128 exchangeRate);
+  event FundsReturned(uint256 amount);
+  event SlashingSettled();
+
+  /**
+   * @dev Returns the current exchange rate
+   * @return exchangeRate as 18 decimal precision uint128
+   **/
+  function getExchangeRate() external view returns (uint128);
+
+  /**
+   * @dev Executes a slashing of the underlying of a certain amount, transferring the seized funds
+   * to destination. Decreasing the amount of underlying will automatically adjust the exchange rate.
+   * A call to `slash` will start a slashing event which has to be settled via `settleSlashing`.
+   * As long as the slashing event is ongoing, stake and slash are deactivated.
+   * - MUST NOT be called when a spevious slashing is still ongoing
+   * @param destination the address where seized funds will be transferred
+   * @param amount the amount to be slashed
+   * - if the amount bigger than maximum allowed, the maximum will be slashed instead.
+   * @return amount the amount slashed
+   **/
+  function slash(address destination, uint256 amount)
+    external
+    returns (uint256);
+
+  /**
+   * @dev Settles an ongoing slashing event
+   */
+  function settleSlashing() external;
+
+  /**
+   * @dev Pulls STAKE_TOKEN and distributes them amonst current stakers by altering the exchange rate.
+   * This method is permissionless and intendet to be used after a slashing event to return potential excess funds.
+   * @param amount amount of STAKE_TOKEN to pull.
+   */
+  function returnFunds(uint256 amount) external;
+
+  /**
+   * @dev Getter of the cooldown seconds
+   * @return cooldownSeconds the amount of seconds between starting the cooldown and being able to redeem
+   */
+  function getCooldownSeconds() external view returns (uint256);
+
+  /**
+   * @dev Setter of cooldown seconds
+   * Can only be called by the cooldown admin
+   * @param cooldownSeconds the new amount of seconds you have to wait between starting the cooldown and being able to redeem
+   */
+  function setCooldownSeconds(uint256 cooldownSeconds) external;
+
+  /**
+   * @dev Getter of the max slashable percentage of the total staked amount.
+   * @return percentage the maximum slashable percentage
+   */
+  function getMaxSlashablePercentage() external view returns (uint256);
+
+  /**
+   * @dev Setter of max slashable percentage of the total staked amount.
+   * Can only be called by the slashing admin
+   * @param percentage the new maximum slashable percentage
+   */
+  function setMaxSlashablePercentage(uint256 percentage) external;
+
+  /**
+   * @dev returns the exact amount of shares that would be received for the provided number of assets
+   * @param assets the number of assets to stake
+   * @return shares the number of shares that would be received
+   */
+  function previewStake(uint256 assets) external view returns (uint256);
+
+  /**
+   * @dev Allows staking a certain amount of STAKED_TOKEN with gasless approvals (permit)
+   * @param to The address to receiving the shares
+   * @param amount The amount to be staked
+   * @param deadline The permit execution deadline
+   * @param v The v component of the signed message
+   * @param r The r component of the signed message
+   * @param s The s component of the signed message
+   **/
+  function stakeWithPermit(
+    address from,
+    address to,
+    uint256 amount,
+    uint256 deadline,
+    uint8 v,
+    bytes32 r,
+    bytes32 s
+  ) external;
+
+  /**
+   * @dev Claims an `amount` of `REWARD_TOKEN` to the address `to` on behalf of the user. Only the claim helper contract is allowed to call this function
+   * @param from The address of the user from to claim
+   * @param to Address to send the claimed rewards
+   * @param amount Amount to claim
+   **/
+  function claimRewardsOnBehalf(
+    address from,
+    address to,
+    uint256 amount
+  ) external returns (uint256);
+
+  /**
+   * @dev returns the exact amount of assets that would be redeemed for the provided number of shares
+   * @param shares the number of shares to redeem
+   * @return assets the number of assets that would be redeemed
+   */
+  function previewRedeem(uint256 shares) external view returns (uint256);
+
+  /**
+   * @dev Redeems shares for a user. Only the claim helper contract is allowed to call this function
+   * @param from Address to redeem from
+   * @param to Address to redeem to
+   * @param amount Amount of shares to redeem
+   **/
+  function redeemOnBehalf(
+    address from,
+    address to,
+    uint256 amount
+  ) external;
+
+  /**
+   * @dev Claims an `amount` of `REWARD_TOKEN` and restakes
+   * @param to Address to stake to
+   * @param amount Amount to claim
+   **/
+  function claimRewardsAndStake(address to, uint256 amount)
+    external
+    returns (uint256);
+
+  /**
+   * @dev Claims an `amount` of `REWARD_TOKEN` and redeem
+   * @param claimAmount Amount to claim
+   * @param redeemAmount Amount to redeem
+   * @param to Address to claim and unstake to
+   **/
+  function claimRewardsAndRedeem(
+    address to,
+    uint256 claimAmount,
+    uint256 redeemAmount
+  ) external;
+
+  /**
+   * @dev Claims an `amount` of `REWARD_TOKEN` and restakes. Only the claim helper contract is allowed to call this function
+   * @param from The address of the from from which to claim
+   * @param to Address to stake to
+   * @param amount Amount to claim
+   **/
+  function claimRewardsAndStakeOnBehalf(
+    address from,
+    address to,
+    uint256 amount
+  ) external returns (uint256);
+
+  /**
+   * @dev Claims an `amount` of `REWARD_TOKEN` and redeem. Only the claim helper contract is allowed to call this function
+   * @param from The address of the from
+   * @param to Address to claim and unstake to
+   * @param claimAmount Amount to claim
+   * @param redeemAmount Amount to redeem
+   **/
+  function claimRewardsAndRedeemOnBehalf(
+    address from,
+    address to,
+    uint256 claimAmount,
+    uint256 redeemAmount
+  ) external;
+}
+
+/**
+ * @title PercentageMath library
+ * @author Aave
+ * @notice Provides functions to perform percentage calculations
+ * @dev Percentages are defined by default with 2 decimals of precision (100.00). The precision is indicated by PERCENTAGE_FACTOR
+ * @dev Operations are rounded half up
+ **/
+
+library PercentageMath {
+  uint256 constant PERCENTAGE_FACTOR = 1e4; //percentage plus two decimals
+  uint256 constant HALF_PERCENT = PERCENTAGE_FACTOR / 2;
+
+  /**
+   * @dev Executes a percentage multiplication
+   * @param value The value of which the percentage needs to be calculated
+   * @param percentage The percentage of the value to be calculated
+   * @return The percentage of value
+   **/
+  function percentMul(uint256 value, uint256 percentage)
+    internal
+    pure
+    returns (uint256)
+  {
+    if (value == 0 || percentage == 0) {
+      return 0;
+    }
+
+    require(
+      value <= (type(uint256).max) / percentage,
+      'MATH_MULTIPLICATION_OVERFLOW'
+    );
+
+    return (value * percentage) / PERCENTAGE_FACTOR;
+  }
+
+  /**
+   * @dev Executes a percentage division
+   * @param value The value of which the percentage needs to be calculated
+   * @param percentage The percentage of the value to be calculated
+   * @return The value divided the percentage
+   **/
+  function percentDiv(uint256 value, uint256 percentage)
+    internal
+    pure
+    returns (uint256)
+  {
+    require(percentage != 0, 'MATH_DIVISION_BY_ZERO');
+
+    require(
+      value <= type(uint256).max / PERCENTAGE_FACTOR,
+      'MATH_MULTIPLICATION_OVERFLOW'
+    );
+
+    return (value * PERCENTAGE_FACTOR) / percentage;
+  }
+}
+
+/**
+ * @title RoleManager
+ * @notice Generic role manager to manage slashing and cooldown admin in StakedAaveV3.
+ *         It implements a claim admin role pattern to safely migrate between different admin addresses
+ * @author Aave
+ **/
+contract RoleManager {
+  struct InitAdmin {
+    uint256 role;
+    address admin;
+  }
+
+  mapping(uint256 => address) private _admins;
+  mapping(uint256 => address) private _pendingAdmins;
+
+  event PendingAdminChanged(address indexed newPendingAdmin, uint256 role);
+  event RoleClaimed(address indexed newAdming, uint256 role);
+
+  modifier onlyRoleAdmin(uint256 role) {
+    require(_admins[role] == msg.sender, 'CALLER_NOT_ROLE_ADMIN');
+    _;
+  }
+
+  modifier onlyPendingRoleAdmin(uint256 role) {
+    require(
+      _pendingAdmins[role] == msg.sender,
+      'CALLER_NOT_PENDING_ROLE_ADMIN'
+    );
+    _;
+  }
+
+  /**
+   * @dev returns the admin associated with the specific role
+   * @param role the role associated with the admin being returned
+   **/
+  function getAdmin(uint256 role) public view returns (address) {
+    return _admins[role];
+  }
+
+  /**
+   * @dev returns the pending admin associated with the specific role
+   * @param role the role associated with the pending admin being returned
+   **/
+  function getPendingAdmin(uint256 role) public view returns (address) {
+    return _pendingAdmins[role];
+  }
+
+  /**
+   * @dev sets the pending admin for a specific role
+   * @param role the role associated with the new pending admin being set
+   * @param newPendingAdmin the address of the new pending admin
+   **/
+  function setPendingAdmin(uint256 role, address newPendingAdmin)
+    public
+    onlyRoleAdmin(role)
+  {
+    _pendingAdmins[role] = newPendingAdmin;
+    emit PendingAdminChanged(newPendingAdmin, role);
+  }
+
+  /**
+   * @dev allows the caller to become a specific role admin
+   * @param role the role associated with the admin claiming the new role
+   **/
+  function claimRoleAdmin(uint256 role) external onlyPendingRoleAdmin(role) {
+    _admins[role] = msg.sender;
+    emit RoleClaimed(msg.sender, role);
+  }
+
+  function _initAdmins(InitAdmin[] memory initAdmins) internal {
+    for (uint256 i = 0; i < initAdmins.length; i++) {
+      require(
+        _admins[initAdmins[i].role] == address(0) &&
+          initAdmins[i].admin != address(0),
+        'ADMIN_CANNOT_BE_INITIALIZED'
+      );
+      _admins[initAdmins[i].role] = initAdmins[i].admin;
+      emit RoleClaimed(initAdmins[i].admin, initAdmins[i].role);
+    }
+  }
+}
+
+/**
+ * @title StakedToken
+ * @notice Contract to stake Aave token, tokenize the position and get rewards, inheriting from a distribution manager contract
+ * @author Aave
+ **/
+contract StakedTokenV3 is StakedTokenV2, IStakedTokenV3, RoleManager {
+  using SafeERC20 for IERC20;
+  using PercentageMath for uint256;
+
+  uint256 public constant SLASH_ADMIN_ROLE = 0;
+  uint256 public constant COOLDOWN_ADMIN_ROLE = 1;
+  uint256 public constant CLAIM_HELPER_ROLE = 2;
+  uint128 public constant INITIAL_EXCHANGE_RATE = 1e18;
+  uint256 public constant TOKEN_UNIT = 1e18;
+
+  /// @notice Seconds between starting cooldown and being able to withdraw
+  uint256 internal _cooldownSeconds;
+  /// @notice The maximum amount of funds that can be slashed at any given time
+  uint256 internal _maxSlashablePercentage;
+  /// @notice Snapshots of the exchangeRate for a given block
+  mapping(uint256 => Snapshot) public _exchangeRateSnapshots;
+  uint120 internal _exchangeRateSnapshotsCount;
+  /// @notice Mirror of latest snapshot value for cheaper access
+  uint128 internal _currentExchangeRate;
+  /// @notice Flag determining if there's an ongoing slashing event that needs to be settled
+  bool public inPostSlashingPeriod;
+
+  modifier onlySlashingAdmin() {
+    require(
+      msg.sender == getAdmin(SLASH_ADMIN_ROLE),
+      'CALLER_NOT_SLASHING_ADMIN'
+    );
+    _;
+  }
+
+  modifier onlyCooldownAdmin() {
+    require(
+      msg.sender == getAdmin(COOLDOWN_ADMIN_ROLE),
+      'CALLER_NOT_COOLDOWN_ADMIN'
+    );
+    _;
+  }
+
+  modifier onlyClaimHelper() {
+    require(
+      msg.sender == getAdmin(CLAIM_HELPER_ROLE),
+      'CALLER_NOT_CLAIM_HELPER'
+    );
+    _;
+  }
+
+  constructor(
+    IERC20 stakedToken,
+    IERC20 rewardToken,
+    uint256 unstakeWindow,
+    address rewardsVault,
+    address emissionManager,
+    uint128 distributionDuration
+  )
+    StakedTokenV2(
+      stakedToken,
+      rewardToken,
+      unstakeWindow,
+      rewardsVault,
+      emissionManager,
+      distributionDuration
+    )
+  {}
+
+  function REVISION() public pure virtual override returns (uint256) {
+    return 3;
+  }
+
+  /**
+   * @dev returns the revision of the implementation contract
+   * @return The revision
+   */
+  function getRevision() internal pure virtual override returns (uint256) {
+    return REVISION();
+  }
+
+  /**
+   * @dev Called by the proxy contract
+   **/
+  function initialize(
+    address slashingAdmin,
+    address cooldownPauseAdmin,
+    address claimHelper,
+    uint256 maxSlashablePercentage,
+    uint256 cooldownSeconds
+  ) external initializer {
+    InitAdmin[] memory initAdmins = new InitAdmin[](3);
+    initAdmins[0] = InitAdmin(SLASH_ADMIN_ROLE, slashingAdmin);
+    initAdmins[1] = InitAdmin(COOLDOWN_ADMIN_ROLE, cooldownPauseAdmin);
+    initAdmins[2] = InitAdmin(CLAIM_HELPER_ROLE, claimHelper);
+
+    _initAdmins(initAdmins);
+
+    _setMaxSlashablePercentage(maxSlashablePercentage);
+    _setCooldownSeconds(cooldownSeconds);
+    _updateExchangeRate(INITIAL_EXCHANGE_RATE);
+
+    // needed to claimRewardsAndStake works without a custom approval each time
+    STAKED_TOKEN.approve(address(this), type(uint256).max);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function previewStake(uint256 assets) public view returns (uint256) {
+    return (assets * _currentExchangeRate) / TOKEN_UNIT;
+  }
+
+  /// @inheritdoc IStakedTokenV2
+  function stake(address to, uint256 amount)
+    external
+    override(IStakedTokenV2, StakedTokenV2)
+  {
+    _stake(msg.sender, to, amount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function stakeWithPermit(
+    address from,
+    address to,
+    uint256 amount,
+    uint256 deadline,
+    uint8 v,
+    bytes32 r,
+    bytes32 s
+  ) external override {
+    IERC20WithPermit(address(STAKED_TOKEN)).permit(
+      from,
+      address(this),
+      amount,
+      deadline,
+      v,
+      r,
+      s
+    );
+    _stake(from, to, amount);
+  }
+
+  /// @inheritdoc IStakedTokenV2
+  function redeem(address to, uint256 amount)
+    external
+    override(IStakedTokenV2, StakedTokenV2)
+  {
+    _redeem(msg.sender, to, amount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function redeemOnBehalf(
+    address from,
+    address to,
+    uint256 amount
+  ) external override onlyClaimHelper {
+    _redeem(from, to, amount);
+  }
+
+  /// @inheritdoc IStakedTokenV2
+  function claimRewards(address to, uint256 amount)
+    external
+    override(IStakedTokenV2, StakedTokenV2)
+  {
+    _claimRewards(msg.sender, to, amount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function claimRewardsOnBehalf(
+    address from,
+    address to,
+    uint256 amount
+  ) external override onlyClaimHelper returns (uint256) {
+    return _claimRewards(from, to, amount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function claimRewardsAndStake(address to, uint256 amount)
+    external
+    override
+    returns (uint256)
+  {
+    return _claimRewardsAndStakeOnBehalf(msg.sender, to, amount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function claimRewardsAndStakeOnBehalf(
+    address from,
+    address to,
+    uint256 amount
+  ) external override onlyClaimHelper returns (uint256) {
+    return _claimRewardsAndStakeOnBehalf(from, to, amount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function claimRewardsAndRedeem(
+    address to,
+    uint256 claimAmount,
+    uint256 redeemAmount
+  ) external override {
+    _claimRewards(msg.sender, to, claimAmount);
+    _redeem(msg.sender, to, redeemAmount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function claimRewardsAndRedeemOnBehalf(
+    address from,
+    address to,
+    uint256 claimAmount,
+    uint256 redeemAmount
+  ) external override onlyClaimHelper {
+    _claimRewards(from, to, claimAmount);
+    _redeem(from, to, redeemAmount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function getExchangeRate() public view override returns (uint128) {
+    return _currentExchangeRate;
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function previewRedeem(uint256 shares)
+    public
+    view
+    override
+    returns (uint256)
+  {
+    return (TOKEN_UNIT * shares) / _currentExchangeRate;
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function slash(address destination, uint256 amount)
+    external
+    override
+    onlySlashingAdmin
+    returns (uint256)
+  {
+    require(!inPostSlashingPeriod, 'PREVIOUS_SLASHING_NOT_SETTLED');
+    uint256 currentShares = totalSupply();
+    uint256 balance = previewRedeem(currentShares);
+
+    uint256 maxSlashable = balance.percentMul(_maxSlashablePercentage);
+
+    if (amount > maxSlashable) {
+      amount = maxSlashable;
+    }
+
+    inPostSlashingPeriod = true;
+    _updateExchangeRate(_getExchangeRate(balance - amount, currentShares));
+
+    STAKED_TOKEN.safeTransfer(destination, amount);
+
+    emit Slashed(destination, amount);
+    return amount;
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function returnFunds(uint256 amount) external override {
+    uint256 currentShares = totalSupply();
+    uint256 assets = previewRedeem(currentShares);
+    _updateExchangeRate(_getExchangeRate(assets + amount, currentShares));
+
+    STAKED_TOKEN.safeTransferFrom(msg.sender, address(this), amount);
+    emit FundsReturned(amount);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function settleSlashing() external override onlySlashingAdmin {
+    inPostSlashingPeriod = false;
+    emit SlashingSettled();
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function setMaxSlashablePercentage(uint256 percentage)
+    external
+    override
+    onlySlashingAdmin
+  {
+    _setMaxSlashablePercentage(percentage);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function getMaxSlashablePercentage()
+    external
+    view
+    override
+    returns (uint256)
+  {
+    return _maxSlashablePercentage;
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function setCooldownSeconds(uint256 cooldownSeconds)
+    external
+    onlyCooldownAdmin
+  {
+    _setCooldownSeconds(cooldownSeconds);
+  }
+
+  /// @inheritdoc IStakedTokenV3
+  function getCooldownSeconds() external view returns (uint256) {
+    return _cooldownSeconds;
+  }
+
+  /// @inheritdoc IStakedTokenV2
+  function getNextCooldownTimestamp(
+    uint256 fromCooldownTimestamp,
+    uint256 amountToReceive,
+    address toAddress,
+    uint256 toBalance
+  ) public view override(IStakedTokenV2, StakedTokenV2) returns (uint256) {
+    uint256 toCooldownTimestamp = stakersCooldowns[toAddress];
+    if (toCooldownTimestamp == 0) {
+      return 0;
+    }
+
+    uint256 minimalValidCooldownTimestamp = block.timestamp -
+      _cooldownSeconds -
+      UNSTAKE_WINDOW;
+
+    if (minimalValidCooldownTimestamp > toCooldownTimestamp) {
+      toCooldownTimestamp = 0;
+    } else {
+      uint256 adjustedFromCooldownTimestamp = (minimalValidCooldownTimestamp >
+        fromCooldownTimestamp)
+        ? block.timestamp
+        : fromCooldownTimestamp;
+
+      if (adjustedFromCooldownTimestamp < toCooldownTimestamp) {
+        return toCooldownTimestamp;
+      } else {
+        toCooldownTimestamp =
+          ((amountToReceive * adjustedFromCooldownTimestamp) +
+            (toBalance * toCooldownTimestamp)) /
+          (amountToReceive + toBalance);
+      }
+    }
+    return toCooldownTimestamp;
+  }
+
+  /// @dev sets the max slashable percentage
+  /// @param percentage must be strictly lower 100% as otherwise the exchange rate calculation would result in 0 division
+  function _setMaxSlashablePercentage(uint256 percentage) internal {
+    require(
+      percentage < PercentageMath.PERCENTAGE_FACTOR,
+      'INVALID_SLASHING_PERCENTAGE'
+    );
+
+    _maxSlashablePercentage = percentage;
+    emit MaxSlashablePercentageChanged(percentage);
+  }
+
+  function _setCooldownSeconds(uint256 cooldownSeconds) internal {
+    _cooldownSeconds = cooldownSeconds;
+    emit CooldownSecondsChanged(cooldownSeconds);
+  }
+
+  function _claimRewards(
+    address from,
+    address to,
+    uint256 amount
+  ) internal returns (uint256) {
+    require(amount != 0, 'INVALID_ZERO_AMOUNT');
+    uint256 newTotalRewards = _updateCurrentUnclaimedRewards(
+      from,
+      balanceOf(from),
+      false
+    );
+
+    uint256 amountToClaim = (amount > newTotalRewards)
+      ? newTotalRewards
+      : amount;
+
+    stakerRewardsToClaim[from] = newTotalRewards - amountToClaim;
+    REWARD_TOKEN.safeTransferFrom(REWARDS_VAULT, to, amountToClaim);
+    emit RewardsClaimed(from, to, amountToClaim);
+    return amountToClaim;
+  }
+
+  function _claimRewardsAndStakeOnBehalf(
+    address from,
+    address to,
+    uint256 amount
+  ) internal returns (uint256) {
+    require(REWARD_TOKEN == STAKED_TOKEN, 'REWARD_TOKEN_IS_NOT_STAKED_TOKEN');
+
+    uint256 userUpdatedRewards = _updateCurrentUnclaimedRewards(
+      from,
+      balanceOf(from),
+      true
+    );
+    uint256 amountToClaim = (amount > userUpdatedRewards)
+      ? userUpdatedRewards
+      : amount;
+
+    if (amountToClaim != 0) {
+      _claimRewards(from, address(this), amountToClaim);
+      _stake(address(this), to, amountToClaim);
+    }
+
+    return amountToClaim;
+  }
+
+  function _stake(
+    address from,
+    address to,
+    uint256 amount
+  ) internal {
+    require(!inPostSlashingPeriod, 'SLASHING_ONGOING');
+    require(amount != 0, 'INVALID_ZERO_AMOUNT');
+
+    uint256 balanceOfTo = balanceOf(to);
+
+    uint256 accruedRewards = _updateUserAssetInternal(
+      to,
+      address(this),
+      balanceOfTo,
+      totalSupply()
+    );
+
+    if (accruedRewards != 0) {
+      stakerRewardsToClaim[to] = stakerRewardsToClaim[to] + accruedRewards;
+      emit RewardsAccrued(to, accruedRewards);
+    }
+
+    stakersCooldowns[to] = getNextCooldownTimestamp(0, amount, to, balanceOfTo);
+
+    uint256 sharesToMint = previewStake(amount);
+
+    STAKED_TOKEN.safeTransferFrom(from, address(this), amount);
+
+    _mint(to, sharesToMint);
+
+    emit Staked(from, to, amount, sharesToMint);
+  }
+
+  /**
+   * @dev Redeems staked tokens, and stop earning rewards
+   * @param from Address to redeem from
+   * @param to Address to redeem to
+   * @param amount Amount to redeem
+   **/
+  function _redeem(
+    address from,
+    address to,
+    uint256 amount
+  ) internal {
+    require(amount != 0, 'INVALID_ZERO_AMOUNT');
+    //solium-disable-next-line
+    uint256 cooldownStartTimestamp = stakersCooldowns[from];
+
+    if (!inPostSlashingPeriod) {
+      require(
+        (block.timestamp > cooldownStartTimestamp + _cooldownSeconds),
+        'INSUFFICIENT_COOLDOWN'
+      );
+      require(
+        (block.timestamp - (cooldownStartTimestamp + _cooldownSeconds) <=
+          UNSTAKE_WINDOW),
+        'UNSTAKE_WINDOW_FINISHED'
+      );
+    }
+    uint256 balanceOfFrom = balanceOf(from);
+
+    uint256 amountToRedeem = (amount > balanceOfFrom) ? balanceOfFrom : amount;
+
+    _updateCurrentUnclaimedRewards(from, balanceOfFrom, true);
+
+    uint256 underlyingToRedeem = (amountToRedeem * TOKEN_UNIT) /
+      _currentExchangeRate;
+
+    _burn(from, amountToRedeem);
+
+    if (balanceOfFrom - amountToRedeem == 0) {
+      stakersCooldowns[from] = 0;
+    }
+
+    IERC20(STAKED_TOKEN).safeTransfer(to, underlyingToRedeem);
+
+    emit Redeem(from, to, underlyingToRedeem, amountToRedeem);
+  }
+
+  /**
+   * @dev Updates the exchangeRate and emits events accordingly
+   * @param newExchangeRate the new exchange rate
+   */
+  function _updateExchangeRate(uint128 newExchangeRate) internal {
+    _exchangeRateSnapshots[_exchangeRateSnapshotsCount] = Snapshot(
+      uint128(block.number),
+      newExchangeRate
+    );
+    ++_exchangeRateSnapshotsCount;
+    _currentExchangeRate = newExchangeRate;
+    emit ExchangeRateChanged(newExchangeRate);
+  }
+
+  /**
+   * @dev calculates the exchange rate based on totalAssets and totalShares
+   * @dev always rounds up to ensure 100% backing of shares by rounding in favor of the contract
+   * @param totalAssets The total amount of assets staked
+   * @param totalShares The total amount of shares
+   * @return exchangeRate as 18 decimal precision uint128
+   */
+  function _getExchangeRate(uint256 totalAssets, uint256 totalShares)
+    internal
+    pure
+    returns (uint128)
+  {
+    return uint128(((totalShares * TOKEN_UNIT) + TOKEN_UNIT) / totalAssets);
+  }
+
+  /// @dev Modified version accounting for exchange rate at block
+  /// @inheritdoc GovernancePowerDelegationERC20
+  function _searchByBlockNumber(
+    mapping(address => mapping(uint256 => Snapshot)) storage snapshots,
+    mapping(address => uint256) storage snapshotsCounts,
+    address user,
+    uint256 blockNumber
+  ) internal view override returns (uint256) {
+    return
+      (super._searchByBlockNumber(
+        snapshots,
+        snapshotsCounts,
+        user,
+        blockNumber
+      ) * TOKEN_UNIT) /
+      _binarySearch(
+        _exchangeRateSnapshots,
+        _exchangeRateSnapshotsCount,
+        blockNumber
+      );
+  }
+}
+
+interface IGhoVariableDebtToken {
+  /**
+   * @dev updates the discount when discount token is transferred
+   * @dev Only callable by discount token
+   * @param sender address of sender
+   * @param recipient address of recipient
+   * @param senderDiscountTokenBalance sender discount token balance
+   * @param recipientDiscountTokenBalance recipient discount token balance
+   * @param amount amount of discount token being transferred
+   **/
+  function updateDiscountDistribution(
+    address sender,
+    address recipient,
+    uint256 senderDiscountTokenBalance,
+    uint256 recipientDiscountTokenBalance,
+    uint256 amount
+  ) external;
+}
+
+/**
+ * @title StakedAaveV3
+ * @notice StakedTokenV3 with AAVE token as staked token
+ * @author Aave
+ **/
+contract StakedAaveV3 is StakedTokenV3 {
+  // GHO
+  IGhoVariableDebtToken public immutable GHO_DEBT_TOKEN;
+
+  function REVISION() public pure virtual override returns (uint256) {
+    return 4;
+  }
+
+  constructor(
+    IERC20 stakedToken,
+    IERC20 rewardToken,
+    uint256 unstakeWindow,
+    address rewardsVault,
+    address emissionManager,
+    uint128 distributionDuration,
+    address ghoDebtToken
+  )
+    StakedTokenV3(
+      stakedToken,
+      rewardToken,
+      unstakeWindow,
+      rewardsVault,
+      emissionManager,
+      distributionDuration
+    )
+  {
+    require(Address.isContract(address(ghoDebtToken)), 'GHO_MUST_BE_CONTRACT');
+    GHO_DEBT_TOKEN = IGhoVariableDebtToken(ghoDebtToken);
+  }
+
+  /// @dev Modified version including GHO hook
+  /// @inheritdoc StakedTokenV2
+  function _beforeTokenTransfer(
+    address from,
+    address to,
+    uint256 amount
+  ) internal override {
+    GHO_DEBT_TOKEN.updateDiscountDistribution(
+      from,
+      to,
+      balanceOf(from),
+      balanceOf(to),
+      amount
+    );
+    super._beforeTokenTransfer(from, to, amount);
+  }
+}
```