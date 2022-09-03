#if !RACE_MANAGER
#define RACE_MANAGER

type race_storage = {
  race_id : int;
  status : int;
  winner : int;
  ready_time: int;
  start_time : timestamp;
}

type race_param = 
  | Ready_race of int
  | Start_race
  | Finish_race of int


let ready_race (ready_time, storage : int * race_storage) : race_storage =
  let new_race_id = 1 + storage.race_id in
  let s = { storage with
    race_id = new_race_id;
    status = 1;
    winner = 0;
    ready_time = ready_time;
  } in
  s

let start_race (storage : race_storage) : race_storage =
  let s = { storage with
    status = 2;
    winner = 0;
    start_time = Tezos.get_now ();
  } in
  s

let finish_race (winner, storage : int * race_storage) : race_storage = 
  let s = { storage with
    status = 3;
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