<template>
  <div class="page">
    <PageHeader />
    <PageNavigation />
    <div class="page-wrapper">
      <div class="container-xl">
        <!-- Page title -->
        <div class="page-header d-print-none">
          <div class="row align-items-center">
            <div class="col">
              <!-- Page pre-title -->
              <h2 class="page-title">Dashboard</h2>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row row-cards">
            <div v-if="importPlayerData" class="col-md-12 col-lg-12">
              <div class="card bg-primary mb-3">
                <div class="card-stamp">
                  <div class="card-stamp-icon bg-white text-primary">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="icon icon-tabler icon-tabler-coffee"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      stroke-width="2"
                      stroke="currentColor"
                      fill="none"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                      <path
                        d="M3 14c.83 .642 2.077 1.017 3.5 1c1.423 .017 2.67 -.358 3.5 -1c.83 -.642 2.077 -1.017 3.5 -1c1.423 -.017 2.67 .358 3.5 1"
                      />
                      <path d="M8 3a2.4 2.4 0 0 0 -1 2a2.4 2.4 0 0 0 1 2" />
                      <path d="M12 3a2.4 2.4 0 0 0 -1 2a2.4 2.4 0 0 0 1 2" />
                      <path
                        d="M3 10h14v5a6 6 0 0 1 -6 6h-2a6 6 0 0 1 -6 -6v-5z"
                      />
                      <path d="M16.746 16.726a3 3 0 1 0 .252 -5.555" />
                    </svg>
                  </div>
                </div>
                <div class="card-body">
                  <h3 class="card-title">
                    Your player data is being imported!
                  </h3>
                  <p>
                    Please wait, your player data is being imported from the
                    League of Legends database. Get yourself a tea or a coffee
                    :)
                  </p>
                  <div class="d-flex mb-2"><i>Current Status ....</i></div>
                  <div class="progress mb-2">
                    <div
                      class="progress-bar bg-lime"
                      style="width: 38%"
                      role="progressbar"
                      aria-valuenow="38"
                      aria-valuemin="0"
                      aria-valuemax="100"
                      aria-label="38% Complete"
                    >
                      <span class="visually-hidden">38% Complete</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-sm-4 col-lg-4">
              <div v-if="playerData" class="card h-100">
                <div class="card-body">
                  <div class="d-flex align-items-center">
                    <div class="subheader">Winrate</div>
                  </div>
                  <div class="h1 mb-3">{{ playerData.win_rate }}%</div>
                  <div class="d-flex mb-2">
                    <div>Winrate</div>
                  </div>
                  <div class="progress">
                    <div
                      class="progress-bar bg-blue"
                      :style="winRateProgressStyle"
                      role="progressbar"
                    ></div>
                  </div>
                </div>
              </div>
              <div v-else>
                <div class="col">
                  <div class="placeholder placeholder-xs col-9"></div>
                  <div class="placeholder placeholder-xs col-7"></div>
                </div>
              </div>
            </div>
            <div class="col-sm-4 col-lg-4">
              <div v-if="playerData.rank" class="card h-100">
                <div class="card-body text-center">
                  <div class="mb-3">
                    <span
                      class="avatar avatar-xl avatar-rounded"
                      style="
                        background-image: url(https://opgg-static.akamaized.net/images/medals/bronze_4.png?image=q_auto&image=q_auto,f_webp,w_auto&v=1651226741046);
                      "
                    ></span>
                  </div>
                  <div class="card-title mb-1">
                    {{ playerData.rank.tier.toUpperCase() }}
                    {{ playerData.rank.division }}
                  </div>
                  <div class="text-muted">
                    League Points: {{ playerData.rank.league_points }}
                  </div>
                  <div class="text-muted">
                    Leve: {{ playerData.level }}
                  </div>
                </div>
              </div>
              <div v-else class="card h-100">
                <div class="card-body py-3 text-center">
                  <div>
                    <div
                      class="avatar avatar-rounded avatar-lg placeholder mb-3"
                    ></div>
                  </div>
                  <div class="mt w-75 mx-auto">
                    <div class="placeholder col-9 mb-3"></div>
                    <div class="placeholder placeholder-xs col-10"></div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-sm-4 col-lg-4">
              <div class="card h-100">
                <div class="card-header">
                  <h3 class="card-title">Most Played</h3>
                </div>
                <table class="table card-table table-vcenter">
                  <thead>
                    <tr>
                      <th>Champion</th>
                      <th class="text-center">Winrate</th>
                      <th class="text-center">Games</th>
                    </tr>
                  </thead>
                  <tbody v-if="playerData">
                    <tr
                      v-for="champion in playerData.most_played"
                      :key="champion.champion_id"
                    >
                      <td class="p-0">
                        <div class="d-flex px-3 align-items-center">
                          <span
                            class="avatar avatar-xs avatar-rounded"
                            :style="championIconPath(champion)"
                          ></span>
                          <div class="flex-fill">
                            <div class="font-weight-medium m-2">
                              <span>{{ champion.champion_name }}</span>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td class="text-center">{{ champion.win_rate }} %</td>
                      <td class="text-center">{{ champion.games }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-12">
              <h3 class="mb-3">Recent Games</h3>
              <div class="card">
                <div class="table-responsive">
                  <table class="table table-vcenter card-table">
                    <thead>
                      <tr>
                        <th class="w-1">ID</th>
                        <th class="w-1">Victory</th>
                        <th>Champion</th>
                        <th>Teammates</th>
                        <th>KDA</th>
                        <th>Playing time</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="game in recentGames.items"
                        :key="game.match_id"
                      >
                        <td class="text-muted">{{ game.match_id }}</td>
                        <td>
                          <span>{{ game.victorious_team.toUpperCase() }}</span>
                        </td>
                        <td>
                          <span
                            class="avatar avatar-s avatar-rounded m-1"
                            style="
                              background-image: url(https://placekitten.com/48/48);
                            "
                          ></span>
                        </td>
                        <td>
                          <div class="row align-items-center">
                            <div class="col">
                              <div>
                                <div
                                  class="avatar avatar-rounded"
                                  v-for="player in game.ally_team"
                                  :key="player.id"
                                >
                                  <span
                                    class="avatar avatar-xs avatar-rounded ml-1"
                                    :style="championIconPath(player.champion)"
                                  ></span>
                                </div>
                              </div>
                              <div>
                                <div
                                  class="avatar avatar-rounded"
                                  v-for="player in game.enemy_team"
                                  :key="player.id"
                                >
                                  <span
                                    class="avatar avatar-xs avatar-rounded ml-1"
                                    :style="championIconPath(player.champion)"
                                  ></span>
                                </div>
                              </div>
                            </div>
                            <div class="col-auto"></div>
                          </div>
                        </td>
                        <td>100 / 100 / 100</td>
                        <td>{{ game.duration }}</td>
                        <td>{{ converTimestamp(game.timestamp) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="card-footer">
                  <div class="text-center">
                    <button
                      class="btn btn-primary ms-auto"
                      @click="loadMoreGames(recentGames.next)"
                    >
                      <span v-if="moreGamesLoading"  class="spinner-border spinner-border-sm icon icon-tabler" role="status" aria-hidden="true"></span>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-refresh" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4"></path>
                        <path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"></path>
                      </svg>
                      Load More
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import moment from 'moment'

export default {
  name: 'IndexPage',
  middleware: ['auth', 'settings'],
  computed: {
    playerData() {
      return this.$store.state.dashboard.playerData
    },
    winRateProgressStyle() {
      return `width: ${this.playerData.win_rate}%;`
    },
  },
  mounted() {
    if (this.$route.query.welcome !== undefined) {
      this.fetchUserData()
    }
    this.getPlayerData()
    this.getRecentGames()
  },
  data() {
    return {
      importPlayerData: true,
      moreGamesLoading: false,
      recentGames: {
        items: [
          {
            match_id: 'LnKDk',
            victorious_team: 'red',
            ally_team: [
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'vyRHLQqqyODzzVHnrGqb',
                  name: 'TMbZSpeThGEfQCpsflAC',
                },
                player_stats: {
                  kda: '1.3333333333333333',
                },
              },
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'RmOyHZHwinFeHGevsowp',
                  name: 'ffKKReHSPmxqxCpEbudH',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'nZpwJnlMwkMguHPXjeYR',
                  name: 'imfvpiYSuiaqfHPGxvFU',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'HfwQDkRrDZBEMVZnKVRo',
                  name: 'vbHHdLSdbHkLhHAaYgFk',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'vfOdMKmUuBZgSheEgdKf',
                  name: 'SZrbVkwbwJwOXWlAFhWg',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
            ],
            enemy_team: [
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'YrRCpxDRcDkyGHPMsWBL',
                  name: 'yUsuPangHPrLNymNJQsn',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'RzKOthaRJpWZHFFgwFGZ',
                  name: 'rrOrxQcOHqcSURavoOcU',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'ABbiDIjQJUBYWnEltJqG',
                  name: 'SfopcBDpErBHOnKPVIKT',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'NZphUySleelcfQYfyYEQ',
                  name: 'LYzGKgkYpXbNFBgpXBlS',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
              {
                champion: {
                  name: 'Aatrox',
                  icon_path:
                    'https://ddragon.leagueoflegends.com/cdn/12.8.1/img/champion/Aatrox.png',
                },
                player: {
                  id: 'BTdFwXbapzpXwNYNVZUF',
                  name: 'OhHRYKdVuDpryEGIeeTh',
                },
                player_stats: [
                  {
                    name: '-damageSelfMitigated',
                    value: 7032.0,
                  },
                  {
                    name: '-largestCriticalStrike',
                    value: 506.0,
                  },
                  {
                    name: '-magicDamageDealt',
                    value: 24260.0,
                  },
                  {
                    name: '-magicDamageDealtToChampions',
                    value: 1474.0,
                  },
                  {
                    name: '-magicDamageTaken',
                    value: 7062.0,
                  },
                  {
                    name: '-physicalDamageDealt',
                    value: 83191.0,
                  },
                  {
                    name: '-physicalDamageDealtToChampions',
                    value: 6535.0,
                  },
                  {
                    name: '-physicalDamageTaken',
                    value: 10580.0,
                  },
                  {
                    name: '-totalDamageDealt',
                    value: 116887.0,
                  },
                  {
                    name: '-totalDamageDealtToChampions',
                    value: 9531.0,
                  },
                  {
                    name: '-totalDamageTaken',
                    value: 17776.0,
                  },
                  {
                    name: '-trueDamageDealt',
                    value: 9435.0,
                  },
                  {
                    name: '-trueDamageDealtToChampions',
                    value: 1521.0,
                  },
                  {
                    name: '-trueDamageTaken',
                    value: 133.0,
                  },
                  {
                    name: 'damagePerMinute',
                    value: 327.23765452306037,
                  },
                  {
                    name: 'damageTakenOnTeamPercentage',
                    value: 0.16427365853437548,
                  },
                  {
                    name: 'teamDamagePercentage',
                    value: 0.10242491893231571,
                  },
                  {
                    name: '-doubleKills',
                    value: 0.0,
                  },
                  {
                    name: '-killingSprees',
                    value: 2.0,
                  },
                  {
                    name: '-largestKillingSpree',
                    value: 3.0,
                  },
                  {
                    name: '-largestMultiKill',
                    value: 1.0,
                  },
                  {
                    name: '-pentaKills',
                    value: 0.0,
                  },
                  {
                    name: '-quadraKills',
                    value: 0.0,
                  },
                  {
                    name: '-tripleKills',
                    value: 0.0,
                  },
                  {
                    name: '12AssistStreakCount',
                    value: 0.0,
                  },
                  {
                    name: 'acesBefore15Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'doubleAces',
                    value: 0.0,
                  },
                  {
                    name: 'flawlessAces',
                    value: 1.0,
                  },
                  {
                    name: 'fullTeamTakedown',
                    value: 0.0,
                  },
                  {
                    name: 'legendaryCount',
                    value: 0.0,
                  },
                  {
                    name: 'multiKillOneSpell',
                    value: 0.0,
                  },
                  {
                    name: 'multikills',
                    value: 0.0,
                  },
                  {
                    name: 'multikillsAfterAggressiveFlash',
                    value: 0.0,
                  },
                  {
                    name: 'elderDragonMultikills',
                    value: 0.0,
                  },
                  {
                    name: '-spell2Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell1Casts',
                    value: 22.0,
                  },
                  {
                    name: '-spell3Casts',
                    value: 20.0,
                  },
                  {
                    name: '-spell4Casts',
                    value: 5.0,
                  },
                  {
                    name: '-summoner1Casts',
                    value: 3.0,
                  },
                  {
                    name: '-summoner2Casts',
                    value: 2.0,
                  },
                  {
                    name: 'abilityUses',
                    value: 67.0,
                  },
                  {
                    name: 'dodgeSkillShotsSmallWindow',
                    value: 13.0,
                  },
                  {
                    name: 'landSkillShotsEarlyGame',
                    value: 5.0,
                  },
                  {
                    name: 'quickCleanse',
                    value: 0.0,
                  },
                  {
                    name: 'skillshotsDodged',
                    value: 7.0,
                  },
                  {
                    name: 'skillshotsHit',
                    value: 19.0,
                  },
                  {
                    name: 'snowballsHit',
                    value: 0.0,
                  },
                  {
                    name: '-timeCCingOthers',
                    value: 3.0,
                  },
                  {
                    name: '-totalDamageShieldedOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalHeal',
                    value: 2043.0,
                  },
                  {
                    name: '-totalHealsOnTeammates',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeCCDealt',
                    value: 16.0,
                  },
                  {
                    name: '-totalUnitsHealed',
                    value: 1.0,
                  },
                  {
                    name: 'effectiveHealAndShielding',
                    value: 0.0,
                  },
                  {
                    name: 'enemyChampionImmobilizations',
                    value: 5.0,
                  },
                  {
                    name: 'immobilizeAndKillWithAlly',
                    value: 1.0,
                  },
                  {
                    name: 'knockEnemyIntoTeamAndKill',
                    value: 1.0,
                  },
                  {
                    name: 'saveAllyFromDeath',
                    value: 0.0,
                  },
                  {
                    name: 'getTakedownsInAllLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'junglerTakedownsNearDamagedEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: 'killAfterHiddenWithAlly',
                    value: 0.0,
                  },
                  {
                    name: 'killedChampTookFullTeamDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: 'killsNearEnemyTurret',
                    value: 2.0,
                  },
                  {
                    name: 'killsOnLanersEarlyJungleAsJungler',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnOtherLanesEarlyJungleAsLaner',
                    value: 0.0,
                  },
                  {
                    name: 'killsOnRecentlyHealedByAramPack',
                    value: 0.0,
                  },
                  {
                    name: 'killsUnderOwnTurret',
                    value: 0.0,
                  },
                  {
                    name: 'killsWithHelpFromEpicMonster',
                    value: 0.0,
                  },
                  {
                    name: '-nexusKills',
                    value: 0.0,
                  },
                  {
                    name: '-nexusTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'outnumberedKills',
                    value: 0.0,
                  },
                  {
                    name: 'outnumberedNexusKill',
                    value: 0.0,
                  },
                  {
                    name: 'pickKillWithAlly',
                    value: 6.0,
                  },
                  {
                    name: 'quickSoloKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloKills',
                    value: 0.0,
                  },
                  {
                    name: 'takedowns',
                    value: 8.0,
                  },
                  {
                    name: 'takedownsAfterGainingLevelAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsBeforeJungleMinionSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsFirst25Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInAlcove',
                    value: 0.0,
                  },
                  {
                    name: 'takedownsInEnemyFountain',
                    value: 0.0,
                  },
                  {
                    name: 'junglerKillsEarlyJungle',
                    value: 0.0,
                  },
                  {
                    name: '-assists',
                    value: 1.0,
                  },
                  {
                    name: '-deaths',
                    value: 6.0,
                  },
                  {
                    name: '-firstBloodAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstBloodKill',
                    value: 0.0,
                  },
                  {
                    name: '-kills',
                    value: 7.0,
                  },
                  {
                    name: 'bountyGold',
                    value: 0.0,
                  },
                  {
                    name: 'deathsByEnemyChamps',
                    value: 6.0,
                  },
                  {
                    name: 'kda',
                    value: 1.3333333333333333,
                  },
                  {
                    name: 'killParticipation',
                    value: 0.25,
                  },
                  {
                    name: 'maxKillDeficit',
                    value: 6.0,
                  },
                  {
                    name: 'maxLevelLeadLaneOpponent',
                    value: 1.0,
                  },
                  {
                    name: 'outerTurretExecutesBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'survivedSingleDigitHpCount',
                    value: 1.0,
                  },
                  {
                    name: 'survivedThreeImmobilizesInFight',
                    value: 0.0,
                  },
                  {
                    name: 'tookLargeDamageSurvived',
                    value: 0.0,
                  },
                  {
                    name: '-damageDealtToBuildings',
                    value: 8232.0,
                  },
                  {
                    name: '-damageDealtToObjectives',
                    value: 12524.0,
                  },
                  {
                    name: '-damageDealtToTurrets',
                    value: 8232.0,
                  },
                  {
                    name: '-firstTowerAssist',
                    value: 0.0,
                  },
                  {
                    name: '-firstTowerKill',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorKills',
                    value: 0.0,
                  },
                  {
                    name: '-inhibitorTakedowns',
                    value: 1.0,
                  },
                  {
                    name: '-inhibitorsLost',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolen',
                    value: 0.0,
                  },
                  {
                    name: '-objectivesStolenAssists',
                    value: 0.0,
                  },
                  {
                    name: '-turretKills',
                    value: 2.0,
                  },
                  {
                    name: '-turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: '-turretsLost',
                    value: 3.0,
                  },
                  {
                    name: 'baronTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'dragonTakedowns',
                    value: 1.0,
                  },
                  {
                    name: 'elderDragonKillsWithOpposingSoul',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsNearEnemyJungler',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterKillsWithin30SecondsOfSpawn',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterSteals',
                    value: 0.0,
                  },
                  {
                    name: 'epicMonsterStolenWithoutSmite',
                    value: 0.0,
                  },
                  {
                    name: 'kTurretsDestroyedBeforePlatesFall',
                    value: 0.0,
                  },
                  {
                    name: 'multiTurretRiftHeraldCount',
                    value: 0.0,
                  },
                  {
                    name: 'perfectDragonSoulsTaken',
                    value: 0.0,
                  },
                  {
                    name: 'quickFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'riftHeraldTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'soloBaronKills',
                    value: 0.0,
                  },
                  {
                    name: 'soloTurretsLategame',
                    value: 1.0,
                  },
                  {
                    name: 'takedownOnFirstTurret',
                    value: 0.0,
                  },
                  {
                    name: 'teamBaronKills',
                    value: 1.0,
                  },
                  {
                    name: 'teamElderDragonKills',
                    value: 0.0,
                  },
                  {
                    name: 'teamRiftHeraldKills',
                    value: 0.0,
                  },
                  {
                    name: 'turretPlatesTaken',
                    value: 2.0,
                  },
                  {
                    name: 'turretTakedowns',
                    value: 5.0,
                  },
                  {
                    name: 'turretsTakenWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: '-champLevel',
                    value: 15.0,
                  },
                  {
                    name: '-gameEndedInEarlySurrender',
                    value: 0.0,
                  },
                  {
                    name: '-gameEndedInSurrender',
                    value: 0.0,
                  },
                  {
                    name: '-longestTimeSpentLiving',
                    value: 456.0,
                  },
                  {
                    name: '-teamEarlySurrendered',
                    value: 0.0,
                  },
                  {
                    name: '-totalTimeSpentDead',
                    value: 180.0,
                  },
                  {
                    name: 'gameLength',
                    value: 1747.688579886358,
                  },
                  {
                    name: 'perfectGame',
                    value: 0.0,
                  },
                  {
                    name: 'blastConeOppositeOpponentCount',
                    value: 0.0,
                  },
                  {
                    name: 'completeSupportQuestInTime',
                    value: 0.0,
                  },
                  {
                    name: 'dancedWithRiftHerald',
                    value: 0.0,
                  },
                  {
                    name: 'hadAfkTeammate',
                    value: 0.0,
                  },
                  {
                    name: 'hadOpenNexus',
                    value: 0.0,
                  },
                  {
                    name: 'moreEnemyJungleThanOpponent',
                    value: -123.50000008940697,
                  },
                  {
                    name: 'poroExplosions',
                    value: 0.0,
                  },
                  {
                    name: 'unseenRecalls',
                    value: 0.0,
                  },
                  {
                    name: '-consumablesPurchased',
                    value: 6.0,
                  },
                  {
                    name: '-goldEarned',
                    value: 11587.0,
                  },
                  {
                    name: '-goldSpent',
                    value: 9550.0,
                  },
                  {
                    name: '-itemsPurchased',
                    value: 25.0,
                  },
                  {
                    name: 'earlyLaningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: 'goldPerMinute',
                    value: 397.8182554240922,
                  },
                  {
                    name: 'laningPhaseGoldExpAdvantage',
                    value: 0.0,
                  },
                  {
                    name: '-visionScore',
                    value: 11.0,
                  },
                  {
                    name: '-visionWardsBought',
                    value: 1.0,
                  },
                  {
                    name: '-wardsKilled',
                    value: 0.0,
                  },
                  {
                    name: '-wardsPlaced',
                    value: 6.0,
                  },
                  {
                    name: 'controlWardsPlaced',
                    value: 0.0,
                  },
                  {
                    name: 'stealthWardsPlaced',
                    value: 5.0,
                  },
                  {
                    name: 'threeWardsOneSweeperCount',
                    value: 0.0,
                  },
                  {
                    name: 'viChampion.cache[name]sionScoreAdvantageLaneOpponent',
                    value: -0.2218838930130005,
                  },
                  {
                    name: 'visionScorePerMinute',
                    value: 0.3787263810293082,
                  },
                  {
                    name: 'wardTakedowns',
                    value: 0.0,
                  },
                  {
                    name: 'wardTakedownsBefore20M',
                    value: 0.0,
                  },
                  {
                    name: 'wardsGuarded',
                    value: 0.0,
                  },
                  {
                    name: '-neutralMinionsKilled',
                    value: 12.0,
                  },
                  {
                    name: '-totalMinionsKilled',
                    value: 163.0,
                  },
                  {
                    name: 'alliedJungleMonsterKills',
                    value: 8.000000029802322,
                  },
                  {
                    name: 'buffsStolen',
                    value: 0.0,
                  },
                  {
                    name: 'enemyJungleMonsterKills',
                    value: 4.000000029802322,
                  },
                  {
                    name: 'initialBuffCount',
                    value: 0.0,
                  },
                  {
                    name: 'initialCrabCount',
                    value: 0.0,
                  },
                  {
                    name: 'jungleCsBefore10Minutes',
                    value: 0.0,
                  },
                  {
                    name: 'laneMinionsFirst10Minutes',
                    value: 53.0,
                  },
                  {
                    name: 'maxCsAdvantageOnLaneOpponent',
                    value: 11.000000059604645,
                  },
                  {
                    name: 'scuttleCrabKills',
                    value: 0.0,
                  },
                  {
                    name: 'twentyMinionsIn3SecondsCount',
                    value: 0.0,
                  },
                ],
              },
            ],
            duration: 1800,
            timestamp: '2000-01-02T00:00:00',
          },
        ],
        "next": "/players/TMbZSpeThGEfQCpsflAC/recent-games?start_before=2000-01-01T00%3A00%3A00&limit=5"
      },
    }
  },
  methods: {
    ...mapActions({
      getPlayerData: 'dashboard/getPlayerData',
      getRecentGames: 'dashboard/getRecentGames',
    }),
    championIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
    async fetchUserData() {
      await this.$auth.fetchUser()
    },
    converTimestamp(value) {
      return moment(String(value)).format('MM-DD-YYYY')
    },
    async loadMoreGames(link) {
      console.log(link)
      try {
        this.moreGamesLoading = true
        await this.$axios.get(link);
        this.moreGamesLoading = false
      } catch (e) {
        console.log(e)
      }
    }
  },
}
</script>
