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
              class="mb-3"
              ref="PlayerSearchInput"
              @playerSelected="playerSelected"
            />
          </div>
          <p v-if="competitorExists" class="text-red m-0">Competitorship already exists. Please select another one.</p>
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
        player: {},
      },
      submitted: false,
      error: null,
      competitorExists: false
    }
  },
  methods: {
    clearForm() {
      this.form.player = {}
      this.$refs.PlayerSearchInput.clear()
    },
    async addCompetitor() {
      try {
        const playerId = this.$auth.user.id
        await this.$axios.post(`/users/${playerId}/competitors/`, {
          player_uuid: this.form.player.player_uuid,
        })
        this.$router.push('/competitors')
        
        // dirty hack to reload the page
        window.location.reload(true)
      } catch (e) {
        if (e.response.status === 409) {
          this.competitorExists = true
        }
        this.error = true
      }

      document.querySelectorAll('.modal-backdrop').forEach((el) => el.remove())

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
      this.competitorExists = false
      this.error = false
    },
  },
}
</script>
