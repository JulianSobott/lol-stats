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
            <div class="col-sm-4 col-lg-4">
              <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                      <div class="subheader">Winrate</div>
                    </div>
                    <div class="h1 mb-3">75%</div>
                    <div class="d-flex mb-2">
                      <div>Winrate</div>
                      <div class="ms-auto">
                        <span class="text-green d-inline-flex align-items-center lh-1">
                          7% <!-- Download SVG icon from http://tabler-icons.io/i/trending-up -->
                          <svg xmlns="http://www.w3.org/2000/svg" class="icon ms-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><polyline points="3 17 9 11 13 15 21 7"></polyline><polyline points="14 7 21 7 21 14"></polyline></svg>
                        </span>
                      </div>
                    </div>
                    <div class="progress progress-sm">
                      <div class="progress-bar bg-blue" style="width: 75%" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" aria-label="75% Complete">
                        <span class="visually-hidden">75% Complete</span>
                      </div>
                    </div>
                  </div>
              </div>
            </div>
            <div class="col-sm-4 col-lg-4">
              <div class="card h-100">
                <div class="card-body text-center">
                  <div class="mb-3">
                    <span class="avatar avatar-xl avatar-rounded" style="background-image: url(https://opgg-static.akamaized.net/images/medals/bronze_4.png?image=q_auto&image=q_auto,f_webp,w_auto&v=1651226741046)"></span>
                  </div>
                  <div class="card-title mb-1">Bronze 4</div>
                </div>
              </div>
            </div>
            <div class="col-sm-4 col-lg-4">
              <div class="card h-100">
                  <div class="card-header">
                    <div>Most Played</div>
                  </div>
                  <table class="table card-table table-vcenter">
                    <thead>
                      <tr>
                        <th class="w-1">Champion</th>
                        <th>Winrate</th>
                        <th>Games</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr  v-for="index in 3" :key="index">
                        <td class="text-center p-0">
                          <span class="avatar avatar-xs avatar-rounded m-1" style="background-image: url(https://placekitten.com/48/48)"></span>
                        </td>
                        <td>25%</td>
                        <td>5233</td>
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
                        <td class="text-muted">{{index}}</td>
                        <td><span class="text-green">WIN</span></td>
                        <td>
                          <span class="avatar avatar-s avatar-rounded m-1" style="background-image: url(https://placekitten.com/48/48)"></span>
                        </td>
                        <td>
                          <div class="row align-items-center">
                            <div class="col">
                              <div>
                                <div class="avatar avatar-rounded" v-for="index in 5" :key="index">
                                  <span class="avatar avatar-xs avatar-rounded ml-1" style="background-image: url(https://placekitten.com/32/32)"></span>
                                </div>
                              </div>
                              <div>
                                <div class="avatar avatar-rounded" v-for="index in 5" :key="index">
                                  <span class="avatar avatar-xs avatar-rounded ml-1" style="background-image: url(https://placekitten.com/32/32)"></span>
                                </div>
                              </div>
                            </div>
                            <div class="col-auto">
                            </div>
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
export default {
  name: 'IndexPage',
}
</script>
