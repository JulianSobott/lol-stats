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
              <h2 class="page-title">Home</h2>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row g-4">
            <div class="col-12">
              <div class="card-tabs">
                <div class="card">
                  <div class="card-body">
                    <div class="empty">
                      <div class="empty-img"></div>
                      <div class="mb-2">
                        <p class="empty-title">Welcome to LOL-Stats.de</p>
                        <p class="empty-subtitle text-muted">
                          Lol-Stats is a web application designed specifically for active "League of Legends" players. Its main functionality lies in the calculation and mediation of statistics
                          statistics that are collected during the game rounds. The statistics are not just usual, simple data, but rather special achievements. 
                          Lol-Stats also offers the possibility to compare these achievements with those of other players. You can also add certain players as competitors to compare with them more often.
                          Moreover, you can compare with the entire group of selected competitors and the global list of players.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="container-xl mt-4">
          <div class="row g-4">
            <div
              v-for="item in challenges.challenges"
              :key="item.challenge"
              class="col-12 col-lg-4"
            >
              <div class="card h-100">
                <div class="card-header">
                  <h3 class="card-title">{{ item.name }}</h3>
                </div>
                <table class="table card-table table-vcenter">
                  <thead>
                    <tr>
                      <th class="w-1">No</th>
                      <th>Player</th>
                      <th class="text-center">AVG</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(player, index) in item.players"
                      :key="player.id"
                    >
                      <td>{{ index + 1 }}</td>
                      <td class="p-0">
                        <div class="d-flex px-3 align-items-center">
                          <span
                            class="avatar avatar-xs avatar-rounded"
                            :style="championIconPath(player.player_icon_path)"
                          ></span>
                          <div class="flex-fill">
                            <div class="font-weight-medium m-2">
                              <span>
                                <NuxtLink :to="'/profiles/' + player.id" class="text-white">{{ player.name }}</NuxtLink>
                              </span>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td class="text-center">{{ formatFloat(player.value) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-12">
              <div class="text-center">
                <button class="btn btn-primary" @click="fetchRandomStats()">
                  <span>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="icon icon-tabler icon-tabler-dice-5"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      stroke-width="2"
                      stroke="currentColor"
                      fill="none"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                      <rect x="4" y="4" width="16" height="16" rx="2"></rect>
                      <circle
                        cx="8.5"
                        cy="8.5"
                        r=".5"
                        fill="currentColor"
                      ></circle>
                      <circle
                        cx="15.5"
                        cy="8.5"
                        r=".5"
                        fill="currentColor"
                      ></circle>
                      <circle
                        cx="15.5"
                        cy="15.5"
                        r=".5"
                        fill="currentColor"
                      ></circle>
                      <circle
                        cx="8.5"
                        cy="15.5"
                        r=".5"
                        fill="currentColor"
                      ></circle>
                      <circle
                        cx="12"
                        cy="12"
                        r=".5"
                        fill="currentColor"
                      ></circle>
                    </svg>
                  </span>
                  Fetch Stats
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  mounted() {
    this.fetchRandomStats()
  },
  data() {
    return {
      challenges: {},
    }
  },
  methods: {
    formatFloat(value) {
      return Math.trunc(value * 1000) / 1000
    },
    championIconPath(path) {
      return `background-image: url("${path}");`
    },
    async fetchRandomStats() {
      try {
        const response = await this.$axios.get(`/achievements/leaderboards`)
        this.challenges = response.data
      } catch (err) {
        console.log(err)
      }
    },
  },
}
</script>
