// state
export const state = () => ({
  playerData: {}
})

// getters
export const getters = {
  getPlayerData(state) {
    return state.playerData;
  }
}

// actions
export const actions = {
  async getPlayerData({
    commit
  }) {
    const response = await this.$axios.get('/players/LinkX20');
    commit("setPlayerData", response.data);
  }
}

// mutations
export const mutations = {
  setPlayerData(state, data) {
    state.playerData = data;
  }
}
