<template>
  <div class="page">
    <PageHeader />
    <PageNavigation />
    <div class="page-wrapper">
      <div class="container-xl">
        <!-- Page title -->
        <div class="page-header d-print-none">
            <div class="row g-2 align-items-center">
              <div class="col">
                <!-- Page pre-title -->
                <h2 class="page-title">
                  Competitors
                </h2>
              </div>
              <!-- Page title actions -->
              <div class="col-12 col-md-auto ms-auto d-print-none">
                <div class="btn-list">
                  <a href="#" class="btn btn-primary d-none d-sm-inline-block" data-bs-toggle="modal" data-bs-target="#modal-add-competitor">
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
              <div class="card">
                <div v-if="this.competitors.length > 0" class="table-responsive">
                  <table class="table table-vcenter card-table">
                    <thead>
                      <tr>
                        <th class="w-1">ID</th>
                        <th>Name</th>
                        <th>Tier</th>
                        <th>Winrate</th>
                        <th>Played</th>
                        <th class="w-1"></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in this.competitors" :key="item.id">
                        <td class="text-muted">{{item.id}}</td>
                        <td>
                          <div class="d-flex py-1 align-items-center">
                            <span
                              class="avatar me-2"
                              style="
                                background-image: url(https://placekitten.com/48/48);
                              "
                            ></span>
                            <div class="flex-fill">
                              <div class="font-weight-medium">
                                <NuxtLink to="/profiles/1234" class="text-reset">{{item.playername}}</NuxtLink>
                              </div>
                              <div class="text-muted"><NuxtLink :to="'/achievements?playername=' + item.playername" class="text-reset">Achievements</NuxtLink></div>
                            </div>
                          </div>
                        </td>
                        <td>
                          <div class="d-flex py-1 align-items-center">
                            <span class="avatar avatar-rounded me-2" style="background-image: url(https://opgg-static.akamaized.net/images/medals/bronze_4.png?image=q_auto&image=q_auto,f_webp,w_auto&v=1651226741046)"></span>
                            <div class="flex-fill">
                              <div class="font-weight-medium">Bronze 4</div>
                            </div>
                          </div>
                        </td>
                        <td>50%</td>
                        <td>5220</td>
                        <td>
                          <a href="#" class="text-red" @click="removeCompetitor(item.id)">
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
            </div>
          </div>
        </div>
      </div>
    </div>
    <AddCompetitorModal />
  </div>
</template>

<script>
export default {
  name: 'CompetitorsPage',
  data() {
    return {
      competitors: [{
        id: 1,
        playername: 'Test',
      },
      {
        id: 2,
        playername: 'Test2',
      },
      {
        id: 3,
        playername: 'Test3',
      }],
      submitted: false,
      error: null
    }
  },
  methods: {
    removeCompetitor(id) {
      console.log("Removing " + id)
      this.competitors = this.competitors.filter(function( obj ) {
        return obj.id !== id;
      });
    }
  }
}
</script>
