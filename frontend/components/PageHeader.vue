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
          <img src="~/assets/images/logo.png" height="20"/>
        </NuxtLink>
      </h1>
      <div class="navbar-nav flex-row order-md-last">
        <div class="nav-item d-none d-md-flex me-3"></div>
        <div class="nav-item dropdown">
          <a
            href="#"
            class="nav-link d-flex lh-1 text-reset p-0"
            data-bs-toggle="dropdown"
            aria-label="Open user menu"
          >
            <span
              class="avatar avatar-sm"
              style="background-image: url(https://i.imgur.com/6lCL9uU.png)"
            ></span>
            <div class="d-none d-xl-block ps-2">
              <div>{{ user.username }}</div>
              <div class="mt-1 small text-muted">{{ user.rank }}</div>
            </div>
          </a>
          <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
            <NuxtLink :to="'/profiles/' + user.playerUuid" class="dropdown-item">Profile</NuxtLink>
            <div class="dropdown-divider"></div>
            <NuxtLink to="/login" class="dropdown-item">Logout</NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'PageHeader',
  data() {
    return {
      user: {
        id: 0,
        username: 'FooBar',
        rank: 'Silver II',
        playerUuid: '351123'
      }
      // user data fetched by nuxtjs/auth package on logins
    }
  }
}
</script>
