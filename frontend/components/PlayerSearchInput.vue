<template>
  <div class="input-icon mb-3">
    <input
      v-model="playername"
      :class="{ 'is-invalid': error, 'is-valid': success }"
      placeholder="Search Player name"
      type="text"
      class="form-control"
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
      error: false,
      success: false,
      loading: false,
    }
  },
  methods: {
    clear() {
      this.playername = ''
      this.loading = false
      this.error = false
      this.success = false
    },
    setPlayername(playername) {
      this.playername = playername
      this.searchPlayerName()
    },
    async searchPlayerName() {
      if (!this.playername) {
        this.loading = false
        this.error = false
        this.success = false
        this.$emit('playernameSelected', null)
      }

      if (this.playername && this.playername.length >= 1) {
        try {
          this.loading = true
          const response = await this.$axios.get(`/players/${this.playername}`)
          this.$emit('playernameSelected', response.name, this.playername)
          this.error = false
          this.success = true
        } catch (err) {
          if (err.response.status !== 200) {
            this.$emit('playernameSelected', null, null)

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
