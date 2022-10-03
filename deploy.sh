cd ligo/src/.build

tezos-client originate contract Tezrun transferring 10.0 from tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq \
running tezrun.tz \
--force \
--init '
(Pair (Pair (Pair "tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq" False) None)
      (Pair (Pair {} 0) 300 {})
      (Pair "1970-01-01T00:00:59Z" 0)
      0)
' \
--burn-cap 1.1165