type admin_storage = {
  admin : address;
  paused : bool;
}

type race_storage = {
  race_id : nat;
  state : nat;
  winner : nat;
  start_time : timestamp;
}

type betting_storage = {
  race_id : nat;
  horse_id : nat;
  payout : nat;
  amount : nat;
}  

type tezrun_storage = {
  admin : admin_storage;
  race : race_storage;
  betting : betting_storage;
}

(* `simple_admin` entry points *)
type simple_admin =
  | Set_admin of address
  | Confirm_admin of unit
  | Pause of bool

type tezrun_param =
  | Admin of simple_admin

let tezrun_main
    (param, s : tezrun_param * tezrun_storage)
    : (operation list) * multi_asset_storage =
  match param with
  | Admin p ->
      let 