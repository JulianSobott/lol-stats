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
                          Lorem ipsum dolor sit amet, consetetur sadipscing
                          elitr, sed diam nonumy eirmod tempor invidunt ut
                          labore et dolore magna aliquyam erat, sed diam
                          voluptua. At vero eos et accusam et justo duo dolores
                          et ea rebum. Stet clita kasd gubergren, no sea
                          takimata sanctus est Lorem ipsum dolor sit amet. Lorem
                          ipsum dolor sit amet, consetetur sadipscing elitr, sed
                          diam nonumy eirmod tempor invidunt ut labore et dolore
                          magna aliquyam erat, sed diam voluptua. At vero eos et
                          accusam et justo duo dolores et ea rebum. Stet clita
                          kasd gubergren, no sea takimata sanctus est Lorem
                          ipsum dolor sit amet.
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
            <div class="col-12 col-lg-4">
              <div class="card h-100">
                <div class="card-header">
                  <h3 class="card-title">Kills</h3>
                </div>
                <table class="table card-table table-vcenter">
                  <thead>
                    <tr>
                      <th class="w-1">No</th>
                      <th>Player</th>
                      <th class="text-center">AVG</th>
                    </tr>
                  </thead>
                  <tbody></tbody>
                </table>
              </div>
            </div>
            <div class="col-12 col-lg-4">
              <div class="card h-100">
                <div class="card-header">
                  <h3 class="card-title">Kills</h3>
                </div>
                <table class="table card-table table-vcenter">
                  <thead>
                    <tr>
                      <th class="w-1">No</th>
                      <th>Player</th>
                      <th class="text-center">AVG</th>
                    </tr>
                  </thead>
                  <tbody></tbody>
                </table>
              </div>
            </div>
            <div class="col-12 col-lg-4">
              <div class="card h-100">
                <div class="card-header">
                  <h3 class="card-title">Kills</h3>
                </div>
                <table class="table card-table table-vcenter">
                  <thead>
                    <tr>
                      <th class="w-1">No</th>
                      <th>Player</th>
                      <th class="text-center">AVG</th>
                    </tr>
                  </thead>
                  <tbody></tbody>
                </table>
              </div>
            </div>
            <div class="col-12">
              <div class="text-center">
                <a
                  href="#"
                  class="btn btn-primary"
                >
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
                </a>
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
