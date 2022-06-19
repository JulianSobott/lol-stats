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
              With LoL Stats you can compare your stats and achievements with other League of Legends players. Compare them to specific players or all the players on your server.
            </p>
          </div>
        </div>
        <div class="hr-text hr-text-center hr-text-spaceless">
          ACCOUNT SETUP
        </div>
        <div class="card-body">
          <div class="mb-3">
            <label class="form-label">Region</label>
            <select v-model="form.region" class="form-select mb-0">
              <option value="euw">Europe West</option>
              <option value="br">Brazil</option>
              <option value="eunue">Europe Nordic & East</option>
              <option value="jp">Japan</option>
              <option value="kr">Korea</option>
              <option value="lan">Latein America North</option>
              <option value="las">Latein America South</option>
              <option value="na">North America</option>
              <option value="oce">Oceania</option>
              <option value="ru">Russia</option>
              <option value="tr">Turkey</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Select your Player Name</label>
            <PlayerSearchInput
              ref="playerSearchInput"
              @playerSelected="playerSelected"
            />
            <div class="form-hint">
              Please enter your <strong>League of Legends summoner name</strong>.
            </div>
          </div>
        </div>
      </div>
      <div class="row align-items-center mt-3">
        <div class="col">
          <div class="btn-list justify-content-start">
            <button
              v-if="!firstSetup"
              class="btn btn-danger"
              @click="deleteAccount()"
            >
              Delete Account
            </button>
          </div>
        </div>
        <div class="col">
          <div class="btn-list justify-content-end">
            <NuxtLink
              v-if="!firstSetup"
              to="/dashboard"
              class="btn btn-link link-secondary"
            >
              Cancel
            </NuxtLink>
            <button
              class="btn btn-primary"
              :disabled="!form.player"
              @click="savePlayername()"
            >
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
  middleware: 'auth',
  mounted() {
    if (this.$route.query.firstsetup !== undefined) {
      this.firstSetup = this.$route.query.firstsetup === 'true'
    } else {
      this.firstSetup = false
      this.getPlayerData()
    }
  },
  data() {
    return {
      form: {
        region: 'euw',
        player: null,
      },
      submitted: false,
      error: null,
      firstSetup: false,
    }
  },
  head: {
    bodyAttrs: {
      class: 'theme-dark border-top-wide border-primary d-flex flex-column',
    },
  },
  methods: {
    playerSelected(playerData) {
      this.form.player = playerData
    },
    async deleteAccount() {
      try {
        await this.$axios.delete(`/auth/delete`)
        this.$router.push('/login?logout=true')
        this.$auth.setUser(null)
      } catch (e) {
        this.error = true
      }
    },
    getPlayerData() {
      try {
        this.$refs.playerSearchInput.setPlayerData(this.$auth.user.player_stats.name)
        this.form.region = this.$auth.user.region
      } catch (e) {
        this.error = true
      }
    },
    async savePlayername() {
      try {
        const playerId = this.$auth.user.id
        await this.$axios.put(`/users/${playerId}`, {
          region: this.form.region,
          player_uuid: this.form.player.player_uuid,
        })
 
        await this.$axios.post(
          `/players/${this.this.form.player.player_uuid}/import`
        )
      } catch (e) {
        this.error = true
      }
      await this.$auth.fetchUser()
      this.$router.push('/dashboard')
    },
  },
}
</script>
