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
                <a href="#" class="btn btn-danger" @click="importPlayerData">
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
                  Import User
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row row-cards">
            <PlayerStatsWinrate :playerData="playerData" />
            <div class="col-sm-4 col-lg-4">
              <div
                v-if="playerData.rank !== undefined && playerData.rank != null"
                class="card h-100"
              >
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
                  <div class="text-muted">Level: {{ playerData.level }}</div>
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
            </div>
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
    console.log(
      'Page mounted... fetching user with ID: ' + this.$route.params.id
    )
    this.fetchPlayerData()
  },
  data() {
    return {
      playerData: {},
      isImportingData: false
    }
  },
  methods: {
    championIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
    async fetchPlayerData() {
      const response = await this.$axios.get(
        `/players/${this.$route.params.id}`
      )
      this.playerData = response.data
    },
    async importPlayerData() {
      try {
        const response = await this.$axios.post(
          `/players/${this.$route.params.id}/import`,
          {}
        )
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
