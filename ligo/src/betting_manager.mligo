#if !BETTING_MANAGER
#define BETTING_MANAGER

type place_bet_param = {
  race_id : int;
  horse_id : int;
  payout : int;
}

type betting = {
  race_id : int;
  horse_id : int;
  amount : int;
  payout : int;
}

type betting_ledger = (address, betting) big_map

type betting_storage = {
  ledger : betting_ledger;
}

type betting_param = 
  | Place_bet of place_bet_param


let place_bet (param, storage : place_bet_param * betting_storage) : betting_storage =
  let bet: betting = {
    race_id = param.race_id;
    horse_id = param.horse_id;
    payout = param.payout;
    amount = 1;
  } in
  let updated_ledger : betting_ledger =
    Big_map.update (Tezos.get_sender()) (Some bet) storage.ledger in  
  let s = { storage with ledger = updated_ledger; } in
  s
  
let betting_main (param, storage : betting_param * betting_storage) 
    : (operation list) * betting_storage =
  match param with

  | Place_bet p ->
    let s = place_bet (p, storage) in
    (([]: operation list), s)

#endif