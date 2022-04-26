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
            <div class="col-sm-6 col-lg-4">
              <div class="card">
                <div class="card-body">
                  <h3 class="card-title">Winrate</h3>
                  <p class="text-muted">
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Aperiam deleniti fugit incidunt, iste, itaque minima neque
                    pariatur perferendis sed suscipit velit vitae voluptatem.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-sm-6 col-lg-4">
              <div class="card">
                <div class="card-body">
                  <h3 class="card-title">Rank</h3>
                  <p class="text-muted">
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Aperiam deleniti fugit incidunt, iste, itaque minima neque
                    pariatur perferendis sed suscipit velit vitae voluptatem.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-sm-6 col-lg-4">
              <div class="card">
                <div class="card-body">
                  <h3 class="card-title">Stats</h3>
                  <p class="text-muted">
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Aperiam deleniti fugit incidunt, iste, itaque minima neque
                    pariatur perferendis sed suscipit velit vitae voluptatem.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-12">
              <h3 class="mb-3">Recent Games</h3>
              <div class="card">
                <div class="table-responsive">
                  <table class="table table-vcenter card-table">
                    <thead>
                      <tr>
                        <th>Victory</th>
                        <th>Champion</th>
                        <th>Teammates</th>
                        <th>KDA</th>
                        <th>Playing time</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="index in 10" :key="index">
                        <td>Team Red</td>
                        <td>Foo Bar</td>
                        <td>
                          <span class="avatar avatar-xs avatar-rounded m-1" style="background-image: url(https://placekitten.com/32/32)" v-for="index in 5" :key="index"></span>
                        </td>
                        <td>1:20</td>
                        <td>200</td>
                        <td>05-24-2022</td>
                      </tr>
                    </tbody>
                  </table>
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
