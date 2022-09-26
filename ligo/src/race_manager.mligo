#if !RACE_MANAGER
#define RACE_MANAGER

type place_bet_param = {
  race_id : int;
  horse_id : int;
  payout : int;
}

type betting = {
  race_id : int;
  horse_id : int;
  amount : tez;
  payout : int;
}

type betting_ledger = (address, betting) big_map

type race_storage = {
  race_id : nat;
  status : nat;
  winner : nat;
  ready_time: nat;
  start_time : timestamp;
  bettings : betting_ledger;
}

type race_param = 
  | Ready_race of nat
  | Start_race
  | Finish_race of nat
  | Place_bet of place_bet_param


let ready_race (ready_time, storage : nat * race_storage) : race_storage =
  let new_race_id = 1n + storage.race_id in
  let s = { storage with
    race_id = new_race_id;
    status = 1n;
    winner = 0n;
    ready_time = ready_time;
  } in
  s


let start_race (storage : race_storage) : race_storage =
  let s = { storage with
    status = 2n;
    winner = 0n;
    start_time = Tezos.get_now ();
  } in
  s


let finish_race (winner, storage : nat * race_storage) : race_storage = 
  let s = { storage with
    status = 3n;
    winner = winner;
  } in
  s


let place_bet (param, storage : place_bet_param * race_storage) : race_storage =
  let bet: betting = {
    race_id = param.race_id;
    horse_id = param.horse_id;
    payout = param.payout;
    amount = 10000mutez;
  } in
  let updated_bettings : betting_ledger =
    Big_map.update (Tezos.get_sender()) (Some bet) storage.bettings in  
  let s = { storage with bettings = updated_bettings; } in
  s


let race_main (param, storage : race_param * race_storage) 
    : (operation list) * race_storage =
  match param with

  | Ready_race p ->
    let s = ready_race (p, storage) in
    (([]: operation list), s)
    
  | Start_race -> 
    let s = start_race (storage) in
    (([]: operation list), s)

  | Finish_race winner ->
    let s = finish_race (winner, storage) in
    (([]: operation list), s)

  | Place_bet p ->
    let s = place_bet (p, storage) in
    (([]: operation list), s)

#endif