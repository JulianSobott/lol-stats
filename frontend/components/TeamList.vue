<template>
  <div>
    <div
      class="row align-items-center mb-1"
      v-for="player in team"
      :key="player.id"
    >
      <div class="col-auto">
        <span
          class="avatar avatar-xs avatar-rounded ml-1"
          :style="championIconPath(player.champion)"
        ></span>
      </div>
      <div class="col d-none d-md-block" :class="{ 'text-red': player.team === 'red',  'text-blue': player.team === 'blue'}">
        <span v-if="match.self.player.name === player.player.name">You</span>
        <span v-else
          ><NuxtLink :to="'profiles/' + player.player.id">{{ player.player.name }}</NuxtLink>
          <span class="text-muted"
            >({{ player.stats.kills }}/{{ player.stats.deaths }}/{{
              player.stats.assists
            }})</span
          ></span
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TeamList',
  props: ['match', 'team'],
  methods: {
    championIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
  },
}
</script>
