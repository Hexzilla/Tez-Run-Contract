cd ligo/src
mkdir .build

ligo compile contract tezrun.mligo --entry-point tezrun  > ./.build/tezrun.tz

ligo compile storage tezrun.mligo --entry-point tezrun '
{
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
' > ./.build/tezrun_storage.tz

