// state
export const state = () => ({
  playerData: {},
  recentGames: [],
  nextRecentGamesLink: ''
})

// getters
export const getters = {
  getPlayerData(state) {
    return state.playerData;
  },
  getRecentGames(state) {
    return state.recentGames;
  },
  getNextRecentGamesLink(state) {
    return state.nextRecentGamesLink;
  }
}

// actions
export const actions = {
  async getPlayerData({
    commit
  }) {
    commit("clearStore")
    const playerUuid = this.$auth.user.player_uuid
    const response = await this.$axios.get(`/players/${playerUuid}`);
    commit("setPlayerData", response.data);
  },
  async getRecentGames({
    commit
  }) {
    const playerUuid = this.$auth.user.player_uuid
    const response = await this.$axios.get(`/players/${playerUuid}/recent-games`);
    commit("setRecentGames", response.data.items);
    commit("setNextRecentGamesLink", response.data.next);
  },
  async loadMoreRecentGames({
    commit,
    state
  }) {
    if (state.nextRecentGamesLink !== null) {
      const response = await this.$axios.get(state.nextRecentGamesLink);
      commit("setRecentGames", response.data.items);
      commit("setNextRecentGamesLink", response.data.next);
    }
  },
  clearRecentGames({
    commit,
  }) {
    commit("clearRecentGames");
  },
  clearStore({ commit }) {
    commit("clearStore")
  }
}

// mutations
export const mutations = {
  setPlayerData(state, data) {
    state.playerData = data;
  },
  setRecentGames(state, data) {
    state.recentGames.push(...data);
  },
  setNextRecentGamesLink(state, data) {
    state.nextRecentGamesLink = data;
  },
  clearRecentGames(state) {
    state.recentGames = [];
  },
  clearStore(state) {
    state.recentGames = [];
    state.playerData = {};
    state.nextRecentGamesLink = '';
  },
}
