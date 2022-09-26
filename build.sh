cd ligo/src
rm -rf .build
mkdir -p .build

ligo compile contract tezrun.mligo --entry-point main  > ./.build/tezrun.tz

ligo compile storage tezrun.mligo --entry-point main '
{
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
    bettings = (Big_map.empty : betting_ledger);
  };
}
' > ./.build/tezrun_storage.tz

