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
              <h2 class="page-title">{{ playerData.name }}</h2>
            </div>
            <div
              v-if="!playerData.imported"
              class="col-12 col-md-auto ms-auto d-print-none"
            >
              <div class="d-flex">
                <button href="#" class="btn btn-danger" @click="importPlayerData" :disabled="isImportingData">
                  <svg v-if="!isImportingData"
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
            <PlayerStatsWinrate :playerData="playerData" />
            <PlayerStatsRank :playerData="playerData"/>
            <PlayerStatsMostPlayed :playerData="playerData"/>
            <PlayerStatsRecentGames ref="recentGames" :playerUuid="this.$route.params.id" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfilePage',
  mounted() {
    this.fetchPlayerData()
    this.$refs.recentGames.fetchPlayerData()
  },
  data() {
    return {
      playerData: {},
      isImportingData: false,
    }
  },
  methods: {
    async fetchPlayerData() {
      const response = await this.$axios.get(
        `/players/${this.$route.params.id}`
      )
      this.playerData = response.data
    },
    championIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
    async importPlayerData() {
      try {
        const response = await this.$axios.post(
          `/players/${this.$route.params.id}/import`,
          {}
        )
        this.isImportingData = true
        this.importData = response.data

        if (this.importData.imported) {
          this.isImportingData = false
          // send request to show all data
        }
      } catch (err) {
        console.log(err)
      }
    },
  },
}
</script>
