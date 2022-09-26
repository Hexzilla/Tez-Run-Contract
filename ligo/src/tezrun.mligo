#include "simple_admin.mligo"
#include "race_manager.mligo"

type tezrun_storage = {
  admin : simple_admin_storage;
  race : race_storage;
}

type tezrun_param =
  | Admin of simple_admin
  | Race of race_param


let main (param, storage : tezrun_param * tezrun_storage)
    : (operation list) * tezrun_storage =
  match param with
  | Admin p ->  
    let ops, admin = simple_admin (p, storage.admin) in
    let s = { storage with admin = admin; } in
    (ops, s)

  | Race p ->
    let _ = fail_if_not_admin storage.admin in
    let ops, race = race_main (p, storage.race) in 
    let s = { storage with race = race; } in
    (ops, s)


(**
This is a sample initial fa2_multi_asset storage.
 *)

let store : tezrun_storage = {
  admin = {
    admin = ("tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq" : address);
    pending_admin = (None : address option);
    paused = false;
  };
  race = {
    race_id = 0n;
    status = 0n;
    winner = 0n;
    ready_time = 0n;
    start_time = Tezos.get_now ();
    bettings = ([] : betting_list);
    rewards = (Big_map.empty : reward_ledger);
  };
}