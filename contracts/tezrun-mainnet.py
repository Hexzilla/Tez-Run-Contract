import smartpy as sp

class Constants:
    ADMINISTRATOR = "tz1LFGoM2YyYekx1NwnNKGajzY4ZC2Cr6CPp"
    CONTRACT_UUSD = "KT1XRPEPXbZK25r3Htzp2o1x7xdMMmfocKNW"
    TOKEN_UUSD = 1


class Tezrun(sp.Contract):
    def __init__(self, admin):
        self.name = "Tezrun"
        self.init(
            admin = admin,
            raceState = 2,
            startTime = sp.timestamp(0),
            raceId = 1,
            winner = 0,
            bets = sp.big_map(tvalue = sp.TList(
                sp.TRecord(
                    raceId = sp.TNat,
                    horseId = sp.TNat,
                    payout = sp.TNat,
                    amount = sp.TMutez,
                    token = sp.TNat,
                    tokenAmount = sp.TNat,
                    rewarded = sp.TBool
                )
            )),
        )

    @sp.entry_point
    def readyRace(self, readyTime):
        sp.verify(readyTime > 0)
        sp.verify(self.is_admin(sp.sender))        
        self.data.raceId += 1
        self.data.raceState = 1
        self.data.startTime = sp.now.add_minutes(readyTime)
        self.data.winner = 0

    @sp.entry_point
    def startRace(self):
        sp.verify(self.is_admin(sp.sender))
        sp.verify(self.data.raceState == 1)
        self.data.raceState = 2
        self.data.startTime = sp.now
        self.data.winner = 0

    @sp.entry_point
    def finishRace(self, winner):
        sp.verify(self.is_admin(sp.sender))
        sp.verify(self.data.raceState == 2)
        self.data.raceState = 3
        self.data.startTime = sp.timestamp(0)
        self.data.winner = winner

    @sp.entry_point
    def placeBet(self, params):
        sp.set_type(params, sp.TRecord(raceId = sp.TNat, horseId = sp.TNat, payout = sp.TNat))

        sp.verify(self.data.raceState == 2, "Race is not started")
        sp.verify(self.data.raceId == params.raceId, "Invalid Race ID")
        sp.verify(sp.amount > sp.tez(0), "Invalid Amount")

        sp.send(self.data.admin, sp.amount)

        record = sp.record(
            raceId = self.data.raceId,
            horseId = params.horseId,
            payout = params.payout,
            amount = sp.amount,
            token = 0,
            tokenAmount = 0,
            rewarded = sp.bool(False)
        )
        self.addBet(record)


    @sp.entry_point
    def placeBetByToken(self, params):
        sp.set_type(params, sp.TRecord(raceId = sp.TNat, horseId = sp.TNat, payout = sp.TNat, token = sp.TNat, amount = sp.TNat))

        sp.verify(self.data.raceState == 2, "Race is not started")
        sp.verify(self.data.raceId == params.raceId, "Invalid Race ID")
        sp.verify(params.token == Constants.TOKEN_UUSD, "Invalid Token")
        sp.verify(params.amount > 0, "Invalid Amount")

        c = sp.contract(
            t_transfer_params,
            sp.address(Constants.CONTRACT_UUSD),
            entry_point = "transfer"
        ).open_some()

        sp.transfer(
            [
                sp.record(
                    from_=sp.sender,
                    txs=[sp.record(to_=sp.self_address, amount=params.amount, token_id=0)],
                ),
            ]
            sp.mutez(0),
            c
        )

        record = sp.record(
            raceId = self.data.raceId,
            horseId = params.horseId,
            payout = params.payout,
            amount = sp.mutez(0),
            token = params.token,
            tokenAmount = params.amount,
            rewarded = sp.bool(False)
        )
        self.addBet(record)
        

    def addBet(self, record):
        sp.if ~ self.data.bets.contains(sp.sender):
            self.data.bets[sp.sender] = sp.list([])

        self.data.bets[sp.sender].push(record)


    @sp.entry_point
    def takeReward(self):
        sp.verify(self.data.raceState == 3, "Race is not finished")
        sp.verify(self.data.winner != 0)
        sp.verify(self.data.bets.contains(sp.sender))

        rewards = sp.local("rewards", sp.mutez(0))
        tokens = sp.local("tokens", 0)

        sp.for bet in self.data.bets[sp.sender]:
            sp.if self.is_rewardable(bet):
                sp.if self.is_token(bet):
                    tokens.value += (bet.tokenAmount * bet.payout)
                sp.if bet.amount > sp.mutez(0):
                    rewards.value += sp.split_tokens(bet.amount, bet.payout, 1)

        sp.if rewards.value > sp.mutez(0):
            sp.if sp.balance > rewards.value:
                sp.send(sp.sender, rewards.value)
                self.updateRewarded(sp.sender)

        sp.if tokens.value > 0:
            c = sp.contract(
                t_transfer_params,
                sp.address(Constants.CONTRACT_UUSD),
                entry_point = "transfer"
            ).open_some()

            sp.transfer(
                [
                    sp.record(
                        from_=sp.self_address,
                        txs=[sp.record(to_=sp.sender, amount=tokens.value, token_id=0)],
                    ),
                ]
                sp.mutez(0),
                c
            )
            
            self.updateTokenRewarded(sp.sender)


    def updateRewarded(self, address):
        sp.for bet in self.data.bets[address]:
            sp.if (self.is_rewardable(bet)) & (bet.amount > sp.mutez(0)):
                bet.rewarded = sp.bool(True)

    def updateTokenRewarded(self, address):
        sp.for bet in self.data.bets[address]:
            sp.if (self.is_rewardable(bet)) & (self.is_token(bet)):
                bet.rewarded = sp.bool(True)


    def is_token(self, bet):
        sp.if (bet.token == Constants.TOKEN_UUSD) & (bet.tokenAmount > 0):
            return sp.bool(True)
        return sp.bool(False) 


    def is_winner(self, bet):
        sp.if (bet.raceId == self.data.raceId) & (bet.horseId == self.data.winner):
            return sp.bool(True)
        return sp.bool(False)


    def is_rewardable(self, bet):
        sp.if self.is_winner(bet):
            sp.if ~ bet.rewarded:
                return sp.bool(True)
        return sp.bool(False)

    # this is not part of the standard but can be supported through inheritance.
    def is_paused(self):
        return sp.bool(False)

    # this is not part of the standard but can be supported through inheritance.
    def is_admin(self, sender):
        return sender == self.data.admin


