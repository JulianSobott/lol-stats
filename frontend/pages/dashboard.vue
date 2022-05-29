<template>
  <div class="page">
    <ImportHeaderWarning />
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
            <div v-if="this.isImportPlayerData" class="col-md-12 col-lg-12">
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
                    Please wait, your player data is being imported and
                    calculated. Get yourself a tea or a coffee :)
                  </p>
                  <div class="d-flex mb-2">
                    <div v-if="importData.import_state == 'IMPORTING'">
                      Import: Recent matches
                      {{ importData.imported_games }} of
                      {{ importData.total_games }}
                    </div>
                    <div v-if="importData.import_state == 'PENDING'">
                      Start importing data...
                    </div>
                    <div class="ms-auto">
                      <span
                        v-if="importData.import_state == 'IMPORTING'"
                        class="text-white d-inline-flex align-items-center lh-1"
                      >
                        {{ importData.percentage }}%
                      </span>
                    </div>
                  </div>
                  <div class="progress mb-2">
                    <div
                      v-if="
                        ['PENDING', 'FINISHED'].includes(
                          importData.import_state
                        )
                      "
                      class="progress-bar progress-bar-indeterminate bg-lime"
                    ></div>
                    <div
                      v-else-if="importData.import_state == 'IMPORTING'"
                      class="progress-bar bg-lime"
                      :style="{ width: importData.percentage + '%' }"
                      role="progressbar"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            <PlayerStatsWinrate :playerData="playerData"/>
            <PlayerStatsRank :playerData="playerData"/>
            <PlayerStatsMostPlayed :playerData="playerData"/>
            <div class="col-12">
              <h3 class="mb-3">Recent Games</h3>
              <div class="card">
                <div class="table-responsive">
                  <table class="table table-vcenter card-table">
                    <thead>
                      <tr>
                        <th class="w-1">Victory</th>
                        <th class="text-center">Champion</th>
                        <th class="text-center">Teammates</th>
                        <th class="text-center">KDA</th>
                        <th class="text-center">Duration</th>
                        <th class="text-center">Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="game in recentGames" :key="game.match_id">
                        <td>
                          <strong v-if="game.win" class="text-green"
                            >Victory</strong
                          >
                          <strong v-else class="text-red">Defeat</strong>
                        </td>
                        <td class="text-center">
                          <span
                            class="avatar avatar-s avatar-rounded m-1"
                            :style="championIconPath(game.self.champion)"
                          ></span>
                          <span class="text-muted d-block">{{
                            game.self.champion.name
                          }}</span>
                        </td>
                        <td>
                          <div class="row">
                            <div class="col-12 col-sm-6">
                              <TeamList :match="game" :team="game.ally_team" />
                            </div>
                            <div class="col-12 col-sm-6">
                              <TeamList :match="game" :team="game.enemy_team" />
                            </div>
                          </div>
                        </td>
                        <td class="text-center">
                          {{ game.self.stats.kills }} /
                          {{ game.self.stats.deaths }} /
                          {{ game.self.stats.assists }}
                        </td>
                        <td class="text-center">
                          {{ converDuration(game.duration) }}
                        </td>
                        <td class="text-center">
                          {{ converTimestamp(game.timestamp) }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="card-footer">
                  <div class="text-center">
                    <button
                      class="btn btn-primary ms-auto"
                      @click="loadMoreGames()"
                      :disabled="!getNextRecentGamesLink()"
                    >
                      <span
                        v-if="moreGamesLoading"
                        class="spinner-border spinner-border-sm icon icon-tabler"
                        role="status"
                        aria-hidden="true"
                      ></span>
                      <svg
                        v-else
                        xmlns="http://www.w3.org/2000/svg"
                        class="icon icon-tabler icon-tabler-refresh"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        stroke-width="2"
                        stroke="currentColor"
                        fill="none"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <path
                          stroke="none"
                          d="M0 0h24v24H0z"
                          fill="none"
                        ></path>
                        <path
                          d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4"
                        ></path>
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
import { mapActions, mapGetters } from 'vuex'
import moment from 'moment'

export default {
  name: 'IndexPage',
  middleware: ['auth', 'settings'],
  computed: {
    playerData() {
      return this.$store.state.dashboard.playerData
    },
    recentGames() {
      return this.$store.state.dashboard.recentGames
    },
  },
  mounted() {
    this.fetchUserData()
    this.clearRecentGames()
    if (this.$auth.user.player_stats.imported) {
      this.getPlayerData()
      this.getRecentGames()
    } else {
      this.isImportingData = true
      this.importPlayerData()
      this.importInterval = setInterval((async) => {
        this.importPlayerData()
      }, 5000)
    }
  },
  destroyed() {
    clearInterval(this.importInterval)
  },
  data() {
    return {
      isImportPlayerData: false,
      moreGamesLoading: false,
      importInterval: null,
      importData: {
        import_state: 'PENDING',
        imported_games: 0,
        total_games: 0,
        imported: true,
        percentage: 100,
      },
    }
  },
  methods: {
    ...mapGetters({
      getNextRecentGamesLink: 'dashboard/getNextRecentGamesLink',
    }),
    ...mapActions({
      getPlayerData: 'dashboard/getPlayerData',
      getRecentGames: 'dashboard/getRecentGames',
      loadMoreRecentGames: 'dashboard/loadMoreRecentGames',
      clearRecentGames: 'dashboard/clearRecentGames',
    }),
    championIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
    async importPlayerData() {
      try {
        const response = await this.$axios.post(
          `/players/${this.$auth.user.player_uuid}/import`,
          {}
        )
        this.importData = response.data

        if (this.importData.imported) {
          clearInterval(this.importInterval)
          this.isImportingData = false
          this.$router.go(this.$router.currentRoute)
          // send request to show all data
        }
      } catch (err) {
        console.log(err)
      }
    },
    async fetchUserData() {
      await this.$auth.fetchUser()
      this.isImportPlayerData = !this.$auth.user.player_stats.imported
    },
    converTimestamp(value) {
      return moment(String(value)).format('MM-DD-YYYY')
    },
    converDuration(secs) {
      return moment.utc(secs * 1000).format('mm:ss')
    },
    async loadMoreGames() {
      try {
        this.moreGamesLoading = true
        await this.loadMoreRecentGames()
        this.moreGamesLoading = false
      } catch (e) {
        console.log(e)
      }
    },
  },
}
</script>
