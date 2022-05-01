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
    async searchPlayerName() {
      this.loading = true
      if (this.playername.length === 0) {
        this.loading = false
        this.error = false
        this.success = false
        this.$emit('changePlayername', null)
      }

      if (this.playername.length > 3) {
        try {
          await this.$axios.get(`/players/${this.playername}`)
          this.$emit('changePlayername', this.playername)
          this.error = false
          this.success = true
        } catch (err) {
          console.log(err.response.status)
          if (err.response.status === 404) {
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
