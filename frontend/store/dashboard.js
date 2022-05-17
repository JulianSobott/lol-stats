// state
export const state = () => ({
  playerData: {},
  recentGames: {},
})

// getters
export const getters = {
  getPlayerData(state) {
    return state.playerData;
  },
  getRecentGames(state) {
    return state.recentGames;
  }
}

// actions
export const actions = {
  async getPlayerData({
    commit
  }) {
    const playerUuid = this.$auth.user.player_uuid
    const response = await this.$axios.get(`/players/${playerUuid}`);
    commit("setPlayerData", response.data);
  },
  async getRecentGames({
    commit
  }) {
    const playerUuid = this.$auth.user.player_uuid
    const response = await this.$axios.get(`/players/${playerUuid}/recent-games`);
    commit("setRecentGames", response.data);
  }
}

// mutations
export const mutations = {
  setPlayerData(state, data) {
    state.playerData = data;
  },
  setRecentGames(state, data) {
    state.recentGames = data;
  }
}
