class Handler(object):
    def Binary(self):
        print "bin"
        pass

    def Error(self, msg):
        pass

    def Hello(self, nick, pkey, client, clientVer, octgnVer, gameId, gameVersion):
        print "hello", gameId
        pass

    def Settings(self, twoSidedTable):
        pass

    def PlayerSettings(self, playerId, invertedTable):
        pass

    def NickReq(self, nick):
        pass

    def Start(self):
        pass

    def ResetReq(self):
        pass

    def NextTurn(self, nextPlayer):
        pass

    def StopTurnReq(self, turnNumber, stop):
        pass

    def ChatReq(self, text):
        pass

    def PrintReq(self, text):
        pass

    def RandomReq(self, id, min, max):
        pass

    def RandomAnswer1Req(self, id, value):
        pass

    def RandomAnswer2Req(self, id, value):
        pass

    def CounterReq(self, counter, value):
        pass

    def LoadDeck(self, id, type, group):
        pass

    def CreateCard(self, id, type, group):
        pass

    def CreateCardAt(self, id, key, modelId, x, y, faceUp, persist):
        pass

    def CreateAlias(self, id, type):
        pass

    def MoveCardReq(self, card, group, idx, faceUp):
        pass

    def MoveCardAtReq(self, card, x, y, idx, faceUp):
        pass

    def Reveal(self, card, revealed, guid):
        pass

    def RevealToReq(self, sendTo, revealTo, card, encrypted):
        pass

    def PeekReq(self, card):
        pass

    def UntargetReq(self, card):
        pass

    def TargetReq(self, card):
        pass

    def TargetArrowReq(self, card, otherCard):
        pass

    def Highlight(self, card, color):
        pass

    def TurnReq(self, card, up):
        pass

    def RotateReq(self, card, rot):
        pass

    def Shuffle(self, group, card):
        pass

    def Shuffled(self, group, card, pos):
        pass

    def UnaliasGrp(self, group):
        pass

    def Unalias(self, card, type):
        pass

    def AddMarkerReq(self, card, id, name, count):
        pass

    def RemoveMarkerReq(self, card, id, name, count):
        pass

    def SetMarkerReq(self, card, id, name, count):
        pass

    def TransferMarkerReq(self, from_, to, id, name, count):
        pass

    def PassToReq(self, id, to, requested):
        pass

    def TakeFromReq(self, id, from_):
        pass

    def DontTakeReq(self, id, to):
        pass

    def FreezeCardsVisibility(self, group):
        pass

    def GroupVisReq(self, group, defined, visible):
        pass

    def GroupVisAddReq(self, group, who):
        pass

    def GroupVisRemoveReq(self, group, who):
        pass

    def LookAtReq(self, uid, group, look):
        pass

    def LookAtTopReq(self, uid, group, count, look):
        pass

    def LookAtBottomReq(self, uid, group, count, look):
        pass

    def StartLimitedReq(self, packs):
        pass

    def CancelLimitedReq(self):
        pass

