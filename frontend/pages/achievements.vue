<template>
  <div class="page">
    <ImportHeaderWarning />
    <PageHeader />
    <PageNavigation />
    <div class="page-wrapper">
      <div class="container-xl">
        <div class="page-header d-print-none">
          <div class="row g-2 align-items-center">
            <div class="col">
              <!-- Page pre-title -->
              <h2 class="page-title">Achievements</h2>
            </div>
            <!-- Page title actions -->
            <div class="col-auto col-md-auto ms-auto d-print-none">
              <div class="btn-list">
                <a
                  class="btn btn-primary d-sm-none btn-icon"
                  data-bs-toggle="offcanvas"
                  href="#achivement-filters"
                  role="button"
                  aria-controls="achivement-filters"
                  aria-label="Open Filters"
                >
                  <!-- Download SVG icon from http://tabler-icons.io/i/plus -->
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="icon icon-tabler icon-tabler-filter"
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
                    <path
                      d="M5.5 5h13a1 1 0 0 1 .5 1.5l-5 5.5l0 7l-4 -3l0 -4l-5 -5.5a1 1 0 0 1 .5 -1.5"
                    ></path>
                  </svg>
                </a>
              </div>
            </div>
            <div class="col-auto col-md-auto ms-auto d-print-none">
              <button class="btn btn-primary d-sm-inline-block btn-icon" @click="fetchAchievements()">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-refresh" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4"></path>
                  <path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
        <!-- Page title -->
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row g-4">
            <div class="col-3 col-achievements-filter">
              <AchievementFilters @filterApplied="filterApplied" />
            </div>
            <div class="col-9 col-achivements-table">
              <div v-if="!loadingAchiements" class="card-tabs">
                <div v-if="achievements.length == 0" class="card">
                  <div class="card-body">
                      <div class="empty">
                        <div class="empty-img">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            data-name="Layer 1"
                            height="128"
                            viewBox="0 0 647.63626 632.17383"
                            xmlns:xlink="http://www.w3.org/1999/xlink"
                          >
                            <path
                              d="M687.3279,276.08691H512.81813a15.01828,15.01828,0,0,0-15,15v387.85l-2,.61005-42.81006,13.11a8.00676,8.00676,0,0,1-9.98974-5.31L315.678,271.39691a8.00313,8.00313,0,0,1,5.31006-9.99l65.97022-20.2,191.25-58.54,65.96972-20.2a7.98927,7.98927,0,0,1,9.99024,5.3l32.5498,106.32Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#f2f2f2"
                            />
                            <path
                              d="M725.408,274.08691l-39.23-128.14a16.99368,16.99368,0,0,0-21.23-11.28l-92.75,28.39L380.95827,221.60693l-92.75,28.4a17.0152,17.0152,0,0,0-11.28028,21.23l134.08008,437.93a17.02661,17.02661,0,0,0,16.26026,12.03,16.78926,16.78926,0,0,0,4.96972-.75l63.58008-19.46,2-.62v-2.09l-2,.61-64.16992,19.65a15.01489,15.01489,0,0,1-18.73-9.95l-134.06983-437.94a14.97935,14.97935,0,0,1,9.94971-18.73l92.75-28.4,191.24024-58.54,92.75-28.4a15.15551,15.15551,0,0,1,4.40966-.66,15.01461,15.01461,0,0,1,14.32032,10.61l39.0498,127.56.62012,2h2.08008Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#3f3d56"
                            />
                            <path
                              d="M398.86279,261.73389a9.0157,9.0157,0,0,1-8.61133-6.3667l-12.88037-42.07178a8.99884,8.99884,0,0,1,5.9712-11.24023l175.939-53.86377a9.00867,9.00867,0,0,1,11.24072,5.9707l12.88037,42.07227a9.01029,9.01029,0,0,1-5.9707,11.24072L401.49219,261.33887A8.976,8.976,0,0,1,398.86279,261.73389Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#00b0ff"
                            />
                            <circle
                              cx="190.15351"
                              cy="24.95465"
                              r="20"
                              fill="#00b0ff"
                            />
                            <circle
                              cx="190.15351"
                              cy="24.95465"
                              r="12.66462"
                              fill="#fff"
                            />
                            <path
                              d="M878.81836,716.08691h-338a8.50981,8.50981,0,0,1-8.5-8.5v-405a8.50951,8.50951,0,0,1,8.5-8.5h338a8.50982,8.50982,0,0,1,8.5,8.5v405A8.51013,8.51013,0,0,1,878.81836,716.08691Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#e6e6e6"
                            />
                            <path
                              d="M723.31813,274.08691h-210.5a17.02411,17.02411,0,0,0-17,17v407.8l2-.61v-407.19a15.01828,15.01828,0,0,1,15-15H723.93825Zm183.5,0h-394a17.02411,17.02411,0,0,0-17,17v458a17.0241,17.0241,0,0,0,17,17h394a17.0241,17.0241,0,0,0,17-17v-458A17.02411,17.02411,0,0,0,906.81813,274.08691Zm15,475a15.01828,15.01828,0,0,1-15,15h-394a15.01828,15.01828,0,0,1-15-15v-458a15.01828,15.01828,0,0,1,15-15h394a15.01828,15.01828,0,0,1,15,15Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#3f3d56"
                            />
                            <path
                              d="M801.81836,318.08691h-184a9.01015,9.01015,0,0,1-9-9v-44a9.01016,9.01016,0,0,1,9-9h184a9.01016,9.01016,0,0,1,9,9v44A9.01015,9.01015,0,0,1,801.81836,318.08691Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#00b0ff"
                            />
                            <circle
                              cx="433.63626"
                              cy="105.17383"
                              r="20"
                              fill="#00b0ff"
                            />
                            <circle
                              cx="433.63626"
                              cy="105.17383"
                              r="12.18187"
                              fill="#fff"
                            />
                          </svg>
                        </div>
                        <div class="mb-2">
                          <p class="empty-title">No Data</p>
                          <p class="empty-subtitle text-muted">
                            There is no player data in our system that could be compared to your filter.
                            Please try another filter.
                          </p>
                        </div>
                      </div>
                    </div>
                </div>
                <!-- Cards navigation -->
                <ul class="nav nav-tabs" style="background: #1e293b; border-top-left-radius: 5px; border-top-right-radius: 5px">
                  <li
                    v-for="item in achievements"
                    :key="item.category"
                    class="nav-item nav-item-tab"
                  >
                    <a
                      :href="getTabIdRef(item.category)"
                      class="nav-link"
                      :class="{ active: item.category === 'Favourites' }"
                      data-bs-toggle="tab"
                      >{{ item.category }}</a
                    >
                  </li>
                </ul>
                <div v-if="showImportPlayerModal" class="tab-content">
                  <div id="tab-favorites" class="card show active">
                    <div class="card-body">
                      <div class="empty">
                        <div class="empty-img">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            data-name="Layer 1"
                            height="128"
                            viewBox="0 0 647.63626 632.17383"
                            xmlns:xlink="http://www.w3.org/1999/xlink"
                          >
                            <path
                              d="M687.3279,276.08691H512.81813a15.01828,15.01828,0,0,0-15,15v387.85l-2,.61005-42.81006,13.11a8.00676,8.00676,0,0,1-9.98974-5.31L315.678,271.39691a8.00313,8.00313,0,0,1,5.31006-9.99l65.97022-20.2,191.25-58.54,65.96972-20.2a7.98927,7.98927,0,0,1,9.99024,5.3l32.5498,106.32Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#f2f2f2"
                            />
                            <path
                              d="M725.408,274.08691l-39.23-128.14a16.99368,16.99368,0,0,0-21.23-11.28l-92.75,28.39L380.95827,221.60693l-92.75,28.4a17.0152,17.0152,0,0,0-11.28028,21.23l134.08008,437.93a17.02661,17.02661,0,0,0,16.26026,12.03,16.78926,16.78926,0,0,0,4.96972-.75l63.58008-19.46,2-.62v-2.09l-2,.61-64.16992,19.65a15.01489,15.01489,0,0,1-18.73-9.95l-134.06983-437.94a14.97935,14.97935,0,0,1,9.94971-18.73l92.75-28.4,191.24024-58.54,92.75-28.4a15.15551,15.15551,0,0,1,4.40966-.66,15.01461,15.01461,0,0,1,14.32032,10.61l39.0498,127.56.62012,2h2.08008Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#3f3d56"
                            />
                            <path
                              d="M398.86279,261.73389a9.0157,9.0157,0,0,1-8.61133-6.3667l-12.88037-42.07178a8.99884,8.99884,0,0,1,5.9712-11.24023l175.939-53.86377a9.00867,9.00867,0,0,1,11.24072,5.9707l12.88037,42.07227a9.01029,9.01029,0,0,1-5.9707,11.24072L401.49219,261.33887A8.976,8.976,0,0,1,398.86279,261.73389Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#00b0ff"
                            />
                            <circle
                              cx="190.15351"
                              cy="24.95465"
                              r="20"
                              fill="#00b0ff"
                            />
                            <circle
                              cx="190.15351"
                              cy="24.95465"
                              r="12.66462"
                              fill="#fff"
                            />
                            <path
                              d="M878.81836,716.08691h-338a8.50981,8.50981,0,0,1-8.5-8.5v-405a8.50951,8.50951,0,0,1,8.5-8.5h338a8.50982,8.50982,0,0,1,8.5,8.5v405A8.51013,8.51013,0,0,1,878.81836,716.08691Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#e6e6e6"
                            />
                            <path
                              d="M723.31813,274.08691h-210.5a17.02411,17.02411,0,0,0-17,17v407.8l2-.61v-407.19a15.01828,15.01828,0,0,1,15-15H723.93825Zm183.5,0h-394a17.02411,17.02411,0,0,0-17,17v458a17.0241,17.0241,0,0,0,17,17h394a17.0241,17.0241,0,0,0,17-17v-458A17.02411,17.02411,0,0,0,906.81813,274.08691Zm15,475a15.01828,15.01828,0,0,1-15,15h-394a15.01828,15.01828,0,0,1-15-15v-458a15.01828,15.01828,0,0,1,15-15h394a15.01828,15.01828,0,0,1,15,15Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#3f3d56"
                            />
                            <path
                              d="M801.81836,318.08691h-184a9.01015,9.01015,0,0,1-9-9v-44a9.01016,9.01016,0,0,1,9-9h184a9.01016,9.01016,0,0,1,9,9v44A9.01015,9.01015,0,0,1,801.81836,318.08691Z"
                              transform="translate(-276.18187 -133.91309)"
                              fill="#00b0ff"
                            />
                            <circle
                              cx="433.63626"
                              cy="105.17383"
                              r="20"
                              fill="#00b0ff"
                            />
                            <circle
                              cx="433.63626"
                              cy="105.17383"
                              r="12.18187"
                              fill="#fff"
                            />
                          </svg>
                        </div>
                        <div class="mb-2">
                          <p class="empty-title">Player not imported</p>
                          <p class="empty-subtitle text-muted">
                            There is no player data in our system yet. To be
                            able to compare you with the player, please click
                            the button below import the player.
                          </p>
                        </div>
                        <div class="w-100">
                          <div class="mb-2 text-center">
                            <div class="d-flex">
                              <div
                                v-if="importData.import_state == 'IMPORTING'"
                              >
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
                                  class="text-green d-inline-flex align-items-center lh-1"
                                >
                                  {{ importData.percentage }}%
                                </span>
                              </div>
                            </div>
                          </div>
                          <div v-if="importData" class="progress mb-2">
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
                              role="progressbar"
                              class="progress-bar bg-lime"
                              :style="{ width: importData.percentage + '%' }"
                            ></div>
                          </div>
                        </div>
                        <div class="empty-action">
                          <a
                            href="#"
                            class="btn btn-primary"
                            :class="{ disabled: isImportingData }"
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
                              <path
                                stroke="none"
                                d="M0 0h24v24H0z"
                                fill="none"
                              />
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
                            Import Player
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="tab-content">  
                  <div
                    v-for="item in achievements"
                    :id="getTabId(item.category)"
                    class="card tab-pane"
                    :key="item.category"
                    :class="{ 'show active': item.category === 'Favourites' }"
                  >
                    <div class="table-responsive">
                      <table
                        class="table card-table table-vcenter text-nowrap datatable"
                      >
                        <thead>
                          <tr>
                            <th>Achievement</th>
                            <th>You (Max / Average / Sum)</th>
                            <th>Other (Max / Average / Sum)</th>
                            <th class="w-1"></th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="achievement in item.achievements"
                            :key="achievement.name"
                          >
                            <td><strong>{{ achievement.description }}</strong></td>
                            <td>
                              <span :class="getCompareColor(achievement.you.max.compare)">{{ formatFloat(achievement.you.max.value) }}</span>
                              <span class="text-muted">/</span>
                              <span :class="getCompareColor(achievement.you.avg.compare)">{{ formatFloat(achievement.you.avg.value) }}</span>
                              <span class="text-muted">/</span>
                              <span :class="getCompareColor(achievement.you.total.compare)">{{ formatFloat(achievement.you.total.value) }}</span>
                            </td>
                            <td>
                              <span :class="getCompareColor(achievement.other.max.compare)">{{ formatFloat(achievement.other.max.value) }}</span>
                              <span class="text-muted">/</span>
                              <span :class="getCompareColor(achievement.other.avg.compare)">{{ formatFloat(achievement.other.avg.value) }}</span>
                              <span class="text-muted">/</span>
                              <span :class="getCompareColor(achievement.other.total.compare)">{{ formatFloat(achievement.other.total.value) }}</span>
                            </td>
                            <td>
                              <FavoriteAchivementStar
                                :userId="$auth.user.id"
                                :achivementId="achievement.name"
                                :initState="achievement.fav"
                              />
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <div class="card-footer d-flex align-items-center"></div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center">
                <div class="spinner-border text-light" role="status">
                </div>
                <p class="card-title mt-1">Loading Achievements...</p>
              </div>
            </div>
          </div>
        </div>
        <SidebarAchievementFilters @filterApplied="filterApplied" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AchievementsPage',
  beforeRouteUpdate(to, from, next) {
    clearInterval(this.importInterval)
    next()
  },
  middleware: ['auth', 'settings'],
  data() {
    return {
      showImportPlayerModal: false,
      isImportingData: false,
      selectedPlayerUuid: null,
      requiresImport: false,
      importData: {
        imported_games: 0,
        total_games: 0,
        imported: false,
        percentage: 100,
      },
      importInterval: null,
      achievements: [],
      loadingAchiements: false,
    }
  },
  mounted() {
    if (this.$route.query.import !== undefined) {
      this.showImportPlayerModal = this.$route.query.import === 'true'
    } else {
      this.showImportPlayerModal = false
    }

    if (this.$route.query.player_name === undefined) {
      this.fetchAchievements()
    }
  },
  destroyed() {
    clearInterval(this.importInterval)
  },
  methods: {
    getCompareColor(key){
      if (key === 'WORSE') {
        return 'text-red'
      }
      if (key === 'BETTER') {
        return 'text-green'
      }
      return ''
    },
    formatFloat(value) {
      return Math.trunc(value * 1000) / 1000
    },
    getTabId(name) {
      return `tab-${name}`
    },
    getTabIdRef(name) {
      return `#tab-${name}`
    },
    async fetchAchievements() {
      this.loadingAchiements = true
      try {
        const response = await this.$axios.get(
          `/achievements?me=${this.$auth.user.id}`
        )
        this.achievements = response.data.items
      } catch (err) {
        console.log(err)
      }
      this.loadingAchiements = false
    },
    async importPlayer() {
      try {
        const response = await this.$axios.post(
          `/players/${this.selectedPlayerUuid}/import`,
          {}
        )
        this.importData = response.data

        if (this.importData.imported) {
          clearInterval(this.importInterval)
          this.isImportingData = false
          this.showImportPlayerModal = false
          // send request to show all data
        }
      } catch (err) {
        console.log(err)
      }
    },
    async toggleFavoriteAchivement(achivementId, state) {
      try {
        if (state) {
          await this.$axios.post(`/users/${this.$auth.user.id}/achievements`, {
            name: achivementId,
          })
        } else {
          await this.$axios.delete(
            `/users/${this.$auth.user.id}/achievements/${achivementId}`
          )
        }
      } catch (err) {
        console.log(err)
      }
    },
    triggerImportPlayer() {
      this.isImportingData = true

      this.importPlayer()
      this.importInterval = setInterval((async) => {
        this.importPlayer()
      }, 5000)
    },
    async getCompetitors(userId) {
      try {
        const response = await this.$axios.get(`/users/${userId}/competitors/`)
        return response.data.competitors
      } catch (e) {
        console.log(e)
      }
    },
    async filterApplied(filters) {
      try {
        const query = { ...filters }
        let compareRequest = ''
        this.selectedPlayerUuid = null
        this.showImportPlayerModal = false

        if (query.compare === 'global') {
          compareRequest = '&global=true'
        } else if (query.compare === 'competitors') {
          compareRequest = '&competitors=true'
        } else if (query.compare === 'player') {
          const response = await this.$axios.get(
            `/players?player_name=${query.player.playername}`
          )
          compareRequest = `&competitor=${response.data.id}`
          this.selectedPlayerUuid = response.data.id

          if (!response.data.imported) {
            this.showImportPlayerModal = true
            this.requiresImport = true
          }
        }

        if (!this.isImportingData && !this.requiresImport) {
          this.loadingAchiements = true
          const response = await this.$axios.get(
            `/achievements?me=${this.$auth.user.id}&champion=${query.champion}&rank=${query.rank}${compareRequest}`
          )
          this.achievements = response.data.items
        }
      } catch (err) {
        console.log(err)
      }
      this.loadingAchiements = false
    },
  },
}
</script>

<style>
.nav-item-tab a {
  padding: 10px;
}

.nav-item-tab .active,
.nav-item-tab:hover a{
  color: #fff !important;
  background-color: #206bc4  !important;
}

@media screen and (max-width: 575px) {
  .col-achievements-filter {
    display: none;
  }

  .col-achivements-table {
    width: 100%;
  }
}
</style>
