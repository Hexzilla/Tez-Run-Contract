import smartpy as sp

class Tezrun(sp.Contract):
    def __init__(self, owner):
        self.name = "Tezrun"
        self.init(
            owner = owner,
            raceState = False,
            raceId = 0,
            winner = 0,
            bets = sp.big_map(
                tvalue = sp.TMap(
                    sp.TNat, 
                    sp.TList(sp.TRecord(horseId = sp.TNat, payout = sp.TNat, amount = sp.TMutez))))
        )

    @sp.entry_point
    def startRace(self):
        sp.verify(self.is_owner(sp.sender))
        self.data.raceId += 1
        self.data.raceState = True
        self.data.winner = 0

    @sp.entry_point
    def finishRace(self, winner):
        sp.verify(self.is_owner(sp.sender))
        self.data.raceState = False
        self.data.winner = winner

    @sp.entry_point
    def placeBet(self, params):
        sp.set_type(params, sp.TRecord(raceId = sp.TNat, horseId = sp.TNat, payout = sp.TNat))      

        raceId = self.data.raceId
        sp.verify(raceId == params.raceId, "Invalid Race ID")
        sp.verify(sp.amount > sp.tez(0), "Invalid Amount")
        sp.send(self.data.owner, sp.amount)

        record = sp.record(
            horseId = params.horseId,
            payout = params.payout,
            amount = sp.amount)

        sp.if ~ self.data.bets.contains(sp.sender):
            self.data.bets[sp.sender] = { raceId: sp.list([]) }

        self.data.bets[sp.sender][raceId].push(record)

    @sp.entry_point
    def takeReward(self):
        pass

    # this is not part of the standard but can be supported through inheritance.
    def is_paused(self):
        return sp.bool(False)

    # this is not part of the standard but can be supported through inheritance.
    def is_owner(self, sender):
        return sender == self.data.owner
      

if "templates" not in __name__:
    @sp.add_test(name = "FA12")
    def test():
        scenario = sp.test_scenario()
        scenario.h1("Tezrun")

        # sp.test_account generates ED25519 key-pairs deterministically:
        admin = sp.test_account("Administrator")
        alice = sp.test_account("Alice")
        bob   = sp.test_account("Robert")

        # Let's display the accounts:
        scenario.h1("Accounts")
        scenario.show([admin, alice, bob])

        scenario.h1("Contract")
        c1 = Tezrun(admin.address)
        scenario += c1

        scenario.h1("Entry points")
        c1.startRace().run(sender = admin)
        scenario.verify(c1.data.raceId == 1)
        scenario.verify(c1.data.raceState == True)

        scenario.h1("Place Bet")
        c1.placeBet(raceId = 1, horseId = 1, payout = 3).run(sender = alice, amount = sp.tez(10))
        c1.placeBet(raceId = 1, horseId = 2, payout = 3).run(sender = alice, amount = sp.tez(20))

        winner = 2
        c1.finishRace(winner).run(sender = admin)
        scenario.verify(c1.data.raceState == False)
        scenario.verify(c1.data.winner == winner)
