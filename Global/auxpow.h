gh repo clone dogecoin/dogecoin

// Copyright (c) 2009-2010 Satoshi Nakamoto
// Copyright (c) 2009-2014 The Bitcoin developers
// Copyright (c) 2014-2016 Daniel Kraft
// Distributed under the MIT/X11 software license, see the accompanying
// file license.txt or http://www.opensource.org/licenses/mit-license.php.

#ifndef BITCOIN_AUXPOW_H
#define BITCOIN_AUXPOW_H

#include "consensus/params.h"
#include "consensus/validation.h"
#include "primitives/pureheader.h"
#include "primitives/transaction.h"
#include "serialize.h"
#include "uint256.h"

#include <vector>

 CBlock;
 CBlockHeader;
 CBlockIndex;

/** Header for merge-mining data in the coinbase.  */
 unsigned char pchMergedMiningHeader[] = { 0xfa, 0xbe, 'm', 'm' };

/* Because it is needed for auxpow, the definition of CMerkleTx is moved
   here from wallet.h.  */

/** A transaction with a merkle branch linking it to the block chain. */
 CMerkleTx
{
 :
  /** Constant used in hashBlock to indicate tx has been abandoned */
     uint256 ABANDON_HASH;


 :
    CTransactionRef tx;
    uint256 hashBlock;

    /** Merkle branch connecting this transaction to the block's merkle root.
     *  Set by InitMerkleBranch() and verified in CAuxPow::check(). */
    std::vector<uint256> vMerkleBranch;

    /* An nIndex == -1 means that hashBlock (in nonzero) refers to the earliest
     * block in the chain we know this or any in-wallet dependency conflicts
     * with. Older clients interpret nIndex == -1 as unconfirmed for backward
     * compatibility.
     */
    int nIndex;

    CMerkleTx()
    {
        SetTx(MakeTransactionRef());
        Init();
    }

    CMerkleTx(CTransactionRef arg)
    {
        SetTx(std::move(arg));
        Init();
    }

    /** Helper conversion operator to allow passing CMerkleTx where CTransaction is expected.
     *  TODO: adapt callers and remove this operator. */
      CTransaction&()   {       *tx; }

    void Init()
    {
        hashBlock = uint256();
        nIndex = -1;
    }

    void SetTx(CTransactionRef arg)
    {
        tx = std::move(arg);
    }

    ADD_SERIALIZE_METHODS;

              < Stream,  Operation>
            void SerializationOp(Stream& s, Operation ser_action) {
        READWRITE(tx);
        READWRITE(hashBlock);
        READWRITE(vMerkleBranch);
        READWRITE(nIndex);
    }

    /**
     * Actually compute the Merkle branch.  This is used for unit tests when
     * constructing an auxpow.  It is not needed for actual production, since
     * we do not care in the Namecoin client how the auxpow is constructed
     * by a miner.
     */
    void InitMerkleBranch(const CBlock& block, int posInBlock);

    void SetMerkleBranch(const CBlockIndex* pindex, int posInBlock);

    /**
     * Return depth of transaction in blockchain:
     * <0  : conflicts with a transaction this deep in the blockchain
     *  0  : in memory pool, waiting to be included in a block
     * >=1 : this many blocks deep in the main chain
     */
    int GetDepthInMainChain( CBlockIndex* &pindexRet) ;
    int GetDepthInMainChain()  {  CBlockIndex *pindexRet;  GetDepthInMainChain(pindexRet); }
    bool IsInMainChain()  {  CBlockIndex *pindexRet;  GetDepthInMainChain(pindexRet) > 0; }
    int GetBlocksToMaturity() const;
    /** Pass this transaction to the mempool. Fails if absolute fee exceeds absurd fee. */
    bool AcceptToMemoryPool(const CAmount& nAbsurdFee, CValidationState& state);
    bool hashUnset() const { return (hashBlock.IsNull() || hashBlock == ABANDON_HASH); }
    bool isAbandoned() const { return (hashBlock == ABANDON_HASH); }
    void setAbandoned() { hashBlock = ABANDON_HASH; }

    const uint256& GetHash() const { return tx->GetHash(); }
    bool IsCoinBase() const { return tx->IsCoinBase(); }
};

/**
 * Data for the merge-mining auxpow.  This is a merkle tx (the parent block's
 * coinbase tx) that can be verified to be in the parent block, and this
 * transaction's input (the coinbase script) contains the reference
 * to the actual merge-mined block.
 */
class CAuxPow : public CMerkleTx
{

/* Public for the unit tests.  */
public:

  /** The merkle branch connecting the aux block to our coinbase.  */
  std::vector<uint256> vChainMerkleBranch;

  /** Merkle tree index of the aux block header in the coinbase.  */
  int nChainIndex;

  /** Parent block header (on which the real PoW is done).  */
  CPureBlockHeader parentBlock;

public:

  /* Prevent accidental conversion.  */
  inline explicit CAuxPow(CTransactionRef txIn)
    : CMerkleTx(txIn)
  {
  }

  inline CAuxPow()
    : CMerkleTx()
  {
  }

  ADD_SERIALIZE_METHODS;

  template<typename Stream, typename Operation>
    inline void
    SerializationOp (Stream& s, Operation ser_action)
  {
    READWRITE (*static_cast<CMerkleTx*> (this));
    READWRITE (vChainMerkleBranch);
    READWRITE (nChainIndex);
    READWRITE (parentBlock);
  }

  /**
   * Check the auxpow, given the merge-mined block's hash and our chain ID.
   * Note that this does not verify the actual PoW on the parent block!  It
   * just confirms that all the merkle branches are valid.
   * @param hashAuxBlock Hash of the merge-mined block.
   * @param nChainId The auxpow chain ID of the block to check.
   * @param params Consensus parameters.
   * @return True if the auxpow is valid.
   */
  bool check(const uint256& hashAuxBlock, int nChainId, const Consensus::Params& params) const;

  /**
   * Get the parent block's hash.  This is used to verify that it
   * satisfies the PoW requirement.
   * @return The parent block hash.
   */
  inline uint256
  getParentBlockPoWHash() const
  {
    return parentBlock.GetPoWHash ();
  }

  /**
   * Return parent block.  This is only used for the temporary parentblock
   * auxpow version check.
   * @return The parent block.
   */
  /* FIXME: Remove after the hardfork.  */
  inline const CPureBlockHeader&
  getParentBlock() const
  {
    return parentBlock;
  }

  /**
   * Calculate the expected index in the merkle tree.  This is also used
   * for the test-suite.
   * @param nNonce The coinbase's nonce value.
   * @param nChainId The chain ID.
   * @param h The merkle block height.
   * @return The expected index for the aux hash.
   */
  static int getExpectedIndex(uint32_t nNonce, int nChainId, unsigned h);

  /**
   * Check a merkle branch.  This used to be in CBlock, but was removed
   * upstream.  Thus include it here now.
   */
  static uint256 CheckMerkleBranch(uint256 hash,
                                   const std::vector<uint256>& vMerkleBranch,
                                   int nIndex);

  /**
   * Initialise the auxpow of the given block header.  This constructs
   * a minimal CAuxPow object with a minimal parent block and sets
   * it on the block header.  The auxpow is not necessarily valid, but
   * can be "mined" to make it valid.
   * @param header The header to set the auxpow on.
   */
  static void initAuxPow(CBlockHeader& header);

};

#endif // BITCOIN_AUXPOW_H
