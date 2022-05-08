<template>
  <div class="page">
    <PageHeader />
    <PageNavigation />
    <div class="page-wrapper">
      <div class="container-xl">
        <div class="page-header d-print-none">
          <div class="row g-2 align-items-center">
            <div class="col">
              <!-- Page pre-title -->
              <h2 class="page-title">Achievements</h2>
              <div class="text-muted mt-1">99999 results</div>
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
              <div class="card-tabs">
                <!-- Cards navigation -->
                <ul class="nav nav-tabs">
                  <li class="nav-item">
                    <a
                      href="#tab-favorites"
                      class="nav-link active"
                      data-bs-toggle="tab"
                      >Favorites</a
                    >
                  </li>
                  <li class="nav-item">
                    <a href="#tab-kills" class="nav-link" data-bs-toggle="tab"
                      >Kills</a
                    >
                  </li>
                  <li class="nav-item">
                    <a href="#tab-gold" class="nav-link" data-bs-toggle="tab"
                      >Gold</a
                    >
                  </li>
                  <li class="nav-item">
                    <a href="#tab-gold" class="nav-link" data-bs-toggle="tab"
                      >Multikills</a
                    >
                  </li>
                  <li class="nav-item">
                    <a href="#tab-gold" class="nav-link" data-bs-toggle="tab"
                      >Utility</a
                    >
                  </li>
                  <li class="nav-item">
                    <a href="#tab-gold" class="nav-link" data-bs-toggle="tab"
                      >Special Kills</a
                    >
                  </li>
                  <li class="nav-item">
                    <a href="#tab-gold" class="nav-link" data-bs-toggle="tab"
                      >Combat</a
                    >
                  </li>
                  <li class="nav-item">
                    <a href="#tab-gold" class="nav-link" data-bs-toggle="tab"
                      >Survival</a
                    >
                  </li>
                  <li class="nav-item">
                    <a href="#tab-gold" class="nav-link" data-bs-toggle="tab"
                      >Objectives</a
                    >
                  </li>
                </ul>
                <div class="tab-content">
                  <!-- Content of card #1 -->
                  <div id="tab-favorites" class="card tab-pane show active">
                    <div class="table-responsive">
                      <table
                        class="
                          table
                          card-table
                          table-vcenter
                          text-nowrap
                          datatable
                        "
                      >
                        <thead>
                          <tr>
                            <th class="w-1">ID</th>
                            <th>Achievement</th>
                            <th>You (Max/Average/Sum)</th>
                            <th>Player (Max/Average/Sum)</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="index in 10" :key="index">
                            <td><span class="text-muted">321</span></td>
                            <td>Lorem Ipsum</td>
                            <td>
                              300 / <span class="text-green">300</span> / 300
                            </td>
                            <td>
                              300 / 300 / <span class="text-red">300</span>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <div class="card-footer d-flex align-items-center">
                      <p class="m-0 text-muted">
                        Showing <span>1</span> to <span>8</span> of
                        <span>16</span> entries
                      </p>
                      <ul class="pagination m-0 ms-auto">
                        <li class="page-item disabled">
                          <a
                            class="page-link"
                            href="#"
                            tabindex="-1"
                            aria-disabled="true"
                          >
                            <!-- Download SVG icon from http://tabler-icons.io/i/chevron-left -->
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              class="icon"
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
                              ></path>
                              <polyline points="15 6 9 12 15 18"></polyline>
                            </svg>
                            prev
                          </a>
                        </li>
                        <li class="page-item active">
                          <a class="page-link" href="#">1</a>
                        </li>
                        <li class="page-item">
                          <a class="page-link" href="#">2</a>
                        </li>
                        <li class="page-item">
                          <a class="page-link" href="#">3</a>
                        </li>
                        <li class="page-item">
                          <a class="page-link" href="#">4</a>
                        </li>
                        <li class="page-item">
                          <a class="page-link" href="#">5</a>
                        </li>
                        <li class="page-item">
                          <a class="page-link" href="#">
                            next
                            <!-- Download SVG icon from http://tabler-icons.io/i/chevron-right -->
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              class="icon"
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
                              ></path>
                              <polyline points="9 6 15 12 9 18"></polyline>
                            </svg>
                          </a>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <!-- Content of card #2 -->
                  <div id="tab-kills" class="card tab-pane">
                    <div class="card-body">
                      <div class="card-title">Content of tab #2</div>
                      <p class="text-muted">
                        Lorem ipsum dolor sit amet, consectetur adipisicing
                        elit. Adipisci, alias aliquid distinctio dolorem
                        expedita, fugiat hic magni molestiae molestias odit.
                      </p>
                    </div>
                  </div>
                  <!-- Content of card #3 -->
                  <div id="tab-gold" class="card tab-pane">
                    <div class="card-body">
                      <div class="card-title">Content of tab #3</div>
                      <p class="text-muted">
                        Lorem ipsum dolor sit amet, consectetur adipisicing
                        elit. Adipisci, alias aliquid distinctio dolorem
                        expedita, fugiat hic magni molestiae molestias odit.
                      </p>
                    </div>
                  </div>
                  <!-- Content of card #4 -->
                  <div id="tab-top-4" class="card tab-pane">
                    <div class="card-body">
                      <div class="card-title">Content of tab #4</div>
                      <p class="text-muted">
                        Lorem ipsum dolor sit amet, consectetur adipisicing
                        elit. Adipisci, alias aliquid distinctio dolorem
                        expedita, fugiat hic magni molestiae molestias odit.
                      </p>
                    </div>
                  </div>
                </div>
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
  methods: {
    async filterApplied(filters) {
      try {
        const query = { ...filters }
        const puuids = []

        if (query.compare === 'global') {
          // keep puuids empty
        } else if (query.compare === 'friends') {
          puuids.push('123')
          puuids.push('123')
          puuids.push('123')
        } else if (query.compare === 'player') {
          // get id of player
          console.log(query);
          const response = await this.$axios.get(`/players?player_name=${query.player.playername}`)
          puuids.push(response.data.id)
        }

        await this.$axios.get(
          `/achievements?puuids=[${puuids.join()}]&champion=${
            query.champion
          }&rank=${query.rank}`
        )
      } catch (err) {
        console.log(err)
      }
    },
  },
}
</script>

<style>
@media screen and (max-width: 575px) {
  .col-achievements-filter {
    display: none;
  }

  .col-achivements-table {
    width: 100%;
  }
}
</style>