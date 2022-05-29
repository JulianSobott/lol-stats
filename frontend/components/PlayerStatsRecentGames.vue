<template>
  <div class="col-12">
    <h3 class="mb-3">Recent Games</h3>
    <div class="card">
      <div class="table-responsive">
        <table class="table table-vcenter card-table">
          <thead>
            <tr>
              <th class="w-1">Victory</th>
              <th class="text-center">Champion</th>
              <th class="text-center">Teammates</th>
              <th class="text-center">KDA</th>
              <th class="text-center">Duration</th>
              <th class="text-center">Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="game in recentGames" :key="game.match_id">
              <td>
                <strong v-if="game.win" class="text-green">Victory</strong>
                <strong v-else class="text-red">Defeat</strong>
              </td>
              <td class="text-center">
                <span
                  class="avatar avatar-s avatar-rounded m-1"
                  :style="championIconPath(game.self.champion)"
                ></span>
                <span class="text-muted d-block">{{
                  game.self.champion.name
                }}</span>
              </td>
              <td>
                <div class="row">
                  <div class="col-12 col-sm-6">
                    <TeamList :match="game" :team="game.ally_team" />
                  </div>
                  <div class="col-12 col-sm-6">
                    <TeamList :match="game" :team="game.enemy_team" />
                  </div>
                </div>
              </td>
              <td class="text-center">
                {{ game.self.stats.kills }} / {{ game.self.stats.deaths }} /
                {{ game.self.stats.assists }}
              </td>
              <td class="text-center">
                {{ converDuration(game.duration) }}
              </td>
              <td class="text-center">
                {{ converTimestamp(game.timestamp) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer">
        <div class="text-center">
          <button
            class="btn btn-primary ms-auto"
            @click="loadMoreGames()"
            :disabled="nextRecentGamesLink === ''"
          >
            <span
              v-if="moreGamesLoading"
              class="spinner-border spinner-border-sm icon icon-tabler"
              role="status"
              aria-hidden="true"
            ></span>
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              class="icon icon-tabler icon-tabler-refresh"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4"></path>
              <path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"></path>
            </svg>
            Load More
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'PlayerStatsRecentGames',
  props: ['playerUuid'],
  data() {
    return {
      nextRecentGamesLink: "",
      recentGames: [],
      moreGamesLoading: false,
    }
  },
  methods: {
    championIconPath(champion) {
      return `background-image: url("${champion.icon_path}");`
    },
    converTimestamp(value) {
      return moment(String(value)).format('MM-DD-YYYY')
    },
    converDuration(secs) {
      return moment.utc(secs * 1000).format('mm:ss')
    },
    async fetchPlayerData() {
      const recentGamesResponse = await this.$axios.get(
        `/players/${this.playerUuid}/recent-games`
      )
      this.recentGames = recentGamesResponse.data.items
      this.nextRecentGamesLink = recentGamesResponse.data.next
    },
    async loadMoreGames() {
      this.moreGamesLoading = true
      const response = await this.$axios.get(this.nextRecentGamesLink);
      this.recentGames.push(...response.data.items);
      this.nextRecentGamesLink = response.data.next
      this.moreGamesLoading = false
    },
  },
}
</script>
