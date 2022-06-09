<template>
  <div class="col-sm-4 col-lg-4">
    <div v-if="playerData" class="card h-100">
      <div class="card-body">
        <div class="d-flex align-items-center">
          <div class="subheader">Winrate</div>
        </div>
        <div v-if="playerData.win_rate" class="h1 mb-3">
          {{ playerData.win_rate }}%
        </div>
        <div v-else class="h1 mb-3"><div class="placeholder col-4"></div></div>
        <div class="d-flex mb-2">
          <div>Winrate</div>
        </div>
        <div class="progress">
          <div
            class="progress-bar bg-blue"
            :style="{ width: playerData.win_rate + '%' }"
            role="progressbar"
          ></div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="col">
        <div class="placeholder placeholder-xs col-9"></div>
        <div class="placeholder placeholder-xs col-7"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayerStatsWinrate',
  props: ['playerData'],
}
</script>
