cd ligo/src
rm -rf .build
mkdir -p .build

ligo compile contract tezrun.jsligo --entry-point main  > ./.build/tezrun.tz

ligo compile storage tezrun.jsligo --entry-point main '
{
  admin: {
    admin: ("tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq" as address),
    pending_admin: None() as option<address>,
    paused: false,
  },
  race: {
    race_id: 0 as nat,
    status: 0 as nat,
    winner: 0 as nat,
    start_time: Tezos.get_now(),
    bets: list([]) as Types.bet_list,
    rewards: Big_map.empty as Types.reward_ledger
  }
}
' > ./.build/tezrun_storage.tz

