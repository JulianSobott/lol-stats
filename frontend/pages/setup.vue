<template>
  <div class="page page-center">
    <div class="container-tight py-4">
      <div class="text-center mb-4">
        <span class="navbar-brand navbar-brand-autodark"
          ><img src="~/assets/images/logo.png" height="36" alt=""
        /></span>
      </div>
      <div class="card card-md">
        <div v-if="error" class="card-status-top bg-danger"></div>
        <div v-if="firstSetup">
          <div class="card-body text-center py-2 p-sm-5">
            <h1 class="mt-1">Welcome to LoL Stats!</h1>
            <p class="text-muted">
              On LoL Stats you can compare your player stats and achievements
              with all League of legends players over the world or just with
              your friends.
            </p>
          </div>
        </div>
        <div class="hr-text hr-text-center hr-text-spaceless">SETUP</div>
        <div class="card-body">
          <div class="mb-3">
            <label class="form-label">Select your Player Name</label>
            <PlayerSearchInput @changePlayername="changePlayername" />
            <div class="form-hint">
              In order for you to view player information and statistics, we
              still need your gamer tag. Please enter your gamer tag in this
              field, which you also use in <strong>League of Legends</strong>.
            </div>
          </div>
        </div>
      </div>
      <div class="row align-items-center mt-3">
        <div class="col">
          <div class="btn-list justify-content-end">
            <NuxtLink
              v-if="!firstSetup"
              to="/dashboard"
              class="btn btn-link link-secondary"
            >
              Cancel
            </NuxtLink>
            <button class="btn btn-primary" @click="savePlayername()">
              Continue
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SetupPage',
  data() {
    return {
      form: {
        player_uuid: '',
      },
      submitted: false,
      error: null,
      firstSetup: true,
    }
  },
  head: {
    bodyAttrs: {
      class: 'theme-dark border-top-wide border-primary d-flex flex-column',
    },
  },
  methods: {
    changePlayername(playerUuid, playername) {
      this.form.player_uuid = playerUuid
    },
    async savePlayername() {
      try {
        await this.$axios.patch('/users/1234', {
          player_uuid: this.form.player_uuid,
        })
        this.$router.push('/dashboard')
      } catch (e) {
        this.error = true
      }
    },
  },
}
</script>
