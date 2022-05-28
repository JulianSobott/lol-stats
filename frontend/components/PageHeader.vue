<template>
  <header class="navbar navbar-expand-md navbar-light d-print-none">
    <div class="container-xl">
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbar-menu"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <h1
        class="
          navbar-brand navbar-brand-autodark
          d-none-navbar-horizontal
          pe-0 pe-md-3
        "
      >
        <NuxtLink to="/">
          <img src="~/assets/images/logo.png" height="20" />
        </NuxtLink>
      </h1>
      <div class="navbar-nav flex-row order-md-last">
        <div class="nav-item d-none d-md-flex me-3"></div>
        <div v-if="$auth.loggedIn && Object.keys($auth.user.player_stats).length > 1" class="nav-item dropdown">
          <a
            href="#"
            class="nav-link d-flex lh-1 text-reset p-0"
            data-bs-toggle="dropdown"
            aria-label="Open user menu"
          >
            <span class="avatar avatar-sm" :style="userIcon"></span>
            <div class="d-none d-xl-block ps-2">
              <div>{{ $auth.user.player_stats.name }}</div>
              <div v-if="$auth.user.player_stats.rank !== undefined && $auth.user.player_stats.rank != null" class="mt-1 small text-muted">
                {{ $auth.user.player_stats.rank.tier.toUpperCase() }} {{ $auth.user.player_stats.rank.division }}
              </div>
            </div>
          </a>
          <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
            <NuxtLink to="/settings" class="dropdown-item">Settings</NuxtLink>
            <div class="dropdown-divider"></div>
            <a href="#" class="dropdown-item" @click="logoutUser">Logout</a>
          </div>
        </div>
        <div v-else class="nav-item dropdown">
          <NuxtLink to="/login" class="text-white"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              class="icon icon-tabler icon-tabler-login"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <desc>
                Download more icon variants from https://tabler-icons.io/i/login
              </desc>
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path
                d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2"
              ></path>
              <path d="M20 12h-13l3 -3m0 6l-3 -3"></path></svg
            >Login</NuxtLink
          >
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'PageHeader',
  computed: {
    userIcon() {
      if (this.$auth.user.player_stats.player_icon_path === "") {
        return "background-image: url('https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png')";
      }
      return `background-image: url("${this.$auth.user.player_stats.player_icon_path}");`
    },
  },
  methods: {
    async logoutUser() {
      try {
        await this.$auth.logout('local')
        this.$router.push('/login?logout=true')
      } catch (err) {
        console.log(err)
      }
    },
  },
}
</script>
