<template>
  <form ref="filters" class="achievement-filters">
    <div class="mb-3">
      <label class="form-label subheader mb-2">Compare with</label>
      <div>
        <label class="form-check mb-1">
          <input
            v-model="filters.compare"
            type="radio"
            class="form-check-input"
            value="global"
          />
          <span class="form-check-label">Global</span>
        </label>
        <label class="form-check mb-1">
          <input
            v-model="filters.compare"
            type="radio"
            class="form-check-input"
            value="friends"
          />
          <span class="form-check-label">Friends</span>
        </label>
      </div>
    </div>
    <div class="form-group mb-3">
      <label class="form-label subheader mb-2">Player</label>
      <PlayerSearchInput
        ref="PlayerSearchInput"
        @playernameSelected="playernameChanged"
      />
    </div>
    <div class="form-group mb-3">
      <label class="form-label subheader mb-2">Champion</label>
      <div>
        <select v-model="filters.champion" class="form-select">
          <option value="*">All Champions</option>
          <option v-for="champ in allChampions" :key="champ" :value="champ">
            {{ champ }}
          </option>
        </select>
      </div>
    </div>
    <div class="form-group mb-3">
      <label class="form-label subheader mb-2">Rank</label>
      <div>
        <select v-model="filters.rank" class="form-select">
          <option value="*">All Ranks</option>
          <option value="iron">Iron</option>
          <option value="bronze">Bronze</option>
          <option value="silver">Silver</option>
          <option value="gold">Gold</option>
          <option value="platinum">Platinum</option>
          <option value="diamond">Diamond</option>
          <option value="master">Master</option>
          <option value="grandmaster">Grandmaster</option>
          <option value="challenger">Challenger</option>
        </select>
      </div>
    </div>
    <div class="mt-4">
      <button
        class="btn btn-primary w-100"
        data-bs-dismiss="offcanvas"
        @click="search"
      >
        Confirm changes
      </button>
      <a class="btn btn-link w-100" @click="clearFilters">
        Reset to defaults
      </a>
    </div>
  </form>
</template>

<script>
export default {
  name: 'AchievementFilters',
  data() {
    return {
      filters: {
        compare: 'global',
        playername: '',
        champion: '*',
        rank: '*',
      },
      // TODO: all champs fetched from backend
      allChampions: ['Aatrox', 'Ahri', 'Akali', 'FooBar'],
    }
  },
  mounted() {
    this.filters.playername = this.$route.query.playername
    if (this.filters.playername !== null) {
      this.$refs.PlayerSearchInput.setPlayername(this.filters.playername)
    }
  },
  methods: {
    search(e) {
      this.$emit('filterApplied', {...this.filters})
      e.preventDefault();
    },
    playernameChanged(playerUuid, playername) {
      this.filters.playername = playername
    },
    clearFilters() {
      this.$refs.PlayerSearchInput.clear()
      this.filters = {
        compare: 'global',
        playername: '',
        champion: '*',
        rank: '*',
      }
    },
  },
}
</script>
