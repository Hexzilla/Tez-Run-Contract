cd ligo/src/.build

tezos-client originate contract Tezrun transferring 0.0001 from tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq \
running multi_asset_main.tz \
--force \
--init '
(Pair (Pair (Pair "tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq" False) None)
      (Pair 0 "1970-01-01T00:00:59Z")
      0
      0)
' \
--burn-cap 1.1165