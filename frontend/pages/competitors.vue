<template>
  <div class="page">
    <ImportHeaderWarning />
    <PageHeader />
    <PageNavigation />
    <div class="page-wrapper">
      <div class="container-xl">
        <!-- Page title -->
        <div class="page-header d-print-none">
          <div class="row g-2 align-items-center">
            <div class="col">
              <!-- Page pre-title -->
              <h2 class="page-title">Competitors</h2>
            </div>
            <!-- Page title actions -->
            <div class="col-12 col-md-auto ms-auto d-print-none">
              <div class="btn-list">
                <a
                  href="#"
                  class="btn btn-primary d-sm-inline-block"
                  data-bs-toggle="modal"
                  data-bs-target="#modal-add-competitor"
                  @click="openAddCompetitorModal"
                >
                  Add Competitor
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row row-cards">
            <div class="col-12">
              <div v-if="!loadingCompetitors" class="card">
                <div v-if="competitors.length > 0" class="table-responsive">
                  <table class="table table-vcenter card-table">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Tier</th>
                        <th>Winrate</th>
                        <th class="w-1"></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in competitors" :key="item.id">
                        <td>
                          <div class="d-flex py-1 align-items-center">
                            <span
                              class="avatar me-2"
                              :style="championIconPath(item.player_stats.player_icon_path)"
                            ></span>
                            <div class="flex-fill">
                              <div class="font-weight-medium">
                                <NuxtLink
                                  :to="'/profiles/' + item.player_uuid"
                                  class="text-reset"
                                  >{{ item.player_name }}</NuxtLink
                                >
                              </div>
                              <div class="text-muted">
                                <NuxtLink
                                  :to="
                                    '/achievements?playername=' +
                                    item.player_name
                                  "
                                  class="text-reset"
                                  >Achievements</NuxtLink
                                >
                              </div>
                            </div>
                          </div>
                        </td>
                        <td>
                          <div
                            v-if="item.player_stats.imported"
                            class="d-flex py-1 align-items-center"
                          >
                            <span
                              class="avatar avatar-rounded me-2"
                              :style="loadRankIcon(item.player_stats.rank.tier)"
                            ></span>
                            <div class="flex-fill">
                              <div class="font-weight-medium">
                                {{ item.player_stats.rank.tier.toUpperCase() }}
                                {{ item.player_stats.rank.division }}
                              </div>
                            </div>
                          </div>
                          <div v-else class="d-flex py-1 align-items-center">
                            <span class="text-muted"
                              >Player not imported yet.</span
                            >
                          </div>
                        </td>
                        <td>{{ item.player_stats.win_rate }}%</td>
                        <td>
                          <a
                            href="#"
                            class="text-red"
                            @click="removeCompetitor(item.player_uuid)"
                          >
                            Remove
                          </a>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else class="card card-borderless">
                  <div class="card-body text-center">
                    <h3 class="card-title">No Competitors</h3>
                    <div>Add some competitors to compare your skills.</div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center">
                <div class="spinner-border text-light" role="status"></div>
                <p class="card-title mt-1">Loading Competitors...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <AddCompetitorModal ref="addCompetitorModal" />
  </div>
</template>

<script>
export default {
  name: 'CompetitorsPage',
  middleware: ['auth', 'settings'],
  data() {
    return {
      competitors: [],
      submitted: false,
      error: null,
      loadingCompetitors: false
    }
  },
  mounted() {
    this.getCompetitors()
  },
  methods: {
    championIconPath(path) {
      return `background-image: url("${path}");`
    },
    loadRankIcon(rankIcon) {
      const path = require(`../assets/images/ranks/${rankIcon}.png`)
      return `background-image: url("${path}"); background-size: 75%`
    },
    openAddCompetitorModal() {
      this.$refs.addCompetitorModal.clearForm()
    },
    async getCompetitors() {
      this.loadingCompetitors = true
      try {
        const userId = this.$auth.user.id
        const response = await this.$axios.get(`/users/${userId}/competitors/`)
        this.competitors = response.data.competitors
      } catch (e) {
        this.error = true
      }
      this.loadingCompetitors = false
    },
    async removeCompetitor(competitorUuid) {
      try {
        const userId = this.$auth.user.id
        await this.$axios.delete(
          `/users/${userId}/competitors/${competitorUuid}`,
          {}
        )

        this.competitors = this.competitors.filter(function (obj) {
          return obj.player_uuid !== competitorUuid
        })
      } catch (e) {
        this.error = true
      }
    },
  },
}
</script>
