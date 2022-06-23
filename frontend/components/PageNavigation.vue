<template>
  <div class="navbar-expand-md">
    <div id="navbar-menu" class="collapse navbar-collapse">
      <div class="navbar navbar-light">
        <div class="container-xl">
          <ul class="navbar-nav">
            <li class="nav-item" :class="{ active: activeRoute('index') }">
              <NuxtLink to="/" class="nav-link">
                <span class="nav-link-title">Home</span>
              </NuxtLink>
            </li>
            <li class="nav-item" :class="{ active: activeRoute('dashboard') }">
              <NuxtLink to="/dashboard" class="nav-link">
                <span class="nav-link-title">Dashboard</span>
              </NuxtLink>
            </li>
            <li
              class="nav-item"
              :class="{ active: activeRoute('competitors') }"
            >
              <NuxtLink to="/competitors" class="nav-link">
                <span class="nav-link-title">Competitors</span>
              </NuxtLink>
            </li>
            <li
              class="nav-item"
              :class="{ active: activeRoute('achievements') }"
            >
              <NuxtLink to="/achievements" class="nav-link">
                <span class="nav-link-title">Achievements</span>
              </NuxtLink>
            </li>
          </ul>
          <div
            class="my-2 my-md-0 flex-grow-1 flex-md-grow-0 order-first order-md-last"
          >
            <div class="btn-list">
              <PlayerSearchInput
                ref="PlayerSearchInput"
                :showMessage="false"
                @playerSelected="playerSelected"
              />
              <button class="btn" :class="{ 'btn-primary': searchedPlayer }" :disabled="!searchedPlayer" @click="openPlayerProfile">Go</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageNavigation',
  data() {
    return {
      searchedPlayer: null
    }
  },
  methods: {
    playerSelected(playerData) {
      this.searchedPlayer = playerData
    },
    activeRoute(route) {
      return this.$route.name === route
    },
    openPlayerProfile() {
      this.$router.push(`/profiles/${this.searchedPlayer.player_uuid}`)
    }
  },
}
</script>
