<template>
  <div
    id="modal-add-competitor"
    class="modal modal-blur fade"
    tabindex="-1"
    role="dialog"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Add Competitor</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Player</label>
            <PlayerSearchInput
              ref="PlayerSearchInput"
              @playerSelected="playerSelected"
            />
          </div>
        </div>
        <div class="modal-footer">
          <a
            href="#"
            class="btn btn-link link-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </a>
          <button
            class="btn btn-primary ms-auto"
            :class="{ disabled: !form.player }"
            @click="addCompetitor()"
          >
            Add competitor
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddCompetitorModal',
  data() {
    return {
      form: {
        player: {}
      },
      submitted: false,
      error: null,
    }
  },
  methods: {
    async addCompetitor() {
      try {
        const playerId = this.$auth.user.id
        await this.$axios.post(`/users/${playerId}/competitors/`, {
          player_uuid: this.form.player.player_uuid,
        })
        this.$router.push('/competitors')
      } catch (e) {
        this.error = true
      }

      if (this.error) return

      this.$refs.PlayerSearchInput.clear()

      // remove modal
      const modal = document.getElementById('modal-add-competitor')
      modal.classList.remove('show')
      modal.style.removeProperty('display')

      document.querySelectorAll('.modal-backdrop').forEach((el) => el.remove())

      const body = document.getElementsByTagName('body')[0]
      body.classList.remove('modal-open')
      body.style.removeProperty('overflow')
    },
    playerSelected(playerData) {
      this.form.player = playerData
    },
  },
}
</script>
