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
        <div class="nav-item dropdown">
          <a
            v-if="user"
            href="#"
            class="nav-link d-flex lh-1 text-reset p-0"
            data-bs-toggle="dropdown"
            aria-label="Open user menu"
          >
            <span class="avatar avatar-sm" :style="userIcon"></span>
            <div class="d-none d-xl-block ps-2">
              <div>{{ user.name }}</div>
              <div class="mt-1 small text-muted">
                {{ user.rank.tier }} {{ user.rank.division }}
              </div>
            </div>
          </a>
          <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
            <NuxtLink to="/setup" class="dropdown-item">Settings</NuxtLink>
            <div class="dropdown-divider"></div>
            <a href="#" class="dropdown-item" @click="logoutUser">Logout</a>
          </div>
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
      return `background-image: url("${this.user.player_icon_path}");`
    },
  },
  mounted() {
    this.getUserData()
  },
  data() {
    return {
      user: null,
    }
  },
  methods: {
    async getUserData() {
      try {
        const response = await this.$axios.get('/players/i6rhuj9rVlNXt0WRoGzMelbaGItog4yYs6mC8yZXQOY2rpuY68virbdeyvnoptwJ07u1cgZKW1tBPA')
        this.user = response.data
      } catch (err) {
        console.log(err)
      }
    },
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
