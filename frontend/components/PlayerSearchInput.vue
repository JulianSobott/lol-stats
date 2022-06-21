<template>
  <div class="input-icon">
    <span class="input-icon-addon">
      <!-- Download SVG icon from http://tabler-icons.io/i/search -->
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
        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
        <circle cx="10" cy="10" r="7"></circle>
        <line x1="21" y1="21" x2="15" y2="15"></line>
      </svg>
    </span>
    <input
      v-model="playername"
      :class="{ 'is-invalid': error, 'is-valid': success && !loading }"
      placeholder="Search Player name"
      type="text"
      class="form-control"
      :disabled="disabled"
      @input="debouncePlayerSearch"
    />
    <div v-if="showMessage">
      <span v-if="loading && !error" class="input-icon-addon">
        <div
          class="spinner-border spinner-border-sm text-muted"
          role="status"
        ></div>
      </span>
      <div v-if="error" class="invalid-feedback">Playername not found.</div>
      <div v-if="success" class="invalid-feedback text-green d-block">
        Player found.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showMessage: {
      type: Boolean,
      default: true,
      required: false
    },
  },
  name: 'PlayerSearchInput',
  data() {
    return {
      playername: '',
      player_uuid: '',
      error: false,
      success: false,
      loading: false,
      disabled: false,
      debounce: null,
    }
  },
  methods: {
    disable(value) {
      this.disabled = value
    },
    clear() {
      this.playername = ''
      this.player_uuid = ''
      this.loading = false
      this.error = false
      this.success = false
    },
    setPlayerData(playername, playerUuid) {
      this.playername = playername
      this.player_uuid = playerUuid
      this.searchPlayerName(playername)
    },
    debouncePlayerSearch(event) {
      this.loading = true
      clearTimeout(this.debounce)
      this.debounce = setTimeout(() => {
        this.searchPlayerName(event.target.value)
        this.loading = false
      }, 500)
    },
    async searchPlayerName(playername) {
      this.playername = playername
      if (!this.playername) {
        this.loading = false
        this.error = false
        this.success = false
        this.$emit('playerSelected', null)
      }

      if (this.playername && this.playername.length >= 1) {
        try {
          this.loading = true
          const response = await this.$axios.get(
            `/players?player_name=${this.playername}&region=euw`
          )
          this.$emit('playerSelected', {
            playername: response.data.name,
            player_uuid: response.data.id,
          })
          this.error = false
          this.success = true
        } catch (err) {
          if (err.response.status !== 200) {
            this.$emit('playerSelected', null)

            this.loading = false
            this.error = true
            this.success = false
          }
        } finally {
          this.loading = false
        }
      }
    },
  },
}
</script>
