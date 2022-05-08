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
    const response = await this.$axios.get('/players/i6rhuj9rVlNXt0WRoGzMelbaGItog4yYs6mC8yZXQOY2rpuY68virbdeyvnoptwJ07u1cgZKW1tBPA');
    commit("setPlayerData", response.data);
  }
}

// mutations
export const mutations = {
  setPlayerData(state, data) {
    state.playerData = data;
  }
}