t_transfer_batch = sp.TRecord(
    from_=sp.TAddress,
    txs=sp.TList(
        sp.TRecord(
            to_=sp.TAddress,
            token_id=sp.TNat,
            amount=sp.TNat,
        ).layout(("to_", ("token_id", "amount")))
    ),
).layout(("from_", "txs"))

t_transfer_params = sp.TList(t_transfer_batch)


if "templates" not in __name__:
    @sp.add_test(name = "FA12")
    def test():
        scenario = sp.test_scenario()
        scenario.h1("Tezrun")
        
        admin = sp.address(Constants.ADMINISTRATOR)
        alice = sp.address("tz1NvdDA5jtTNmRZD94ZUWP7dBwARStrQcFM")
        bob   = sp.test_account("Robert")

        c1 = Tezrun(admin)
        scenario += c1

        scenario.h1("Contract")
        c1 = Tezrun(admin)
        scenario += c1

        scenario.h1("Ready Race")
        raceId = 1
        c1.readyRace(1).run(sender = admin)
        scenario.verify(c1.data.raceId == raceId)
        scenario.verify(c1.data.raceState == 1)

        scenario.h1("Start Race")
        c1.startRace().run(sender = admin)
        scenario.verify(c1.data.raceId == raceId)
        scenario.verify(c1.data.raceState == 2)

        scenario.h1("Place Bet")        
        c1.placeBet(raceId = raceId, horseId = 1, payout = 3).run(sender = alice, amount = sp.mutez(20))
        c1.placeBet(raceId = raceId, horseId = 2, payout = 3).run(sender = alice, amount = sp.mutez(10))
        scenario.verify(sp.len(c1.data.bets[alice]) == 2)

        scenario.h1("Place Bet by Token")
        c1.placeBetByToken(raceId = raceId, horseId = 1, payout = 3, token = Constants.TOKEN_UUSD, amount = 10).run(sender = alice)

        scenario.h1("Finish Race")
        winner = 2
        c1.finishRace(winner).run(sender = admin)
        scenario.verify(c1.data.raceState == 3)
        scenario.verify(c1.data.winner == winner)

        scenario.h1("Take Reward")        
        c1.takeReward().run(sender = alice)


    sp.add_compilation_target(
        "Tezrun",
        Tezrun(sp.address(Constants.ADMINISTRATOR))
    )
