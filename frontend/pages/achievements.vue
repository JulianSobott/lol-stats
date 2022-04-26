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
              <h2 class="page-title">Achievements</h2>
              <div class="text-muted mt-1">99999 results</div>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row g-4">
            <div class="col-3">
              <form action="" method="get">
                <div class="form-group mb-3">
                  <label class="form-label">Compare with</label>
                  <div>
                    <select class="form-select">
                      <option>Global</option>
                      <option>Friends</option>
                      <option>Favorites</option>
                    </select>
                  </div>
                </div>
                <div class="form-group mb-3">
                  <label class="form-label">Player</label>
                  <div>
                    <input
                      type="text"
                      class="form-control"
                      name="example-text-input"
                      placeholder="Search player"
                    />
                  </div>
                </div>
                <div class="form-group mb-3">
                  <label class="form-label">Champion</label>
                  <div>
                    <select class="form-select">
                      <option>Aatrox</option>
                      <option>Ahri</option>
                      <option>Akali</option>
                      <option>Alistar</option>
                      <option>Amumu</option>
                      <option>Anivia</option>
                    </select>
                  </div>
                </div>
                <div class="form-group mb-3">
                  <label class="form-label">Rank</label>
                  <div>
                    <select class="form-select">
                      <option>Iron</option>
                      <option>Bronze</option>
                      <option>Silver</option>
                      <option>Gold</option>
                      <option>Platinum</option>
                      <option>Diamond</option>
                      <option>Master</option>
                      <option>Grandmaster</option>
                      <option>Challenger</option>
                    </select>
                  </div>
                </div>
                <div class="mt-5">
                  <button class="btn btn-primary w-100">Confirm changes</button>
                  <a href="#" class="btn btn-link w-100"> Reset to defaults </a>
                </div>
              </form>
            </div>
            <div class="col-9">
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
                            <th>You</th>
                            <th>Oppoment</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
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
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AchievementsPage',
}
</script>
