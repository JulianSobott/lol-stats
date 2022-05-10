<template>
  <div class="input-icon mb-3">
    <input
      v-model="playername"
      :class="{ 'is-invalid': error, 'is-valid': success }"
      placeholder="Search Player name"
      type="text"
      class="form-control"
      :disabled="disabled"
      @input="searchPlayerName()"
    />
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
</template>

<script>
export default {
  name: 'PlayerSearchInput',
  data() {
    return {
      playername: '',
      player_uuid: '',
      error: false,
      success: false,
      loading: false,
      disabled: false,
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
      this.searchPlayerName()
    },
    async searchPlayerName() {
      if (!this.playername) {
        this.loading = false
        this.error = false
        this.success = false
        this.$emit('playerSelected', null)
      }

      if (this.playername && this.playername.length >= 1) {
        try {
          this.loading = true
          const response = await this.$axios.get(`/players?player_name=${this.playername}&region=ewu`)
          this.$emit('playerSelected', {
            playername: response.data.name,
            player_uuid: response.data.id
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
