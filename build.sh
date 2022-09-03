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
    race_id = 0;
    status = 0;
    winner = 0;
    start_time = Tezos.get_now ();
  };
}
' > ./.build/tezrun_storage.tz

