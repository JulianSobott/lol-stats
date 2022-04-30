<template>
<div class="modal modal-blur fade" id="modal-add-competitor" tabindex="-1" role="dialog" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Competitor</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
          <label class="form-label">Player</label>
          <input v-model="form.player" type="text" class="form-control" placeholder="Search player">
        </div>
      </div>
      <div class="modal-footer">
        <a href="#" class="btn btn-link link-secondary" data-bs-dismiss="modal">
          Cancel
        </a>
        <a href="#" class="btn btn-primary ms-auto" @click="addCompetitor()">
          Add competitor
        </a>
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
        player: '',
      },
      submitted: false,
      error: null
    }
  },
  methods: {
    addCompetitor() {
      console.log(this.form.player + ' added!');
      const element = document.getElementById("modal-add-competitor");
      element.classList.remove("show");
    }
  }
}
</script>
