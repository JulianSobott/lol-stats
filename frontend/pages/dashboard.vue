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
                    <div class="progress-bar bg-lime" style="width: 38%" role="progressbar" aria-valuenow="38" aria-valuemin="0" aria-valuemax="100" aria-label="38% Complete">
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
                  <div class="progress progress-sm">
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
                    {{ playerData.rank.tier }} {{ playerData.rank.division }}
                  </div>
                  <div class="text-muted">
                    {{ playerData.rank.league_points }}
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
                            :style="mostPlayedIconPath(champion)"
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
                      <tr v-for="index in 10" :key="index">
                        <td class="text-muted">{{ index }}</td>
                        <td><span class="text-green">WIN</span></td>
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
                                  v-for="index in 5"
                                  :key="index"
                                >
                                  <span
                                    class="avatar avatar-xs avatar-rounded ml-1"
                                    style="
                                      background-image: url(https://placekitten.com/32/32);
                                    "
                                  ></span>
                                </div>
                              </div>
                              <div>
                                <div
                                  class="avatar avatar-rounded"
                                  v-for="index in 5"
                                  :key="index"
                                >
                                  <span
                                    class="avatar avatar-xs avatar-rounded ml-1"
                                    style="
                                      background-image: url(https://placekitten.com/32/32);
                                    "
                                  ></span>
                                </div>
                              </div>
                            </div>
                            <div class="col-auto"></div>
                          </div>
                        </td>
                        <td>100 / 100 / 100</td>
                        <td>200</td>
                        <td>05-24-2022</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="card-footer">
                  <div class="text-center">
                    <a href="#" class="btn btn-primary ms-auto">Load More</a>
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

export default {
  name: 'IndexPage',
  computed: {
    playerData() {
      return this.$store.state.dashboard.playerData
    },
    winRateProgressStyle() {
      return `width: ${this.playerData.win_rate}%;`
    },
  },
  mounted() {
    this.getPlayerData()
  },
  data() {
    return {
      importPlayerData: true,
    }
  },
  methods: {
    ...mapActions({
      getPlayerData: 'dashboard/getPlayerData',
    }),
    mostPlayedIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
  },
}
</script>
