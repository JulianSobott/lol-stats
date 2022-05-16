import json
import random
import string
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models.player import Player
from player_api.db import Champions, Summoners, Base, Games
from player_api.models.factories import PlayerModelFactory

DEFAULT_GAME_LENGTH = 30


class PlayerFactory:
    def __init__(self, db: Session):
        self.db = db
        self.players: list["Testplayer"] = []

    def player(self) -> "PlayerFactory":
        self.players.append(Testplayer(self.db))
        return self

    def n_players(self, num_players: int) -> "PlayerFactory":
        self.players.extend(Testplayer(self.db) for i in range(num_players))
        return self

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        objects = []
        for player in self.players:
            objects.append(player.summoner)
            for game in player.games:
                objects.append(game)
        self.db.bulk_save_objects(objects)
        self.db.commit()

    def __getitem__(self, item):
        return self.players[item]

    def __iter__(self):
        for player in self.players:
            yield player


class Testplayer:
    def __init__(self, db: Session, **kwargs):
        self.db = db
        self.player: Player = PlayerModelFactory.build(**kwargs)
        self.games_factories: list[GamesFactory] = []

    def play_n_games(self, num_games: int) -> "GamesFactory":
        factory = GamesFactory(self.db, self).with_n_games(num_games)
        self.games_factories.append(factory)
        return factory

    @property
    def summoner(self):
        return Summoners(
            puuid=self.player.id,
            name=self.player.name,
            level=self.player.level,
            icon_path=self.player.player_icon_path,
            last_update=datetime.now(),
            tier=self.player.rank.tier,
            division=self.player.rank.division_str,
            league_points=self.player.rank.league_points,
        )

    @property
    def name(self):
        return self.player.name

    @property
    def games(self):
        objects = []
        for factory in self.games_factories:
            objects.extend(factory.games)
        return objects


