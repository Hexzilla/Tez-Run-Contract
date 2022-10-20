cd ligo/src/.build

tezos-client originate contract Tezrun transferring 0.00001 from tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq \
running tezrun.tz \
--force \
--init '
(Pair (Pair (Pair (Pair "tz1bxwduvRwBhq59FmThGKD5ceDFadr57JTq" False) None 0)
            (Pair 300 {})
            "1970-01-01T00:00:59Z"
            0)
      (Pair {} (Some "KT1XRPEPXbZK25r3Htzp2o1x7xdMMmfocKNW"))
      0)
' \
--burn-cap 1.1165