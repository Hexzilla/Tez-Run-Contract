#include "simple_admin.mligo"
#include "race_manager.mligo"

type tezrun_storage = {
  admin : simple_admin_storage;
  race : race_manager;
}

type tezrun_param =
  | Admin of simple_admin
  | Race of race_manager


let main (param, storage : tezrun_param * tezrun_storage)
    : (operation list) * multi_asset_storage =
  match param with
  | Admin p ->  
    let ops, admin = simple_admin (p, storage.admin) in
    let s = { storage with admin = admin; } in
    (ops, s)

  | Race p ->
    let _ = fail_if_not_admin storage.admin in
    let ops, s = race_manager (p, storage) in 
    (ops, s)


(**
This is a sample initial fa2_multi_asset storage.
 *)

let store : tezrun_storage = {
  admin = {
    admin = ("tz1YPSCGWXwBdTncK2aCctSZAXWvGsGwVJqU" : address);
    pending_admin = (None : address option);
    paused = false;
  };
  race = {
    race_id = 0;
    status = 0;
    winner = 0;
    start_time = Tezos.get_now ();
  };
}