from eth2spec.test.helpers.keys import privkeys
from eth2spec.test.helpers.block import (
    build_empty_block_for_next_slot,
)
from eth2spec.utils import bls


def compute_sync_committee_signature(spec, state, slot, privkey):
    domain = spec.get_domain(state, spec.DOMAIN_SYNC_COMMITTEE, spec.compute_epoch_at_slot(slot))
    if slot == state.slot:
        block_root = build_empty_block_for_next_slot(spec, state).parent_root
    else:
        block_root = spec.get_block_root_at_slot(state, slot)
    signing_root = spec.compute_signing_root(block_root, domain)
    return bls.Sign(privkey, signing_root)


def compute_aggregate_sync_committee_signature(spec, state, slot, participants):
    if len(participants) == 0:
        return spec.G2_POINT_AT_INFINITY

    signatures = []
    for validator_index in participants:
        privkey = privkeys[validator_index]
        signatures.append(
            compute_sync_committee_signature(
                spec,
                state,
                slot,
                privkey,
            )
        )
    return bls.Aggregate(signatures)


def get_padded_sync_committee_bits(spec, sync_committee_bits):
    if len(sync_committee_bits) < spec.SYNC_COMMITTEE_SIZE:
        return sync_committee_bits + [False] * (spec.SYNC_COMMITTEE_SIZE - len(sync_committee_bits))
    return sync_committee_bits
