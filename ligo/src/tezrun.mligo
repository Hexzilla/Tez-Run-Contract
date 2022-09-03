#include "simple_admin.mligo"
#include "race_manager.mligo"
#include "betting_manager.mligo"

type tezrun_storage = {
  admin : simple_admin_storage;
  race : race_storage;
  betting: betting_storage;
}

type tezrun_param =
  | Admin of simple_admin
  | Race of race_param
  | Betting of betting_param


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

  | Betting p ->
    let ops, b = betting_main (p, storage.betting) in 
    let s = { storage with betting = b; } in
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
    race_id = 0;
    status = 0;
    winner = 0;
    ready_time = 0;
    start_time = Tezos.get_now ();
  };
  betting = {
    ledger = (Big_map.empty : betting_ledger);
  };
}