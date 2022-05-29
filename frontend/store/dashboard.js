// state
export const state = () => ({
  playerData: {},
})

// getters
export const getters = {
  getPlayerData(state) {
    return state.playerData;
  },
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
  clearStore({ commit }) {
    commit("clearStore")
  }
}

// mutations
export const mutations = {
  setPlayerData(state, data) {
    state.playerData = data;
  },
  clearStore(state) {
    state.playerData = {};
  },
}