class GamesFactory:
    def __init__(self, db: Session, player: Testplayer):
        self.db = db
        self.num_games = 0
        self.champion = "Aatrox"
        self.won = 0
        self.player = player
        self.start = datetime.now() - timedelta(days=7)

    def with_n_games(self, num_games: int) -> "GamesFactory":
        self.num_games = num_games
        return self

    def starting_at(self, start: datetime) -> "GamesFactory":
        self.start = start
        return self

    def with_champion(self, champion: str) -> "GamesFactory":
        self.champion = champion
        return self

    def win(self, num_games: int):
        if num_games > self.num_games:
            raise ValueError(
                f"Won more games than played. {self.num_games=} won={num_games}"
            )
        self.won = num_games
        return self

    @property
    def games(self):
        objects = []
        available_won = self.won

        for i in range(self.num_games):
            if available_won == 0:
                won = False
            else:
                won = True
                available_won -= 1
            objects.append(
                Games(
                    match_id=random_name(),
                    summoner_id=self.player.summoner.puuid,
                    champ_id=Champion(self.db, self.champion).id,
                    start_time=self.start + timedelta(minutes=i * DEFAULT_GAME_LENGTH),
                    duration=timedelta(minutes=DEFAULT_GAME_LENGTH).total_seconds(),
                    win=won,
                    lane="bottom",
                    team="red",
                    stats=json.dumps(
                        {
                            "-damageSelfMitigated": 7032,
                            "-largestCriticalStrike": 506,
                            "-magicDamageDealt": 24260,
                            "-magicDamageDealtToChampions": 1474,
                            "-magicDamageTaken": 7062,
                            "-physicalDamageDealt": 83191,
                            "-physicalDamageDealtToChampions": 6535,
                            "-physicalDamageTaken": 10580,
                            "-totalDamageDealt": 116887,
                            "-totalDamageDealtToChampions": 9531,
                            "-totalDamageTaken": 17776,
                            "-trueDamageDealt": 9435,
                            "-trueDamageDealtToChampions": 1521,
                            "-trueDamageTaken": 133,
                            "damagePerMinute": 327.23765452306037,
                            "damageTakenOnTeamPercentage": 0.16427365853437548,
                            "teamDamagePercentage": 0.10242491893231571,
                            "-doubleKills": 0,
                            "-killingSprees": 2,
                            "-largestKillingSpree": 3,
                            "-largestMultiKill": 1,
                            "-pentaKills": 0,
                            "-quadraKills": 0,
                            "-tripleKills": 0,
                            "12AssistStreakCount": 0,
                            "acesBefore15Minutes": 0,
                            "doubleAces": 0,
                            "flawlessAces": 1,
                            "fullTeamTakedown": 0,
                            "legendaryCount": 0,
                            "multiKillOneSpell": 0,
                            "multikills": 0,
                            "multikillsAfterAggressiveFlash": 0,
                            "elderDragonMultikills": 0,
                            "-spell2Casts": 20,
                            "-spell1Casts": 22,
                            "-spell3Casts": 20,
                            "-spell4Casts": 5,
                            "-summoner1Casts": 3,
                            "-summoner2Casts": 2,
                            "abilityUses": 67,
                            "dodgeSkillShotsSmallWindow": 13,
                            "landSkillShotsEarlyGame": 5,
                            "quickCleanse": 0,
                            "skillshotsDodged": 7,
                            "skillshotsHit": 19,
                            "snowballsHit": 0,
                            "-timeCCingOthers": 3,
                            "-totalDamageShieldedOnTeammates": 0,
                            "-totalHeal": 2043,
                            "-totalHealsOnTeammates": 0,
                            "-totalTimeCCDealt": 16,
                            "-totalUnitsHealed": 1,
                            "effectiveHealAndShielding": 0,
                            "enemyChampionImmobilizations": 5,
                            "immobilizeAndKillWithAlly": 1,
                            "knockEnemyIntoTeamAndKill": 1,
                            "saveAllyFromDeath": 0,
                            "getTakedownsInAllLanesEarlyJungleAsLaner": 0,
                            "junglerTakedownsNearDamagedEpicMonster": 0,
                            "killAfterHiddenWithAlly": 0,
                            "killedChampTookFullTeamDamageSurvived": 0,
                            "killsNearEnemyTurret": 2,
                            "killsOnLanersEarlyJungleAsJungler": 0,
                            "killsOnOtherLanesEarlyJungleAsLaner": 0,
                            "killsOnRecentlyHealedByAramPack": 0,
                            "killsUnderOwnTurret": 0,
                            "killsWithHelpFromEpicMonster": 0,
                            "-nexusKills": 0,
                            "-nexusTakedowns": 1,
                            "outnumberedKills": 0,
                            "outnumberedNexusKill": 0,
                            "pickKillWithAlly": 6,
                            "quickSoloKills": 0,
                            "soloKills": 0,
                            "takedowns": 8,
                            "takedownsAfterGainingLevelAdvantage": 0,
                            "takedownsBeforeJungleMinionSpawn": 0,
                            "takedownsFirst25Minutes": 0,
                            "takedownsInAlcove": 0,
                            "takedownsInEnemyFountain": 0,
                            "junglerKillsEarlyJungle": 0,
                            "-assists": 1,
                            "-deaths": 6,
                            "-firstBloodAssist": False,
                            "-firstBloodKill": False,
                            "-kills": 7,
                            "bountyGold": 0,
                            "deathsByEnemyChamps": 6,
                            "kda": 1.3333333333333333,
                            "killParticipation": 0.25,
                            "maxKillDeficit": 6,
                            "maxLevelLeadLaneOpponent": 1,
                            "outerTurretExecutesBefore10Minutes": 0,
                            "survivedSingleDigitHpCount": 1,
                            "survivedThreeImmobilizesInFight": 0,
                            "tookLargeDamageSurvived": 0,
                            "-damageDealtToBuildings": 8232,
                            "-damageDealtToObjectives": 12524,
                            "-damageDealtToTurrets": 8232,
                            "-firstTowerAssist": False,
                            "-firstTowerKill": False,
                            "-inhibitorKills": 0,
                            "-inhibitorTakedowns": 1,
                            "-inhibitorsLost": 0,
                            "-objectivesStolen": 0,
                            "-objectivesStolenAssists": 0,
                            "-turretKills": 2,
                            "-turretTakedowns": 5,
                            "-turretsLost": 3,
                            "baronTakedowns": 1,
                            "dragonTakedowns": 1,
                            "elderDragonKillsWithOpposingSoul": 0,
                            "epicMonsterKillsNearEnemyJungler": 0,
                            "epicMonsterKillsWithin30SecondsOfSpawn": 0,
                            "epicMonsterSteals": 0,
                            "epicMonsterStolenWithoutSmite": 0,
                            "kTurretsDestroyedBeforePlatesFall": 0,
                            "multiTurretRiftHeraldCount": 0,
                            "perfectDragonSoulsTaken": 0,
                            "quickFirstTurret": 0,
                            "riftHeraldTakedowns": 0,
                            "soloBaronKills": 0,
                            "soloTurretsLategame": 1,
                            "takedownOnFirstTurret": 0,
                            "teamBaronKills": 1,
                            "teamElderDragonKills": 0,
                            "teamRiftHeraldKills": 0,
                            "turretPlatesTaken": 2,
                            "turretTakedowns": 5,
                            "turretsTakenWithRiftHerald": 0,
                            "-champLevel": 15,
                            "-gameEndedInEarlySurrender": 0,
                            "-gameEndedInSurrender": 0,
                            "-longestTimeSpentLiving": 456,
                            "-teamEarlySurrendered": 0,
                            "-totalTimeSpentDead": 180,
                            "gameLength": 1747.688579886358,
                            "perfectGame": 0,
                            "blastConeOppositeOpponentCount": 0,
                            "completeSupportQuestInTime": 0,
                            "dancedWithRiftHerald": 0,
                            "hadAfkTeammate": 0,
                            "hadOpenNexus": 0,
                            "moreEnemyJungleThanOpponent": -123.50000008940697,
                            "poroExplosions": 0,
                            "unseenRecalls": 0,
                            "-consumablesPurchased": 6,
                            "-goldEarned": 11587,
                            "-goldSpent": 9550,
                            "-itemsPurchased": 25,
                            "earlyLaningPhaseGoldExpAdvantage": 0,
                            "goldPerMinute": 397.8182554240922,
                            "laningPhaseGoldExpAdvantage": 0,
                            "-visionScore": 11,
                            "-visionWardsBought": 1,
                            "-wardsKilled": 0,
                            "-wardsPlaced": 6,
                            "controlWardsPlaced": 0,
                            "stealthWardsPlaced": 5,
                            "threeWardsOneSweeperCount": 0,
                            "viChampion.cache[name]sionScoreAdvantageLaneOpponent": -0.2218838930130005,
                            "visionScorePerMinute": 0.3787263810293082,
                            "wardTakedowns": 0,
                            "wardTakedownsBefore20M": 0,
                            "wardsGuarded": 0,
                            "-neutralMinionsKilled": 12,
                            "-totalMinionsKilled": 163,
                            "alliedJungleMonsterKills": 8.000000029802322,
                            "buffsStolen": 0,
                            "enemyJungleMonsterKills": 4.000000029802322,
                            "initialBuffCount": 0,
                            "initialCrabCount": 0,
                            "jungleCsBefore10Minutes": 0,
                            "laneMinionsFirst10Minutes": 53,
                            "maxCsAdvantageOnLaneOpponent": 11.000000059604645,
                            "scuttleCrabKills": 0,
                            "twentyMinionsIn3SecondsCount": 0,
                        },
                    ),
                    challenges="",
                )
            )
        return objects


class Champion:

    def __new__(cls, db: Session, name, *args, **kwargs) -> Champions:
        res = db.query(Champions).where(Champions.name == name).all()
        if res:
            return res[0]

        champ = Champions(
            id=random.randint(0, 50000),
            name=name,
            icon_path=f"https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/{name}.png",
        )
        db.add(champ)
        db.commit()
        db.refresh(champ)
        # champ = db.session.query(Champions).where(Champions.name == name).all()[0]
        return champ


def random_name():
    return "".join(
        random.choice(string.ascii_letters) for _ in range(random.randint(5, 10))
    )
