<template>
  <div class="navbar-expand-md">
    <div class="collapse navbar-collapse" id="navbar-menu">
      <div class="navbar navbar-light">
        <div class="container-xl">
          <ul class="navbar-nav">
            <li class="nav-item" :class="{'active': activeRoute('index') }">
              <NuxtLink to="/" class="nav-link">
                <span class="nav-link-title">Home</span>
              </NuxtLink>
            </li>
            <li class="nav-item" :class="{'active': activeRoute('dashboard')}">
              <NuxtLink to="/dashboard" class="nav-link">
                <span class="nav-link-title">Dashboard</span>
              </NuxtLink>
            </li>
            <li class="nav-item" :class="{'active': activeRoute('competitors')}">
              <NuxtLink to="/competitors" class="nav-link">
                <span class="nav-link-title">Competitors</span>
              </NuxtLink>
            </li>
            <li class="nav-item" :class="{'active': activeRoute('achievements')}">
              <NuxtLink to="/achievements" class="nav-link">
                <span class="nav-link-title">Achievements</span>
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageNavigation',
  methods: {
    activeRoute(route) {
      return this.$route.name === route;
    }
  }
}
</script>
