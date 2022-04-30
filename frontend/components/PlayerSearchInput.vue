<template>
  <div class="input-icon mb-3">
    <input
      v-model="playername"
      :class="{ 'is-invalid': error }"
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
    <div v-if="error" class="invalid-feedback">Playername not found</div>
  </div>
</template>

<script>
export default {
  name: 'PlayerSearchInput',
  data() {
    return {
      playername: '',
      error: false,
      loading: false,
    }
  },
  methods: {
    searchPlayerName() {
      this.loading = true
      if (this.playername.length === 0) {
        this.loading = false
        this.error = false;
        this.$emit('changePlayername', null)
      }

      if (this.playername.length > 3) {
        this.$emit('changePlayername', this.playername)

        // simulate api search
        setTimeout(() => {
          this.loading = false;
          this.error = true;
        }, 500)
      }
    },
  },
}
</script>
