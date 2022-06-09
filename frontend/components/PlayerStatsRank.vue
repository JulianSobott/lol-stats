<template>
  <div class="col-sm-4 col-lg-4">
    <div
      v-if="playerData.rank !== undefined && playerData.rank != null"
      class="card h-100"
    >
      <div class="card-body text-center">
        <div class="mb-3">
          <span
            class="avatar avatar-xl avatar-rounded"
            :style="loadRankIcon(playerData.rank.tier)"
          ></span>
        </div>
        <div class="card-title mb-1">
          {{ playerData.rank.tier.toUpperCase() }}
          {{ playerData.rank.division }}
        </div>
        <div class="text-muted">
          League Points: {{ playerData.rank.league_points }}
        </div>
        <div class="text-muted">Level: {{ playerData.level }}</div>
      </div>
    </div>
    <div v-else class="card h-100">
      <div class="card-body py-3 text-center">
        <div>
          <div class="avatar avatar-rounded avatar-lg placeholder mb-3"></div>
        </div>
        <div class="mt w-75 mx-auto">
          <div class="placeholder col-9 mb-3"></div>
          <div class="placeholder placeholder-xs col-10"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayerStatsRank',
  props: ['playerData'],
  methods: {
    loadRankIcon(rankIcon) {
      const path = require(`../assets/images/ranks/${rankIcon}.png`)
      return `background-image: url("${path}"); background-size: 75%`
    },
  }
}
</script>
