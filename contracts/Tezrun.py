import smartpy as sp

class Tezrun(sp.Contract):
    def __init__(self, owner):
        self.name = "Tezrun"
        self.init(
            owner = owner,
            raceState = 0,
            startTime = sp.timestamp(0),
            raceId = 0,
            winner = 0,
            bets = sp.big_map(
                tvalue = sp.TList(
                    sp.TRecord(raceId = sp.TNat, horseId = sp.TNat, payout = sp.TNat, amount = sp.TMutez)))
        )

    @sp.entry_point
    def readyRace(self, readyTime):
        sp.verify(readyTime > 0)
        sp.verify(self.is_owner(sp.sender))        
        self.data.raceId += 1
        self.data.raceState = 1
        self.data.startTime = sp.now.add_minutes(readyTime)
        self.data.winner = 0

    @sp.entry_point
    def startRace(self):
        sp.verify(self.is_owner(sp.sender))
        sp.verify(self.data.raceState == 1)
        self.data.raceState = 2
        self.data.startTime = sp.now
        self.data.winner = 0

    @sp.entry_point
    def finishRace(self, winner):
        sp.verify(self.is_owner(sp.sender))
        sp.verify(self.data.raceState == 2)
        self.data.raceState = 0
        self.data.startTime = sp.timestamp(0)
        self.data.winner = winner

    @sp.entry_point
    def placeBet(self, params):
        sp.set_type(params, sp.TRecord(raceId = sp.TNat, horseId = sp.TNat, payout = sp.TNat))      

        sp.verify(self.data.raceState == 2, "Race is not started")
        sp.verify(self.data.raceId == params.raceId, "Invalid Race ID")
        sp.verify(sp.amount > sp.tez(0), "Invalid Amount")
        
        sp.send(self.data.owner, sp.amount)

        record = sp.record(
            raceId = self.data.raceId,
            horseId = params.horseId,
            payout = params.payout,
            amount = sp.amount)

        sp.if ~ self.data.bets.contains(sp.sender):
            self.data.bets[sp.sender] = sp.list([])

        self.data.bets[sp.sender].push(record)


    @sp.entry_point
    def takeReward(self):
        sp.verify(self.data.winner != 0)
        sp.verify(self.data.bets.contains(sp.sender))
        
        rewards = sp.local("rewards", sp.mutez(0))

        records = self.data.bets[sp.sender]
        sp.for x in records:
            sp.if x.raceId == self.data.raceId:
                sp.if x.horseId == self.data.winner:
                    rewards.value += sp.split_tokens(x.amount, x.payout, 1)

        sp.if rewards.value > sp.mutez(0):
            sp.if sp.balance > rewards.value:
                sp.send(sp.sender, rewards.value)


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
        
        admin = sp.address("tz1hmPbNNcaH91bkrYDeyAbUmYzjbPtJjPQR")#("tz1NvdDA5jtTNmRZD94ZUWP7dBwARStrQcFM")
        alice = sp.test_account("Alice")
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
        scenario.verify(sp.len(c1.data.bets[alice.address]) == 2)

        scenario.h1("Finish Race")
        winner = 2
        c1.finishRace(winner).run(sender = admin)
        scenario.verify(c1.data.raceState == 0)
        scenario.verify(c1.data.winner == winner)

        scenario.h1("Take Reward")        
        c1.takeReward().run(sender = alice)

    """@sp.add_test(name = "FA12")
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

        scenario.h1("Start Race")
        raceId = 1
        c1.startRace().run(sender = admin)
        scenario.verify(c1.data.raceId == raceId)
        scenario.verify(c1.data.raceState == True)

        scenario.h1("Place Bet")        
        c1.placeBet(raceId = raceId, horseId = 1, payout = 3).run(sender = alice, amount = sp.mutez(20))
        c1.placeBet(raceId = raceId, horseId = 2, payout = 3).run(sender = alice, amount = sp.mutez(10))
        scenario.verify(sp.len(c1.data.bets[alice.address][raceId]) == 2)

        scenario.h1("Finish Race")
        winner = 2
        c1.finishRace(winner).run(sender = admin)
        scenario.verify(c1.data.raceState == False)
        scenario.verify(c1.data.winner == winner)

        scenario.h1("Take Reward")        
        c1.takeReward().run(sender = alice, valid = False)"""