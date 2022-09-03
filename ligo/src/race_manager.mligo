#if !RACE_MANAGER
#define RACE_MANAGER

type race_storage = {
  race_id : nat;
  status : nat;
  winner : nat;
  ready_time: nat;
  start_time : timestamp;
}

type race_param = 
  | Ready_race of nat
  | Start_race
  | Finish_race of nat


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

#endif