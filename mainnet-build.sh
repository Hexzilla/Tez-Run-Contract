cd ligo/src
rm -rf .build
mkdir -p .build

ligo compile contract tezrun.jsligo --entry-point main  > ./.build/tezrun.tz

ligo compile storage tezrun.jsligo --entry-point main '
{
    admin: ("tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq" as address),
    pending_admin: None() as option<address>,
    paused: false,
    
    race_id: 0 as nat,
    status: 0 as nat,
    winner: 0 as nat,
    ready_time: 300 as int,
    start_time: Tezos.get_now(),
    bets: list([]) as Types.ticket_list,
    rewards: Big_map.empty as Types.reward_ledger,
    
    uusd: Some("KT1XRPEPXbZK25r3Htzp2o1x7xdMMmfocKNW" as address),
}
' > ./.build/tezrun_storage.tz

