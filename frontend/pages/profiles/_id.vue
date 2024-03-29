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
              <div class="page-pretitle">Profile</div>
              <h2 v-if="playerData.name" class="page-title">
                <span class="pt-1">{{ playerData.name }}</span>
                <FavoriteCompetitorStar
                  :userId="$auth.user.id"
                  :competitorUuidId="playerData.id"
                />
              </h2>
              <div v-else class="placeholder col-3 mt-1"></div>
            </div>
            <div
              v-if="!playerData.imported && !isFetchingData"
              class="col-12 col-md-auto ms-auto d-print-none"
            >
              <div class="d-flex">
                <button
                  href="#"
                  class="btn btn-danger"
                  :disabled="isImportingData"
                  @click="triggerImportPlayer"
                >
                  <svg
                    v-if="!isImportingData"
                    xmlns="http://www.w3.org/2000/svg"
                    class="icon icon-tabler icon-tabler-database-import"
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
                    <ellipse cx="12" cy="6" rx="8" ry="3" />
                    <path
                      d="M4 6v8m5.009 .783c.924 .14 1.933 .217 2.991 .217c4.418 0 8 -1.343 8 -3v-6"
                    />
                    <path
                      d="M11.252 20.987c.246 .009 .496 .013 .748 .013c4.418 0 8 -1.343 8 -3v-6m-18 7h7m-3 -3l3 3l-3 3"
                    />
                  </svg>
                  <span
                    v-else
                    class="spinner-border spinner-border-sm icon icon-tabler"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  Import User
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row row-cards">
            <div
              v-if="!playerData.imported && !isFetchingData"
              class="col-md-12 col-lg-12"
            >
              <div class="card bg-danger mb-3">
                <div class="card-stamp">
                  <div class="card-stamp-icon bg-white text-primary">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="icon icon-tabler icon-tabler-database-import"
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
                      <ellipse cx="12" cy="6" rx="8" ry="3" />
                      <path
                        d="M4 6v8m5.009 .783c.924 .14 1.933 .217 2.991 .217c4.418 0 8 -1.343 8 -3v-6"
                      />
                      <path
                        d="M11.252 20.987c.246 .009 .496 .013 .748 .013c4.418 0 8 -1.343 8 -3v-6m-18 7h7m-3 -3l3 3l-3 3"
                      />
                    </svg>
                  </div>
                </div>
                <div class="card-body">
                  <h3 class="card-title">Player data is not imported!</h3>
                  <p>Click the Import Button to import the player.</p>
                  <div v-if="isImportingData" class="d-flex mb-2">
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
                  <div v-if="isImportingData" class="progress mb-2">
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
            <PlayerStatsWinrate :playerData="playerData" />
            <PlayerStatsRank :playerData="playerData" />
            <PlayerStatsMostPlayed :playerData="playerData" />
            <PlayerStatsRecentGames
              ref="recentGames"
              :playerUuid="$route.params.id"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfilePage',
  beforeRouteUpdate(to, from, next) {
    clearInterval(this.importInterval)
    next()
  },
  data() {
    return {
      playerData: {},
      isImportingData: false,
      importInterval: null,
      isFetchingData: false,
      importData: {
        import_state: 'PENDING',
        imported_games: 0,
        total_games: 0,
        imported: true,
        percentage: 100,
      },
    }
  },
  mounted() {
    this.fetchPlayerData()
    this.$refs.recentGames.fetchPlayerData()
  },
  destroyed() {
    clearInterval(this.importInterval)
  },
  methods: {
    async fetchPlayerData() {
      this.isFetchingData = true
      try {
        const response = await this.$axios.get(
          `/players/${this.$route.params.id}`
        )
        this.playerData = response.data
      } catch (e) {
        if (e.response.status === 404) {
          this.$router.push('/dashboard')
        }
      }
      this.isFetchingData = false
    },
    championIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
    triggerImportPlayer() {
      this.isImportingData = true

      this.importPlayer()
      this.importInterval = setInterval((async) => {
        this.importPlayer()
      }, 5000)
    },
    async importPlayer() {
      try {
        const response = await this.$axios.post(
          `/players/${this.$route.params.id}/import`,
          {}
        )
        this.isImportingData = true
        this.importData = response.data

        if (this.importData.imported) {
          clearInterval(this.importInterval)
          this.isImportingData = false
          this.$router.go(this.$router.currentRoute)
        }
      } catch (err) {
        console.log(err)
      }
    },
  },
}
</script>
