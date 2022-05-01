// state
export const state = () => ({
  mostPlayedChampions: []
})

// getters
export const getters = {
  getMostPlayedChampions(state) {
    return state.mostPlayedChampions;
  }
}

// actions
export const actions = {
  async getMostPlayedChampions({
    commit
  }) {
    const response = await this.$axios.get('/players/TEST');
    commit("addMostPlayedChampions", response.data.most_played.splice(0, 3));
  }
}

// mutations
export const mutations = {
  addMostPlayedChampions(state, mostPlayedChampions) {
    state.mostPlayedChampions = mostPlayedChampions;
  }
}
