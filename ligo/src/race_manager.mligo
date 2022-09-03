#if !RACE_MANAGER
#define RACE_MANAGER

type race_storage = {
  race_id : int;
  status : int;
  winner : int;
  start_time : timestamp;
}

type race_manager = 
  | Start_race
  | Finish_race of int


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

let race_manager (param, storage : race_param * race_storage) 
    : (operation list) * race_storage =
  match param with
  | Start_race -> 
    let s = start_race (storage) in
    (([]: operation list), s)

  | Finish_race winner ->
    let s = finish_race (winner, storage) in
    (([]: operation list), s)

#endif